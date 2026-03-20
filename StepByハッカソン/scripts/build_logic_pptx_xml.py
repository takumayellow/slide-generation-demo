"""Compose a polished StepBy logic slide PPTX by merging template visuals."""
from copy import deepcopy
from pathlib import Path
import tempfile
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "青と白　シンプル　ポートフォリオ　プレゼンテーション.pptx"
SOURCE = ROOT / "outputs" / "StepByハッカソン" / "ロジック_スライド.pptx"
OUTPUT = ROOT / "outputs" / "StepByハッカソン" / "ロジック_スライド_完成.pptx"

SLIDE_XML = "ppt/slides/slide1.xml"

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}

ET.register_namespace("a", NS["a"])
ET.register_namespace("p", NS["p"])


def get_sp_tree(root: ET.Element) -> ET.Element:
    return root.find("p:cSld/p:spTree", NS)


def next_shape_id(sp_tree: ET.Element) -> int:
    max_id = 0
    for elem in sp_tree:
        nv = (
            elem.find("p:nvSpPr/p:cNvPr", NS)
            or elem.find("p:nvGrpSpPr/p:cNvPr", NS)
            or elem.find("p:nvPicPr/p:cNvPr", NS)
            or elem.find("p:nvCxnSpPr/p:cNvPr", NS)
        )
        if nv is not None:
            max_id = max(max_id, int(nv.attrib.get("id", "0")))
    return max_id + 1


def set_new_ids(elem: ET.Element, start_id: int) -> int:
    for nv in elem.findall(".//p:cNvPr", NS):
        nv.set("id", str(start_id))
        start_id += 1
    return start_id


def copy_elements(src_tree: ET.Element, indexes: list[int]) -> list[ET.Element]:
    return [deepcopy(list(src_tree)[i]) for i in indexes]


def insert_many(sp_tree: ET.Element, index: int, elems: list[ET.Element]) -> None:
    for offset, elem in enumerate(elems):
        sp_tree.insert(index + offset, elem)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(TEMPLATE, "r") as zf:
        template_root = ET.fromstring(zf.read(SLIDE_XML))

    with zipfile.ZipFile(SOURCE, "r") as zf:
        generated_root = ET.fromstring(zf.read(SLIDE_XML))
        template_tree = get_sp_tree(template_root)
        generated_tree = get_sp_tree(generated_root)

        new_id = next_shape_id(generated_tree)

        # Copy template visuals only.
        header_group = copy_elements(template_tree, [2, 10])
        flow_visuals = copy_elements(template_tree, [3, 11, 4, 5, 6, 7, 8, 9])

        for elem in header_group + flow_visuals:
            new_id = set_new_ids(elem, new_id)

        # Insert header bar and page block behind generated page/title text.
        insert_many(generated_tree, 2, header_group[:1])
        insert_many(generated_tree, 4, header_group[1:])

        # Insert icon circles, icons and dividers before the flow boxes.
        insert_many(generated_tree, 8, flow_visuals)

        slide_xml = ET.tostring(generated_root, encoding="utf-8", xml_declaration=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
        temp_path = Path(tmp.name)

    with zipfile.ZipFile(SOURCE, "r") as src_zip, zipfile.ZipFile(temp_path, "w") as dst_zip:
        for info in src_zip.infolist():
            data = slide_xml if info.filename == SLIDE_XML else src_zip.read(info.filename)
            dst_zip.writestr(info, data)

    OUTPUT.write_bytes(temp_path.read_bytes())
    temp_path.unlink(missing_ok=True)

    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
