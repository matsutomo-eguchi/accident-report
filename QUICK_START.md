# 🚀 クイックスタートガイド

## すぐに起動する方法

### ターミナルで以下のコマンドをコピー＆ペーストして実行してください：

```bash
cd "/Users/matsutomoeguchi/Downloads/my.python/accident report" && /Users/matsutomoeguchi/Library/Python/3.9/bin/streamlit run app.py
```

### または、起動スクリプトを使用：

```bash
cd "/Users/matsutomoeguchi/Downloads/my.python/accident report"
./start.sh
```

## 起動が成功したら

ターミナルに以下のようなメッセージが表示されます：

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

**ブラウザで http://localhost:8501 を開いてください。**

## エラーが出る場合

### 1. Streamlitが見つからない場合

```bash
cd "/Users/matsutomoeguchi/Downloads/my.python/accident report"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### 2. ポート8501が使用中の場合

別のポートで起動：

```bash
streamlit run app.py --server.port 8502
```

### 3. 権限エラーが出る場合

```bash
chmod +x start.sh
./start.sh
```

## 停止方法

ターミナルで `Ctrl + C` を押してください。

