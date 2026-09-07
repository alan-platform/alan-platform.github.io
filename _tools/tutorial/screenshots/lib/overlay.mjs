export function drawOverlay(annotations) {
  document.getElementById("shot-annotations")?.remove();
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.id = "shot-annotations";
  svg.setAttribute("width", "100%");
  svg.setAttribute("height", "100%");
  svg.setAttribute("viewBox", `0 0 ${window.innerWidth} ${window.innerHeight}`);
  svg.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:2147483647";
  const defs = document.createElementNS(ns, "defs");
  const marker = document.createElementNS(ns, "marker");
  marker.id = "shot-arrow";
  marker.setAttribute("markerWidth", "10"); marker.setAttribute("markerHeight", "10");
  marker.setAttribute("refX", "8"); marker.setAttribute("refY", "3"); marker.setAttribute("orient", "auto");
  const path = document.createElementNS(ns, "path");
  path.setAttribute("d", "M0,0 L0,6 L9,3 z"); path.setAttribute("fill", "#e5322d");
  marker.append(path); defs.append(marker); svg.append(defs);
  const style = element => { element.setAttribute("stroke", "#e5322d"); element.setAttribute("stroke-width", "3"); element.setAttribute("fill", "none"); };
  for (const annotation of annotations) {
    if (annotation.kind === "box") {
      const e = document.createElementNS(ns, "rect");
      e.setAttribute("x", annotation.rect.x); e.setAttribute("y", annotation.rect.y);
      e.setAttribute("width", annotation.rect.width); e.setAttribute("height", annotation.rect.height);
      e.setAttribute("rx", "6"); style(e); svg.append(e);
    } else if (annotation.kind === "arrow" || annotation.kind === "underline") {
      const e = document.createElementNS(ns, "line");
      e.setAttribute("x1", annotation.from.x); e.setAttribute("y1", annotation.from.y);
      e.setAttribute("x2", annotation.to.x); e.setAttribute("y2", annotation.to.y); style(e);
      if (annotation.kind === "arrow") e.setAttribute("marker-end", "url(#shot-arrow)");
      svg.append(e);
    } else if (annotation.kind === "label") {
      const e = document.createElementNS(ns, "text");
      e.setAttribute("x", annotation.at.x); e.setAttribute("y", annotation.at.y);
      e.setAttribute("fill", "#e5322d"); e.setAttribute("font-family", "sans-serif");
      e.setAttribute("font-size", String(annotation.size ?? 18)); e.setAttribute("font-weight", "bold");
      e.setAttribute("dominant-baseline", "middle"); e.textContent = annotation.text; svg.append(e);
    }
  }
  document.body.append(svg);
}
