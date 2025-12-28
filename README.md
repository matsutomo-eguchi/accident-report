# 🛡️ 放課後等デイサービス 事故報告書生成システム (J-ARGS)

放課後等デイサービスで発生した事故の報告書を、AIアシスト機能付きで簡単に作成できるWebアプリケーションです。

## ✨ 主な機能

- 📝 **直感的な入力フォーム**: 事故情報を簡単に入力
- 🤖 **AIアシスト機能**: メモ書きから自動的に報告書を生成（OpenAI/Grok/Claude対応）
- 📄 **PDF自動生成**: 公式書式に準拠したPDFを即座に生成
- 🌐 **Streamlit Cloud対応**: どこからでもアクセス可能
- 🎨 **日本語フォント対応**: 美しい日本語レンダリング

## 🚀 クイックスタート

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd "accident report"
```

### 2. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 3. 日本語フォントの配置

**重要**: PDF生成に日本語フォントが必要です。

1. [IPAexフォント](https://moji.or.jp/ipafont/ipafontdownload/)から `IPAexGothic` をダウンロード
2. ダウンロードしたZIPファイルを解凍
3. `IPAexGothic.ttf` を `fonts/` ディレクトリに配置

```bash
# fontsディレクトリが存在することを確認
mkdir -p fonts

# IPAexGothic.ttfをfontsディレクトリに配置
# （ダウンロードしたファイルをコピー）
```

### 4. ローカルで実行

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` にアクセスします。

## 🌐 Streamlit Cloudへのデプロイ

### 1. GitHubリポジトリの準備

1. GitHubに新しいリポジトリを作成
2. このプロジェクトをプッシュ

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

**重要**: `fonts/IPAexGothic.ttf` もリポジトリに含める必要があります。

### 2. Streamlit Cloudでの設定

1. [Streamlit Cloud](https://streamlit.io/cloud)にログイン
2. "New app"をクリック
3. GitHubリポジトリを選択
4. Main file path: `app.py` を指定
5. Python version: `3.11` を指定

### 3. Secretsの設定（AI機能を使用する場合）

Streamlit CloudのSettings > Secretsに以下を追加：

#### OpenAI/Grokを使用する場合

```toml
OPENAI_API_KEY = "your-api-key-here"
OPENAI_BASE_URL = "https://api.openai.com/v1"  # Grok使用時は適宜変更
OPENAI_MODEL = "gpt-4"  # または "grok-beta"
```

#### Anthropic Claudeを使用する場合

```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

**注意**: AI機能を使用しない場合は、Secretsの設定は不要です。その場合、モックデータが使用されます。

## 📖 使用方法

### 基本情報の入力

1. サイドバーで以下を入力：
   - 事業所名
   - 報告者氏名
   - 記録日

### 事故情報の入力

1. **発生日時**: 事故が発生した日付と時刻を選択
2. **発生場所**: 事故が発生した場所を入力
3. **対象者**: 児童名を入力

### AIアシスト機能の使用

1. 「AIアシスト入力」エリアに、箇条書きやメモ書きで事故の内容を入力
   ```
   例：
   - バランスボールで遊んでいて転んだ
   - 手首を痛がったので冷やした
   - お母さんに電話して説明した
   ```
2. 「AIで報告書案を作成」ボタンをクリック
3. 自動生成された内容を確認・編集

### PDF生成

1. すべての情報を入力
2. 「PDFを生成」ボタンをクリック
3. 生成されたPDFをダウンロード

## 🏗️ プロジェクト構造

```
accident report/
├── app.py                  # メインアプリケーション (Streamlit UI)
├── pdf_generator.py        # PDF生成モジュール (ReportLab)
├── requirements.txt        # 依存ライブラリ
├── .streamlit/
│   └── config.toml        # Streamlit設定
├── fonts/
│   └── IPAexGothic.ttf    # 日本語フォント（要配置）
├── .gitignore             # Git除外設定
├── README.md              # このファイル
└── 仕様書.md              # システム仕様書
```

## 🔧 技術スタック

- **フロントエンド**: Streamlit
- **PDF生成**: ReportLab
- **AI統合**: OpenAI API / Anthropic Claude API
- **言語**: Python 3.11+
- **デプロイ**: Streamlit Cloud

## 📝 ライセンス

このプロジェクトは、放課後等デイサービスでの使用を目的として作成されています。

## 🤝 サポート

問題が発生した場合や質問がある場合は、GitHubのIssuesでお知らせください。

## 📌 注意事項

- **プライバシー**: 事故報告書には個人情報が含まれます。適切に管理してください。
- **フォント**: 日本語フォント（IPAexGothic.ttf）が配置されていない場合、PDFで文字化けが発生する可能性があります。
- **AI機能**: AI生成された内容は必ず確認・編集してください。最終的な責任は報告者にあります。

## 🎯 今後の改善予定

- [ ] 複数の報告書テンプレート対応
- [ ] 過去の報告書の保存・管理機能
- [ ] エクスポート機能（Excel、CSV）
- [ ] 多言語対応
- [ ] モバイル最適化

---

**J-ARGS** - Japanese Accident Report Generation System for Day Service

