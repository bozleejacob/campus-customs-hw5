/**
 * The backend truncates any audit detail over ~500 chars to
 * `{ truncated: true, preview: "<raw JSON text, cut off>" }` before writing
 * it (see backend/audit.py's _summarize). That preview string is frequently
 * cut off mid-value, so it isn't always valid JSON on its own — this
 * unwraps it when it parses, and otherwise falls back to the raw text so
 * the UI never just silently shows nothing.
 */
export function unwrapDetail(detail: Record<string, unknown>): Record<string, unknown> {
  if (detail.truncated && typeof detail.preview === "string") {
    try {
      return JSON.parse(detail.preview) as Record<string, unknown>;
    } catch {
      return { _rawPreview: detail.preview };
    }
  }
  return detail;
}

export function textOf(d: Record<string, unknown>, key: string): string {
  if (typeof d[key] === "string") return d[key] as string;
  if (typeof d._rawPreview === "string") return `${d._rawPreview}…`;
  return "";
}
