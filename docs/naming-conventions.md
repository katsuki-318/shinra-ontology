# 命名規約

**文書バージョン**: 1.0.0  
**作成日**: 2026-05-12  
**状態**: 確定（凍結）

---

## 基本原則

1. **英語名（ASCII）が正式 ID** — URI を構成する識別子は必ず英語 ASCII で書く
2. **日本語ラベルは必須** — `rdfs:label@ja` をすべてのクラス・プロパティに付ける
3. **英語ラベルも必須** — `rdfs:label@en` をすべてに付ける（LOD 接続・国際公開のため）
4. **コメントは両言語** — `rdfs:comment@ja` と `rdfs:comment@en` を両方記述
5. **連番 ID を必ず付ける** — `skos:notation "SHINRA_0000001"` でリネーム耐性を確保

---

## クラス（Class）

### 命名形式

```
PascalCase + 単数形名詞
```

| 例 | 読み |
|---|---|
| `shinra:MaterialEntity` | 物質的実体 |
| `shinra:InformationContentEntity` | 情報内容実体 |
| `shinra:NaturalProcess` | 自然過程 |
| `shinra:AstronomicalBody` | 天体 |

### 禁止事項

- 複数形（`shinra:Persons` → `shinra:Person`）
- 略語（`shinra:InfoEnt` → `shinra:InformationContentEntity`）
- 日本語・漢字を URI に含める（`shinra:物体` は不可）

### クラス定義テンプレート

```turtle
shinra:MaterialEntity
  a owl:Class ;
  rdfs:subClassOf bfo:0000030 ;          # bfo:Object
  rdfs:label "物質的実体"@ja ;
  rdfs:label "Material Entity"@en ;
  skos:altLabel "物理的対象"@ja ;
  rdfs:comment "空間的に位置を持ち、独立して存在する物質的なもの。"@ja ;
  rdfs:comment "A material entity that exists independently and has spatial location."@en ;
  skos:notation "SHINRA_0000001" ;
  dcterms:created "2026-05-12"^^xsd:date .
```

---

## プロパティ（Property）

### 命名形式

```
lowerCamelCase + 動詞句（Object Property）
lowerCamelCase + 名詞句（Data Property）
```

| 例 | 種別 | 読み |
|---|---|---|
| `shinra:participatesIn` | ObjectProperty | 〜に参加する |
| `shinra:hasPart` | ObjectProperty | 〜を部分として持つ |
| `shinra:aboutness` | ObjectProperty | 〜について（情報→対象） |
| `shinra:bearerOf` | ObjectProperty | 〜を担持する |
| `shinra:hasRole` | ObjectProperty | 〜という役割を持つ |
| `shinra:birthDate` | DataProperty | 誕生日 |
| `shinra:hasName` | DataProperty | 名前を持つ |

### プロパティ定義テンプレート

```turtle
shinra:participatesIn
  a owl:ObjectProperty ;
  rdfs:domain bfo:0000004 ;              # IndependentContinuant
  rdfs:range  bfo:0000015 ;             # Process
  owl:inverseOf shinra:hasParticipant ;
  rdfs:label "〜に参与する"@ja ;
  rdfs:label "participates in"@en ;
  rdfs:comment "継続物が過程に参与している関係。"@ja ;
  rdfs:comment "Relation between a continuant and a process it participates in."@en ;
  skos:notation "SHINRA_P000001" ;
  dcterms:created "2026-05-12"^^xsd:date .
```

### BFO 既存プロパティとの関係

BFO 2020 にすでに定義されているプロパティは **再定義しない**。そのまま使う。

| BFO プロパティ | 利用場面 |
|---|---|
| `bfo:participates-in` | 継続物→過程 |
| `bfo:has-participant` | 過程→継続物 |
| `bfo:has-part` | 部分関係 |
| `bfo:located-in` | 場所関係 |
| `bfo:bearer-of` | 担持関係 |
| `bfo:inheres-in` | 内在関係 |

独自プロパティは BFO に存在しない概念の場合のみ定義する。

---

## インスタンス（Individual）

### 命名形式

```
英語小文字 + ハイフン区切りの slug + ハイフン + UUID 短縮（6文字）
```

```
shinra-data:tokyo-station-a3f4c9
shinra-data:natsume-soseki-b2e7d1
shinra-data:pacific-ocean-c8d3e2
```

### slug の作り方

- 英語の一般名称を使う（固有名詞の場合はローマ字 or 英訳）
- ハイフン区切り、小文字のみ
- 長すぎる場合は主要単語のみ（3語程度まで）

---

## ラベル・コメントの記述規則

### rdfs:label

```turtle
rdfs:label "物質的実体"@ja ;    # 日本語：漢字・ひらがな・カタカナ混在OK
rdfs:label "Material Entity"@en ;  # 英語：頭文字大文字のタイトルケース
```

### skos:altLabel（別名）

```turtle
skos:altLabel "物理的対象"@ja ;
skos:altLabel "物理的実体"@ja ;
skos:altLabel "material thing"@en ;
```

別名は `rdfs:label` より検索精度を高めるために使う。同義語・上位語・口語表現を登録する。

### rdfs:comment

- 1〜3文で簡潔に
- 「何であるか」を定義する文（「〜とは〜である」形式）
- BFO の定義がある場合は参照し、独自解釈を上乗せしない

---

## 連番 ID（skos:notation）

全クラス・プロパティに連番 ID を付与する。

| 種別 | プレフィックス | 例 |
|---|---|---|
| クラス | `SHINRA_` + 7桁ゼロ埋め | `SHINRA_0000001` |
| オブジェクトプロパティ | `SHINRA_P` + 6桁ゼロ埋め | `SHINRA_P000001` |
| データプロパティ | `SHINRA_D` + 6桁ゼロ埋め | `SHINRA_D000001` |

連番 ID により、URI の名称を変更した場合でも同一概念を追跡できる。  
ROBOT report で重複がないことを月次で確認する。

---

## 外部 ID マッピング

```turtle
shinra:MaterialEntity
  skos:exactMatch <http://www.wikidata.org/entity/Q35120> ;  # Wikidata: entity
  skos:closeMatch <https://schema.org/Thing> .
```

- `owl:sameAs`: インスタンスレベルのみ
- `skos:exactMatch`: 概念が完全に等価
- `skos:closeMatch`: 概念が近いが微妙にずれる
- `skos:broadMatch`: より広い上位概念にマッピング

---

## 変更禁止事項

- `skos:notation` の連番 ID は一度付けたら変えない（URI が変わっても ID は不変）
- BFO と同名の URI を `shinra:` 名前空間で作らない（`shinra:Process` は可だが `shinra:Continuant` を BFO と別定義するのは混乱の元）
- 英語クラス名に日本語・漢字を含めない
