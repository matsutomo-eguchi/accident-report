#!/bin/bash
# macOS用の起動スクリプト（ダブルクリックで起動可能）

cd "$(dirname "$0")"

echo "🛡️  放課後等デイサービス 事故報告書生成システム (J-ARGS)"
echo "=========================================="
echo ""

# プロジェクトディレクトリに移動
cd "/Users/matsutomoeguchi/Downloads/my.python/accident report"

# Streamlitのパスを確認
STREAMLIT_PATH=""

if [ -f "/Users/matsutomoeguchi/Library/Python/3.9/bin/streamlit" ]; then
    STREAMLIT_PATH="/Users/matsutomoeguchi/Library/Python/3.9/bin/streamlit"
    echo "✅ Streamlitが見つかりました（Python 3.9）"
elif command -v streamlit &> /dev/null; then
    STREAMLIT_PATH="streamlit"
    echo "✅ Streamlitが見つかりました"
else
    echo "⚠️  Streamlitが見つかりません"
    echo ""
    echo "仮想環境を作成して依存ライブラリをインストールします..."
    
    # 仮想環境を作成
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # 仮想環境を有効化
    source venv/bin/activate
    
    # 依存ライブラリをインストール
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    
    STREAMLIT_PATH="streamlit"
fi

echo ""
echo "Streamlitアプリを起動中..."
echo "ブラウザで http://localhost:8501 にアクセスしてください"
echo ""
echo "停止する場合は、このウィンドウで Ctrl + C を押してください"
echo ""

# Streamlitを起動
$STREAMLIT_PATH run app.py

# エラーが発生した場合
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ エラーが発生しました"
    echo ""
    echo "手動で起動する場合は、以下のコマンドを実行してください："
    echo ""
    echo "  cd \"/Users/matsutomoeguchi/Downloads/my.python/accident report\""
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo "  streamlit run app.py"
    echo ""
    read -p "Enterキーを押して終了..."
fi

