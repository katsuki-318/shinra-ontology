# 神羅万象オントロジー (Shinra-Ontology)

> 公開情報をもとに世の神羅万象をオントロジー／セマンティックレイヤーで整理する個人プロジェクト

**バージョン**: 0.0.1（開発中）  
**ライセンス**: CC-BY 4.0（文書・語彙）+ Apache 2.0（コード）  
**永続URI**: `https://w3id.org/shinra/` （取得手続き中）  
**開始日**: 2026-05-12

---

## 目的

「世の中にある事物・現象・概念のすべて」を、公開情報を根拠として、推論可能な RDF/OWL オントロジーとして外在化する。  
完璧な網羅を目指すのではなく、**自分の脳内モデルを段階的に明示化していくプロセス**そのものを目的とする。

## スコープ

- **対象**: あらゆる存在領域（時空・物理・生物・人間・社会・文化・技術・抽象概念）
- **言語**: 日本語を主ラベル、英語を必須サブラベルとして両方記述
- **根拠**: Wikipedia / Wikidata / schema.org / 政府統計 / 学術論文 / 公的標準など公開情報のみ

## 非ゴール

- Wikidata の全データを取り込むことは目指さない（構造の整合性を優先）
- ビジネス用途・商用配布を目的としない
- 特定ドメインに閉じた専門オントロジーにはしない

---

## 上位オントロジー

**BFO 2020 (ISO/IEC 21838-2:2021)** を採用。  
37クラスからなるミニマルな骨格に、独自の中位クラス・ドメインクラスを積み上げていく。

```
bfo:Entity
└── bfo:Continuant          ← 存在し続けるもの
    ├── bfo:IndependentContinuant
    ├── bfo:GenericallyDependentContinuant
    └── bfo:SpecificallyDependentContinuant
└── bfo:Occurrent           ← 起こること
    ├── bfo:Process
    └── bfo:TemporalRegion
```

---

## リポジトリ構造

```
shinra-ontology/
├── src/                    主オントロジーファイル（Turtle）
│   ├── shinra-core.ttl     上位骨格（BFO ブリッジクラス）
│   ├── shinra-mid.ttl      中位骨格（8カテゴリ）
│   └── modules/            ドメイン別モジュール
├── imports/                外部オントロジーのローカルミラー
│   └── bfo-2020.owl        BFO 2020
├── tests/                  SHACL バリデーション・SPARQL テスト
├── docs/
│   ├── URI-policy.md       URI 設計戦略
│   ├── naming-conventions.md  命名規約
│   └── journal/            月次進捗ジャーナル
└── releases/               バージョン付きリリーススナップショット
```

---

## 構築ロードマップ

| Phase | 目的 | 目安 |
|---|---|---|
| 0. 設計確定 | URI・憲章・ツール凍結 | Day 0–14 |
| 1. 上位骨格 | BFO 直下ブリッジクラス（10–20クラス） | Day 15–45 |
| 2. 中位骨格 | 8カテゴリ・50–80クラス | Day 46–120 |
| 3. 時空・物理・情報 | 第1ドメイン群（累計200–400クラス） | Day 121–240 |
| 4. 生物・人間・社会 | 第2ドメイン群・Wikidata接続本格化 | Day 241–450 |
| 5. 文化・技術・抽象 | 第3ドメイン群（累計1500–2500クラス） | Day 451–720 |
| 6. 統合・自己記述 | メタオントロジー | Day 721以降 |

---

## ツールチェーン

| 役割 | ツール |
|---|---|
| 編集（主） | VS Code + Turtle 拡張 |
| 編集（副） | Protégé 5.6+ |
| CLI ワークフロー | ROBOT |
| ストレージ | Oxigraph |
| 推論 | ELK（日常）/ HermiT（リリース前） |
| バリデーション | SHACL + pySHACL |
| 可視化 | WebVOWL |
| ホスティング | GitHub + GitHub Pages + w3id.org |

---

## 詳細ドキュメント

- [URI 設計戦略](docs/URI-policy.md)
- [命名規約](docs/naming-conventions.md)
- [月次ジャーナル](docs/journal/)

---

## ライセンス

- **語彙・ドキュメント**: [Creative Commons Attribution 4.0 International (CC-BY 4.0)](LICENSE-CC)
- **ソースコード・スクリプト**: [Apache License 2.0](LICENSE-APACHE)
