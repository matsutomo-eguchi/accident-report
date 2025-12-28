"""
PDF生成機能のテストスクリプト
"""
from pdf_generator import AccidentReportGenerator
import datetime

def test_pdf_generation():
    """PDF生成のテスト"""
    
    # テストデータ
    test_data = {
        "facility_name": "放課後等デイサービス テスト事業所",
        "year": "2024",
        "month": "12",
        "day": "25",
        "weekday": "水",
        "hour": "15",
        "minute": "30",
        "location": "プレイルーム",
        "subject": "山田 太郎",
        "situation": "バランスボールで遊んでいた際に、バランスを崩して転倒しました。\n手首を強く打ち、痛がっていました。",
        "process": "直ちに職員が駆けつけ、状況を確認しました。\n手首を冷やし、保護者に連絡を取って状況を説明しました。\n保護者の了解を得て、医療機関を受診することになりました。",
        "cause": "・環境要因：バランスボールの使用環境に注意が不足していた\n・人的要因：職員の監視が不十分だった",
        "countermeasure": "・バランスボール使用時の安全ルールを再確認\n・職員の監視体制を強化\n・定期的な安全点検の実施",
        "others": "保護者には迅速に連絡し、適切な対応ができました。",
        "reporter": "佐藤 花子",
        "record_date": "2024年12月25日"
    }
    
    print("PDF生成テストを開始します...")
    
    try:
        generator = AccidentReportGenerator(font_path="fonts/IPAexGothic.ttf")
        output_path = "test_report.pdf"
        generator.generate(test_data, output_path)
        print(f"✅ PDF生成成功: {output_path}")
        return True
    except Exception as e:
        print(f"❌ PDF生成エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_pdf_generation()

