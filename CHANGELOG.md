# Changelog

All notable changes to this project will be documented in this file.

Format: `MAJOR.MINOR.PATCH` — SemVer
- MAJOR: 上位骨格（BFO ブリッジ）の改変
- MINOR: 新ドメイン追加
- PATCH: ラベル修正・コメント追加・誤字修正

---

## [Unreleased]

---

## [0.4.0] — 2026-05-27

### Added
- **shinra-mind.ttl** (Phase 5-b): 精神・認知・心理ドメイン
  - 認知過程: Cognition / Perception / Memory / Learning / Reasoning / DecisionMaking / Imagination / Attention
  - 感情・動機: Emotion / Motivation / Mood / Stress
  - 心的傾向: Desire / Intention / Attitude / CognitiveBias / Personality
  - 意識・自己: Consciousness / SelfConcept
  - 社会的認知: SocialCognition / Empathy
  - 心理・神経科学: PsychologicalTheory / MentalDisorder / NeuroscientificProcess
  - データプロパティ: hasEmotionalValence
  - オブジェクトプロパティ: hasCognitiveAgent
  - インスタンス: maslow-hierarchy-001 / cognitive-dissonance-001 / depression-001 / freudian-unconscious-001
- **shinra-technology.ttl** (Phase 5-c): 技術・工学詳細ドメイン
  - 情報技術: ComputerSystem / Software / OperatingSystem / Database / ComputerNetwork
  - AI・機械学習: ArtificialIntelligence / MachineLearning / DeepLearning / LargeLanguageModel
  - 医療・生命工学: MedicalTechnology / Drug / Vaccine / Biotechnology
  - エネルギー: EnergyTechnology / RenewableEnergy / NuclearTechnology
  - 農業・食料: AgriculturalTechnology / FoodProcessing
  - 材料・建設: CivilEngineering / Material / Semiconductor
  - データプロパティ: hasTechnologyReadinessLevel / hasInventionYear
  - インスタンス: internet-001 / crispr-001 / solar-cell-001 / penicillin-001 / linux-001
- **shinra-economics.ttl** (Phase 5-d): 経済・金融詳細ドメイン
  - 経済主体・制度: Market / Industry / SupplyChain
  - 金融商品: FinancialInstrument / Currency / Stock / Bond / Cryptocurrency
  - 経済過程: Production / Consumption / Investment / Taxation
  - 経済理論・指標: EconomicTheory / EconomicIndicator / EconomicCrisis
  - データプロパティ: hasGDP / hasInflationRate
  - インスタンス: bitcoin-001 / new-york-stock-exchange-001 / great-depression-001 / keynesian-economics-001

### Changed
- `tests/validate.py`: ALL_MODULES をハードコードリストから `src/` 自動スキャン方式に変更
- `src/catalog-v001.xml`: mind / technology / economics エントリ追加

### Stats
- クラス: 266（+60）  ObjectProperty: 32（+1）  DataProperty: 26（+5）  トリプル: 3,192（+661）

---

## [0.3.0] — 2026-05-12

### Added
- **shinra-physical.ttl** (Phase 3-a): 物理・自然科学ドメイン
  - 化学: Element / Compound / Mixture
  - 天体: Star / Planet / Moon / Galaxy
  - 物理現象: Mechanical / Electromagnetic / Thermal / QuantumPhenomenon
  - 生命過程: Metabolism / Reproduction / Evolution
  - 地球科学: GeologicalProcess / MeteorologicalProcess
  - 物理量: Mass / Temperature / Energy
- **shinra-social.ttl** (Phase 3-b): 社会・人間・制度ドメイン
  - 人間の状態: LifeStage / Occupation / Nationality
  - 社会制度: SocialInstitution / LegalSystem / EconomicSystem / PoliticalSystem / Religion
  - 社会的出来事: War / Election / EconomicTransaction / Communication
  - 技術・工学: Technology / Infrastructure / Tool / Vehicle / Building
  - データプロパティ: hasFoundingDate / hasBirthDate / hasDeathDate / hasPopulation
- **shinra-information.ttl** (Phase 3-c): 情報・知識・文化ドメイン
  - テキスト: Book / Article / LegalText / ReligiousText
  - 視聴覚: VisualArtWork / MusicalWork / FilmWork / PerformativeWork
  - デジタル: WebResource / KnowledgeBase / Ontology / Algorithm
  - 言語・記号: NaturalLanguage / FormalLanguage / SignSystem
  - 知識: ScientificTheory / Philosophy / Mathematics / Mythology
- **shinra-biology.ttl** (Phase 3-d): 生物・生命科学ドメイン
  - 生物分類: Animal / Plant / Fungus / Microorganism / Virus
  - 解剖: BodyPart / Organ / Cell
  - 分子生物学: Gene / Genome / Protein
  - 生態系: Ecosystem / Biome / FoodWeb
  - 健康: Disease / Symptom / MedicalTreatment
- **shinra-geography.ttl** (Phase 3-e): 地理・地球空間ドメイン
  - 行政地理: Country / City / Region / Continent / Capital
  - 自然地理: Mountain / River / Lake / Ocean / Desert / Island
  - 人工空間: UrbanArea / Port / Airport / NationalPark
  - 地理プロパティ: hasLatitude / hasLongitude / hasElevation / hasArea / hasISOCountryCode
- **shinra-history.ttl** (Phase 4-a): 歴史・文明ドメイン
  - 時代区分: HistoricalPeriod / Prehistory / AncientHistory / MedievalHistory / ModernHistory
  - 文明・帝国: Civilization / Empire / Dynasty
  - 歴史的出来事: Revolution / Treaty / Expedition / Disaster
  - 人物: HistoricalFigure / Monarch / Inventor
  - プロパティ: hasStartYear / hasEndYear / hasSuccessor / hasPredecessor
- **shinra-abstract.ttl** (Phase 4-b): 抽象・形式・価値ドメイン
  - 数学的対象: MathematicalObject / Number / Set / Function / AlgebraicStructure / Proof
  - 論理: LogicalStatement / Axiom / Theorem / Paradox
  - 価値・規範: EthicalValue / AestheticValue / EpistemicValue / LegalNorm / SocialNorm
  - 形而上学: Identity / Causality / Possibility
- **shinra-culture.ttl** (Phase 5-a): 文化・習慣・スポーツドメイン
  - 文化慣行: CulturalPractice / Ritual / Festival / Cuisine / Fashion
  - スポーツ: Sport / TeamSport / IndividualSport / MartialArt / SportingEvent
  - 教育: EducationalProcess / Curriculum
  - 娯楽: Game / VideoGame / TraditionalGame
- **src/catalog-v001.xml**: ROBOT catalog（ローカルURI→ファイルマッピング）
- **tests/validate.py** 全面改訂: 全ドメイン横断バリデーター（ドメイン別クラス数・notation重複・ラベル欠損・comment欠損チェック）
- **tests/sparql_examples.py** 全面改訂: 12クエリ（MaterialEntity/Process/ConceptualEntity サブクラス、Wikidata ID一覧、歴史インスタンス年代順など）

### Fixed
- shinra-mid.ttl: `owl:imports <https://w3id.org/shinra/ont/>` → `<https://w3id.org/shinra/ont/core>` 修正

### Stats
- クラス: **220** (10 モジュール合計)
- オブジェクトプロパティ: 31
- データプロパティ: 21
- インスタンス: 42
- Oxigraph トリプル: **2,531**
- ROBOT ELK reason (merge 10 files): exit 0 ✅

---

## [0.2.0] — 2026-05-12

### Added
- **shinra-mid.ttl**: 中位骨格（Phase 2）
  - 時間: Era / Duration / RecurringPattern
  - 空間: Coordinate / Boundary / Landform / WaterBody
  - 人間・組織: Person / Organization / Company / GovernmentBody / EducationalInstitution / CommunityGroup
  - 知識: Language / ScientificDiscipline / ArtWork / ScientificPublication / LegalDocument
  - 自然科学: ChemicalSubstance / BiologicalTaxon / CelestialObject / PhysicalPhenomenon / BiologicalProcess
  - 来歴: CreationProcess / DestructionProcess / TransformationProcess / TransferProcess
  - 中位プロパティ: hasCreator / memberOfOrganization / hasLocation / hasLanguage / classifiedAs / hasWikidataMatch
- imports/owl-time.ttl および imports/prov-o.ttl を取得

---

## [0.1.0] — 2026-05-12

### Added
- **shinra-core.ttl**: BFO 2020 import + 10 ブリッジクラス + 34 第1層サブクラス
  - 44 クラス、21 オブジェクトプロパティ、4 データプロパティ、7 インスタンス
  - BFO ID 修正: InformationContentEntity/ConceptualEntity → `bfo:0000031`、TemporalRegion → `bfo:0000008`
- **imports/bfo-2020.owl**: BFO 2020 ローカルミラー（125KB）
- **tests/validate.py**: Turtle 構文・notation重複・ラベル欠損チェック
- **tests/sparql_examples.py**: SPARQL サンプル 4 クエリ
- **setup.bat**: Windows 向けセットアップスクリプト
- README.md / README.html、docs/URI-policy.md、docs/naming-conventions.md
- docs/journal/2026-05.md / HTML

---

<!-- リリースリンク（GitHub Release で更新） -->
[Unreleased]: https://github.com/yourusername/shinra-ontology/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/yourusername/shinra-ontology/releases/tag/v0.3.0
[0.2.0]: https://github.com/yourusername/shinra-ontology/releases/tag/v0.2.0
[0.1.0]: https://github.com/yourusername/shinra-ontology/releases/tag/v0.1.0
