// One-off: downscale committed screenshots that are wider than the site can use.
// usage: node resize-images.mjs <max width> <file>...
import fs from "node:fs/promises";
import puppeteer from "puppeteer";
import { resizePng } from "./lib/resize.mjs";

const [maxWidth, ...files] = process.argv.slice(2);
const browser = await puppeteer.launch({ args: ["--no-sandbox"] });
let saved = 0;
let count = 0;
for (const file of files) {
  const before = (await fs.stat(file)).size;
  const result = await resizePng(browser, file, Number(maxWidth));
  if (result.resized) {
    count += 1;
    saved += before - (await fs.stat(file)).size;
  }
}
await browser.close();
console.log(`resized ${count} of ${files.length} images, saved ${(saved / 1e6).toFixed(1)} MB`);
