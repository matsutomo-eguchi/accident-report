"""
日本語フォント（IPAexGothic）のダウンロードスクリプト
"""
import os
import urllib.request
import zipfile
import shutil

def download_font():
    """IPAexGothicフォントをダウンロードして配置"""
    
    # フォントディレクトリの作成
    fonts_dir = "fonts"
    os.makedirs(fonts_dir, exist_ok=True)
    
    # IPAexGothicのダウンロードURL（IPAフォントの公式サイトから）
    # 注意: 実際のURLは変更される可能性があります
    font_url = "https://moji.or.jp/ipafont/ipafontdownload/"
    
    print("=" * 60)
    print("日本語フォント（IPAexGothic）のダウンロード")
    print("=" * 60)
    print()
    print("IPAexGothicフォントは、以下の手順で手動でダウンロードしてください：")
    print()
    print("1. 以下のURLにアクセス：")
    print("   https://moji.or.jp/ipafont/ipafontdownload/")
    print()
    print("2. 「IPAexゴシック」を選択してダウンロード")
    print()
    print("3. ZIPファイルを解凍")
    print()
    print("4. 解凍したフォルダ内の「IPAexGothic.ttf」を")
    print(f"   {os.path.abspath(fonts_dir)}/ ディレクトリにコピーしてください")
    print()
    print("=" * 60)
    
    # フォントファイルが既に存在するか確認
    font_path = os.path.join(fonts_dir, "IPAexGothic.ttf")
    if os.path.exists(font_path):
        print(f"✅ フォントファイルは既に存在します: {font_path}")
        return True
    else:
        print(f"❌ フォントファイルが見つかりません: {font_path}")
        print("   上記の手順に従ってフォントを配置してください。")
        return False

if __name__ == "__main__":
    download_font()

