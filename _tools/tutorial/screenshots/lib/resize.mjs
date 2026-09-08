// Downscales a PNG to a maximum width, rendered with Chrome so no native image library is needed.
// Screenshots are taken at the app's own resolution; the site shows them in a column of about
// 800 CSS pixels, so anything wider than twice that is bytes nobody sees.
import fs from "node:fs/promises";

export async function resizePng(browser, file, maxWidth) {
  const bytes = await fs.readFile(file);
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width <= maxWidth) return { width, height, resized: false };

  const scaled = { width: maxWidth, height: Math.round((height * maxWidth) / width) };
  const page = await browser.newPage();
  try {
    await page.setViewport({ width: scaled.width, height: scaled.height, deviceScaleFactor: 1 });
    await page.setContent(`<!doctype html><html><head><style>
      html, body { margin: 0; background: transparent; }
      img { display: block; width: ${scaled.width}px; height: ${scaled.height}px; }
    </style></head><body><img src="data:image/png;base64,${bytes.toString("base64")}"></body></html>`);
    await page.waitForFunction(() => document.images[0]?.complete);
    await page.screenshot({ path: file, omitBackground: true, clip: { x: 0, y: 0, ...scaled } });
  } finally {
    await page.close();
  }
  return { ...scaled, resized: true };
}
