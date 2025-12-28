# 🤖 Grok API設定ガイド

## Streamlit SecretsでのGrok API設定方法

Grok API（xAI）を使用する場合の正確な設定方法です。

## 📋 設定手順

### 1. Streamlit Cloudの場合

Streamlit Cloudの **Settings > Secrets** に以下の内容を追加してください：

```toml
XAI_API_KEY = "your-grok-api-key-here"
OPENAI_BASE_URL = "https://api.x.ai/v1"
OPENAI_MODEL = "grok-beta"
```

### 2. ローカル環境の場合

プロジェクトディレクトリの `.streamlit/secrets.toml` ファイルを作成（または編集）してください：

```toml
# Grok API設定
XAI_API_KEY = "your-grok-api-key-here"
OPENAI_BASE_URL = "https://api.x.ai/v1"
OPENAI_MODEL = "grok-beta"
```

**重要**: `.streamlit/secrets.toml` ファイルは `.gitignore` に含まれているため、Gitにコミットされません。

## 🔑 APIキーの取得方法

1. [xAI Console](https://console.x.ai/) にアクセス
2. アカウントを作成またはログイン
3. API Keysセクションで新しいAPIキーを生成
4. 生成されたAPIキーをコピー

## ⚙️ 設定項目の説明

| 項目 | 説明 | 必須 |
|------|------|------|
| `XAI_API_KEY` | Grok APIのAPIキー | ✅ 必須 |
| `OPENAI_BASE_URL` | APIエンドポイントURL（Grokの場合は `https://api.x.ai/v1`） | ✅ 必須 |
| `OPENAI_MODEL` | 使用するモデル名（Grokの場合は `grok-beta` または `grok-2`） | ⚠️ 推奨 |

## 📝 設定例（完全版）

```toml
# Grok API設定（xAI）
XAI_API_KEY = "xai-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_BASE_URL = "https://api.x.ai/v1"
OPENAI_MODEL = "grok-beta"
```

## 🔄 代替設定方法

コードでは `OPENAI_API_KEY` も `XAI_API_KEY` として認識されるため、以下の設定も可能です：

```toml
OPENAI_API_KEY = "your-grok-api-key-here"
OPENAI_BASE_URL = "https://api.x.ai/v1"
OPENAI_MODEL = "grok-beta"
```

## ✅ 動作確認

設定後、アプリケーションを起動して：

1. サイドバーの「AIで文章を自動生成する」にチェックを入れる
2. 「AIアシスト入力」にメモを入力
3. 「AIで報告書案を作成」ボタンをクリック

エラーなく動作すれば設定は成功です。

## ⚠️ トラブルシューティング

### APIキーが認識されない場合

- `.streamlit/secrets.toml` ファイルが正しい場所にあるか確認
- ファイル名が `secrets.toml` であることを確認（`.toml` 拡張子）
- アプリケーションを再起動

### エラーメッセージが表示される場合

- APIキーが正しいか確認
- `OPENAI_BASE_URL` が `https://api.x.ai/v1` になっているか確認
- モデル名が `grok-beta` または `grok-2` になっているか確認

### ローカル環境での設定ファイルの場所

```
accident report/
└── .streamlit/
    ├── config.toml      # Streamlit設定
    └── secrets.toml     # Secrets設定（このファイルを作成）
```

## 📚 参考情報

- [xAI API Documentation](https://docs.x.ai/)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

