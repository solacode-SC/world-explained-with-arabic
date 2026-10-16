#!/usr/bin/env python3
"""
Generate SVG content cards for the README plain-text sections.
Matches the existing design system:
  - Dark: bg gradient #0a2142→#12427f, text #fbf8ea/#e8f0f7, accent #f0cb5a, border #33669b, muted #a9c0d8
  - Light: bg gradient #fbf8ea→#e9f0e2, text #123e7c/#1d2f4a, accent #c9981a, border #b9cfcf, muted #5b6f8a
  - Fonts: FahmRuqaa (embedded), fallback to Aref Ruqaa / Reem Kufi / Amiri
"""

import re, sys, os

# ── Extract font data from an existing SVG ──────────────────────────
def extract_font_css(svg_path):
    """Pull the full @font-face block from an existing SVG."""
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"(<style>.*?</style>)", content, re.DOTALL)
    if m:
        return m.group(1)
    return "<style></style>"

# ── Theme palettes ───────────────────────────────────────────────────
DARK = {
    "bg_start":    "#0a2142",
    "bg_end":      "#12427f",
    "text":        "#fbf8ea",
    "body":        "#e8f0f7",
    "accent":      "#f0cb5a",
    "border":      "#33669b",
    "muted":       "#a9c0d8",
    "card_bg":     "#0c2d5c",
    "card_border": "#33669b",
    "card_op":     ".72",
    "pill_bg":     "#0c2d5c",
    "pill_border": "#9cc7ee",
    "pill_text":   "#fbf8ea",
    "code_bg":     "#0a1929",
    "code_border": "#33669b",
    "code_text":   "#e8f0f7",
    "code_prompt": "#f0cb5a",
    "code_comment":"#a9c0d8",
}

LIGHT = {
    "bg_start":    "#fbf8ea",
    "bg_end":      "#e9f0e2",
    "text":        "#123e7c",
    "body":        "#1d2f4a",
    "accent":      "#c9981a",
    "border":      "#b9cfcf",
    "muted":       "#5b6f8a",
    "card_bg":     "#ffffff",
    "card_border": "#b9cfcf",
    "card_op":     ".82",
    "pill_bg":     "#ffffff",
    "pill_border": "#1c5fa8",
    "pill_text":   "#123e7c",
    "code_bg":     "#f3f0e0",
    "code_border": "#b9cfcf",
    "code_text":   "#1d2f4a",
    "code_prompt": "#c9981a",
    "code_comment":"#5b6f8a",
}


# ── SVG shell ────────────────────────────────────────────────────────
def svg_shell(width, height, palette, style_block, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {width} {height}" width="{width}" height="{height}">{style_block}<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{palette['bg_start']}"/><stop offset="1" stop-color="{palette['bg_end']}"/></linearGradient><clipPath id="card"><rect width="{width}" height="{height}" rx="18"/></clipPath></defs><g clip-path="url(#card)"><rect width="{width}" height="{height}" fill="url(#bg)"/>{body}</g><rect x=".75" y=".75" width="{width-1.5}" height="{height-1.5}" rx="18" fill="none" stroke="{palette['border']}" stroke-width="1.5"/></svg>'''


# ── 1. About section content ────────────────────────────────────────
def make_about(palette, style):
    W, H = 900, 340
    p = palette
    # Paragraph text lines
    lines = [
        ("⁧فهم مشروع يشرح مفاهيم العالم باللغة العربية بأسلوب واضح ودقيق وجميل.⁩", 48),
        ("⁧نؤمن أن المعرفة تُفهم بعمق أكبر، وتنتشر أوسع، حين تُقدَّم بلغة القارئ نفسه.⁩", 78),
    ]
    # Bullet items
    bullets = [
        ("⁧شرح مبسّط لكل مفهوم دون إخلال بالدقة.⁩",                    "📖"),
        ("⁧المصطلح الإنجليزي المقابل بجانب كل مفهوم.⁩",                "🔤"),
        ("⁧أمثلة من الحياة اليومية تقرّب الفكرة.⁩",                     "💡"),
        ("⁧ربط المفاهيم المتقاربة ببعضها.⁩",                           "🔗"),
        ("⁧تصميم هادئ يسهّل القراءة.⁩",                                "🎨"),
    ]
    body = ""
    # Subtitle line
    body += f'<text x="876" y="28" font-size="13" font-family="Georgia,serif" font-style="italic" letter-spacing="1.5" text-anchor="end" fill="{p["muted"]}">Understand the world — in your language</text>'
    # Separator
    body += f'<path d="M40 40H860" stroke="{p["border"]}" stroke-opacity=".5"/>'
    # Paragraph
    for txt, y in lines:
        body += f'<text x="876" y="{y+16}" font-size="19" font-family="\'FahmNaskh\',\'Amiri\',serif" font-weight="400" text-anchor="end" fill="{p["body"]}" >{txt}</text>'
    # Bullet list
    y_start = 130
    for i, (txt, icon) in enumerate(bullets):
        y = y_start + i * 40
        # Card background for each bullet
        body += f'<rect x="40" y="{y-24}" width="836" height="36" rx="10" fill="{p["card_bg"]}" fill-opacity="{p["card_op"]}" stroke="{p["card_border"]}" stroke-opacity=".4"/>'
        # Accent dot
        body += f'<circle cx="856" cy="{y-6}" r="4" fill="{p["accent"]}"/>'
        # Text
        body += f'<text x="840" y="{y}" font-size="17" font-family="\'FahmNaskh\',\'Amiri\',serif" font-weight="400" text-anchor="end" fill="{p["body"]}" >{txt}</text>'
    return svg_shell(W, H, p, style, body)


# ── 2. Quick-start code section ──────────────────────────────────────
def make_quickstart(palette, style):
    W, H = 900, 200
    p = palette
    body = ""
    # Terminal window header
    body += f'<rect x="30" y="16" width="840" height="168" rx="14" fill="{p["code_bg"]}" stroke="{p["code_border"]}"/>'
    # Window dots
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        body += f'<circle cx="{840-i*22}" cy="38" r="6" fill="{c}"/>'
    # Terminal title
    body += f'<text x="750" y="42" font-size="12" font-family="\'FahmNaskh\',\'Amiri\',serif" text-anchor="end" fill="{p["muted"]}">⁧سطر الأوامر⁩</text>'
    # Code lines
    code_lines = [
        (f'<tspan fill="{p["code_prompt"]}">$</tspan>  git clone https://github.com/solacode-SC/REPO_NAME.git', 78),
        (f'<tspan fill="{p["code_prompt"]}">$</tspan>  cd REPO_NAME', 102),
        (f'<tspan fill="{p["code_comment"]}"># أضف هنا خطوات تشغيل مشروعك (تثبيت الحزم ثم التشغيل)</tspan>', 126),
    ]
    for markup, y in code_lines:
        body += f'<text x="830" y="{y}" font-size="15" font-family="\'JetBrains Mono\',\'Fira Code\',monospace" text-anchor="end" fill="{p["code_text"]}" direction="ltr" >{markup}</text>'
    # Hint at bottom
    body += f'<text x="450" y="160" font-size="12" font-family="\'FahmNaskh\',\'Amiri\',serif" text-anchor="middle" fill="{p["muted"]}" >⁧استبدل REPO_NAME باسم مستودعك⁩</text>'
    return svg_shell(W, H, p, style, body)


# ── 3. Contribute section ────────────────────────────────────────────
def make_contribute(palette, style):
    W, H = 900, 300
    p = palette
    body = ""
    steps = [
        ("١", "⁧افتح Issue لاقتراح مفهوم جديد أو لتصحيح شرح موجود.⁩"),
        ("٢", "⁧اتبع قالب الشرح: المفهوم، المصطلح بالإنجليزية، التعريف، مثال، مفاهيم مرتبطة.⁩"),
        ("٣", "⁧أرسل Pull Request بتغييراتك، وسنراجعها معًا.⁩"),
    ]
    y_start = 30
    for i, (num, txt) in enumerate(steps):
        y = y_start + i * 72
        # Card
        body += f'<rect x="40" y="{y}" width="820" height="60" rx="14" fill="{p["card_bg"]}" fill-opacity="{p["card_op"]}" stroke="{p["card_border"]}" stroke-opacity=".5"/>'
        # Number circle
        body += f'<circle cx="826" cy="{y+30}" r="22" fill="{p["accent"]}" fill-opacity=".15" stroke="{p["accent"]}" stroke-opacity=".7"/>'
        body += f'<text x="826" y="{y+40}" font-size="26" font-family="\'FahmRuqaa\',\'Aref Ruqaa\',serif" font-weight="700" text-anchor="middle" fill="{p["text"]}" >{num}</text>'
        # Step text
        body += f'<text x="790" y="{y+38}" font-size="18" font-family="\'FahmNaskh\',\'Amiri\',serif" font-weight="400" text-anchor="end" fill="{p["body"]}" >{txt}</text>'
    # License bar
    ly = y_start + 3 * 72 + 6
    body += f'<rect x="40" y="{ly}" width="820" height="48" rx="14" fill="{p["accent"]}" fill-opacity=".08" stroke="{p["accent"]}" stroke-opacity=".35"/>'
    body += f'<text x="840" y="{ly+32}" font-size="16" font-family="\'FahmKufi\',\'Reem Kufi\',serif" font-weight="400" text-anchor="end" fill="{p["accent"]}" >⁧الترخيص:⁩</text>'
    body += f'<text x="755" y="{ly+32}" font-size="16" font-family="\'FahmNaskh\',\'Amiri\',serif" font-weight="400" text-anchor="end" fill="{p["body"]}" >⁧حدّد ترخيص المشروع هنا (مثال: MIT).⁩</text>'
    return svg_shell(W, H, p, style, body)


# ── Main ─────────────────────────────────────────────────────────────
def main():
    base = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(base, "assets")

    # Extract font style from an existing SVG
    style = extract_font_css(os.path.join(assets, "fields-dark.svg"))

    generators = {
        "about-content":     make_about,
        "quickstart-content":make_quickstart,
        "contribute-content":make_contribute,
    }

    for name, fn in generators.items():
        for theme, palette in [("dark", DARK), ("light", LIGHT)]:
            svg = fn(palette, style)
            path = os.path.join(assets, f"{name}-{theme}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"✅ {path}")

    print("\n🎉 All content SVGs generated!")

if __name__ == "__main__":
    main()

