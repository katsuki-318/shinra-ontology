# 神羅万象オントロジー — セッション引き継ぎ文書

## プロジェクト概要
「神羅万象オントロジー」— BFO 2020準拠のRDF/OWLオントロジー。世界に存在するあらゆる概念・実体を形式的に記述することを目標とする。

- GitHub: https://github.com/katsuki-318/shinra-ontology
- GitHub Pages: https://katsuki-318.github.io/shinra-ontology/
- 永続URI: https://w3id.org/shinra/ （w3id.org PR #6152 マージ待ち）
- 名前空間: `shinra: <https://w3id.org/shinra/ont/>`, `shinra-data: <https://w3id.org/shinra/data/>`

## 現在の状態（2026-06-19時点）
| 項目 | 数値 |
|---|---|
| ドメインモジュール | 136本（src/shinra-*.ttl） |
| クラス | 1,112 |
| インスタンス | 966 |
| トリプル | 16,815 |
| バージョン | v0.5.0 |

## アーキテクチャ（3層）
```
BFO 2020（ISO/IEC 21838-2）  ← imports/bfo-2020.owl
  └─ shinra-core.ttl         ← 44クラス・21オブジェクトプロパティ
       └─ shinra-mid.ttl     ← 27中間層クラス
            └─ shinra-{domain}.ttl × 129本  ← 各専門ドメイン
```

## Notationスキーム
- クラス: `SHINRA_0XXXXXXX`（0000001〜）
- データプロパティ: `SHINRA_DXXXXXX`
- オブジェクトプロパティ: `SHINRA_RXXXXXX`
- インスタンス: `SHINRA_IXXXXXX`

## ドメイン別レンジ
| レンジ | ドメイン |
|---|---|
| 0000001-099 | 基盤コア（core） |
| 0000101-199 | 中間層（mid） |
| 0000201-299 | 自然科学 |
| 0000301-399 | 社会 |
| 0000401-499 | 情報 |
| 0000501-599 | 生物 |
| 0000601-699 | 地理 |
| 0000701-799 | 歴史 |
| 0000801-899 | 抽象・数学 |
| 0000901-999 | 文化 |
| 0001001-099 | 思想・心 |
| 0001101以降 | Phase7〜12（各ドメイン） |
| 0012001-999 | Phase12（最新） |

## ツール
- `tools/robot.jar` — OWL推論・検証（ROBOT v1.9.10）
- `tools/oxigraph.exe` — SPARQLエンドポイント（v0.5.8）
- `tests/validate.py` — rdflib検証（src/shinra-*.ttl を自動スキャン）
- `scripts/fetch_wikidata.py` — Wikidataからインスタンスを取得するスクリプト

## Oxigraphの起動方法
```bash
cd /c/Users/KatsukiMiwa/shinra-ontology
python.exe -c "
import pathlib
lines = []
for f in sorted(pathlib.Path('src').glob('shinra-*.ttl')):
    lines.append(open(f, encoding='utf-8').read())
pathlib.Path('oxigraph-all.ttl').write_text('\n'.join(lines), encoding='utf-8')
"
tools/oxigraph.exe load --location oxigraph-data --file oxigraph-all.ttl
tools/oxigraph.exe serve --location oxigraph-data --bind 0.0.0.0:7878
# → http://localhost:7878 でSPARQLエディタが開く
```

## GitHubへのpush方法（PAT使用）
```bash
git remote set-url origin https://katsuki-318:<PAT>@github.com/katsuki-318/shinra-ontology.git
git push origin master
git remote set-url origin https://github.com/katsuki-318/shinra-ontology.git
```
※ PATはユーザーに確認すること（セッション間で引き継がない）

## 現在の既知の問題
1. **未定義の親クラスが15個ある**（PhilosophicalPosition, EconomicProcess, LinguisticTheory等）
   → mid.ttlに追加するか、各モジュールで定義する必要がある
2. **インスタンスが薄い**（ラベルとWikidata IDのみ、関係プロパティなし）
   → `hasCapital`, `locatedIn`等のプロパティでインスタンス間の関係を記述する必要がある

## 次にやるべきこと（優先順）
1. 未定義親クラス15個をmid.ttlに追加して構造的整合性を確保
2. インスタンス間の関係プロパティを定義・追加（日本→首都→東京等）
3. スキーマ追加が必要なドメイン：地質学・工学・心理学（基礎）・疫学・人口統計学
4. CHANGELOG更新・v0.5.0タグ付け

## インスタンスファイル（Wikidataから取得済み）
- `src/shinra-instances-countries.ttl` — 国家 203件
- `src/shinra-instances-elements.ttl` — 化学元素 120件
- `src/shinra-instances-planets.ttl` — 惑星 4件
- `src/shinra-instances-nobel.ttl` — ノーベル賞受賞者 195件
- `src/shinra-instances-languages.ttl` — 主要言語 98件
