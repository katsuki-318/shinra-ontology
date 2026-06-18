"""
Wikidataから実体を取得してTTLインスタンスファイルを生成する
"""
import requests, time, pathlib, re, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {"User-Agent": "ShinraOntology/0.5 (https://github.com/katsuki-318/shinra-ontology)"}
OUT = pathlib.Path("C:/Users/KatsukiMiwa/shinra-ontology/src")

PREFIXES = """\
@prefix shinra:      <https://w3id.org/shinra/ont/> .
@prefix shinra-data: <https://w3id.org/shinra/data/> .
@prefix owl:         <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:        <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:        <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms:     <http://purl.org/dc/terms/> .
@prefix xsd:         <http://www.w3.org/2001/XMLSchema#> .

"""

def sparql(query, retries=3):
    for i in range(retries):
        try:
            r = requests.get(ENDPOINT, params={"query": query, "format": "json"},
                             headers=HEADERS, timeout=30, verify=False)
            r.raise_for_status()
            return r.json()["results"]["bindings"]
        except Exception as e:
            print(f"  retry {i+1}: {e}")
            time.sleep(5)
    return []

def safe_id(label):
    """ラベルをTurtle安全なIDに変換"""
    s = re.sub(r"[^a-zA-Z0-9]", "-", label.lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:40]

def qid(uri):
    return uri.split("/")[-1]

def write_ttl(filename, title_ja, title_en, triples):
    path = OUT / filename
    lines = [PREFIXES]
    lines.append(f'<https://w3id.org/shinra/ont/{filename.replace("shinra-","").replace(".ttl","")}>')
    lines.append(f'    a owl:Ontology ;')
    lines.append(f'    owl:versionInfo "0.5.0" ;')
    lines.append(f'    owl:imports <https://w3id.org/shinra/ont/mid> ;')
    lines.append(f'    dcterms:title "{title_ja}"@ja , "{title_en}"@en ;')
    lines.append(f'    dcterms:created "2026-06-19"^^xsd:date .\n')
    lines.extend(triples)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  書き込み: {path} ({len(triples)}トリプル)")

# ── 1. 国家 ────────────────────────────────────────────────────────
def fetch_countries():
    print("国家を取得中...")
    q = """
SELECT ?item ?ja ?en WHERE {
  ?item wdt:P31 wd:Q6256 ; wdt:P297 ?iso .
  OPTIONAL { ?item rdfs:label ?ja . FILTER(LANG(?ja)="ja") }
  OPTIONAL { ?item rdfs:label ?en . FILTER(LANG(?en)="en") }
} LIMIT 250"""
    rows = sparql(q)
    triples = []
    for i, b in enumerate(rows):
        qid_ = qid(b["item"]["value"])
        ja = b.get("ja", {}).get("value", "")
        en = b.get("en", {}).get("value", "")
        if not ja or not en: continue
        iid = f"country-{safe_id(en)}-{qid_}"
        notation = f"SHINRA_I060{i+1:03d}"
        triples.append(f"""
shinra-data:{iid}
    a shinra:Country ;
    rdfs:label "{ja}"@ja ; rdfs:label "{en}"@en ;
    shinra:wikidataId "{qid_}" ;
    skos:notation "{notation}" ; dcterms:created "2026-06-19"^^xsd:date .""")
    write_ttl("shinra-instances-countries.ttl",
              "神羅万象オントロジー — 国家インスタンス",
              "Shinra Ontology — Country Instances", triples)
    return len(triples)

# ── 2. 化学元素 ────────────────────────────────────────────────────
def fetch_elements():
    print("化学元素を取得中...")
    q = """
SELECT ?item ?ja ?en ?num WHERE {
  ?item wdt:P31 wd:Q11344 ; wdt:P1086 ?num .
  OPTIONAL { ?item rdfs:label ?ja . FILTER(LANG(?ja)="ja") }
  OPTIONAL { ?item rdfs:label ?en . FILTER(LANG(?en)="en") }
} ORDER BY ?num LIMIT 120"""
    rows = sparql(q)
    triples = []
    for b in rows:
        qid_ = qid(b["item"]["value"])
        ja = b.get("ja", {}).get("value", "")
        en = b.get("en", {}).get("value", "")
        num = int(float(b["num"]["value"]))
        if not ja or not en: continue
        iid = f"element-{safe_id(en)}-{num:03d}"
        notation = f"SHINRA_I020{num:03d}"
        triples.append(f"""
shinra-data:{iid}
    a shinra:Element ;
    rdfs:label "{ja}"@ja ; rdfs:label "{en}"@en ;
    shinra:wikidataId "{qid_}" ;
    skos:notation "{notation}" ; dcterms:created "2026-06-19"^^xsd:date .""")
    write_ttl("shinra-instances-elements.ttl",
              "神羅万象オントロジー — 化学元素インスタンス",
              "Shinra Ontology — Chemical Element Instances", triples)
    return len(triples)

# ── 3. 惑星（太陽系） ─────────────────────────────────────────────
def fetch_planets():
    print("惑星を取得中...")
    q = """
SELECT ?item ?ja ?en WHERE {
  ?item wdt:P31 wd:Q3504248 .
  OPTIONAL { ?item rdfs:label ?ja . FILTER(LANG(?ja)="ja") }
  OPTIONAL { ?item rdfs:label ?en . FILTER(LANG(?en)="en") }
}"""
    rows = sparql(q)
    triples = []
    for i, b in enumerate(rows):
        qid_ = qid(b["item"]["value"])
        ja = b.get("ja", {}).get("value", "")
        en = b.get("en", {}).get("value", "")
        if not ja or not en: continue
        iid = f"planet-{safe_id(en)}"
        notation = f"SHINRA_I021{i+1:03d}"
        triples.append(f"""
shinra-data:{iid}
    a shinra:Planet ;
    rdfs:label "{ja}"@ja ; rdfs:label "{en}"@en ;
    shinra:wikidataId "{qid_}" ;
    skos:notation "{notation}" ; dcterms:created "2026-06-19"^^xsd:date .""")
    write_ttl("shinra-instances-planets.ttl",
              "神羅万象オントロジー — 惑星インスタンス",
              "Shinra Ontology — Planet Instances", triples)
    return len(triples)

# ── 4. ノーベル賞受賞者（一部） ───────────────────────────────────
def fetch_nobel():
    print("ノーベル賞受賞者を取得中...")
    q = """
SELECT DISTINCT ?item ?ja ?en ?award WHERE {
  ?item wdt:P166 ?award .
  ?award wdt:P31 wd:Q7191 .
  OPTIONAL { ?item rdfs:label ?ja . FILTER(LANG(?ja)="ja") }
  OPTIONAL { ?item rdfs:label ?en . FILTER(LANG(?en)="en") }
} LIMIT 200"""
    rows = sparql(q)
    triples = []
    for i, b in enumerate(rows):
        qid_ = qid(b["item"]["value"])
        ja = b.get("ja", {}).get("value", "")
        en = b.get("en", {}).get("value", "")
        if not ja or not en: continue
        iid = f"person-nobel-{safe_id(en)}-{qid_}"
        notation = f"SHINRA_I012{i+1:03d}"
        triples.append(f"""
shinra-data:{iid}
    a shinra:Person ;
    rdfs:label "{ja}"@ja ; rdfs:label "{en}"@en ;
    shinra:wikidataId "{qid_}" ;
    skos:notation "{notation}" ; dcterms:created "2026-06-19"^^xsd:date .""")
    write_ttl("shinra-instances-nobel.ttl",
              "神羅万象オントロジー — ノーベル賞受賞者インスタンス",
              "Shinra Ontology — Nobel Laureate Instances", triples)
    return len(triples)

# ── 5. 主要言語 ───────────────────────────────────────────────────
def fetch_languages():
    print("主要言語を取得中...")
    q = """
SELECT ?item ?ja ?en ?speakers WHERE {
  ?item wdt:P31 wd:Q34770 ; wdt:P1098 ?speakers .
  FILTER(?speakers > 1000000)
  OPTIONAL { ?item rdfs:label ?ja . FILTER(LANG(?ja)="ja") }
  OPTIONAL { ?item rdfs:label ?en . FILTER(LANG(?en)="en") }
} ORDER BY DESC(?speakers) LIMIT 100"""
    rows = sparql(q)
    triples = []
    for i, b in enumerate(rows):
        qid_ = qid(b["item"]["value"])
        ja = b.get("ja", {}).get("value", "")
        en = b.get("en", {}).get("value", "")
        if not ja or not en: continue
        iid = f"language-{safe_id(en)}-{qid_}"
        notation = f"SHINRA_I043{i+1:03d}"
        triples.append(f"""
shinra-data:{iid}
    a shinra:NaturalLanguage ;
    rdfs:label "{ja}"@ja ; rdfs:label "{en}"@en ;
    shinra:wikidataId "{qid_}" ;
    skos:notation "{notation}" ; dcterms:created "2026-06-19"^^xsd:date .""")
    write_ttl("shinra-instances-languages.ttl",
              "神羅万象オントロジー — 主要言語インスタンス",
              "Shinra Ontology — Major Language Instances", triples)
    return len(triples)

if __name__ == "__main__":
    total = 0
    total += fetch_countries(); time.sleep(2)
    total += fetch_elements(); time.sleep(2)
    total += fetch_planets(); time.sleep(2)
    total += fetch_nobel(); time.sleep(2)
    total += fetch_languages()
    print(f"\n完了: 合計 {total} インスタンス生成")
