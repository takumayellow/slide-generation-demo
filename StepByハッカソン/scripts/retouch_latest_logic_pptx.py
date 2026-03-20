"""Retouch the latest StepBy PPTX: bottom text size and number circles."""
from pathlib import Path
import tempfile
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "outputs" / "StepByハッカソン" / "ロジック_スライド_調整版.pptx"
OUTPUT = ROOT / "outputs" / "StepByハッカソン" / "ロジック_スライド_最新版調整_v2.pptx"
SLIDE_XML = "ppt/slides/slide1.xml"

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}

ET.register_namespace("a", NS["a"])
ET.register_namespace("p", NS["p"])


def geom(elem: ET.Element):
    xfrm = elem.find(".//a:xfrm", NS)
    off = xfrm.find("a:off", NS) if xfrm is not None else None
    ext = xfrm.find("a:ext", NS) if xfrm is not None else None
    return (
        xfrm,
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


def set_shape_box(elem: ET.Element, x: int, y: int, w: int, h: int) -> None:
    xfrm = elem.find(".//a:xfrm", NS)
    if xfrm is None:
        return
    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    if off is not None:
        off.set("x", str(x))
        off.set("y", str(y))
    if ext is not None:
        ext.set("cx", str(w))
        ext.set("cy", str(h))


def set_single_text(elem: ET.Element, text: str) -> None:
    texts = elem.findall(".//a:t", NS)
    if not texts:
        return
    texts[0].text = text
    for extra in texts[1:]:
        extra.text = ""


def main() -> None:
    with zipfile.ZipFile(SOURCE, "r") as zf:
        root = ET.fromstring(zf.read(SLIDE_XML))

    for elem in root.findall(".//p:sp", NS):
        _, x, y, cx, cy = geom(elem)

        # Number circles: shrink a bit and normalize vertical rhythm.
        if (x, y, cx, cy) == ("864424", "6447432", "1531620", "1531620"):
            set_shape_box(elem, 980000, 6530000, 1220000, 1220000)
            set_uniform_size(elem, 24)
            set_single_text(elem, "1")
        elif (x, y, cx, cy) == ("9464040", "6541639", "1531620", "1531620"):
            set_shape_box(elem, 9630000, 6530000, 1220000, 1220000)
            set_uniform_size(elem, 24)
            set_single_text(elem, "2")
        elif (x, y, cx, cy) == ("866392", "8275320", "1531620", "1531620"):
            set_shape_box(elem, 980000, 8330000, 1220000, 1220000)
            set_uniform_size(elem, 24)
            set_single_text(elem, "3")
        elif (x, y, cx, cy) == ("9464040", "8386228", "1531620", "1531620"):
            set_shape_box(elem, 9630000, 8330000, 1220000, 1220000)
            set_uniform_size(elem, 24)
            set_single_text(elem, "4")

        # Pipeline texts: bigger and closer to circles.
        elif (x, y, cx, cy) == ("2630466", "7183337", "7863840", "307777"):
            set_shape_box(elem, 2520000, 7020000, 8050000, 620000)
            set_uniform_size(elem, 19)
        elif (x, y, cx, cy) == ("11567160", "7131486", "7269480", "411480"):
            set_shape_box(elem, 11380000, 7020000, 6200000, 620000)
            set_uniform_size(elem, 19)
        elif (x, y, cx, cy) == ("2630466", "8946298", "7269480", "411480"):
            set_shape_box(elem, 2520000, 8820000, 8050000, 620000)
            set_uniform_size(elem, 19)
        elif (x, y, cx, cy) == ("11560239", "9004387", "7269480", "411480"):
            set_shape_box(elem, 11380000, 8820000, 6200000, 620000)
            set_uniform_size(elem, 19)

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
