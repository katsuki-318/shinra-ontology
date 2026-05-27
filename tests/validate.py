"""
神羅万象オントロジー — 全ドメインバリデーション
使い方: python tests/validate.py [--file src/shinra-core.ttl]
依存: pip install rdflib
"""
import sys
import argparse
import pathlib
from collections import defaultdict

try:
    from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef
    from rdflib.namespace import SKOS, DCTERMS
except ImportError:
    print("rdflib が見つかりません。インストールしてください:")
    print("  pip install rdflib")
    sys.exit(1)

ROOT   = pathlib.Path(__file__).parent.parent
SRC    = ROOT / "src"
SHINRA = Namespace("https://w3id.org/shinra/ont/")

# 依存順の先頭2ファイル + 残りは src/ を自動スキャン
_PRIORITY = ["shinra-core.ttl", "shinra-mid.ttl"]
_AUTO = sorted(
    p.name for p in (ROOT / "src").glob("shinra-*.ttl")
    if p.name not in _PRIORITY and p.name != "catalog-v001.xml"
)
ALL_MODULES = _PRIORITY + _AUTO

def parse_args():
    p = argparse.ArgumentParser(description="神羅万象オントロジー バリデーター")
    p.add_argument("--file", help="特定ファイルのみ検証 (例: src/shinra-core.ttl)")
    p.add_argument("--summary", action="store_true", help="サマリーのみ表示（詳細リスト省略）")
    return p.parse_args()

def load_graph(files: list[pathlib.Path]) -> Graph:
    g = Graph()
    loaded = []
    for f in files:
        if not f.exists():
            continue
        try:
            g.parse(str(f), format="turtle")
            loaded.append(f.name)
        except Exception as e:
            print(f"[ERROR] {f.name} パースエラー: {e}")
            sys.exit(1)
    return g, loaded

def print_section(title: str):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")

def validate(g: Graph, loaded: list[str], summary_only: bool = False):
    print("=" * 60)
    print("  神羅万象オントロジー バリデーション")
    print("=" * 60)
    print(f"\n読み込みモジュール ({len(loaded)} 件):")
    for name in loaded:
        print(f"  [OK] {name}")
    print(f"\n[OK] Turtle 構文チェック通過 (累計トリプル数: {len(g):,})")

    # ── クラス ──────────────────────────────────────────────────
    classes = sorted(
        (str(s),
         str(g.value(s, RDFS.label, default="")),
         str(g.value(s, SKOS.notation, default="")))
        for s in g.subjects(RDF.type, OWL.Class)
        if str(s).startswith("https://w3id.org/shinra/ont/")
    )
    print_section(f"クラス: {len(classes)} 個")
    if not summary_only:
        for uri, label, notation in classes:
            name = uri.replace("https://w3id.org/shinra/ont/", "shinra:")
            print(f"  {notation:<22} {name:<42} {label}")

    # ── オブジェクトプロパティ ────────────────────────────────────
    obj_props = sorted(
        (str(s),
         str(g.value(s, RDFS.label, default="")),
         str(g.value(s, SKOS.notation, default="")))
        for s in g.subjects(RDF.type, OWL.ObjectProperty)
        if str(s).startswith("https://w3id.org/shinra/")
    )
    print_section(f"オブジェクトプロパティ: {len(obj_props)} 個")
    if not summary_only:
        for uri, label, notation in obj_props:
            name = uri.replace("https://w3id.org/shinra/ont/", "shinra:")
            print(f"  {notation:<22} {name:<42} {label}")

    # ── データプロパティ ──────────────────────────────────────────
    data_props = sorted(
        (str(s),
         str(g.value(s, RDFS.label, default="")),
         str(g.value(s, SKOS.notation, default="")))
        for s in g.subjects(RDF.type, OWL.DatatypeProperty)
        if str(s).startswith("https://w3id.org/shinra/")
    )
    print_section(f"データプロパティ: {len(data_props)} 個")
    if not summary_only:
        for uri, label, notation in data_props:
            name = uri.replace("https://w3id.org/shinra/ont/", "shinra:")
            print(f"  {notation:<22} {name:<42} {label}")

    # ── インスタンス ──────────────────────────────────────────────
    typed_inds = {}
    for s in g.subjects(RDF.type, None):
        uri = str(s)
        if "shinra/data/" in uri:
            lv = g.value(URIRef(uri), RDFS.label)
            typed_inds[uri] = str(lv) if lv else ""
    print_section(f"インスタンス: {len(typed_inds)} 個")
    if not summary_only:
        for uri, label in sorted(typed_inds.items()):
            name = uri.replace("https://w3id.org/shinra/data/", "shinra-data:")
            print(f"  {name:<52} {label}")

    # ── ドメイン別クラス数 ────────────────────────────────────────
    domain_counts: dict[str, int] = defaultdict(int)
    for s, _, notation in classes:
        n = str(g.value(URIRef(s), SKOS.notation, default=""))
        if n.startswith("SHINRA_00001"): domain_counts["core"] += 1
        elif n.startswith("SHINRA_00002"): domain_counts["physical"] += 1
        elif n.startswith("SHINRA_00003"): domain_counts["social"] += 1
        elif n.startswith("SHINRA_00004"): domain_counts["information"] += 1
        elif n.startswith("SHINRA_00005"): domain_counts["biology"] += 1
        elif n.startswith("SHINRA_00006"): domain_counts["geography"] += 1
        elif n.startswith("SHINRA_00007"): domain_counts["history"] += 1
        elif n.startswith("SHINRA_00008"): domain_counts["abstract"] += 1
        else: domain_counts["mid/other"] += 1
    print_section("ドメイン別クラス数")
    for domain, count in sorted(domain_counts.items()):
        bar = "#" * (count // 2) + ("|" if count % 2 else "")
        print(f"  {domain:<15} {count:>4} {bar}")

    # ── 重複notationチェック ──────────────────────────────────────
    notations: dict[str, str] = {}
    dups = []
    for s, p, o in g.triples((None, SKOS.notation, None)):
        key = str(o)
        if key in notations and notations[key] != str(s):
            dups.append((key, notations[key], str(s)))
        notations[key] = str(s)
    print()
    if dups:
        print(f"[WARNING] notation 重複 ({len(dups)} 件):")
        for key, u1, u2 in dups:
            print(f"  {key}: {u1} vs {u2}")
    else:
        print(f"[OK] notation 重複なし ({len(notations)} 個)")

    # ── ラベル欠損チェック ────────────────────────────────────────
    missing = []
    for s in g.subjects(RDF.type, OWL.Class):
        if not str(s).startswith("https://w3id.org/shinra/"): continue
        langs = {str(l.language) for l in g.objects(s, RDFS.label)
                 if hasattr(l, "language")}
        if "ja" not in langs: missing.append(("@ja 欠損", str(s)))
        if "en" not in langs: missing.append(("@en 欠損", str(s)))
    if missing:
        print(f"[WARNING] ラベル欠損 ({len(missing)} 件):")
        for kind, uri in missing:
            name = uri.replace("https://w3id.org/shinra/ont/", "shinra:")
            print(f"  {kind}: {name}")
    else:
        print(f"[OK] 全クラスに @ja / @en ラベルあり")

    # ── rdfs:comment 欠損チェック ────────────────────────────────
    no_comment = []
    for s in g.subjects(RDF.type, OWL.Class):
        if not str(s).startswith("https://w3id.org/shinra/"): continue
        if not list(g.objects(s, RDFS.comment)):
            no_comment.append(str(s))
    if no_comment:
        print(f"[WARNING] rdfs:comment 欠損 ({len(no_comment)} 件):")
        for uri in no_comment[:10]:
            print(f"  {uri.replace('https://w3id.org/shinra/ont/', 'shinra:')}")
    else:
        print(f"[OK] 全クラスに rdfs:comment あり")

    # ── サマリー ──────────────────────────────────────────────────
    errors = len(dups) + len(missing) + len(no_comment)
    print("\n" + "=" * 60)
    print(f"  クラス: {len(classes)}  プロパティ: {len(obj_props)+len(data_props)}"
          f"  インスタンス: {len(typed_inds)}  トリプル: {len(g):,}")
    status = "[PASS] バリデーション完了 -- 問題なし" if errors == 0 else f"[WARN] 警告 {errors} 件"
    print(f"  {status}")
    print("=" * 60)
    return errors

if __name__ == "__main__":
    args = parse_args()

    if args.file:
        files = [pathlib.Path(args.file)]
    else:
        files = [SRC / m for m in ALL_MODULES]

    g, loaded = load_graph(files)
    rc = validate(g, loaded, summary_only=args.summary)
    sys.exit(0 if rc == 0 else 1)
