"""
shinra-core.ttl SPARQL クエリサンプル
使い方: python tests/sparql_examples.py
依存: pip install rdflib
"""
import pathlib, sys
try:
    from rdflib import Graph
except ImportError:
    print("pip install rdflib"); sys.exit(1)

ROOT = pathlib.Path(__file__).parent.parent
g = Graph()
g.parse(str(ROOT / "src" / "shinra-core.ttl"), format="turtle")
print(f"ロード完了: {len(g)} トリプル\n")

# Q1: すべての MaterialEntity サブクラスを列挙
q1 = """
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?cls ?label WHERE {
  ?cls rdfs:subClassOf+ shinra:MaterialEntity .
  OPTIONAL { ?cls rdfs:label ?label FILTER(lang(?label)="ja") }
}
"""
print("=== Q1: MaterialEntity のサブクラス ===")
for row in g.query(q1):
    name = str(row.cls).replace("https://w3id.org/shinra/ont/","shinra:")
    print(f"  {name:<40} {row.label or ''}")

# Q2: すべての Process サブクラスを列挙
q2 = """
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?cls ?label WHERE {
  ?cls rdfs:subClassOf+ shinra:Process .
  OPTIONAL { ?cls rdfs:label ?label FILTER(lang(?label)="ja") }
}
"""
print("\n=== Q2: Process のサブクラス ===")
for row in g.query(q2):
    name = str(row.cls).replace("https://w3id.org/shinra/ont/","shinra:")
    print(f"  {name:<40} {row.label or ''}")

# Q3: インスタンスと型
q3 = """
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX shinra-data: <https://w3id.org/shinra/data/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?ind ?type ?label WHERE {
  ?ind rdf:type ?type .
  FILTER(STRSTARTS(STR(?ind), "https://w3id.org/shinra/data/"))
  FILTER(STRSTARTS(STR(?type), "https://w3id.org/shinra/ont/"))
  OPTIONAL { ?ind rdfs:label ?label FILTER(lang(?label)="ja") }
}
"""
print("\n=== Q3: インスタンス一覧 ===")
for row in g.query(q3):
    ind = str(row.ind).replace("https://w3id.org/shinra/data/","shinra-data:")
    t   = str(row.type).replace("https://w3id.org/shinra/ont/","shinra:")
    print(f"  {ind:<40} : {t:<30} {row.label or ''}")

# Q4: すべてのクラスの SHINRA notation + label
q4 = """
PREFIX shinra: <https://w3id.org/shinra/ont/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?notation ?label WHERE {
  ?cls a owl:Class .
  FILTER(STRSTARTS(STR(?cls), "https://w3id.org/shinra/ont/"))
  ?cls skos:notation ?notation .
  ?cls rdfs:label ?label FILTER(lang(?label)="ja") .
}
ORDER BY ?notation
"""
print("\n=== Q4: クラス一覧（notation順） ===")
for row in g.query(q4):
    print(f"  {str(row.notation):<20} {str(row.label)}")
