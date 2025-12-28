#!/bin/bash
# Streamlitアプリケーション起動スクリプト

cd "$(dirname "$0")"

echo "🛡️  放課後等デイサービス 事故報告書生成システム (J-ARGS)"
echo "=========================================="
echo ""

# Streamlitがインストールされているか確認
if command -v streamlit &> /dev/null; then
    echo "✅ Streamlitが見つかりました"
    streamlit run app.py
elif [ -f "/Users/matsutomoeguchi/Library/Python/3.9/bin/streamlit" ]; then
    echo "✅ Streamlitが見つかりました（Python 3.9）"
    /Users/matsutomoeguchi/Library/Python/3.9/bin/streamlit run app.py
else
    echo "⚠️  Streamlitが見つかりません"
    echo ""
    echo "仮想環境を作成して依存ライブラリをインストールしますか？ (y/n)"
    read -r answer
    
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        echo ""
        echo "仮想環境を作成中..."
        python3 -m venv venv
        
        echo "仮想環境を有効化中..."
        source venv/bin/activate
        
        echo "依存ライブラリをインストール中..."
        pip install --upgrade pip
        pip install -r requirements.txt
        
        echo ""
        echo "Streamlitアプリを起動中..."
        streamlit run app.py
    else
        echo ""
        echo "以下のコマンドを手動で実行してください："
        echo ""
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -r requirements.txt"
        echo "  streamlit run app.py"
        echo ""
    fi
fi

