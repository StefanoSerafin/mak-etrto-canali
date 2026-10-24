#!/usr/bin/env python3
"""
Rigenera index.html della web app "Canali ETRTO" da Mak/Canali XLS.xlsx.

    python3 data/build.py [percorso/del/file.xlsx]

Excel: prima riga d'intestazione, poi colonna A battistrada, B spalla,
C diametro, dalla D in poi i canali ammessi (es. 5½J, 6J, 3.50B).
Legge il file senza librerie esterne (un .xlsx è uno zip di XML).
"""
import datetime
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_XLSX = os.path.join(ROOT, "..", "Canali XLS.xlsx")
NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def col_index(ref):
    letters = re.match(r"[A-Z]+", ref).group()
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_rows(path):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("a:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["a"])))
    sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    for row in sheet.findall(".//a:row", NS):
        cells = {}
        for c in row.findall("a:c", NS):
            v = c.find("a:v", NS)
            if v is not None:
                val = shared[int(v.text)] if c.get("t") == "s" else v.text
            else:
                t = c.find(".//a:t", NS)
                val = t.text if t is not None else None
            if val is not None and val.strip():
                cells[col_index(c.get("r"))] = val.strip()
        yield cells


def num(x):
    f = float(x.replace(",", "."))
    return str(int(f)) if f == int(f) else str(f)


def canale(x):
    # "3½ J" e "3½J" compaiono entrambi nell'Excel: stessa cosa, una sola forma
    return re.sub(r"\s+", "", x)


def build(xlsx):
    data = {}
    rows = list(read_rows(xlsx))
    for cells in rows[1:]:
        if not all(i in cells for i in (0, 1, 2)):
            continue
        key = "_".join(num(cells[i]) for i in (0, 1, 2))
        canali = [canale(cells[i]) for i in sorted(cells) if i >= 3]
        if not canali:
            print(f"  [avviso] {key}: nessun canale")
        if key in data:
            print(f"  [avviso] {key}: misura ripetuta, tengo l'ultima")
        data[key] = canali
    return data


def main():
    xlsx = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_XLSX
    data = build(xlsx)
    if len(data) < 100:
        sys.exit(f"Solo {len(data)} misure lette da {xlsx}: controllare il file.")
    tpl = open(os.path.join(ROOT, "index.template.html"), encoding="utf-8").read()
    out = tpl.replace("/*ETRTO_DATA*/", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    out = out.replace("/*BUILD*/", datetime.date.today().isoformat())
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
    n_canali = sum(len(v) for v in data.values())
    print(f"index.html scritto: {len(data)} misure, {n_canali} abbinamenti misura-canale.")


if __name__ == "__main__":
    main()
