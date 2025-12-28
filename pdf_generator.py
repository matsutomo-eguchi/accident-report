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
from reportlab.platypus import Table, TableStyle, Paragraph
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
                return
            except Exception as e:
                print(f"フォント登録エラー: {e}")
        
        # 相対パスも試す
        alt_paths = [
            os.path.join(os.path.dirname(__file__), font_path),
            os.path.join(os.path.dirname(__file__), "fonts", "IPAexGothic.ttf"),
            "fonts/IPAexGothic.ttf",
        ]
        
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                try:
                    pdfmetrics.registerFont(TTFont(self.font_name, alt_path))
                    return
                except Exception:
                    continue
        
        # フォールバック: UnicodeCIDFontを試す
        try:
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5-Acro"))
            self.font_name = "HeiseiKakuGo-W5-Acro"
        except Exception:
            # 最終手段: Helvetica（日本語は文字化けするがエラーは防ぐ）
            self.font_name = "Helvetica"
            print("警告: 日本語フォントが見つかりません。文字化けの可能性があります。")
    
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
            )
            self.title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Normal'],
                fontName=self.font_name,
                fontSize=18,
                leading=22,
                alignment=TA_CENTER,
            )
        except Exception:
            # フォールバック
            self.normal_style = self.styles['Normal']
            self.title_style = self.styles['Normal']
    
    def _draw_text_with_wrap(self, canvas_obj, text, x, y, max_width, font_name, font_size):
        """テキストを折り返して描画"""
        if not text:
            return y
        
        # 改行コードで分割
        lines = text.split('\n')
        current_y = y
        
        for line in lines:
            if not line.strip():
                current_y -= font_size * 1.2
                continue
            
            # 長い行を折り返し
            words = line.split()
            current_line = ""
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                width = canvas_obj.stringWidth(test_line, font_name, font_size)
                
                if width > max_width and current_line:
                    canvas_obj.setFont(font_name, font_size)
                    canvas_obj.drawString(x, current_y, current_line)
                    current_y -= font_size * 1.2
                    current_line = word
                else:
                    current_line = test_line
            
            if current_line:
                canvas_obj.setFont(font_name, font_size)
                canvas_obj.drawString(x, current_y, current_line)
                current_y -= font_size * 1.2
        
        return current_y
    
    def generate(self, data, output_path):
        """
        PDFを生成
        
        Args:
            data: 報告書データの辞書
            output_path: 出力ファイルパス
        """
        c = canvas.Canvas(output_path, pagesize=A4)
        c.setTitle("事故状況・対策報告書")
        
        # フォントサイズ設定
        FONT_SIZE_TITLE = 18
        FONT_SIZE_LABEL = 10
        FONT_SIZE_TEXT = 10
        
        # タイトル
        c.setFont(self.font_name, FONT_SIZE_TITLE)
        c.drawCentredString(self.width / 2, self.height - 20 * mm, "事故状況・対策報告書")
        
        # 事業所名
        y_pos = self.height - 40 * mm
        c.setFont(self.font_name, 11)
        c.drawString(20 * mm, y_pos, "【事業所名】")
        c.line(45 * mm, y_pos - 1 * mm, 120 * mm, y_pos - 1 * mm)
        facility_name = data.get("facility_name", "")
        if facility_name:
            c.drawString(45 * mm, y_pos, facility_name)
        
        # 基本情報エリア
        y_pos -= 12 * mm
        
        # 発生日時
        c.setFont(self.font_name, FONT_SIZE_LABEL)
        c.drawString(20 * mm, y_pos, "事故発生日時：")
        
        date_str = f"{data.get('year', '')} 年  {data.get('month', '')} 月  {data.get('day', '')} 日"
        time_str = f"{data.get('hour', '')} 時  {data.get('minute', '')} 分頃"
        weekday = f"({data.get('weekday', '')})曜日"
        
        c.setFont(self.font_name, FONT_SIZE_TEXT)
        c.drawString(50 * mm, y_pos, f"{date_str}   {time_str}   {weekday}")
        
        # 場所・対象者
        y_pos -= 8 * mm
        c.setFont(self.font_name, FONT_SIZE_LABEL)
        c.drawString(20 * mm, y_pos, "発生場所：")
        c.setFont(self.font_name, FONT_SIZE_TEXT)
        c.drawString(50 * mm, y_pos, data.get("location", ""))
        
        c.setFont(self.font_name, FONT_SIZE_LABEL)
        c.drawString(110 * mm, y_pos, "対象者：")
        c.setFont(self.font_name, FONT_SIZE_TEXT)
        c.drawString(130 * mm, y_pos, data.get("subject", ""))
        
        # メインテーブル
        y_pos -= 10 * mm
        
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
        for title, content in table_data:
            title_para = Paragraph(title.replace('\n', '<br/>'), self.normal_style)
            content_para = Paragraph(content.replace('\n', '<br/>'), self.normal_style) if content else Paragraph("", self.normal_style)
            table_data_paragraphs.append([title_para, content_para])
        
        # テーブルスタイル設定
        col_widths = [30 * mm, 140 * mm]
        
        # 行の高さを動的に計算（最小値設定）
        min_row_height = 15 * mm
        row_heights = []
        for title, content in table_data:
            # 内容量に応じて高さを調整
            content_lines = len(content.split('\n')) if content else 1
            estimated_height = max(min_row_height, (content_lines * 4 + 2) * mm)
            row_heights.append(estimated_height)
        
        t = Table(table_data_paragraphs, colWidths=col_widths, rowHeights=row_heights)
        
        t_style = TableStyle([
            ('FONT', (0, 0), (-1, -1), self.font_name, 10),
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
        
        # テーブル描画
        w, h = t.wrapOn(c, self.width, self.height)
        table_y = y_pos - h - 5 * mm
        
        # ページからはみ出さないように調整
        min_y_for_footer = 80 * mm  # フッター用の最小Y位置
        if table_y < min_y_for_footer:
            # テーブルが大きすぎる場合、行の高さを調整
            table_y = min_y_for_footer
            # テーブルの高さを制限
            available_height = y_pos - min_y_for_footer - 5 * mm
            if h > available_height:
                # 行の高さを比例的に縮小
                scale_factor = available_height / h
                row_heights = [h * scale_factor for h in row_heights]
                t = Table(table_data_paragraphs, colWidths=col_widths, rowHeights=row_heights)
                t.setStyle(t_style)
                w, h = t.wrapOn(c, self.width, self.height)
                table_y = y_pos - h - 5 * mm
        
        t.drawOn(c, 20 * mm, table_y)
        
        footer_base_y = table_y - 10 * mm
        
        # 署名・確認欄エリア（最低限のスペースを確保）
        box_y = max(footer_base_y - 25 * mm, 50 * mm)
        
        # 管理者枠
        c.rect(115 * mm, box_y, 25 * mm, 20 * mm)
        c.setFont(self.font_name, 9)
        c.drawString(118 * mm, box_y + 16 * mm, "管理者")
        
        # 報告者枠
        c.rect(145 * mm, box_y, 40 * mm, 20 * mm)
        c.drawString(147 * mm, box_y + 16 * mm, "報告者氏名")
        reporter = data.get("reporter", "")
        if reporter:
            c.setFont(self.font_name, 10)
            c.drawString(150 * mm, box_y + 5 * mm, reporter)
        
        # 記録日
        c.setFont(self.font_name, 9)
        record_date = data.get("record_date", "")
        if record_date:
            c.drawString(145 * mm, box_y + 22 * mm, f"記録日: {record_date}")
        
        # 保護者説明欄（最低限のスペースを確保）
        confirm_y = max(box_y - 35 * mm, 20 * mm)
        # 保護者説明欄を描画（重ならないように調整）
        if confirm_y + 30 * mm < box_y:
            c.rect(20 * mm, confirm_y, 165 * mm, 30 * mm)
            
            c.setFont(self.font_name, 9)
            c.drawString(25 * mm, confirm_y + 25 * mm, "上記について、説明を受けました。")
            c.drawString(110 * mm, confirm_y + 25 * mm, "(説明が必要な場合に署名・捺印を頂きます)")
            
            c.setFont(self.font_name, 11)
            c.drawString(30 * mm, confirm_y + 8 * mm, "年       月       日")
            c.drawString(90 * mm, confirm_y + 8 * mm, "氏名")
            c.line(105 * mm, confirm_y + 8 * mm, 170 * mm, confirm_y + 8 * mm)
        
        c.save()
        return output_path

