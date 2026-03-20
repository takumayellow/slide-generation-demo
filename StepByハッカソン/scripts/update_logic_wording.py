from pathlib import Path
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
PPTX_PATH = ROOT / "outputs" / "StepByハッカソン" / "ロジック.pptx"
SLIDE_XML = "ppt/slides/slide1.xml"
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def replace_texts(text_nodes: list[ET.Element]) -> None:
    replacements = {
        "リポジトリ情報を取得": "必要情報を取得",
        "ファイル構造": "Issue",
        " / README": "",
        "・Issue (title, body)": "・README / Docs",
        "Issueの粒度調整": "Issueの粒度調整",
        "参加しやすい小ステップ": "参加しやすい小ステップ",
        "プロジェクト": "プロジェクト参加",
        "オンボーディングガイド自動生成": "最初の一歩を提示",
    }
    for node in text_nodes:
        if node.text in replacements:
            node.text = replacements[node.text]


def main() -> None:
    backup_path = PPTX_PATH.with_name("ロジック_pre_wording_update.pptx")
    shutil.copy2(PPTX_PATH, backup_path)

    with zipfile.ZipFile(PPTX_PATH, "r") as src_zip:
        slide_xml = src_zip.read(SLIDE_XML)
        other_entries = [
            (info, src_zip.read(info.filename))
            for info in src_zip.infolist()
            if info.filename != SLIDE_XML
        ]

    root = ET.fromstring(slide_xml)
    text_nodes = root.findall(".//a:t", NS)
    replace_texts(text_nodes)
    new_slide_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
        temp_path = Path(tmp.name)

    with zipfile.ZipFile(temp_path, "w") as dst_zip:
        for info, data in other_entries:
            dst_zip.writestr(info, data)
        dst_zip.writestr(SLIDE_XML, new_slide_xml)

    shutil.move(temp_path, PPTX_PATH)
    print(f"Updated: {PPTX_PATH}")
    print(f"Backup: {backup_path}")


if __name__ == "__main__":
    main()
