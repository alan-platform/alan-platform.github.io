import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";
import puppeteer from "puppeteer";
import { drawOverlay } from "./lib/overlay.mjs";
import { framePng } from "./lib/frame.mjs";
import { resizePng } from "./lib/resize.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../..");
const usage = "usage: shoot.mjs <version> [--list <shots.json>] [--only id,id] [--headful] [--keep] [--force-build]";
const args = process.argv.slice(2);
if (!args.length) throw new Error(usage);
const version = args.shift();
let only, headful = false, keep = false, forceBuild = false, listFile;
while (args.length) {
  const arg = args.shift();
  if (arg === "--only") only = new Set((args.shift() ?? "").split(",").filter(Boolean));
  else if (arg === "--list") listFile = path.resolve(args.shift() ?? "");
  else if (arg === "--headful") headful = true;
  else if (arg === "--keep") keep = true;
  else if (arg === "--force-build") forceBuild = true;
  else throw new Error(usage);
}
const config = JSON.parse(await fs.readFile(listFile ?? path.join(here, version, "shots.json"), "utf8"));
const shots = config.shots.filter(shot => !only || only.has(shot.id));
if (!shots.length) throw new Error("error: no shots selected");
const output = path.join(root, config.output);
await fs.mkdir(output, { recursive: true });
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

function selectorFor(selector) {
  if (selector.startsWith("text=")) return `::-p-text(${selector.slice(5)})`;
  if (selector.startsWith("aria=")) return `::-p-aria(${selector.slice(5)})`;
  if (selector.startsWith("widget=")) return `[data-widget="${selector.slice(7).replaceAll("\\", "\\\\").replaceAll('"', '\\"')}"]`;
  return selector;
}

async function elementFor(page, selector) {
  // exact=<text>: deepest visible element whose own text equals <text>; button=<text>: same, buttons only
  // exact=<text>[n] / button=<text>[n] / chevron=<text>: [n] picks the n-th match (0-based) in DOM order;
  // chevron= clicks the icon (expand/collapse) inside the matching navigation button
  if (selector.startsWith("exact=") || selector.startsWith("button=") || selector.startsWith("chevron=")) {
    const kind = selector.slice(0, selector.indexOf("="));
    let wanted = selector.slice(selector.indexOf("=") + 1);
    let index = 0;
    const indexed = wanted.match(/^(.*)\[(\d+)\]$/);
    if (indexed) { wanted = indexed[1]; index = Number(indexed[2]); }
    const tag = kind === "exact" ? "*" : "button, a, [role=button]";
    const handle = await page.evaluateHandle((wanted, tag, index, chevron) => {
      const visible = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      const matches = [...document.querySelectorAll(tag)].filter(e => { if (!visible(e)) return false; const text = (e.innerText ?? "").trim().replace(/\s+/g, " "); return text === wanted || text.replace(/^[a-z_]+ /, "") === wanted || text.replace(/^[a-z_]+(?=[A-Z])/, "") === wanted || text.replace(/ [a-z_]+$/, "") === wanted; });
      const leaves = matches.filter(e => !matches.some(other => other !== e && e.contains(other)));
      const element = leaves[index] ?? null;
      return chevron ? (element?.querySelector(".material-symbols-outlined") ?? null) : element;
    }, wanted, tag, index, kind === "chevron");
    const element = handle.asElement();
    if (!element) { await handle.dispose(); throw new Error(`selector not found: ${selector}`); }
    return element;
  }
  if (selector.startsWith("row=")) {
    const text = selector.slice(4);
    const handle = await page.evaluateHandle(value => {
      const exact = [...document.querySelectorAll("*")].find(e => e.children.length === 0 && e.textContent?.trim() === value);
      return exact?.closest("tr, [role=row], .row") ?? exact?.parentElement ?? null;
    }, text);
    const element = handle.asElement();
    if (!element) { await handle.dispose(); throw new Error(`selector not found: ${selector}`); }
    return element;
  }
  // prop=<label>: the whole property line (label and value) of the property labelled <label>;
  // value=<label>: only the value part of that line. Both accept [n] to pick the n-th match.
  if (selector.startsWith("prop=") || selector.startsWith("value=")) {
    const kind = selector.slice(0, selector.indexOf("="));
    let wanted = selector.slice(selector.indexOf("=") + 1);
    let index = 0;
    const indexed = wanted.match(/^(.*)\[(\d+)\]$/);
    if (indexed) { wanted = indexed[1]; index = Number(indexed[2]); }
    const handle = await page.evaluateHandle((wanted, index, valueOnly) => {
      const visible = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      // the deepest visible elements holding exactly this text: a label may wrap an icon, so match on text, not on leaves
      const labels = [...document.querySelectorAll("body *")].filter(e => e.children.length === 0 && visible(e) && e.textContent?.trim() === wanted);
      const rows = [];
      for (const label of labels) {
        const row = label.closest(".row");
        if (row && !rows.includes(row)) rows.push(row);
      }
      const row = rows[index] ?? null;
      return valueOnly ? (row?.querySelector(".widget") ?? null) : row;
    }, wanted, index, kind === "value");
    const element = handle.asElement();
    if (!element) { await handle.dispose(); throw new Error(`selector not found: ${selector}`); }
    return element;
  }
  if (selector.startsWith("label=") || selector.startsWith("field=")) {
    const text = selector.slice(selector.indexOf("=") + 1);
    const handle = await page.evaluateHandle(value => {
      const visible = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      const labels = [...document.querySelectorAll("label, .common-control-property-info-label, th")];
      // command forms and other layouts label their fields with plain elements: fall back to any leaf element
      const label = labels.find(e => visible(e) && e.innerText?.trim() === value)
        ?? [...document.querySelectorAll("body *")].find(e => e.children.length === 0 && visible(e) && e.innerText?.trim() === value);
      if (!label) return null;
      const box = label.getBoundingClientRect();
      const middle = box.y + box.height / 2;
      // the control of a property sits on the same line, to the right of its label
      return [...document.querySelectorAll("input, select, textarea, [contenteditable=true]")]
        .filter(visible)
        .map(e => ({ e, r: e.getBoundingClientRect() }))
        .filter(({ r }) => r.x >= box.x + box.width - 1 && middle >= r.y - 4 && middle <= r.y + r.height + 4)
        .sort((a, b) => a.r.x - b.r.x)[0]?.e ?? null;
    }, text);
    const element = handle.asElement();
    if (!element) { await handle.dispose(); throw new Error(`selector not found: ${selector}`); }
    return element;
  }
  // plain css: prefer the first visible match, since the client keeps hidden copies of panels around
  if (!/^(text|aria|widget)=/.test(selector)) {
    const visibleMatch = await page.evaluateHandle(css => {
      const visible = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      return [...document.querySelectorAll(css)].find(visible) ?? null;
    }, selector);
    const element = visibleMatch.asElement();
    if (element) return element;
    await visibleMatch.dispose();
  }
  const handle = await page.locator(selectorFor(selector)).waitHandle();
  return handle;
}

async function boxFor(page, selector) {
  const target = await elementFor(page, selector);
  let box = await target.boundingBox();
  // a layout container can be `display: contents`, which has no box of its own: fall back to what it renders
  if (!box || !box.width || !box.height) {
    box = await target.evaluate(element => {
      const rects = [...element.querySelectorAll("*")].map(e => e.getBoundingClientRect()).filter(r => r.width > 0 && r.height > 0);
      if (!rects.length) return null;
      const x = Math.min(...rects.map(r => r.x)), y = Math.min(...rects.map(r => r.y));
      return { x, y, width: Math.max(...rects.map(r => r.right)) - x, height: Math.max(...rects.map(r => r.bottom)) - y };
    });
  }
  if (target.dispose) await target.dispose();
  if (!box) throw new Error(`selector has no bounding box: ${selector}`);
  return box;
}
function rectWithPad(rect, value = 0) {
  const pad = Number(value || 0);
  return { x: rect.x - pad, y: rect.y - pad, width: rect.width + pad * 2, height: rect.height + pad * 2 };
}
async function pointFor(page, point) {
  if (Array.isArray(point)) return { x: point[0], y: point[1] };
  if (typeof point === "object" && "x" in point) return point;
  const box = await boxFor(page, point.selector);
  const anchor = point.anchor ?? "center";
  let x = box.x + box.width / 2, y = box.y + box.height / 2;
  if (anchor === "left") x = box.x;
  if (anchor === "right") x = box.x + box.width;
  if (anchor === "top") y = box.y;
  if (anchor === "bottom") y = box.y + box.height;
  return { x: x + (point.dx ?? 0), y: y + (point.dy ?? 0) };
}
async function annotationsFor(page, annotations = []) {
  const result = [];
  for (const item of annotations) {
    if (item.box) {
      let source;
      if (typeof item.box === "string") source = await boxFor(page, item.box);
      else if (item.box.union) {
        const boxes = [];
        for (const selector of item.box.union) boxes.push(await boxFor(page, selector));
        const x = Math.min(...boxes.map(b => b.x)), y = Math.min(...boxes.map(b => b.y));
        source = { x, y, width: Math.max(...boxes.map(b => b.x + b.width)) - x, height: Math.max(...boxes.map(b => b.y + b.height)) - y };
      } else source = item.box;
      result.push({ kind: "box", rect: rectWithPad(source, item.pad) });
    } else if (item.arrow) result.push({ kind: "arrow", from: await pointFor(page, item.arrow.from), to: await pointFor(page, item.arrow.to) });
    else if (item.underline) {
      const source = typeof item.underline === "string" ? await boxFor(page, item.underline) : item.underline;
      const rect = source.selector ? await boxFor(page, source.selector) : source;
      result.push({ kind: "underline", from: { x: rect.x, y: rect.y + rect.height + (source.dy ?? 2) }, to: { x: rect.x + rect.width, y: rect.y + rect.height + (source.dy ?? 2) } });
    } else if (item.label) result.push({ kind: "label", text: item.label, at: await pointFor(page, item.at) });
  }
  return result;
}
async function runAction(page, action, settleMs) {
  if (action.goto) await page.goto(`${page.url().split("#")[0]}#${action.goto}`, { waitUntil: "networkidle0" });
  else if (action.click) { const target = await elementFor(page, action.click); await target.click(); if (target.dispose) await target.dispose(); }
  else if (action.dblclick) { const target = await elementFor(page, action.dblclick); await target.click({ clickCount: 2 }); if (target.dispose) await target.dispose(); }
  else if (action.hover) { const target = await elementFor(page, action.hover); await target.hover(); if (target.dispose) await target.dispose(); }
  else if (action.type) { const target = await elementFor(page, action.type.selector); await target.click(); await target.evaluate(element => { if (element.select) element.select(); }); await page.keyboard.type(action.type.text); if (target.dispose) await target.dispose(); }
  else if (action.press) await page.keyboard.press(action.press);
  else if (action.clickAt) await page.mouse.click(action.clickAt[0], action.clickAt[1]);
  else if (action.mouse) await page.mouse.move(action.mouse[0], action.mouse[1]);
  else if (action.waitFor !== undefined) { if (typeof action.waitFor === "number") await sleep(action.waitFor); else { const target = await elementFor(page, action.waitFor); if (target.dispose) await target.dispose(); } }
  else if (action.wait !== undefined) await sleep(action.wait);
  else if (action.dump) {
    const rows = await page.evaluate(selector => [...document.querySelectorAll(selector)].slice(0, 40).map(e => {
      const r = e.getBoundingClientRect();
      return `${e.tagName.toLowerCase()}.${(e.className ?? "").toString().split(" ").filter(Boolean).slice(0, 3).join(".")} @${Math.round(r.x)},${Math.round(r.y)} ${Math.round(r.width)}x${Math.round(r.height)} "${(e.innerText ?? "").trim().replace(/\s+/g, " ").slice(0, 50)}"`;
    }), action.dump);
    process.stderr.write(`dump ${action.dump}:\n${rows.join("\n")}\n`);
  }
  else if (action.dumpUp) {
    const html = await page.evaluate(({ selector, up }) => {
      const visible = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      let element = [...document.querySelectorAll("body *")].find(e => e.children.length === 0 && visible(e) && e.innerText?.trim() === selector);
      for (let i = 0; i < up && element?.parentElement; i += 1) element = element.parentElement;
      return element?.outerHTML.slice(0, 2500) ?? "not found";
    }, { selector: action.dumpUp.text ?? action.dumpUp, up: action.dumpUp.up ?? 3 });
    process.stderr.write(`dumpUp ${JSON.stringify(action.dumpUp)}:\n${html}\n`);
  }
  else if (action.select) { const target = await elementFor(page, action.select.selector); const tag = await target.evaluate(e => e.tagName); if (tag === "SELECT") await target.select(action.select.value); else { await target.click(); const option = await elementFor(page, `text=${action.select.value}`); await option.click(); if (option.dispose) await option.dispose(); } if (target.dispose) await target.dispose(); }
  else if (action.view) { const control = await elementFor(page, `button=${action.view === "Full" ? "Compact" : "Full"}`); await control.click(); await sleep(settleMs); const option = await elementFor(page, `button=${action.view}`); await option.click(); }
  else throw new Error(`unknown action: ${JSON.stringify(action)}`);
  await sleep(settleMs);
}
function startServer(buildDir) {
  const serverArgs = [buildDir, "--app-name", config.appName ?? "Sandbox"];
  if (config.dataDir) serverArgs.push("--data-dir", path.resolve(here, config.dataDir));
  const child = spawn(path.join(here, "serve-app.sh"), serverArgs, { stdio: ["ignore", "pipe", "pipe"] });
  child.stderr.on("data", data => process.stderr.write(data));
  const url = new Promise((resolve, reject) => {
    let buffer = "";
    const timer = setTimeout(() => reject(new Error("error: server did not print a client URL within 60 seconds")), 60000);
    child.stdout.on("data", data => { buffer += data; for (const line of buffer.split(/\r?\n/)) if (/^http:\/\//.test(line)) { clearTimeout(timer); resolve(line); return; } });
    child.on("exit", code => reject(new Error(`error: server exited before URL (status ${code})`)));
  });
  return { child, url };
}
async function stopServer(child) { child.kill("SIGTERM"); await new Promise(resolve => child.once("exit", resolve)); }
async function pngSize(file) { const bytes = await fs.readFile(file); return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) }; }

const groups = new Map();
for (const shot of shots) groups.set(shot.dataset, [...(groups.get(shot.dataset) ?? []), shot]);
const summary = [];
let failed = false;
for (const [dataset, datasetShots] of groups) {
  let buildDir;
  try {
    const result = await new Promise((resolve, reject) => {
      const child = spawn(path.join(here, "build-step.sh"), [version, dataset, ...(forceBuild ? ["--force"] : [])], { stdio: ["ignore", "pipe", "pipe"], env: { ...process.env, ...(config.tutorial ? { TUTORIAL: config.tutorial } : {}), ...(config.docs ? { DOCS: config.docs } : {}) } });
      let stdout = ""; child.stdout.on("data", data => stdout += data); child.stderr.on("data", data => process.stderr.write(data));
      child.on("exit", code => code === 0 ? resolve(stdout.trim().split(/\r?\n/).at(-1)) : reject(new Error(`build failed for ${dataset} (status ${code})`)));
    });
    buildDir = result;
    const server = startServer(buildDir);
    const url = await server.url;
    let browser;
    const options = { headless: !headful, args: ["--lang=en-US"] };
    try { browser = await puppeteer.launch(options); }
    catch (error) { if (process.env.SHOT_NO_SANDBOX === "1") throw error; browser = await puppeteer.launch({ ...options, args: [...options.args, "--no-sandbox", "--disable-setuid-sandbox"] }); }
    for (const shot of datasetShots) {
      try {
        const page = await browser.newPage();
        const viewport = { ...config.viewport, ...(shot.viewport ?? {}) };
        if (shot.deviceScaleFactor) viewport.deviceScaleFactor = shot.deviceScaleFactor;
        await page.setViewport(viewport);
        await page.setExtraHTTPHeaders({ "Accept-Language": "en-US" });
        await page.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: "reduce" }]);
        page.on("console", message => { if (message.type() === "error") process.stderr.write(`${shot.id}: ${message.text()}\n`); });
        const settleMs = shot.settleMs ?? config.settleMs ?? 300;
        if (shot.code) {
          // a code fragment rendered like the site's code blocks; every line gets data-line="n" for annotations
          const escape = text => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
          const lines = shot.code.split("\n").map((line, index) => `<span data-line="${index + 1}">${escape(line) || " "}</span>`).join("\n");
          await page.setContent(`<!doctype html><html><head><style>
            body { margin: 0; padding: 16px; background: #fff; }
            pre.code { display: inline-block; margin: 0; padding: 12px 16px; background: #f5f5f5; border-radius: 4px;
              font: 15px/1.5 "Source Code Pro", "DejaVu Sans Mono", monospace; color: #222; tab-size: 4; }
            pre.code span { display: inline-block; min-width: 1px; }
          </style></head><body><pre class="code">${lines}</pre></body></html>`);
        } else {
          const hash = `${shot.goto ?? ""}${shot.debug ? "&debug=true" : ""}`;
          await page.goto(`${url}#${hash}`, { waitUntil: "networkidle0" });
          await page.waitForFunction(() => !document.querySelector("#engine-boot") && document.querySelector("[data-widget]"));
        }
        await sleep(settleMs);
        for (const action of shot.actions ?? []) await runAction(page, action, settleMs);
        // park the mouse on an empty spot so no hover state or tooltip ends up in the capture
        const park = shot.mouse ?? [Math.round(viewport.width * 0.75), Math.round(viewport.height * 0.9)];
        await page.mouse.move(park[0], park[1]);
        await sleep(150);
        let clip = shot.clip;
        if (shot.clipTo) { const box = await boxFor(page, shot.clipTo.selector); clip = rectWithPad(box, shot.clipTo.pad); for (const side of ["Right", "Left", "Top", "Bottom"]) { const value = shot.clipTo[`extend${side}`] ?? 0; if (side === "Right") clip.width += value; if (side === "Left") { clip.x -= value; clip.width += value; } if (side === "Top") { clip.y -= value; clip.height += value; } if (side === "Bottom") clip.height += value; } }
        const annotations = await annotationsFor(page, shot.annotate);
        if (annotations.length) await page.evaluate(drawOverlay, annotations);
        const destination = path.join(output, shot.file);
        await page.screenshot({ path: destination, ...(clip ? { clip } : {}) });
        await page.evaluate(() => document.getElementById("shot-annotations")?.remove());
        if (shot.frame !== false && config.frame !== false) await framePng(browser, destination, { ...(config.frame ?? {}), ...(shot.frame ?? {}) });
      await resizePng(browser, destination, config.maxWidth ?? 1600); // the site shows these in a column of about 800 CSS pixels
        const size = await pngSize(destination); summary.push({ ...shot, ...size });
        await page.close();
      } catch (error) { failed = true; process.stderr.write(`${shot.id}: ${error.stack ?? error}\n`); }
    }
    await browser.close();
    if (keep) process.stdout.write(`${url}\n`); else await stopServer(server.child);
  } catch (error) { failed = true; process.stderr.write(`${error.stack ?? error}\n`); }
}
console.log("id    file      WxH");
for (const row of summary) console.log(`${row.id.padEnd(5)} ${row.file.padEnd(9)} ${row.width}x${row.height}`);
if (failed) process.exitCode = 1;
