// IDE screenshots: VS Code for the Web (`code serve-web`) with the Kjerner.alan extension, driven by puppeteer.
// usage: ide-shoot.mjs <version> [--list <shots.json>] [--only id,id] [--headful] [--keep]
// The shot list defaults to <version>/ide-shots.json; ide/tutorial-shots.json holds the unversioned IDE tutorial.
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";
import puppeteer from "puppeteer";
import { drawOverlay } from "../lib/overlay.mjs";
import { framePng } from "../lib/frame.mjs";
import { resizePng } from "../lib/resize.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const screenshots = path.dirname(here);
const root = path.resolve(screenshots, "../../..");
const usage = "usage: ide-shoot.mjs <version> [--list <shots.json>] [--only id,id] [--headful] [--keep]";
const args = process.argv.slice(2);
if (!args.length) throw new Error(usage);
const version = args.shift();
let only, headful = false, keep = false, listFile;
while (args.length) {
  const arg = args.shift();
  if (arg === "--only") only = new Set((args.shift() ?? "").split(",").filter(Boolean));
  else if (arg === "--list") listFile = path.resolve(args.shift() ?? "");
  else if (arg === "--headful") headful = true;
  else if (arg === "--keep") keep = true;
  else throw new Error(usage);
}
const config = JSON.parse(await fs.readFile(listFile ?? path.join(screenshots, version, "ide-shots.json"), "utf8"));
const shots = config.shots.filter(shot => !only || only.has(shot.id));
if (!shots.length) throw new Error("error: no shots selected");
const output = path.join(root, config.output);
const vscodeRoot = path.join(root, ".toolchains/vscode");
const workspace = path.join(vscodeRoot, config.workspace ?? "workspace/project");
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

let page;

// --- selectors -------------------------------------------------------------------------------------
// css | explorer=<label> (explorer row) | text=<exact text> (deepest visible element) | statusbar=<text>
async function boxFor(selector) {
  const box = await page.evaluate(selector => {
    const visible = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
    const rect = e => { const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; };
    if (selector.startsWith("explorer=")) {
      const label = selector.slice(9);
      const rows = [...document.querySelectorAll(".explorer-viewlet .monaco-list-row")].filter(visible);
      const row = rows.find(r => r.getAttribute("aria-label") === label || r.querySelector(".label-name")?.textContent === label)
        ?? rows.find(r => r.getAttribute("aria-label")?.includes(label) || r.textContent?.includes(label));
      return row ? rect(row) : null;
    }
    if (selector.startsWith("statusbar=")) {
      const text = selector.slice(10);
      const item = [...document.querySelectorAll(".statusbar-item")].filter(visible).find(e => e.textContent?.trim() === text || e.textContent?.includes(text));
      return item ? rect(item) : null;
    }
    if (selector.startsWith("text=")) {
      const text = selector.slice(5);
      const all = [...document.querySelectorAll("body *")].filter(e => visible(e) && e.textContent?.trim() === text);
      const leaf = all.find(e => !all.some(other => other !== e && e.contains(other)));
      return leaf ? rect(leaf) : null;
    }
    const element = [...document.querySelectorAll(selector)].find(visible);
    return element ? rect(element) : null;
  }, selector);
  if (!box) throw new Error(`selector not found: ${selector}`);
  return box;
}
async function unionBox(selectors, pad = 0) {
  const boxes = [];
  for (const selector of selectors) boxes.push(await boxFor(selector));
  const x = Math.min(...boxes.map(b => b.x)), y = Math.min(...boxes.map(b => b.y));
  const right = Math.max(...boxes.map(b => b.x + b.width)), bottom = Math.max(...boxes.map(b => b.y + b.height));
  return { x: x - pad, y: y - pad, width: right - x + 2 * pad, height: bottom - y + 2 * pad };
}
async function rectFor(spec, pad = 0) {
  if (typeof spec === "string") return unionBox([spec], pad);
  if (spec.union) return unionBox(spec.union, pad);
  return { x: spec.x - pad, y: spec.y - pad, width: spec.width + 2 * pad, height: spec.height + 2 * pad };
}
async function pointFor(point) {
  if (Array.isArray(point)) return { x: point[0], y: point[1] };
  const box = await rectFor(point.selector ?? point);
  const anchor = point.anchor ?? "center";
  let x = box.x + box.width / 2, y = box.y + box.height / 2;
  if (anchor === "left") x = box.x;
  if (anchor === "right") x = box.x + box.width;
  if (anchor === "top") y = box.y;
  if (anchor === "bottom") y = box.y + box.height;
  if (anchor === "bottom-right") { x = box.x + box.width; y = box.y + box.height; }
  if (anchor === "top-right") { x = box.x + box.width; y = box.y; }
  return { x: x + (point.dx ?? 0), y: y + (point.dy ?? 0) };
}
async function annotationData(annotations = []) {
  const data = [];
  for (const item of annotations) {
    if (item.box) data.push({ kind: "box", rect: await rectFor(item.box, item.pad ?? 0) });
    else if (item.arrow) data.push({ kind: "arrow", from: await pointFor(item.arrow.from), to: await pointFor(item.arrow.to) });
    else if (item.label) data.push({ kind: "label", text: item.label, at: await pointFor(item.at), size: item.size });
  }
  return data;
}
async function clickSelector(selector) {
  const box = await boxFor(selector);
  await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
}
async function hoverSelector(selector) {
  const box = await boxFor(selector);
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
}

// --- workbench interaction -------------------------------------------------------------------------
// The command palette opens with F1 and its input starts with ">", so commands are typed after that
// prefix; a puppeteer keyboard.press() cannot send chords such as Control+P, hence no shortcuts here.
async function quickInput() {
  await page.keyboard.press("Escape");
  await page.keyboard.press("F1");
  const input = await page.waitForSelector(".quick-input-widget input", { visible: true });
  await input.evaluate(element => { element.value = ">"; element.dispatchEvent(new Event("input", { bubbles: true })); });
  return input;
}
async function run(command) {
  await quickInput();
  await page.keyboard.type(command);
  await sleep(400); await page.keyboard.press("Enter"); await sleep(500);
}
async function openFile(file) {
  for (let attempt = 0; attempt < 2; attempt += 1) {
    await quickInput();
    await page.keyboard.type("Go to File...");
    await sleep(400); await page.keyboard.press("Enter"); await sleep(300);
    await page.keyboard.type(file); await sleep(500); await page.keyboard.press("Enter");
    try { await page.waitForSelector(`.tab[aria-label*="${path.basename(file)}"]`, { timeout: 4000 }); await sleep(500); return; }
    catch (error) { if (attempt) throw error; await sleep(1000); }
  }
}
async function waitFor(spec, timeout = 15000) {
  if (typeof spec === "number") return sleep(spec);
  if (spec.startsWith("quickpick=")) return page.waitForSelector(`.quick-input-widget input[placeholder="${spec.slice(10)}"]`, { visible: true, timeout });
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    try { await boxFor(spec); return; } catch (_) { await sleep(250); }
  }
  throw new Error(`timeout waiting for ${spec}`);
}
async function dump(selector) {
  const rows = await page.evaluate(selector => [...document.querySelectorAll(selector)].map(e => {
    const r = e.getBoundingClientRect();
    const style = getComputedStyle(e);
    return `${e.tagName.toLowerCase()} @${Math.round(r.x)},${Math.round(r.y)} ${Math.round(r.width)}x${Math.round(r.height)} "${(e.textContent ?? "").trim().replace(/\s+/g, " ").slice(0, 60)}" aria=${e.getAttribute("aria-label") ?? ""} class=${(e.className ?? "").toString().slice(0, 60)} style=${style.display}/${style.visibility}/${style.opacity}`;
  }), selector);
  process.stderr.write(`dump ${selector}:\n${rows.join("\n")}\n`);
}
async function runStep(step) {
  if (step.open) await openFile(step.open);
  else if (step.command) await run(step.command);
  else if (step.waitFor !== undefined) await waitFor(step.waitFor, step.timeout);
  else if (step.key) await page.keyboard.press(step.key);
  else if (step.type) await page.keyboard.type(step.type);
  else if (step.click) await clickSelector(step.click);
  else if (step.hover) await hoverSelector(step.hover);
  else if (step.mousedown) { const box = await boxFor(step.mousedown); await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2); await page.mouse.down(); }
  else if (step.mouseup) await page.mouse.up();
  else if (step.focus) await page.evaluate(selector => document.querySelector(selector)?.focus(), step.focus);
  else if (step.mouse) await page.mouse.move(step.mouse[0], step.mouse[1]);
  else if (step.dump) await dump(step.dump);
  else if (step.wait) await sleep(step.wait);
  else throw new Error(`unknown step: ${JSON.stringify(step)}`);
  await sleep(step.settle ?? 300);
}
// legacy shot fields (open, commands, waitFor, keys) are expanded into steps
function stepsOf(shot) {
  if (shot.steps) return shot.steps;
  const steps = [];
  if (shot.open) steps.push({ open: shot.open });
  for (const command of shot.commands ?? []) steps.push({ command });
  if (shot.waitFor) steps.push({ waitFor: shot.waitFor });
  for (const key of shot.keys ?? []) steps.push({ key });
  return steps;
}

// A plain CDP capture: puppeteer's page.screenshot() resizes and refocuses the page around the capture,
// which makes VS Code close its menus and hovers before the picture is taken.
async function capture(destination, clip) {
  const session = await page.createCDPSession();
  try {
    const viewport = page.viewport();
    const region = clip ?? { x: 0, y: 0, width: viewport.width, height: viewport.height };
    const { data } = await session.send("Page.captureScreenshot", {
      format: "png",
      captureBeyondViewport: false,
      clip: { x: region.x, y: region.y, width: region.width, height: region.height, scale: viewport.deviceScaleFactor ?? 1 },
    });
    await fs.writeFile(destination, Buffer.from(data, "base64"));
  } finally {
    await session.detach();
  }
}
async function pngSize(file) { const bytes = await fs.readFile(file); return `${bytes.readUInt32BE(16)}x${bytes.readUInt32BE(20)}`; }
async function fetchReady(url) {
  for (let attempt = 0; attempt < 60; attempt += 1) {
    try { const response = await fetch(url); if ((await response.text()).includes("<html")) return; } catch (_) { }
    await sleep(500);
  }
  throw new Error(`error: VS Code web UI did not become ready: ${url}`);
}
function startServer() {
  const command = path.join(vscodeRoot, "cli/code");
  const env = { ...process.env, ...config.env, LANG: "en_US.UTF-8" };
  const child = spawn(command, ["serve-web", "--accept-server-license-terms", "--without-connection-token", "--host", "127.0.0.1", "--port", "0", "--server-data-dir", path.join(vscodeRoot, "server-data"), "--cli-data-dir", path.join(vscodeRoot, "cli-data"), "--disable-telemetry"], { env, stdio: ["ignore", "pipe", "pipe"] });
  const url = new Promise((resolve, reject) => {
    let log = "";
    let ready = false;
    const accept = data => {
      log += data.toString();
      if (!ready || /error|warn/i.test(data.toString())) process.stderr.write(data);
      const match = log.match(/Web UI available at (http:\/\/127\.0\.0\.1:\d+)/);
      if (match) { ready = true; resolve(match[1]); }
    };
    child.stdout.on("data", accept); child.stderr.on("data", accept);
    const timer = setTimeout(() => reject(new Error("error: code serve-web did not print a URL within 60 seconds")), 60000);
    child.on("exit", code => { clearTimeout(timer); reject(new Error(`error: code serve-web exited before URL (status ${code})`)); });
  });
  return { child, url };
}
async function stop(child) { if (child.exitCode !== null) return; child.kill("SIGTERM"); await new Promise(resolve => child.once("exit", resolve)); }

await fs.mkdir(output, { recursive: true });
const server = startServer();
let browser;
const summary = [];
let failed = false;
try {
  const url = await server.url;
  await fetchReady(`${url}/`);
  const options = { headless: !headful, args: ["--lang=en-US"] };
  try { browser = await puppeteer.launch(options); }
  catch (error) { if (process.env.SHOT_NO_SANDBOX === "1") throw error; browser = await puppeteer.launch({ ...options, args: [...options.args, "--no-sandbox", "--disable-setuid-sandbox"] }); }
  page = await browser.newPage();
  await page.setViewport(config.viewport);
  await page.setExtraHTTPHeaders({ "Accept-Language": "en-US" });
  page.on("console", message => { if (message.type() === "error") process.stderr.write(`page: ${message.text()}\n`); });
  await page.goto(`${url}/?folder=${encodeURIComponent(workspace)}`, { waitUntil: "networkidle0" });
  await page.waitForSelector(".monaco-workbench", { timeout: 60000 });
  await page.waitForSelector(".explorer-viewlet", { timeout: 60000 });
  await sleep(1500);
  // A fresh browser profile opens the folder in Restricted Mode, which disables the Alan extension.
  // Trust it through the Workspace Trust editor; the extension host restarts afterwards.
  await run("Workspaces: Manage Workspace Trust");
  const trust = await page.waitForSelector(".workspace-trust-editor .monaco-button, .workspace-trust-editor a.monaco-text-button", { visible: true, timeout: 15000 });
  await trust.evaluate(() => {
    const button = [...document.querySelectorAll(".workspace-trust-editor .monaco-button, .workspace-trust-editor a.monaco-text-button")]
      .find(element => element.textContent?.trim() === "Trust");
    if (!button) throw new Error("workspace trust editor: no Trust button");
    button.click();
  });
  await sleep(4000);
  if (await page.$(".part.auxiliarybar:not(.hidden)")) await run("View: Close Secondary Side Bar");
  await openFile("models/model/application.alan");
  // the extension activates on the first .alan file and may open a terminal for its start-up fetch
  await sleep(6000);
  await run("Terminal: Kill All Terminals");
  await run("Notifications: Clear All Notifications");
  await run("View: Close All Editors");
  await run("View: Close Panel");
  for (const shot of shots) {
    try {
      if (shot.viewport) await page.setViewport({ ...config.viewport, ...shot.viewport });
      if (shot.reset !== false) { await run("View: Close All Editors"); if (shot.closePanel !== false) await run("View: Close Panel"); }
      for (const step of stepsOf(shot)) await runStep(step);
      let clip = shot.clip;
      if (shot.clipTo) clip = await rectFor(shot.clipTo.selector ?? shot.clipTo, shot.clipTo.pad ?? 0);
      const annotations = await annotationData(shot.annotate);
      if (annotations.length) await page.evaluate(drawOverlay, annotations);
      const destination = path.join(output, shot.file);
      if (process.env.SHOT_DEBUG) await dump(process.env.SHOT_DEBUG);
      await capture(destination, clip);
      if (process.env.SHOT_DEBUG) await dump(process.env.SHOT_DEBUG);
      await page.evaluate(() => document.getElementById("shot-annotations")?.remove());
      if (shot.frame !== false && config.frame !== false) await framePng(browser, destination, { ...(config.frame ?? {}), ...(shot.frame ?? {}) });
      await resizePng(browser, destination, config.maxWidth ?? 1600); // the site shows these in a column of about 800 CSS pixels
      summary.push({ id: shot.id, file: shot.file, size: await pngSize(destination) });
      for (const key of shot.after ?? []) await page.keyboard.press(key);
      if (shot.viewport) await page.setViewport(config.viewport);
    } catch (error) {
      failed = true; process.stderr.write(`${shot.id}: ${error.stack ?? error}\n`);
      const debugFile = path.join(vscodeRoot, `debug-${shot.id}.png`);
      try { await page.screenshot({ path: debugFile }); process.stderr.write(`${shot.id}: debug screenshot ${debugFile}\n`); } catch (_) { }
      await page.keyboard.press("Escape");
    }
  }
  if (keep) process.stdout.write(`${url}\n`);
} catch (error) { failed = true; process.stderr.write(`${error.stack ?? error}\n`); }
finally {
  if (browser) await browser.close();
  if (!keep) await stop(server.child);
}
console.log("id      file         WxH");
for (const row of summary) console.log(`${row.id.padEnd(7)} ${row.file.padEnd(12)} ${row.size}`);
if (failed) process.exitCode = 1;
