"""
PDF生成モジュール
ReportLabを使用して事故報告書のPDFを生成します。
size.htmlのレイアウトを忠実に再現します。
"""
import os
import platform
import glob
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER


class AccidentReportGenerator:
    """事故報告書PDF生成クラス"""
    
    def __init__(self, font_path=None):
        """
        初期化
        
        Args:
            font_path: 日本語フォントファイルのパス（Noneの場合は自動検出）
        """
        self.width, self.height = A4
        self.font_name = "CustomJapaneseFont"
        
        # フォントの登録（環境に応じて自動選択）
        self._register_font(font_path)
        
        # スタイルシートの初期化
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _find_system_fonts(self):
        """環境に応じたシステムフォントを検索"""
        system = platform.system()
        font_paths = []
        
        if system == "Darwin":  # macOS
            # macOSのフォントパス
            mac_font_dirs = [
                "/System/Library/Fonts/Supplemental",
                "/Library/Fonts",
                os.path.expanduser("~/Library/Fonts"),
            ]
            
            # macOSでよく使われる日本語フォント（優先順位順）
            mac_font_patterns = [
                # 日本語フォント（優先）
                "HiraginoSans-W*.ttc",
                "Hiragino Sans GB.ttc",
                "Yu Gothic*.ttc",
                "YuMincho*.ttc",
                "Osaka.ttc",
                # その他のフォント
                "AppleGothic.ttf",
                "AppleMyungjo.ttf",
            ]
            
            for font_dir in mac_font_dirs:
                if os.path.exists(font_dir):
                    for pattern in mac_font_patterns:
                        matches = glob.glob(os.path.join(font_dir, pattern))
                        # 日本語フォントを優先的に追加
                        if "Hiragino" in pattern or "Yu" in pattern or "Osaka" in pattern:
                            font_paths = matches + font_paths
                        else:
                            font_paths.extend(matches)
        
        elif system == "Linux":
            # Linuxのフォントパス
            linux_font_dirs = [
                "/usr/share/fonts",
                "/usr/local/share/fonts",
                os.path.expanduser("~/.fonts"),
                os.path.expanduser("~/.local/share/fonts"),
            ]
            
            # Linuxでよく使われる日本語フォント
            linux_font_names = [
                "**/NotoSansCJK-*.ttc",
                "**/NotoSansCJK-*.ttf",
                "**/IPAexGothic*.ttf",
                "**/IPAGothic*.ttf",
                "**/TakaoGothic*.ttf",
                "**/VL-Gothic*.ttf",
                "**/VL-PGothic*.ttf",
            ]
            
            for font_dir in linux_font_dirs:
                if os.path.exists(font_dir):
                    for pattern in linux_font_names:
                        matches = glob.glob(os.path.join(font_dir, pattern), recursive=True)
                        font_paths.extend(matches)
        
        elif system == "Windows":
            # Windowsのフォントパス
            windows_font_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
            
            if os.path.exists(windows_font_dir):
                # Windowsでよく使われる日本語フォント
                windows_font_names = [
                    "msgothic.ttc",
                    "msmincho.ttc",
                    "yugothic.ttf",
                    "yumin.ttf",
                    "meiryo.ttc",
                    "meiryob.ttc",
                ]
                
                for font_name in windows_font_names:
                    font_path = os.path.join(windows_font_dir, font_name)
                    if os.path.exists(font_path):
                        font_paths.append(font_path)
        
        return font_paths
    
    def _register_font(self, font_path=None):
        """フォントを登録する（環境に応じた自動選択）"""
        # 1. 指定されたパスを確認
        if font_path and os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(self.font_name, font_path))
                print(f"✅ フォント登録成功（指定パス）: {font_path}")
                return
            except Exception as e:
                print(f"フォント登録エラー（指定パス）: {e}")
        
        # 2. 相対パス（プロジェクト内のフォント）を試す
        project_font_paths = [
            os.path.join(os.path.dirname(__file__), font_path) if font_path else None,
            os.path.join(os.path.dirname(__file__), "fonts", "IPAexGothic.ttf"),
            os.path.join(os.path.dirname(__file__), "fonts", "ipagp.ttf"),
            "fonts/IPAexGothic.ttf",
            "fonts/ipagp.ttf",
        ]
        
        for alt_path in project_font_paths:
            if alt_path and os.path.exists(alt_path):
                try:
                    pdfmetrics.registerFont(TTFont(self.font_name, alt_path))
                    print(f"✅ フォント登録成功（プロジェクト内）: {alt_path}")
                    return
                except Exception as e:
                    continue
        
        # 3. システムフォントを検索して試す
        system_fonts = self._find_system_fonts()
        # .ttfファイルを優先（.ttcファイルはReportLabで直接読み込めない場合がある）
        ttf_fonts = [f for f in system_fonts if f.lower().endswith('.ttf')]
        ttc_fonts = [f for f in system_fonts if f.lower().endswith('.ttc')]
        prioritized_fonts = ttf_fonts + ttc_fonts
        
        for sys_font_path in prioritized_fonts:
            if os.path.exists(sys_font_path):
                try:
                    pdfmetrics.registerFont(TTFont(self.font_name, sys_font_path))
                    print(f"✅ フォント登録成功（システムフォント）: {sys_font_path}")
                    return
                except Exception as e:
                    # .ttcファイルの場合はスキップして次を試す
                    if sys_font_path.lower().endswith('.ttc'):
                        continue
                    # その他のエラーもログに記録せずにスキップ
                    continue
        
        # 4. フォールバック: UnicodeCIDFontを試す
        try:
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            # 複数のCIDフォントを試す
            cid_fonts = [
                "HeiseiKakuGo-W5-Acro",
                "HeiseiMin-W3-Acro",
                "KozMinPro-Regular-Acro",
            ]
            for cid_font in cid_fonts:
                try:
                    pdfmetrics.registerFont(UnicodeCIDFont(cid_font))
                    self.font_name = cid_font
                    print(f"✅ UnicodeCIDFontを使用: {cid_font}")
                    return
                except:
                    continue
        except Exception as e:
            print(f"UnicodeCIDFont登録エラー: {e}")
        
        # 5. 最終手段: Helvetica（日本語は文字化けするがエラーは防ぐ）
        self.font_name = "Helvetica"
        print("⚠️ 警告: 日本語フォントが見つかりません。文字化けの可能性があります。")
    
    def _setup_custom_styles(self):
        """カスタムスタイルを設定"""
        try:
            self.table_title_style = ParagraphStyle(
                'TableTitle',
                parent=self.styles['Normal'],
                fontName=self.font_name,
                fontSize=11,
                leading=14,
                alignment=TA_CENTER,
                wordWrap='CJK',
            )
            self.table_content_style = ParagraphStyle(
                'TableContent',
                parent=self.styles['Normal'],
                fontName=self.font_name,
                fontSize=11,
                leading=14,
                alignment=TA_LEFT,
                wordWrap='CJK',
            )
        except Exception as e:
            print(f"スタイル設定エラー: {e}")
            # フォールバック
            self.table_title_style = self.styles['Normal']
            self.table_content_style = self.styles['Normal']
    
    def generate(self, data, output_path):
        """
        PDFを生成（size.htmlのレイアウトを忠実に再現）
        
        Args:
            data: 報告書データの辞書
            output_path: 出力ファイルパス
        """
        c = canvas.Canvas(output_path, pagesize=A4)
        c.setTitle("事故状況・対策報告書")
        
        # マージン設定（size.htmlに合わせて20mm）
        LEFT_MARGIN = 20 * mm
        RIGHT_MARGIN = 20 * mm
        TOP_MARGIN = 20 * mm
        BOTTOM_MARGIN = 20 * mm
        
        # ページサイズ（A4: 210mm x 297mm）
        page_width = 210 * mm
        page_height = 297 * mm
        
        # 現在のY位置（上から下へ、ReportLabは下から上なので変換）
        current_y = page_height - TOP_MARGIN
        
        # ヘッダー: 事業所名
        c.setFont(self.font_name, 12)
        facility_name = data.get("facility_name", "")
        office_text = f"【事業所名： {facility_name} 】" if facility_name else "【事業所名：                                        】"
        c.drawString(LEFT_MARGIN, current_y, office_text)
        current_y -= 10 * mm
        
        # タイトル: 事故状況・対策報告書（20pt、太字、中央揃え）
        c.setFont(self.font_name, 20)
        title = "事故状況・対策報告書"
        title_width = c.stringWidth(title, self.font_name, 20)
        c.drawString((page_width - title_width) / 2, current_y, title)
        current_y -= 15 * mm
        
        # 基本情報テーブル
        # 事故発生日時
        c.setFont(self.font_name, 11)
        label_x = LEFT_MARGIN
        content_x = LEFT_MARGIN + 26.5 * mm  # 100px相当
        
        c.drawString(label_x, current_y, "事故発生日時")
        
        # 日時の描画
        year = data.get('year', '')
        month = data.get('month', '')
        day = data.get('day', '')
        weekday = data.get('weekday', '')
        hour = data.get('hour', '')
        minute = data.get('minute', '')
        
        date_x = content_x
        if year:
            c.drawString(date_x, current_y, year)
        date_x += 15 * mm
        c.drawString(date_x, current_y, "年")
        date_x += 8 * mm
        if month:
            c.drawString(date_x, current_y, month)
        date_x += 12 * mm
        c.drawString(date_x, current_y, "月")
        date_x += 8 * mm
        if day:
            c.drawString(date_x, current_y, day)
        date_x += 12 * mm
        c.drawString(date_x, current_y, "日")
        date_x += 8 * mm
        c.drawString(date_x, current_y, "（")
        date_x += 6 * mm
        if weekday:
            c.drawString(date_x, current_y, weekday)
        date_x += 10 * mm
        c.drawString(date_x, current_y, "）曜日")
        date_x += 15 * mm
        if hour:
            c.drawString(date_x, current_y, hour)
        date_x += 12 * mm
        c.drawString(date_x, current_y, "時")
        date_x += 8 * mm
        if minute:
            c.drawString(date_x, current_y, minute)
        date_x += 12 * mm
        c.drawString(date_x, current_y, "分頃")
        
        current_y -= 8 * mm
        
        # 発生場所
        c.drawString(label_x, current_y, "発生場所")
        location = data.get("location", "")
        if location:
            c.drawString(content_x, current_y, location)
        current_y -= 8 * mm
        
        # 対象者
        c.drawString(label_x, current_y, "対象者")
        subject = data.get("subject", "")
        if subject:
            c.drawString(content_x, current_y, subject)
        current_y -= 5 * mm
        
        # メインテーブル（size.htmlに合わせて正確なサイズで）
        # テーブルデータの準備（HTMLの見出しに合わせる）
        table_data = [
            ["事故発生\n状況", data.get("situation", "")],
            ["ことの\n経緯", data.get("process", "")],  # HTMLでは"ことの経緯"
            ["事故\n原因", data.get("cause", "")],
            ["対　策", data.get("countermeasure", "")],  # 全角スペースあり
            ["その他", data.get("others", "")]
        ]
        
        # 列幅設定（HTMLに合わせて）
        col_widths = [35 * mm, page_width - LEFT_MARGIN - RIGHT_MARGIN - 35 * mm]
        
        # 行の高さ設定（HTMLに合わせて）
        row_heights = [
            35 * mm,  # 事故発生の状況
            35 * mm,  # ことの経緯
            35 * mm,  # 事故原因
            40 * mm,  # 対策
            20 * mm,  # その他
        ]
        
        # Paragraphオブジェクトを作成
        table_data_paragraphs = []
        for title, content in table_data:
            title_para = Paragraph(
                title.replace('\n', '<br/>'), 
                self.table_title_style
            )
            content_para = Paragraph(
                content.replace('\n', '<br/>') if content else "", 
                self.table_content_style
            )
            table_data_paragraphs.append([title_para, content_para])
        
        # テーブル作成
        t = Table(table_data_paragraphs, colWidths=col_widths, rowHeights=row_heights)
        
        # テーブルスタイル（HTMLに合わせて）
        # 外枠を2px、内部を1pxにするため、まず内部の線を描画
        t_style = TableStyle([
            # 内部の縦線（1px）
            ('LINEAFTER', (0, 0), (0, -1), 1, colors.black),
            # 内部の横線（1px）
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.black),
            # 外枠（2px）- 上
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
            # 外枠（2px）- 下
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            # 外枠（2px）- 左
            ('LINEBEFORE', (0, 0), (0, -1), 2, colors.black),
            # 外枠（2px）- 右
            ('LINEAFTER', (-1, 0), (-1, -1), 2, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),  # HTMLの背景色
        ])
        
        t.setStyle(t_style)
        
        # テーブルのサイズを計算
        available_height = current_y - BOTTOM_MARGIN - 80 * mm  # フッター用のスペース
        w, h = t.wrapOn(c, page_width - LEFT_MARGIN - RIGHT_MARGIN, available_height)
        
        # テーブル描画
        table_y = current_y - h
        t.drawOn(c, LEFT_MARGIN, table_y)
        
        # フッターエリア（HTMLに合わせて右側に配置）
        footer_y = table_y - 5 * mm
        
        # 管理者・報告者エリア（右側に配置、HTMLのflexboxレイアウトに合わせる）
        # HTMLでは gap: 20px (約7mm) で配置
        box_y = footer_y - 25 * mm
        
        # 報告者エリア（右側、先に配置して幅を計算）
        reporter_label = "報告者氏名："
        c.setFont(self.font_name, 11)
        reporter_label_width = c.stringWidth(reporter_label, self.font_name, 11)
        reporter = data.get("reporter", "")
        reporter_text_width = c.stringWidth(reporter, self.font_name, 11) if reporter else 0
        reporter_total_width = max(150 * mm, reporter_label_width + reporter_text_width + 10 * mm)
        
        # 管理者枠（20mm x 20mm、報告者エリアの左側、gap 7mm）
        manager_box_x = page_width - RIGHT_MARGIN - reporter_total_width - 7 * mm - 20 * mm
        manager_label_y = box_y + 20 * mm + 5 * mm
        c.setFont(self.font_name, 11)
        c.drawString(manager_box_x + (20 * mm - c.stringWidth("管理者", self.font_name, 11)) / 2, manager_label_y, "管理者")
        c.rect(manager_box_x, box_y, 20 * mm, 20 * mm)
        
        # 報告者エリア（右側）
        reporter_box_x = page_width - RIGHT_MARGIN - reporter_total_width
        
        # 報告者氏名
        c.setFont(self.font_name, 11)
        c.drawString(reporter_box_x, box_y + 15 * mm, reporter_label)
        if reporter:
            reporter_x = reporter_box_x + reporter_label_width
            c.drawString(reporter_x, box_y + 15 * mm, reporter)
        
        # 記録日
        record_date = data.get("record_date", "")
        if record_date:
            record_label = "記録日："
            c.setFont(self.font_name, 11)
            c.drawString(reporter_box_x, box_y + 5 * mm, record_label)
            record_x = reporter_box_x + c.stringWidth(record_label, self.font_name, 11)
            c.drawString(record_x, box_y + 5 * mm, record_date)
        
        # 保護者説明欄（下部、全幅、HTMLに合わせて）
        confirm_y = box_y - 35 * mm
        
        # ページからはみ出さないようにチェック
        if confirm_y >= BOTTOM_MARGIN + 30 * mm:
            # 枠線（全幅）
            confirm_width = page_width - LEFT_MARGIN - RIGHT_MARGIN
            c.rect(LEFT_MARGIN, confirm_y, confirm_width, 30 * mm)
            
            # 説明文（上段、HTMLに合わせて）
            c.setFont(self.font_name, 10)
            note_text = "(説明が必要な場合に署名・捺印を頂きます)"
            note_x = LEFT_MARGIN + 5 * mm
            c.drawString(note_x, confirm_y + 22 * mm, note_text)
            
            # メインテキスト（中段、太字、HTMLに合わせて）
            c.setFont(self.font_name, 11)
            main_text = "上記について、説明を受けました。"
            c.drawString(LEFT_MARGIN + 5 * mm, confirm_y + 15 * mm, main_text)
            
            # 日付と氏名欄（下段、右寄せ、HTMLに合わせて）
            c.setFont(self.font_name, 11)
            # 右寄せで配置
            date_label = "年       月       日"
            name_label = "氏名："
            name_line_width = 200 * mm  # HTMLの200px相当
            total_width = c.stringWidth(date_label, self.font_name, 11) + 15 * mm + c.stringWidth(name_label, self.font_name, 11) + name_line_width + c.stringWidth("(印)", self.font_name, 11)
            
            # 右寄せの開始位置
            right_start_x = page_width - RIGHT_MARGIN - total_width
            
            date_label_x = right_start_x
            c.drawString(date_label_x, confirm_y + 8 * mm, date_label)
            
            name_label_x = date_label_x + c.stringWidth(date_label, self.font_name, 11) + 15 * mm
            c.drawString(name_label_x, confirm_y + 8 * mm, name_label)
            
            # 氏名入力欄の下線
            name_line_x = name_label_x + c.stringWidth(name_label, self.font_name, 11) + 2 * mm
            c.line(name_line_x, confirm_y + 8 * mm, name_line_x + name_line_width, confirm_y + 8 * mm)
            
            # "(印)"テキスト
            stamp_text = "(印)"
            stamp_x = name_line_x + name_line_width + 2 * mm
            c.drawString(stamp_x, confirm_y + 8 * mm, stamp_text)
        
        c.save()
        return output_path
