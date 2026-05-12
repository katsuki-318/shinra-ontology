"""
shinra-core.ttl バリデーション + サマリー表示スクリプト
使い方: python tests/validate.py
依存: pip install rdflib
"""
import sys
import pathlib

try:
    from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS
    from rdflib.namespace import DCTERMS
except ImportError:
    print("rdflib が見つかりません。インストールしてください:")
    print("  pip install rdflib")
    sys.exit(1)

ROOT = pathlib.Path(__file__).parent.parent
TTL  = ROOT / "src" / "shinra-core.ttl"

SHINRA = Namespace("https://w3id.org/shinra/ont/")
BFO    = Namespace("http://purl.obolibrary.org/obo/BFO_")

# ── 構文チェック ──────────────────────────────────────────────
print("=" * 60)
print("神羅万象オントロジー バリデーション")
print("=" * 60)
print(f"\nファイル: {TTL}\n")

g = Graph()
try:
    # BFO importを解決しないで読み込み（ローカル構文チェックのみ）
    g.parse(str(TTL), format="turtle")
    print(f"[OK] Turtle 構文チェック通過 (トリプル数: {len(g)})")
except Exception as e:
    print(f"[ERROR] Turtle パースエラー: {e}")
    sys.exit(1)

# ── クラス一覧 ────────────────────────────────────────────────
classes = sorted(
    (str(s), str(g.value(s, RDFS.label, default="") ),
     str(g.value(s, SKOS.notation, default="")))
    for s in g.subjects(RDF.type, OWL.Class)
    if str(s).startswith("https://w3id.org/shinra/")
)
print(f"\n[クラス] {len(classes)} 個定義済み")
print("-" * 60)
for uri, label, notation in classes:
    name = uri.replace("https://w3id.org/shinra/ont/", "shinra:")
    print(f"  {notation:<20} {name:<40} {label}")

# ── プロパティ一覧 ─────────────────────────────────────────────
obj_props = sorted(
    (str(s), str(g.value(s, RDFS.label, default="")),
     str(g.value(s, SKOS.notation, default="")))
    for s in g.subjects(RDF.type, OWL.ObjectProperty)
    if str(s).startswith("https://w3id.org/shinra/")
)
print(f"\n[オブジェクトプロパティ] {len(obj_props)} 個定義済み")
print("-" * 60)
for uri, label, notation in obj_props:
    name = uri.replace("https://w3id.org/shinra/ont/", "shinra:")
    print(f"  {notation:<20} {name:<40} {label}")

data_props = sorted(
    (str(s), str(g.value(s, RDFS.label, default="")),
     str(g.value(s, SKOS.notation, default="")))
    for s in g.subjects(RDF.type, OWL.DatatypeProperty)
    if str(s).startswith("https://w3id.org/shinra/")
)
print(f"\n[データプロパティ] {len(data_props)} 個定義済み")
print("-" * 60)
for uri, label, notation in data_props:
    name = uri.replace("https://w3id.org/shinra/ont/", "shinra:")
    print(f"  {notation:<20} {name:<40} {label}")

# ── インスタンス一覧 ──────────────────────────────────────────
inds = sorted(
    (str(s), str(g.value(s, RDFS.label, default="")),
     str(g.value(s, SKOS.notation, default="")))
    for s in g.subjects(RDF.type, OWL.NamedIndividual)
    if str(s).startswith("https://w3id.org/shinra/")
)
# NamedIndividual でないものも拾う（型指定インスタンス）
typed_inds = set()
for s in g.subjects(RDF.type, None):
    uri = str(s)
    if "shinra/data/" in uri:
        typed_inds.add(uri)

print(f"\n[インスタンス] {len(typed_inds)} 個定義済み")
print("-" * 60)
for uri in sorted(typed_inds):
    label = str(g.value(next(g.subjects(SKOS.notation, None), None), RDFS.label, default=""))
    name = uri.replace("https://w3id.org/shinra/data/", "shinra-data:")
    label_val = g.value(next(iter(g.subjects()), None), RDFS.label)
    # 各インスタンスのラベルを取得
    from rdflib import URIRef
    lv = g.value(URIRef(uri), RDFS.label)
    print(f"  {name:<50} {lv or ''}")

# ── 重複チェック ──────────────────────────────────────────────
notations = {}
dup = False
for s, p, o in g.triples((None, SKOS.notation, None)):
    key = str(o)
    if key in notations:
        print(f"\n[WARNING] 重複 notation: {key}")
        print(f"  1: {notations[key]}")
        print(f"  2: {s}")
        dup = True
    notations[key] = str(s)
if not dup:
    print(f"\n[OK] notation 重複なし ({len(notations)} 個)")

# ── ラベル欠損チェック ────────────────────────────────────────
missing_label = []
for s in g.subjects(RDF.type, OWL.Class):
    if not str(s).startswith("https://w3id.org/shinra/"): continue
    labels = list(g.objects(s, RDFS.label))
    langs = [str(l.language) for l in labels if hasattr(l, 'language')]
    if "ja" not in langs:
        missing_label.append(("@ja 欠損", str(s)))
    if "en" not in langs:
        missing_label.append(("@en 欠損", str(s)))

if missing_label:
    print(f"\n[WARNING] ラベル欠損 ({len(missing_label)}件):")
    for kind, uri in missing_label:
        print(f"  {kind}: {uri}")
else:
    print(f"[OK] 全クラスに @ja / @en ラベルあり")

print("\n" + "=" * 60)
print("バリデーション完了")
print("=" * 60)
