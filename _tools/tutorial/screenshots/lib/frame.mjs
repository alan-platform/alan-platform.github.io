// Frames a captured PNG: rounded corners, a thin border and a drop shadow on a transparent margin,
// rendered with Chrome itself so no native image library is needed. The file is replaced in place.
import fs from "node:fs/promises";

export async function framePng(browser, file, options = {}) {
  const { margin = 48, radius = 14, border = "1px solid rgba(0, 0, 0, 0.18)", shadow = "0 18px 48px rgba(0, 0, 0, 0.28)" } = options;
  const bytes = await fs.readFile(file);
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  const page = await browser.newPage();
  try {
    await page.setViewport({ width: width + 2 * margin, height: height + 2 * margin, deviceScaleFactor: 1 });
    await page.setContent(`<!doctype html><html><head><style>
      html, body { margin: 0; background: transparent; }
      img { display: block; position: absolute; left: ${margin}px; top: ${margin}px; width: ${width}px; height: ${height}px;
        border-radius: ${radius}px; border: ${border}; box-sizing: border-box; box-shadow: ${shadow}; }
    </style></head><body><img src="data:image/png;base64,${bytes.toString("base64")}"></body></html>`);
    await page.waitForFunction(() => document.images[0]?.complete);
    await page.screenshot({ path: file, omitBackground: true, clip: { x: 0, y: 0, width: width + 2 * margin, height: height + 2 * margin } });
  } finally {
    await page.close();
  }
}
