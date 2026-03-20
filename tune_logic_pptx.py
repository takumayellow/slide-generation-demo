"""Tune the committed StepBy logic slide PPTX for readability only."""
from pathlib import Path
import tempfile
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "outputs" / "StepByハッカソン" / "_baseline_from_head.pptx"
OUTPUT = ROOT / "outputs" / "StepByハッカソン" / "ロジック_スライド_調整版.pptx"
SLIDE_XML = "ppt/slides/slide1.xml"

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}

ET.register_namespace("a", NS["a"])
ET.register_namespace("p", NS["p"])


def geom(elem: ET.Element) -> tuple[str, str, str, str]:
    xfrm = elem.find(".//a:xfrm", NS)
    off = xfrm.find("a:off", NS) if xfrm is not None else None
    ext = xfrm.find("a:ext", NS) if xfrm is not None else None
    return (
        off.attrib.get("x", "") if off is not None else "",
        off.attrib.get("y", "") if off is not None else "",
        ext.attrib.get("cx", "") if ext is not None else "",
        ext.attrib.get("cy", "") if ext is not None else "",
    )


def set_uniform_size(elem: ET.Element, pt: int) -> None:
    val = str(pt * 100)
    for rpr in elem.findall(".//a:rPr", NS):
        rpr.set("sz", val)
    for end in elem.findall(".//a:endParaRPr", NS):
        end.set("sz", val)


def set_fill(elem: ET.Element, hex_color: str) -> None:
    solid = elem.find(".//a:solidFill", NS)
    if solid is None:
        return
    srgb = solid.find("a:srgbClr", NS)
    if srgb is None:
        srgb = ET.SubElement(solid, f"{{{NS['a']}}}srgbClr")
    srgb.set("val", hex_color)


def main() -> None:
    with zipfile.ZipFile(SOURCE, "r") as zf:
        root = ET.fromstring(zf.read(SLIDE_XML))

    for elem in root.findall(".//p:sp", NS):
        x, y, cx, cy = geom(elem)

        # Content boxes
        if (x, y, cx, cy) == ("1371600", "3200400", "3840480", "2286000"):
            set_uniform_size(elem, 14)
        elif (x, y, cx, cy) == ("7223760", "3200400", "3840480", "2286000"):
            set_uniform_size(elem, 15)
        elif (x, y, cx, cy) == ("13075920", "3200400", "3840480", "2286000"):
            set_uniform_size(elem, 14)

        # 4 pipeline texts
        elif cy == "411480":
            set_uniform_size(elem, 14)

        # Footer note
        elif (x, y, cx, cy) == ("1463040", "7955280", "15361920", "457200"):
            set_uniform_size(elem, 14)

        # Background shapes behind boxes
        elif (x, y, cx, cy) == ("1005840", "2926080", "4572000", "2743200"):
            set_fill(elem, "1F2933")
        elif (x, y, cx, cy) == ("6858000", "2926080", "4572000", "2743200"):
            set_fill(elem, "5548E5")
        elif (x, y, cx, cy) == ("12710160", "2926080", "4572000", "2743200"):
            set_fill(elem, "2563EB")

    slide_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

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
