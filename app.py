"""
放課後等デイサービス 事故報告書生成システム (J-ARGS)
StreamlitベースのWebアプリケーション
"""
import streamlit as st
import datetime
import os
import tempfile
import base64
from pdf_generator import AccidentReportGenerator

# AI統合モジュール
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def generate_ai_draft(raw_text, facility_name="", location="", subject=""):
    """
    AIを使用して報告書の各セクションを生成
    
    Args:
        raw_text: ユーザーのラフなメモ
        facility_name: 事業所名
        location: 発生場所
        subject: 対象者名
    
    Returns:
        各セクションのテキストを含む辞書
    """
    if not raw_text or not raw_text.strip():
        return {
            "situation": "",
            "process": "",
            "cause": "",
            "countermeasure": ""
        }
    
    # プロンプトの構築
    system_prompt = """あなたは放課後等デイサービスの経験豊富な管理者です。
以下のメモから、行政文書として適切な事故報告書を作成してください。

要件：
- 客観的で事実に基づいた記述
- 感情的な表現を避ける
- 5W1H（いつ、どこで、誰が、何を、なぜ、どのように）を明確に
- 専門用語を適切に使用
- 箇条書きではなく、文章形式で記述

以下の4つのセクションに分けて回答してください：
1. 事故発生の状況：何が起きたか、具体的な状況
2. 経過：事故発生後の対応、保護者への連絡など
3. 事故原因：なぜ起きたか、環境要因・人的要因など
4. 対策：再発防止策、改善点など

各セクションは2-3文程度で簡潔に記述してください。"""

    user_prompt = f"""【事業所名】{facility_name}
【発生場所】{location}
【対象者】{subject}

【メモ内容】
{raw_text}

上記のメモから、事故報告書の各セクションを作成してください。"""
    
    # OpenAI APIを使用（Grok互換またはOpenAI）
    if OPENAI_AVAILABLE:
        try:
            # Streamlit SecretsからAPIキーを取得
            api_key = None
            base_url = "https://api.openai.com/v1"
            try:
                api_key = st.secrets.get("OPENAI_API_KEY") or st.secrets.get("XAI_API_KEY")
                base_url = st.secrets.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
            except (AttributeError, KeyError):
                # secretsが設定されていない場合
                pass
            
            if api_key:
                client = OpenAI(api_key=api_key, base_url=base_url)
                
                model = "gpt-4"
                try:
                    model = st.secrets.get("OPENAI_MODEL", "gpt-4")
                except (AttributeError, KeyError):
                    pass
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1500
                )
                
                content = response.choices[0].message.content
                
                # レスポンスをパース（セクションごとに分割）
                sections = {
                    "situation": "",
                    "process": "",
                    "cause": "",
                    "countermeasure": ""
                }
                
                # セクションを抽出
                current_section = None
                for line in content.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    
                    if '状況' in line or '1.' in line:
                        current_section = "situation"
                        sections[current_section] = line.replace('1.', '').replace('事故発生の状況', '').strip()
                    elif '経過' in line or '2.' in line:
                        current_section = "process"
                        sections[current_section] = line.replace('2.', '').replace('経過', '').strip()
                    elif '原因' in line or '3.' in line:
                        current_section = "cause"
                        sections[current_section] = line.replace('3.', '').replace('事故原因', '').strip()
                    elif '対策' in line or '4.' in line:
                        current_section = "countermeasure"
                        sections[current_section] = line.replace('4.', '').replace('対策', '').strip()
                    elif current_section:
                        sections[current_section] += "\n" + line
                
                # 空のセクションを埋める
                for key in sections:
                    if not sections[key]:
                        sections[key] = content  # フォールバック
                
                return sections
        except Exception as e:
            st.warning(f"AI生成エラー: {e}")
    
    # Anthropic Claude APIを使用
    if ANTHROPIC_AVAILABLE:
        try:
            api_key = None
            try:
                api_key = st.secrets.get("ANTHROPIC_API_KEY")
            except (AttributeError, KeyError):
                pass
            
            if api_key:
                client = anthropic.Anthropic(api_key=api_key)
                
                message = client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1500,
                    temperature=0.3,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                
                content = message.content[0].text
                
                # 同様にパース
                sections = {
                    "situation": "",
                    "process": "",
                    "cause": "",
                    "countermeasure": ""
                }
                
                current_section = None
                for line in content.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    
                    if '状況' in line or '1.' in line:
                        current_section = "situation"
                        sections[current_section] = line.replace('1.', '').replace('事故発生の状況', '').strip()
                    elif '経過' in line or '2.' in line:
                        current_section = "process"
                        sections[current_section] = line.replace('2.', '').replace('経過', '').strip()
                    elif '原因' in line or '3.' in line:
                        current_section = "cause"
                        sections[current_section] = line.replace('3.', '').replace('事故原因', '').strip()
                    elif '対策' in line or '4.' in line:
                        current_section = "countermeasure"
                        sections[current_section] = line.replace('4.', '').replace('対策', '').strip()
                    elif current_section:
                        sections[current_section] += "\n" + line
                
                for key in sections:
                    if not sections[key]:
                        sections[key] = content
                
                return sections
        except Exception as e:
            st.warning(f"AI生成エラー: {e}")
    
    # フォールバック: モックデータ
    return {
        "situation": f"{raw_text}の状況において、事故が発生しました。",
        "process": "直ちに職員が駆けつけ、状況を確認しました。保護者への連絡を実施しました。",
        "cause": "環境要因および人的要因が重なったことが原因と考えられます。",
        "countermeasure": "再発防止策として、環境の整備と職員の研修を実施します。"
    }


# Streamlit UI設定
st.set_page_config(
    page_title="事故報告書生成システム",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<div class="main-header">🛡️ 放課後等デイサービス 事故報告書ジェネレーター</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">入力データとAIアシストを用いて、公式書式のPDFを即座に作成します。</div>', unsafe_allow_html=True)

# セッション状態の初期化
if 'ai_generated' not in st.session_state:
    st.session_state.ai_generated = False
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = {}
if 'situation' not in st.session_state:
    st.session_state.situation = ""
if 'process' not in st.session_state:
    st.session_state.process = ""
if 'cause' not in st.session_state:
    st.session_state.cause = ""
if 'countermeasure' not in st.session_state:
    st.session_state.countermeasure = ""
if 'others' not in st.session_state:
    st.session_state.others = ""
if 'ai_success_message' not in st.session_state:
    st.session_state.ai_success_message = False

# サイドバー: 基本設定
with st.sidebar:
    st.header("⚙️ 基本設定")
    facility_name = st.text_input("事業所名", value="放課後等デイサービス ミライ", key="facility_name")
    reporter_name = st.text_input("報告者氏名", key="reporter_name")
    record_date = st.date_input("記録日", datetime.date.today(), key="record_date")
    
    st.markdown("---")
    st.header("🤖 AI設定")
    use_ai = st.checkbox("AIで文章を自動生成する", value=True, key="use_ai")
    
    if use_ai:
        st.info("""
        AI機能を使用するには、Streamlit Secretsに以下を設定してください：
        - OPENAI_API_KEY または XAI_API_KEY
        - OPENAI_BASE_URL (Grok使用時)
        - OPENAI_MODEL (デフォルト: gpt-4)
        
        または
        
        - ANTHROPIC_API_KEY (Claude使用時)
        """)

# 事故発生情報入力
st.subheader("📋 1. 事故発生情報")

col1, col2, col3 = st.columns(3)
with col1:
    accident_date = st.date_input("発生日", datetime.date.today(), key="accident_date")
with col2:
    accident_time = st.time_input("発生時刻", datetime.time(16, 30), key="accident_time")
with col3:
    weekday_map = {0: '月', 1: '火', 2: '水', 3: '木', 4: '金', 5: '土', 6: '日'}
    weekday_val = weekday_map[accident_date.weekday()]
    st.info(f"**曜日**: {weekday_val}曜日")

col_loc, col_sub = st.columns([1, 1])
with col_loc:
    location = st.text_input("発生場所", placeholder="例：プレイルーム、送迎車内", key="location")
with col_sub:
    subject = st.text_input("対象者（児童名）", placeholder="例：山田 太郎", key="subject")

st.markdown("---")
st.subheader("✍️ 2. 詳細内容")

# AI入力エリア
st.markdown("**AIアシスト入力（メモ書きでOK）**")
ai_input = st.text_area(
    "ここに「何が起きたか」を箇条書きやメモ書きで入力してください。",
    height=120,
    placeholder="例：\n- バランスボールで遊んでいて転んだ\n- 手首を痛がったので冷やした\n- お母さんに電話して説明した",
    key="ai_input"
)

# AI生成ボタン（フォーム外）
if use_ai and ai_input:
    if st.button("🤖 AIで報告書案を作成", use_container_width=True, type="secondary"):
        with st.spinner("AIが報告書を作成中..."):
            ai_draft = generate_ai_draft(ai_input, facility_name, location, subject)
            st.session_state.ai_generated = True
            st.session_state.generated_data = ai_draft
            # テキストエリアのセッション状態を更新
            st.session_state.situation = ai_draft.get("situation", "")
            st.session_state.process = ai_draft.get("process", "")
            st.session_state.cause = ai_draft.get("cause", "")
            st.session_state.countermeasure = ai_draft.get("countermeasure", "")
            st.session_state.ai_success_message = True
        st.rerun()  # ページを再読み込みしてテキストエリアを更新

# AI生成結果の表示
if st.session_state.ai_success_message:
    st.success("✅ AI生成が完了しました！下記のフィールドを確認・編集してください。")
    st.session_state.ai_success_message = False  # メッセージを1回だけ表示

if st.session_state.ai_generated and st.session_state.generated_data:
    st.info("💡 AI生成された内容が下記のフィールドに自動入力されています。必要に応じて編集してください。")

st.markdown("---")
st.markdown("**詳細記述フィールド（手動編集可）**")

col_main_1, col_main_2 = st.columns(2)

with col_main_1:
    situation = st.text_area(
        "事故発生の状況",
        height=150,
        value=st.session_state.situation,
        key="situation"
    )
    cause = st.text_area(
        "事故原因",
        height=120,
        value=st.session_state.cause,
        key="cause"
    )
    others = st.text_area(
        "その他",
        height=80,
        value=st.session_state.others,
        key="others"
    )

with col_main_2:
    process = st.text_area(
        "経過",
        height=150,
        value=st.session_state.process,
        key="process"
    )
    countermeasure = st.text_area(
        "対策",
        height=120,
        value=st.session_state.countermeasure,
        key="countermeasure"
    )

# PDF生成ボタン（フォーム外）
submitted = st.button("📄 PDFを生成", use_container_width=True, type="primary")

# PDF生成処理
if submitted:
    # バリデーション
    if not facility_name:
        st.error("⚠️ 事業所名を入力してください。")
    elif not location:
        st.error("⚠️ 発生場所を入力してください。")
    elif not subject:
        st.error("⚠️ 対象者（児童名）を入力してください。")
    else:
        # データの辞書化
        data = {
            "facility_name": facility_name,
            "year": str(accident_date.year),
            "month": str(accident_date.month),
            "day": str(accident_date.day),
            "weekday": weekday_val,
            "hour": str(accident_time.hour),
            "minute": f"{accident_time.minute:02d}",
            "location": location,
            "subject": subject,
            "situation": situation,
            "process": process,
            "cause": cause,
            "countermeasure": countermeasure,
            "others": others,
            "reporter": reporter_name,
            "record_date": record_date.strftime("%Y年%m月%d日")
        }
        
        # PDF生成
        try:
            with st.spinner("PDFを生成中..."):
                # 一時ファイルを使用
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    output_path = tmp_file.name
                
                # フォントファイルのパス
                font_path = "fonts/IPAexGothic.ttf"
                
                generator = AccidentReportGenerator(font_path=font_path)
                generator.generate(data, output_path)
                
                st.success("✅ PDFの生成が完了しました！")
                
                # ダウンロードボタン
                with open(output_path, "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                
                # ファイル名から使用できない文字を削除
                safe_facility_name = "".join(c for c in facility_name if c.isalnum() or c in (' ', '-', '_')).strip()
                if not safe_facility_name:
                    safe_facility_name = "事業所"
                filename = f"事故報告書_{safe_facility_name}_{accident_date.strftime('%Y%m%d')}.pdf"
                
                st.download_button(
                    label="📥 報告書PDFをダウンロード",
                    data=PDFbyte,
                    file_name=filename,
                    mime='application/pdf',
                    use_container_width=True
                )
                
                # プレビュー表示
                st.markdown("---")
                st.subheader("📄 PDFプレビュー")
                base64_pdf = base64.b64encode(PDFbyte).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
                
                # 一時ファイルを削除
                try:
                    os.unlink(output_path)
                except Exception:
                    pass
                    
        except Exception as e:
            st.error(f"❌ PDF生成エラー: {e}")
            st.exception(e)

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>J-ARGS (Japanese Accident Report Generation System for Day Service)</p>
    <p>© 2024 放課後等デイサービス 事故報告書生成システム</p>
</div>
""", unsafe_allow_html=True)

