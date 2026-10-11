#!/usr/bin/env python3
"""VofGo Instagram post renderer (1080x1350).

Usage:  python3 template/render.py spec.json out.png

spec.json fields:
  theme       "light" | "dark"   (feed alternates: look at the previous post)
  tag         small uppercase category, e.g. "YAPAY ZEKÂ"
  headline    text; wrap the highlighted words in **double stars**
  small_h1    optional bool, use for long headlines (80px instead of 92px)
  sub         1-2 sentence grey description
  visual_html HTML for the bottom visual, built from components in base.html
              (.card/.row/.badge, .tiles/.tile, .split, .steps/.step, .stats/.stat, .cta)
"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
FONT_DIR = pathlib.Path.home() / ".cache" / "vofgo-fonts"


def ensure_fonts():
    files = FONT_DIR / "node_modules/@fontsource/plus-jakarta-sans/files"
    if not files.exists():
        FONT_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.run(["npm", "i", "--prefix", str(FONT_DIR), "@fontsource/plus-jakarta-sans"],
                       check=True, stdout=subprocess.DEVNULL)
    css = []
    for w in (400, 500, 600, 700, 800):
        css.append(f"@font-face{{font-family:PJS;font-weight:{w};src:url(file://{files}/plus-jakarta-sans-latin-{w}-normal.woff2)}}")
        css.append(f"@font-face{{font-family:PJS;font-weight:{w};src:url(file://{files}/plus-jakarta-sans-latin-ext-{w}-normal.woff2);unicode-range:U+0100-02AF}}")
    return "\n".join(css)


def build_html(spec):
    html = (ROOT / "base.html").read_text(encoding="utf-8")
    headline = re.sub(r"\*\*(.+?)\*\*", r'<span class="hl"><span>\1</span></span>', spec["headline"])
    return (html.replace("/*__FONTS__*/", ensure_fonts())
                .replace("__THEME__", "dark" if spec.get("theme") == "dark" else "light")
                .replace("__TAG__", spec["tag"])
                .replace("__H1CLASS__", "s" if spec.get("small_h1") else "")
                .replace("__HEADLINE__", headline)
                .replace("__SUB__", spec["sub"])
                .replace("__VISUAL__", spec["visual_html"]))


def main():
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = pathlib.Path(sys.argv[2]).resolve()
    tmp = out.with_suffix(".html")
    tmp.write_text(build_html(spec), encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(700)
        if not pg.evaluate("document.fonts.check('800 40px PJS')"):
            sys.exit("font did not load")
        overflow = pg.evaluate("document.querySelector('.wrap').scrollHeight > 1350")
        pg.screenshot(path=str(out))
        b.close()
    tmp.unlink()
    print(f"rendered {out}" + ("  WARNING: content overflows, shorten text" if overflow else ""))


if __name__ == "__main__":
    main()
