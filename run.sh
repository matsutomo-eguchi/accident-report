#!/bin/bash
# アプリケーション起動スクリプト

echo "🛡️  放課後等デイサービス 事故報告書生成システム (J-ARGS)"
echo "=========================================="
echo ""

# 仮想環境の確認
if [ ! -d "venv" ]; then
    echo "仮想環境を作成中..."
    python3 -m venv venv
fi

# 仮想環境の有効化
echo "仮想環境を有効化中..."
source venv/bin/activate

# 依存ライブラリのインストール
echo "依存ライブラリをインストール中..."
pip install -r requirements.txt

# フォントファイルの確認
if [ ! -f "fonts/IPAexGothic.ttf" ]; then
    echo ""
    echo "⚠️  警告: 日本語フォントファイルが見つかりません"
    echo "   fonts/IPAexGothic.ttf を配置してください"
    echo "   詳細は README.md を参照してください"
    echo ""
fi

# Streamlitアプリの起動
echo ""
echo "Streamlitアプリを起動中..."
echo "ブラウザで http://localhost:8501 にアクセスしてください"
echo ""
streamlit run app.py

