"""Generate the 'Logic' slide for StepBy hackathon presentation."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import copy

# -- Constants --
NAVY = RGBColor(0x26, 0x22, 0x62)
BLUE = RGBColor(0x00, 0xAE, 0xEF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_GRAY = RGBColor(0x2D, 0x33, 0x3B)
PURPLE = RGBColor(0x6C, 0x5C, 0xE7)
ACCENT_BLUE = RGBColor(0x3B, 0x82, 0xF6)
LIGHT_BG = RGBColor(0xF0, 0xF4, 0xF8)
MUTED = RGBColor(0x64, 0x74, 0x8B)

SLIDE_W = Emu(18288000)  # 20 inches
SLIDE_H = Emu(10287000)  # 11.25 inches

# Load template to get dimensions and header
src = Presentation("青と白　シンプル　ポートフォリオ　プレゼンテーション.pptx")
prs = Presentation()
prs.slide_width = src.slide_width
prs.slide_height = src.slide_height

# Use blank layout
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)


def add_text_box(slide, left, top, width, height, text, font_size=18,
                 bold=False, color=NAVY, alignment=PP_ALIGN.LEFT,
                 font_name="BIZ UDPGothic"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name
    return txBox


def add_rounded_rect(slide, left, top, width, height, fill_color,
                     border_color=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    # Adjust corner radius
    shape.adjustments[0] = 0.05
    return shape


def add_multiline_box(slide, left, top, width, height, lines, font_size=14,
                      color=WHITE, bold_first=True, line_spacing=1.4,
                      font_name="BIZ UDPGothic"):
    """Add a text box with multiple lines."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(4)
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.bold = bold_first and i == 0
        run.font.name = font_name
    return txBox


# ============================================================
# 1. Header bar (matching template)
# ============================================================
header_h = Emu(1619250)
header = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, header_h
)
header.fill.solid()
header.fill.fore_color.rgb = NAVY
header.line.fill.background()

# Page number "03"
add_text_box(
    slide, Inches(0.4), Inches(0.15), Inches(1.5), Inches(1.4),
    "03", font_size=60, bold=True, color=WHITE, alignment=PP_ALIGN.LEFT
)

# Title "ロジック"
add_text_box(
    slide, Inches(2.5), Inches(0.15), Inches(10), Inches(1.4),
    "ロジック", font_size=60, bold=True, color=WHITE, alignment=PP_ALIGN.LEFT
)


# ============================================================
# 2. Subtitle
# ============================================================
add_text_box(
    slide, Inches(1.0), Inches(2.2), Inches(18), Inches(0.7),
    "GitHub API  →  Gemini AI (JSON)  →  初心者向けUI",
    font_size=26, bold=True, color=NAVY, alignment=PP_ALIGN.CENTER
)


# ============================================================
# 3. Flow diagram - 3 boxes with arrows
# ============================================================
box_w = Inches(5.0)
box_h = Inches(3.0)
box_y = Inches(3.2)
gap = Inches(1.4)
total_w = box_w * 3 + gap * 2
start_x = (SLIDE_W - total_w) // 2

# --- Box 1: GitHub API / Octokit ---
box1_x = start_x
add_rounded_rect(slide, box1_x, box_y, box_w, box_h, DARK_GRAY)
add_multiline_box(
    slide, box1_x + Inches(0.4), box_y + Inches(0.3),
    box_w - Inches(0.8), box_h - Inches(0.5),
    [
        "GitHub API / Octokit",
        "",
        "リポジトリ情報を取得",
        "・ファイル構造 / README",
        "・Issue (title, body)",
        "・PR diff",
    ],
    font_size=16, color=WHITE, bold_first=True
)

# --- Arrow 1 ---
arrow1_x = box1_x + box_w + Inches(0.15)
arrow1_y = box_y + box_h // 2 - Inches(0.25)
add_text_box(
    slide, arrow1_x, arrow1_y, gap - Inches(0.3), Inches(0.5),
    "→", font_size=48, bold=True, color=BLUE, alignment=PP_ALIGN.CENTER
)

# --- Box 2: Gemini 2.5 Flash ---
box2_x = box1_x + box_w + gap
add_rounded_rect(slide, box2_x, box_y, box_w, box_h, PURPLE)
add_multiline_box(
    slide, box2_x + Inches(0.4), box_y + Inches(0.3),
    box_w - Inches(0.8), box_h - Inches(0.5),
    [
        "Gemini 2.5 Flash",
        "",
        "初心者向けに構造化",
        "→ JSON出力",
    ],
    font_size=16, color=WHITE, bold_first=True
)

# --- Arrow 2 ---
arrow2_x = box2_x + box_w + Inches(0.15)
add_text_box(
    slide, arrow2_x, arrow1_y, gap - Inches(0.3), Inches(0.5),
    "→", font_size=48, bold=True, color=BLUE, alignment=PP_ALIGN.CENTER
)

# --- Box 3: 初心者向けUI ---
box3_x = box2_x + box_w + gap
add_rounded_rect(slide, box3_x, box_y, box_w, box_h, ACCENT_BLUE)
add_multiline_box(
    slide, box3_x + Inches(0.4), box_y + Inches(0.3),
    box_w - Inches(0.8), box_h - Inches(0.5),
    [
        "初心者向けUI",
        "",
        "わかりやすく表示",
        "・極小ステップ",
        "・公式ドキュメントリンク",
        "・コマンドコピペ",
    ],
    font_size=16, color=WHITE, bold_first=True
)


# ============================================================
# 4. Four pipelines (below flow diagram)
# ============================================================
pipeline_y = Inches(6.8)
pipeline_x = start_x + Inches(0.3)
pipeline_w = Inches(17.5)

pipelines = [
    ("①", "リポジトリ分析", "学習ロードマップ + 全Issue分解"),
    ("②", "Issue", "極小タスク分解"),
    ("③", "プロジェクト", "オンボーディングガイド自動生成"),
    ("④", "PR diff", "AIコードレビュー"),
]

col_w = pipeline_w // 2
row_h = Inches(0.65)

for i, (num, input_text, output_text) in enumerate(pipelines):
    row = i // 2
    col = i % 2
    px = pipeline_x + col * col_w
    py = pipeline_y + row * row_h

    # Number circle
    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, px, py + Inches(0.05), Inches(0.45), Inches(0.45)
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = BLUE
    circle.line.fill.background()

    # Number text
    tf = circle.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = num
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = WHITE
    run.font.name = "BIZ UDPGothic"

    # Pipeline text
    add_text_box(
        slide, px + Inches(0.6), py + Inches(0.05),
        col_w - Inches(0.8), Inches(0.45),
        f"{input_text}  →  {output_text}",
        font_size=16, bold=False, color=NAVY
    )


# ============================================================
# 5. Bottom note
# ============================================================
note_y = Inches(8.6)
note_bg = add_rounded_rect(
    slide, start_x, note_y, total_w, Inches(0.7), LIGHT_BG
)
add_text_box(
    slide, start_x + Inches(0.5), note_y + Inches(0.1),
    total_w - Inches(1.0), Inches(0.5),
    "全パイプライン共通:  Gemini 2.5 Flash  /  JSON構造化出力  /  Firestore永続化",
    font_size=16, bold=False, color=MUTED, alignment=PP_ALIGN.CENTER
)


# ============================================================
# Save
# ============================================================
output_path = "outputs/StepByハッカソン/ロジック_スライド.pptx"
prs.save(output_path)
print(f"Saved: {output_path}")
