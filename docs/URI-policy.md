# URI 設計戦略

**文書バージョン**: 1.0.0  
**作成日**: 2026-05-12  
**状態**: 確定（凍結）

---

## 原則

> **URI は変えない。URI が変わるとリンクが死ぬ。**

オントロジーの価値はリンクの安定性に依存する。個人ドメイン（例: `miwa.dev`）は廃止リスクがあるため、永続 URI サービス **w3id.org** を使用する。

---

## ベース URI

| 名前空間 | URI |
|---|---|
| クラス・プロパティ | `https://w3id.org/shinra/ont/` |
| インスタンス（データ） | `https://w3id.org/shinra/data/` |
| バージョン付き | `https://w3id.org/shinra/ont/YYYY-MM-DD/` |

w3id.org の PR を提出し、GitHub Pages へのリダイレクトを設定する。  
PR 提出先: https://github.com/perma-id/w3id.org

---

## Prefix 宣言（Turtle ファイルの冒頭）

```turtle
@prefix shinra:      <https://w3id.org/shinra/ont/> .
@prefix shinra-data: <https://w3id.org/shinra/data/> .
@prefix bfo:         <http://purl.obolibrary.org/obo/BFO_> .
@prefix owl:         <http://www.w3.org/2002/07/owl#> .
@prefix rdf:         <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:        <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:         <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:        <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms:     <http://purl.org/dc/terms/> .
@prefix prov:        <http://www.w3.org/ns/prov#> .
@prefix time:        <http://www.w3.org/2006/time#> .
@prefix qudt:        <http://qudt.org/schema/qudt/> .
```

---

## クラス・プロパティの URI 設計

### クラス

```
https://w3id.org/shinra/ont/MaterialEntity
https://w3id.org/shinra/ont/InformationContentEntity
https://w3id.org/shinra/ont/ConceptualEntity
```

- 名前空間直後に PascalCase の英語名
- 単数形
- BFO のクラス名と被る場合は `shinra:` 名前空間で明示的に区別

### プロパティ

```
https://w3id.org/shinra/ont/participatesIn
https://w3id.org/shinra/ont/hasPart
https://w3id.org/shinra/ont/aboutness
```

- 名前空間直後に lowerCamelCase の英語動詞句

### インスタンス

```
https://w3id.org/shinra/data/tokyo-station-a3f4c9
https://w3id.org/shinra/data/natsume-soseki-b2e7d1
```

- 意味のある slug（英語小文字・ハイフン区切り）+ UUID 短縮（6文字）
- slug は人間可読性のため。UUID 部分がリネームへの耐性を担保

---

## バージョニング

### バージョン番号（SemVer）

```
MAJOR.MINOR.PATCH

例: 0.1.0 / 1.0.0 / 1.2.3
```

| 種別 | 変更の例 |
|---|---|
| MAJOR | BFO ブリッジクラスの再設計、上位階層の根本変更 |
| MINOR | 新ドメインモジュール（`shinra-bio.ttl` 等）の追加 |
| PATCH | ラベル修正、コメント追加、外部IDマッピング追記 |

### OWL バージョン宣言

```turtle
<https://w3id.org/shinra/ont/>
  a owl:Ontology ;
  owl:versionIRI <https://w3id.org/shinra/ont/2026-05-12/> ;
  owl:versionInfo "0.0.1" ;
  dcterms:created "2026-05-12"^^xsd:date ;
  dcterms:title "神羅万象オントロジー"@ja , "Shinra Ontology"@en ;
  dcterms:creator <https://w3id.org/shinra/data/katsuki-miwa> ;
  dcterms:license <https://creativecommons.org/licenses/by/4.0/> .
```

### Git タグ規約

- リリースごとに `v0.1.0` 形式でタグを打つ
- `owl:versionIRI` の日付 = タグを打った日付
- `releases/` ディレクトリに Turtle + OWL のスナップショットを保存

---

## 外部語彙との整合

### 再利用する外部 prefix（import の要否）

| 語彙 | 再利用方法 | import |
|---|---|---|
| BFO 2020 | クラス・プロパティを継承 | `owl:imports` で完全 import |
| OWL-Time | 時間表現の型 | 完全 import（Phase 2） |
| QUDT | 量・単位の型 | 完全 import（Phase 2） |
| PROV-O | 来歴の記述 | 完全 import（Phase 2） |
| SKOS | 概念マッピング述語 | 語彙のみ参照（import しない） |
| FOAF | 人物プロパティ | 語彙のみ参照（import しない） |
| Dublin Core (dcterms) | メタデータ | 語彙のみ参照 |

### Wikidata マッピング方針

```turtle
shinra-data:tokyo-station-a3f4c9
  owl:sameAs <http://www.wikidata.org/entity/Q941320> .

shinra:Station
  skos:exactMatch <http://www.wikidata.org/entity/Q12819564> .
```

- インスタンス: `owl:sameAs` を使用
- クラス: `skos:exactMatch` / `skos:closeMatch` を使用（`owl:equivalentClass` は推論爆発のため禁止）

---

## 変更禁止事項（凍結ルール）

以下は一度確定したら変更しない:

1. **ベース URI**（`https://w3id.org/shinra/`）
2. **クラス・プロパティ名の ASCII slug** — `skos:notation` の連番 ID でリネームを追跡
3. **名前空間の分離方式**（`/ont/` と `/data/` の区別）

クラス名を変えたい場合は、旧クラスを `owl:deprecated true` として残し、新クラスに `owl:sameAs` 参照を追加する。旧クラスは削除しない。
