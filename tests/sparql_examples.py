"""
神羅万象オントロジー — SPARQL クエリサンプル集（全ドメイン対応）
使い方: python tests/sparql_examples.py
依存: pip install rdflib
"""
import sys
import pathlib

try:
    from rdflib import Graph
except ImportError:
    print("pip install rdflib"); sys.exit(1)

ROOT = pathlib.Path(__file__).parent.parent
SRC  = ROOT / "src"

ALL_MODULES = [
    "shinra-core.ttl",
    "shinra-mid.ttl",
    "shinra-physical.ttl",
    "shinra-social.ttl",
    "shinra-information.ttl",
    "shinra-biology.ttl",
    "shinra-geography.ttl",
    "shinra-history.ttl",
    "shinra-abstract.ttl",
    "shinra-culture.ttl",
]

g = Graph()
loaded = []
for m in ALL_MODULES:
    f = SRC / m
    if f.exists():
        g.parse(str(f), format="turtle")
        loaded.append(m)

print(f"ロード完了: {len(loaded)} モジュール / {len(g):,} トリプル\n")

SHINRA_ONT  = "https://w3id.org/shinra/ont/"
SHINRA_DATA = "https://w3id.org/shinra/data/"

def run(title, sparql):
    print(f"=== {title} ===")
    rows = list(g.query(sparql))
    for row in rows:
        parts = []
        for v in row:
            if v is None:
                continue
            s = str(v)
            s = s.replace(SHINRA_ONT, "shinra:").replace(SHINRA_DATA, "shinra-data:")
            parts.append(s)
        print("  " + "  |  ".join(parts))
    if not rows:
        print("  (結果なし)")
    print(f"  --> {len(rows)} 件\n")

# Q1: MaterialEntity の全サブクラス（推移的）
run("Q1: MaterialEntity の全サブクラス",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?cls ?label WHERE {
  ?cls rdfs:subClassOf+ shinra:MaterialEntity .
  OPTIONAL { ?cls rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?cls
""")

# Q2: Process の全サブクラス（推移的）
run("Q2: Process の全サブクラス",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?cls ?label WHERE {
  ?cls rdfs:subClassOf+ shinra:Process .
  OPTIONAL { ?cls rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?cls
""")

# Q3: 全インスタンスと型・ラベル
run("Q3: 全インスタンス一覧（型 + @ja ラベル）",
"""
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?ind ?type ?label WHERE {
  ?ind rdf:type ?type .
  FILTER(STRSTARTS(STR(?ind),  "https://w3id.org/shinra/data/"))
  FILTER(STRSTARTS(STR(?type), "https://w3id.org/shinra/ont/"))
  OPTIONAL { ?ind rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?type ?ind
""")

# Q4: 全クラスをドメイン別に notation 順で列挙
run("Q4: 全クラス（notation 順）",
"""
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?notation ?cls ?label WHERE {
  ?cls a owl:Class .
  FILTER(STRSTARTS(STR(?cls), "https://w3id.org/shinra/ont/"))
  ?cls skos:notation ?notation .
  ?cls rdfs:label ?label FILTER(lang(?label)="ja") .
} ORDER BY ?notation
""")

# Q5: ConceptualEntity の全サブクラス（抽象・価値・知識）
run("Q5: ConceptualEntity の全サブクラス",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?cls ?label WHERE {
  ?cls rdfs:subClassOf+ shinra:ConceptualEntity .
  OPTIONAL { ?cls rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?cls
""")

# Q6: Organism の全サブクラス
run("Q6: Organism の全サブクラス（生物分類）",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?cls ?label WHERE {
  ?cls rdfs:subClassOf+ shinra:Organism .
  OPTIONAL { ?cls rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?cls
""")

# Q7: SocialInstitution の全サブクラス
run("Q7: SocialInstitution の全サブクラス",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?cls ?label WHERE {
  ?cls rdfs:subClassOf+ shinra:SocialInstitution .
  OPTIONAL { ?cls rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?cls
""")

# Q8: Wikidata ID を持つインスタンス一覧
run("Q8: Wikidata ID 付きインスタンス",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?ind ?wdId ?label WHERE {
  ?ind shinra:wikidataId ?wdId .
  OPTIONAL { ?ind rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?wdId
""")

# Q9: InformationContentEntity の全サブクラス（テキスト・データ・デジタル）
run("Q9: InformationContentEntity の全サブクラス",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?cls ?label WHERE {
  ?cls rdfs:subClassOf+ shinra:InformationContentEntity .
  OPTIONAL { ?cls rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?cls
""")

# Q10: HistoricalPeriod と開始・終了年を持つインスタンス
run("Q10: 歴史インスタンス（開始年付き）",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?ind ?label ?startYear ?endYear WHERE {
  ?ind shinra:hasStartYear ?startYear .
  OPTIONAL { ?ind rdfs:label ?label FILTER(lang(?label)="ja") }
  OPTIONAL { ?ind shinra:hasEndYear ?endYear }
} ORDER BY ?startYear
""")

# Q11: 全プロパティ（オブジェクト+データ）の domain / range サマリー
run("Q11: オブジェクトプロパティ domain/range 一覧",
"""
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?prop ?domain ?range WHERE {
  ?prop a owl:ObjectProperty .
  FILTER(STRSTARTS(STR(?prop), "https://w3id.org/shinra/"))
  OPTIONAL { ?prop rdfs:domain ?domain }
  OPTIONAL { ?prop rdfs:range  ?range  }
} ORDER BY ?prop
""")

# Q12: AdministrativeRegion の全サブクラスと地理インスタンス
run("Q12: 地理インスタンス（国・都市・山など）",
"""
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?ind ?type ?label WHERE {
  ?type rdfs:subClassOf+ shinra:GeographicRegion .
  ?ind rdf:type ?type .
  OPTIONAL { ?ind rdfs:label ?label FILTER(lang(?label)="ja") }
} ORDER BY ?type
""")
