"""
PDF生成モジュール
ReportLabを使用して事故報告書のPDFを生成します。
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class AccidentReportGenerator:
    """事故報告書PDF生成クラス"""
    
    def __init__(self, font_path="fonts/IPAexGothic.ttf"):
        """
        初期化
        
        Args:
            font_path: 日本語フォントファイルのパス
        """
        self.width, self.height = A4
        self.font_name = "CustomJapaneseFont"
        
        # フォントの登録
        self._register_font(font_path)
        
        # スタイルシートの初期化
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _register_font(self, font_path):
        """フォントを登録する（フォールバック付き）"""
        # まず指定されたパスを確認
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(self.font_name, font_path))
                print(f"✅ フォント登録成功: {font_path}")
                return
            except Exception as e:
                print(f"フォント登録エラー: {e}")
        
        # 相対パスも試す
        alt_paths = [
            os.path.join(os.path.dirname(__file__), font_path),
            os.path.join(os.path.dirname(__file__), "fonts", "IPAexGothic.ttf"),
            os.path.join(os.path.dirname(__file__), "fonts", "ipagp.ttf"),
            "fonts/IPAexGothic.ttf",
            "fonts/ipagp.ttf",
        ]
        
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                try:
                    pdfmetrics.registerFont(TTFont(self.font_name, alt_path))
                    print(f"✅ フォント登録成功: {alt_path}")
                    return
                except Exception as e:
                    print(f"フォント登録エラー ({alt_path}): {e}")
                    continue
        
        # フォールバック: UnicodeCIDFontを試す
        try:
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5-Acro"))
            self.font_name = "HeiseiKakuGo-W5-Acro"
            print("✅ UnicodeCIDFontを使用")
            return
        except Exception as e:
            print(f"UnicodeCIDFont登録エラー: {e}")
        
        # 最終手段: Helvetica（日本語は文字化けするがエラーは防ぐ）
        self.font_name = "Helvetica"
        print("⚠️ 警告: 日本語フォントが見つかりません。文字化けの可能性があります。")
    
    def _setup_custom_styles(self):
        """カスタムスタイルを設定"""
        try:
            self.normal_style = ParagraphStyle(
                'CustomNormal',
                parent=self.styles['Normal'],
                fontName=self.font_name,
                fontSize=10,
                leading=14,
                alignment=TA_LEFT,
                wordWrap='CJK',
            )
            self.title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Normal'],
                fontName=self.font_name,
                fontSize=18,
                leading=22,
                alignment=TA_CENTER,
            )
            self.table_title_style = ParagraphStyle(
                'TableTitle',
                parent=self.styles['Normal'],
                fontName=self.font_name,
                fontSize=10,
                leading=14,
                alignment=TA_CENTER,
                wordWrap='CJK',
            )
            self.table_content_style = ParagraphStyle(
                'TableContent',
                parent=self.styles['Normal'],
                fontName=self.font_name,
                fontSize=10,
                leading=14,
                alignment=TA_LEFT,
                wordWrap='CJK',
            )
        except Exception as e:
            print(f"スタイル設定エラー: {e}")
            # フォールバック
            self.normal_style = self.styles['Normal']
            self.title_style = self.styles['Normal']
            self.table_title_style = self.styles['Normal']
            self.table_content_style = self.styles['Normal']
    
    def _calculate_paragraph_height(self, paragraph, width):
        """Paragraphオブジェクトの実際の高さを計算"""
        if not paragraph or not paragraph.text:
            return 14  # デフォルトのleading
        
        try:
            # wrapメソッドで実際の高さを計算（canvasは不要）
            w, h = paragraph.wrap(width, 10000)  # 十分な高さを指定
            return max(14, h)
        except Exception:
            # フォールバック: 簡易計算
            text = paragraph.text if hasattr(paragraph, 'text') else ""
            lines = text.split('\n') if text else [""]
            return max(14, len(lines) * 14)
    
    def generate(self, data, output_path):
        """
        PDFを生成
        
        Args:
            data: 報告書データの辞書
            output_path: 出力ファイルパス
        """
        c = canvas.Canvas(output_path, pagesize=A4)
        c.setTitle("事故状況・対策報告書")
        
        # マージン設定
        LEFT_MARGIN = 20 * mm
        RIGHT_MARGIN = 20 * mm
        TOP_MARGIN = 20 * mm
        BOTTOM_MARGIN = 20 * mm
        
        # フォントサイズ設定
        FONT_SIZE_TITLE = 18
        FONT_SIZE_LABEL = 10
        FONT_SIZE_TEXT = 10
        
        # 現在のY位置（上から下へ）
        current_y = self.height - TOP_MARGIN
        
        # タイトル
        c.setFont(self.font_name, FONT_SIZE_TITLE)
        title_y = current_y
        c.drawCentredString(self.width / 2, title_y, "事故状況・対策報告書")
        current_y = title_y - 25 * mm
        
        # 事業所名
        c.setFont(self.font_name, 11)
        c.drawString(LEFT_MARGIN, current_y, "【事業所名】")
        c.line(45 * mm, current_y - 1 * mm, 120 * mm, current_y - 1 * mm)
        facility_name = data.get("facility_name", "")
        if facility_name:
            c.drawString(45 * mm, current_y, facility_name)
        current_y -= 15 * mm
        
        # 基本情報エリア
        # 発生日時
        c.setFont(self.font_name, FONT_SIZE_LABEL)
        c.drawString(LEFT_MARGIN, current_y, "事故発生日時：")
        
        date_str = f"{data.get('year', '')} 年  {data.get('month', '')} 月  {data.get('day', '')} 日"
        time_str = f"{data.get('hour', '')} 時  {data.get('minute', '')} 分頃"
        weekday = f"({data.get('weekday', '')})曜日"
        
        c.setFont(self.font_name, FONT_SIZE_TEXT)
        c.drawString(50 * mm, current_y, f"{date_str}   {time_str}   {weekday}")
        current_y -= 10 * mm
        
        # 場所・対象者
        c.setFont(self.font_name, FONT_SIZE_LABEL)
        c.drawString(LEFT_MARGIN, current_y, "発生場所：")
        c.setFont(self.font_name, FONT_SIZE_TEXT)
        location = data.get("location", "")
        c.drawString(50 * mm, current_y, location)
        
        c.setFont(self.font_name, FONT_SIZE_LABEL)
        c.drawString(110 * mm, current_y, "対象者：")
        c.setFont(self.font_name, FONT_SIZE_TEXT)
        subject = data.get("subject", "")
        c.drawString(130 * mm, current_y, subject)
        current_y -= 12 * mm
        
        # メインテーブル
        # テーブルデータの準備
        table_data = [
            ["事故発生の\n状況", data.get("situation", "")],
            ["経過", data.get("process", "")],
            ["事故原因", data.get("cause", "")],
            ["対策", data.get("countermeasure", "")],
            ["その他", data.get("others", "")]
        ]
        
        # Paragraphを使用して自動改行対応
        table_data_paragraphs = []
        col_widths = [30 * mm, 140 * mm]
        content_width = col_widths[1] - 12 * mm  # パディングを考慮
        
        # Paragraphオブジェクトを作成
        for i, (title, content) in enumerate(table_data):
            title_para = Paragraph(
                title.replace('\n', '<br/>'), 
                self.table_title_style
            )
            content_para = Paragraph(
                content.replace('\n', '<br/>') if content else "", 
                self.table_content_style
            )
            table_data_paragraphs.append([title_para, content_para])
        
        # 各行の高さを事前に計算（Paragraphの実際の高さを使用）
        row_heights = []
        for title_para, content_para in table_data_paragraphs:
            # タイトルの高さ
            title_height = self._calculate_paragraph_height(
                title_para, 
                col_widths[0] - 12 * mm
            )
            
            # コンテンツの高さ
            content_height = self._calculate_paragraph_height(
                content_para, 
                content_width
            )
            
            # パディングを考慮（上下各6mm）
            row_height = max(20 * mm, max(title_height, content_height) + 12 * mm)
            row_heights.append(row_height)
        
        # テーブル作成
        t = Table(table_data_paragraphs, colWidths=col_widths, rowHeights=row_heights)
        
        t_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ])
        
        t.setStyle(t_style)
        
        # テーブルのサイズを計算
        available_height = current_y - BOTTOM_MARGIN - 80 * mm  # フッター用のスペースを確保
        w, h = t.wrapOn(c, self.width - LEFT_MARGIN - RIGHT_MARGIN, available_height)
        
        # テーブルが大きすぎる場合は調整
        if h > available_height:
            # 行の高さを比例的に縮小
            scale_factor = available_height / h
            row_heights = [max(15 * mm, h * scale_factor) for h in row_heights]
            t = Table(table_data_paragraphs, colWidths=col_widths, rowHeights=row_heights)
            t.setStyle(t_style)
            w, h = t.wrapOn(c, self.width - LEFT_MARGIN - RIGHT_MARGIN, available_height)
        
        # テーブル描画
        table_y = current_y - h
        t.drawOn(c, LEFT_MARGIN, table_y)
        
        # フッターエリア
        footer_y = table_y - 15 * mm
        
        # 署名・確認欄エリア
        # 管理者・報告者枠（右側）
        box_y = footer_y - 25 * mm
        
        # 管理者枠
        c.rect(115 * mm, box_y, 25 * mm, 20 * mm)
        c.setFont(self.font_name, 9)
        c.drawString(118 * mm, box_y + 16 * mm, "管理者")
        
        # 報告者枠
        c.rect(145 * mm, box_y, 40 * mm, 20 * mm)
        c.setFont(self.font_name, 9)
        c.drawString(147 * mm, box_y + 16 * mm, "報告者氏名")
        reporter = data.get("reporter", "")
        if reporter:
            c.setFont(self.font_name, 10)
            # 報告者名を中央に配置
            text_width = c.stringWidth(reporter, self.font_name, 10)
            text_x = 145 * mm + (40 * mm - text_width) / 2
            c.drawString(text_x, box_y + 5 * mm, reporter)
        
        # 記録日
        c.setFont(self.font_name, 9)
        record_date = data.get("record_date", "")
        if record_date:
            c.drawString(145 * mm, box_y + 22 * mm, f"記録日: {record_date}")
        
        # 保護者説明欄（左側）
        confirm_y = box_y - 35 * mm
        
        # ページからはみ出さないようにチェック
        if confirm_y >= BOTTOM_MARGIN + 30 * mm:
            c.rect(LEFT_MARGIN, confirm_y, 165 * mm, 30 * mm)
            
            c.setFont(self.font_name, 9)
            c.drawString(25 * mm, confirm_y + 25 * mm, "上記について、説明を受けました。")
            c.drawString(110 * mm, confirm_y + 25 * mm, "(説明が必要な場合に署名・捺印を頂きます)")
            
            c.setFont(self.font_name, 11)
            c.drawString(30 * mm, confirm_y + 8 * mm, "年       月       日")
            c.drawString(90 * mm, confirm_y + 8 * mm, "氏名")
            c.line(105 * mm, confirm_y + 8 * mm, 170 * mm, confirm_y + 8 * mm)
        
        c.save()
        return output_path
