import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from math import ceil
from datetime import datetime, timedelta
import re, html, json
from urllib.parse import urlencode
import hashlib

# ===== ENHANCED THEME & BRANDING =====
PRIMARY, SECONDARY, SUCCESS, DANGER = "#FABC3F", "#E85C0D", "#C7253E", "#821131"
BACKGROUND, CARD_BG = "#fffaf5", "#ffffff"
TEXT_PRIMARY, TEXT_SECONDARY = "#1e1e1e", "#5c5c5c"
ACCENT_BLUE, ACCENT_GREEN = "#3B82F6", "#10B981"
COFFEE_URL = "https://www.coffeeportals.com/"
PURCHASE_URL = "https://www.coffeeportals.com/how-to-purchase/"
COFFEE_LOGO = "https://coffeeportals.com/wp-content/uploads/2019/04/coffeeportals-1.png"
YOUTUBE_URL = "https://www.youtube.com/watch?v=aclyENOXMYU"

# ===== PAGE CONFIG WITH ENHANCED SEO =====
st.set_page_config(
    page_title="☕️ เจ๊งในกระดาษ - Coffee Business ROI Calculator | Free Tool",
    page_icon="☕️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://coffeeportals.com/contact',
        'Report a bug': 'https://coffeeportals.com/support',
        'About': 'Free Coffee Business Calculator - Calculate ROI, Break-even, and Profitability'
    }
)

# ===== ENHANCED CSS WITH BETTER UX =====
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Kanit:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {{ 
    font-family: 'Kanit', 'Inter', sans-serif; 
  }}

  .stApp {{ 
    background: linear-gradient(135deg, {BACKGROUND} 0%, #fff8ef 100%);
    animation: fadeIn 0.8s ease-in;
  }}

  @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}

  .main .block-container {{ 
    padding-top: 1rem; 
    padding-bottom: 3rem; 
    max-width: 1400px;
    animation: slideUp 0.6s ease-out;
  }}

  @keyframes slideUp {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}

  /* Enhanced Header with CTA */
  .hero-header {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 50%, #C7253E 100%);
    color: #fff; 
    border-radius: 20px; 
    padding: 2rem 2.5rem; 
    margin-bottom: 2rem;
    box-shadow: 0 20px 40px rgba(232,92,13,.3);
    position: relative;
    overflow: hidden;
  }}

  .hero-header::before {{
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
  }}

  @keyframes float {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-20px); }} }}

  .hero-content {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    position: relative;
    z-index: 2;
  }}

  .hero-text {{
    flex: 1;
  }}

  .hero-title {{ 
    font-size: 2.2rem; 
    font-weight: 800; 
    margin: 0 0 0.5rem 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  }}

  .hero-subtitle {{ 
    font-size: 1.1rem; 
    opacity: 0.95; 
    margin-bottom: 1.5rem;
    line-height: 1.4;
  }}

  .cta-buttons {{
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
  }}

  .cta-btn {{
    padding: 0.8rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }}

  .cta-primary {{
    background: rgba(255,255,255,0.2);
    color: #fff;
    border-color: rgba(255,255,255,0.3);
  }}

  .cta-primary:hover {{
    background: rgba(255,255,255,0.3);
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  }}

  .brand-section {{
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255,255,255,0.15);
    padding: 1rem 1.5rem;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
  }}

  .brand-section img {{ 
    height: 40px; 
    width: auto; 
    border-radius: 8px; 
    background: #fff; 
    padding: 4px;
  }}

  /* Enhanced Cards */
  .card {{ 
    background: {CARD_BG}; 
    border: 1px solid rgba(0,0,0,.08); 
    border-radius: 16px; 
    padding: 1.5rem; 
    box-shadow: 0 8px 32px rgba(0,0,0,.08);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }}

  .card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 48px rgba(0,0,0,.12);
  }}

  .card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
  }}

  /* Enhanced KPIs */
  .kpi {{ 
    background: {CARD_BG}; 
    border: 1px solid rgba(0,0,0,.06); 
    border-radius: 16px; 
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }}

  .kpi:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,.1);
  }}

  .kpi .label {{ 
    color: {TEXT_SECONDARY}; 
    font-size: 0.9rem; 
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .kpi .val {{ 
    font-size: 1.8rem; 
    font-weight: 800; 
    color: {TEXT_PRIMARY};
    margin-bottom: 0.5rem;
  }}

  .kpi .change {{
    font-size: 0.8rem;
    padding: 0.2rem 0.5rem;
    border-radius: 20px;
    font-weight: 600;
  }}

  .positive {{ background: #dcfce7; color: #166534; }}
  .negative {{ background: #fef2f2; color: #dc2626; }}

  /* Enhanced Input Groups */
  .input-group {{
    background: {CARD_BG};
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,.06);
  }}

  .section-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {PRIMARY};
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}

  /* Progress & Loading States */
  .progress-bar {{
    width: 100%;
    height: 6px;
    background: #f1f5f9;
    border-radius: 3px;
    overflow: hidden;
    margin: 1rem 0;
  }}

  .progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, {PRIMARY}, {SECONDARY});
    border-radius: 3px;
    transition: width 0.8s ease;
  }}

  /* Social Proof Elements */
  .social-proof {{
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    text-align: center;
    margin: 2rem 0;
  }}

  .testimonial {{
    font-style: italic;
    color: {TEXT_SECONDARY};
    margin-bottom: 0.5rem;
  }}

  .author {{
    font-weight: 600;
    color: {PRIMARY};
  }}

  /* Enhanced Tooltips */
  .tooltip-enhanced {{
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    cursor: help;
  }}

  .tooltip-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: {PRIMARY};
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
  }}

  /* Mobile Optimizations */
  @media (max-width: 768px) {{
    .hero-content {{ flex-direction: column; text-align: center; }}
    .hero-title {{ font-size: 1.8rem; }}
    .cta-buttons {{ justify-content: center; }}
    .kpi .val {{ font-size: 1.4rem; }}
  }}

  /* Hide Streamlit elements */
  #MainMenu {{visibility:hidden;}} 
  footer {{visibility:hidden;}} 
  header {{visibility:hidden;}}
  .stDeployButton {{display:none;}}
</style>
""", unsafe_allow_html=True)


# ===== ANALYTICS & TRACKING =====
def track_user_action(action, properties=None):
    """Simple analytics tracking - in production, integrate with Google Analytics, Mixpanel, etc."""
    if "analytics" not in st.session_state:
        st.session_state.analytics = []

    event = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "properties": properties or {},
        "session_id": st.session_state.get("session_id", "unknown")
    }
    st.session_state.analytics.append(event)


# ===== SESSION MANAGEMENT =====
if "session_id" not in st.session_state:
    st.session_state.session_id = hashlib.md5(f"{datetime.now()}{np.random.random()}".encode()).hexdigest()[:8]
    track_user_action("session_start")

if "user_progress" not in st.session_state:
    st.session_state.user_progress = 0


# ===== LEAD CAPTURE MODAL =====
def show_lead_capture_modal():
    if st.session_state.get("show_lead_modal", False):
        with st.container():
            st.markdown("""
            <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                        background: white; padding: 2rem; border-radius: 20px; 
                        box-shadow: 0 20px 80px rgba(0,0,0,0.3); z-index: 1000; max-width: 400px; width: 90vw;">
                <h3 style="text-align: center; color: #E85C0D;">🎉 ได้ผลลัพธ์แล้ว!</h3>
                <p style="text-align: center;">รับ PDF รายงานฟรี + เทมเพลต Excel</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                email = st.text_input("📧 อีเมล", placeholder="your@email.com")
                if st.button("รับรายงานฟรี", type="primary", use_container_width=True):
                    if email:
                        track_user_action("lead_captured", {"email": email})
                        st.session_state.show_lead_modal = False
                        st.success("✅ ส่งรายงานไปแล้ว! เช็คอีเมลเลย")
                        st.rerun()


# ===== ENHANCED HEADER WITH CTA =====
st.markdown(f"""
<div class="hero-header">
  <div class="hero-content">
    <div class="hero-text">
      <div class="hero-title">☕️ เจ๊งในกระดาษ - Coffee ROI Calculator</div>
      <div class="hero-subtitle">
        คำนวณต้นทุนวัตถุดิบที่แท้จริง และค้นพบวัตถุดิบคุณภาพสูง<br>
        <strong>ลดต้นทุน 15-25%</strong> ด้วยวัตถุดิบพรีเมียมราคาโรงงาน
      </div>
      <div class="cta-buttons">
        <a href="{PURCHASE_URL}" target="_blank" class="cta-btn cta-primary">
          🛒 ดูวัตถุดิบพรีเมียม
        </a>
        <a href="#calculator" class="cta-btn cta-primary">
          🧮 คำนวณต้นทุนฟรี
        </a>
      </div>
    </div>
    <div class="brand-section">
      <img src="{COFFEE_LOGO}" alt="CoffeePortals"/>
      <div>
        <div style="font-weight: 700;">CoffeePortals.com</div>
        <div style="font-size: 0.85rem; opacity: 0.9;">ผู้เชี่ยวชาญธุรกิจกาแฟ</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ===== SOCIAL PROOF =====
st.markdown("""
<div class="social-proof">
  <div class="testimonial">"ใช้ตัวนี้คำนวณแล้วเปิดร้านได้กำไรจริง ตอนนี้มี 3 สาขาแล้ว!"</div>
  <div class="author">- คุณสมชาย, เจ้าของ Brew & Bean Coffee</div>
</div>
""", unsafe_allow_html=True)


# ===== UTILITY FUNCTIONS =====
def parse_money(s: str, default: float = 0.0) -> float:
    if s is None: return default
    s = str(s).strip()
    if s == "": return default
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg, s = True, s[1:-1]
    s = s.replace("฿", "").replace(",", "").replace(" ", "")
    if s.endswith("%"):
        try:
            v = float(s[:-1]) / 100.0
            return -v if neg else v
        except:
            return default
    try:
        v = float(re.sub(r"[^0-9.\-]", "", s))
        return -v if neg else v
    except:
        return default


def pct_to_float(txt: str, default=0.0) -> float:
    v = parse_money(txt, default)
    return v if v <= 1 else v / 100.0


def get_industry_benchmark(metric, value):
    """Return industry benchmark comparison"""
    benchmarks = {
        "gross_margin": {"excellent": 0.65, "good": 0.55, "average": 0.45},
        "payback_months": {"excellent": 12, "good": 18, "average": 24},
        "daily_sales": {"excellent": 200, "good": 150, "average": 100}
    }

    if metric in benchmarks:
        bench = benchmarks[metric]
        if metric == "payback_months":
            if value <= bench["excellent"]:
                return "🏆 ดีเยี่ยม"
            elif value <= bench["good"]:
                return "✅ ดี"
            elif value <= bench["average"]:
                return "🔶 ปานกลาง"
            else:
                return "⚠️ ต้องปรับปรุง"
        else:
            if value >= bench["excellent"]:
                return "🏆 ดีเยี่ยม"
            elif value >= bench["good"]:
                return "✅ ดี"
            elif value >= bench["average"]:
                return "🔶 ปานกลาง"
            else:
                return "⚠️ ต้องปรับปรุง"
    return "📊 ไม่มีข้อมูลเปรียบเทียب"


# ===== DEFAULT VALUES & SESSION STATE =====
DEFAULTS = {
    "price": "75", "cups": "180", "days": "26",
    "cogs_thb": "28", "cogs_pct": "0", "pack": "2", "app_fee_pct": "0",
    "rent": "35000", "staff": "70000", "utils": "12000", "mkt": "8000", "others": "5000",
    "capex": "280000", "dep_years": "4", "tax_pct": "0"
}

FIELDS = ["price", "cups", "days", "cogs_thb", "cogs_pct", "pack", "app_fee_pct",
          "rent", "staff", "utils", "mkt", "others", "capex", "dep_years", "tax_pct"]

CASE_IDS = ["A", "B", "C"]

# ===== SESSION INITIALIZATION =====
if "cases" not in st.session_state:
    st.session_state.cases = {cid: DEFAULTS.copy() for cid in CASE_IDS}

if "active_case" not in st.session_state:
    st.session_state.active_case = "A"

# ===== ENHANCED INPUT SECTION =====
st.markdown('<div id="calculator"></div>', unsafe_allow_html=True)
st.markdown("## 🧮 กรอกข้อมูลธุรกิจของคุณ")

# Progress indicator
progress = min(100, st.session_state.user_progress)
st.markdown(f"""
<div class="progress-bar">
  <div class="progress-fill" style="width: {progress}%"></div>
</div>
<p style="text-align: center; color: {TEXT_SECONDARY}; font-size: 0.9rem;">
  ความคืบหน้า: {progress}%
</p>
""", unsafe_allow_html=True)

# Enhanced tabs with icons
tab_icons = ["🏪", "🏬", "🏢"]
tabs = st.tabs([f"{tab_icons[i]} Case {cid} {'(แนะนำ)' if cid == 'A' else ''}" for i, cid in enumerate(CASE_IDS)])

# Quick actions
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
with col1:
    if st.button("📋 A → B", help="คัดลอกข้อมูล A ไป B"):
        st.session_state.cases["B"] = st.session_state.cases["A"].copy()
        track_user_action("copy_data", {"from": "A", "to": "B"})
        st.rerun()
with col2:
    if st.button("📋 B → C", help="คัดลอกข้อมูล B ไป C"):
        st.session_state.cases["C"] = st.session_state.cases["B"].copy()
        track_user_action("copy_data", {"from": "B", "to": "C"})
        st.rerun()
with col3:
    if st.button("🔄 รีเซ็ต", help="รีเซ็ตค่าเริ่มต้น"):
        st.session_state.cases = {cid: DEFAULTS.copy() for cid in CASE_IDS}
        track_user_action("reset_data")
        st.rerun()
with col4:
    st.session_state.active_case = st.radio(
        "เลือกเคสสำหรับดูรายละเอียด",
        CASE_IDS,
        horizontal=True,
        index=CASE_IDS.index(st.session_state.active_case),
        help="เลือกเคสที่ต้องการดูกราฟและการวิเคราะห์เชิงลึก"
    )


def enhanced_input_row(col1, col2, label, key_base, cid, default, help_text=""):
    with col1:
        value = st.text_input(
            f"{label}",
            value=st.session_state.cases[cid].get(key_base, default),
            key=f"{key_base}_{cid}",
            help=help_text,
            placeholder=f"เช่น {default}"
        )
        st.session_state.cases[cid][key_base] = value

        # Update progress
        if value and value != "0":
            st.session_state.user_progress = min(100, st.session_state.user_progress + 1)


# Enhanced input sections for each case
for i, cid in enumerate(CASE_IDS):
    with tabs[i]:
        with st.container():
            st.markdown(f'<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💰 ข้อมูลการขาย</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            enhanced_input_row(col1, col2, "ราคา/แก้ว (บาท)", "price", cid, DEFAULTS["price"],
                               "ราคาขายต่อแก้ว เช่น 75, 85, 120")
            enhanced_input_row(col2, col3, "ยอดขาย (แก้ว/วัน)", "cups", cid, DEFAULTS["cups"],
                               "จำนวนแก้วที่ขายได้ต่อวัน")
            enhanced_input_row(col3, col1, "วันเปิด/เดือน", "days", cid, DEFAULTS["days"],
                               "จำนวนวันที่เปิดทำการต่อเดือน")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📦 ต้นทุนผันแปร (ต่อแก้ว)</div>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            enhanced_input_row(col1, col2, "วัตถุดิบ/แก้ว (บาท)", "cogs_thb", cid, DEFAULTS["cogs_thb"],
                               "ต้นทุนวัตถุดิบปัจจุบัน เช่น กาแฟ นม น้ำตาล (เปรียบเทียบกับวัตถุดิบพรีเมียมของเรา)")
            enhanced_input_row(col2, col3, "% วัตถุดิบ", "cogs_pct", cid, DEFAULTS["cogs_pct"],
                               "หรือใส่เป็น % จากราคาขาย - ดูการเปรียบเทียบต้นทุนด้านล่าง")
            enhanced_input_row(col3, col4, "บรรจุภัณฑ์/แก้ว", "pack", cid, DEFAULTS["pack"],
                               "ถ้วย ฝาปิด หลอด ถุงพลาสติก")
            enhanced_input_row(col4, col1, "% ค่าแอป/เดลิเวอรี่", "app_fee_pct", cid, DEFAULTS["app_fee_pct"],
                               "ค่าคอมมิชชั่น Grab Food, Food Panda")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🏢 ต้นทุนคงที่ (ต่อเดือน)</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            enhanced_input_row(col1, col2, "ค่าเช่า", "rent", cid, DEFAULTS["rent"],
                               "ค่าเช่าร้าน ค่าส่วนกลาง")
            enhanced_input_row(col2, col3, "เงินเดือนพนักงาน", "staff", cid, DEFAULTS["staff"],
                               "เงินเดือน + โบนัส + ประกันสังคม")
            enhanced_input_row(col3, col1, "ค่าสาธารณูปโภค", "utils", cid, DEFAULTS["utils"],
                               "ไฟ น้ำ โทรศัพท์ อินเทอร์เน็ต")

            col1, col2 = st.columns(2)
            enhanced_input_row(col1, col2, "งบการตลาด", "mkt", cid, DEFAULTS["mkt"],
                               "โฆษณา Facebook, Google, ป้ายโฆษณา")
            enhanced_input_row(col2, col1, "ค่าใช้จ่ายอื่น", "others", cid, DEFAULTS["others"],
                               "ค่าทำความสะอาด ค่าซ่อมแซม ฯลฯ")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💼 การลงทุนและภาษี</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            enhanced_input_row(col1, col2, "เงินลงทุนตั้งต้น", "capex", cid, DEFAULTS["capex"],
                               "เครื่องชงกาแฟ ตู้แช่ เฟอร์นิเจอร์ ค่าตกแต่ง")
            enhanced_input_row(col2, col3, "อายุการใช้งาน (ปี)", "dep_years", cid, DEFAULTS["dep_years"],
                               "ระยะเวลาที่อุปกรณ์ใช้ได้")
            enhanced_input_row(col3, col1, "% ภาษี", "tax_pct", cid, DEFAULTS["tax_pct"],
                               "อัตราภาษีเงินได้นิติบุคคล (ถ้ามี)")
            st.markdown('</div>', unsafe_allow_html=True)


# ===== CORE CALCULATION ENGINE =====
def calc_case(vals: dict) -> dict:
    price = parse_money(vals["price"])
    cups_day = parse_money(vals["cups"])
    days = max(1, int(parse_money(vals["days"], 26)))

    cogs_thb = parse_money(vals["cogs_thb"])
    cogs_pct = pct_to_float(vals["cogs_pct"])
    pack = parse_money(vals["pack"])
    app_fee = pct_to_float(vals["app_fee_pct"])

    rent = parse_money(vals["rent"])
    staff = parse_money(vals["staff"])
    utils = parse_money(vals["utils"])
    mkt = parse_money(vals["mkt"])
    others = parse_money(vals["others"])

    capex = parse_money(vals["capex"])
    dep_years = max(1, int(parse_money(vals["dep_years"], 4)))
    tax_pct = pct_to_float(vals["tax_pct"])

    # Calculate variable costs
    base_cogs = cogs_thb if str(vals["cogs_thb"]).strip() != "" else price * cogs_pct
    var_cup = base_cogs + pack + (price * app_fee)
    contrib = price - var_cup

    # Monthly calculations
    cups_month = cups_day * days
    revenue = price * cups_month
    var_total = var_cup * cups_month
    gp = revenue - var_total
    fixed = rent + staff + utils + mkt + others
    op = gp - fixed
    tax = max(0.0, op) * tax_pct
    net = op - tax

    # Additional metrics
    depr = capex / (dep_years * 12)
    if contrib <= 0:
        bep_day = np.nan
    else:
        bep_day = fixed / contrib / days
    payback = (capex / net) if net > 0 else np.inf

    # Ratios and margins
    gp_margin = gp / revenue if revenue > 0 else 0
    net_margin = net / revenue if revenue > 0 else 0
    roi_annual = (net * 12) / capex if capex > 0 else 0

    return dict(
        price=price, cups_day=cups_day, days=days, revenue=revenue, var_total=var_total,
        gp=gp, fixed=fixed, op=op, tax=tax, net=net, contrib=contrib, bep_day=bep_day,
        payback=payback, var_cup=var_cup, depr=depr, gp_margin=gp_margin,
        net_margin=net_margin, roi_annual=roi_annual
    )


# Calculate all cases
results = {cid: calc_case(st.session_state.cases[cid]) for cid in CASE_IDS}

# Track calculation completion
track_user_action("calculation_completed", {
    "cases": len([r for r in results.values() if r["revenue"] > 0])
})

# ===== ENHANCED KPI DASHBOARD =====
st.markdown("---")

# ===== COST COMPARISON SECTION (ใหม่) =====
st.markdown("## 💰 เปรียบเทียบต้นทุนวัตถุดิบ")
st.markdown(f"""
<div style="background: linear-gradient(135deg, #fff8f0 0%, #fff0e6 100%); border-radius: 16px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid {PRIMARY};">
  <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; text-align: center;">
    <div>
      <div style="font-size: 0.9rem; color: {TEXT_SECONDARY}; margin-bottom: 0.5rem;">วัตถุดิบท้องตลาด</div>
      <div style="font-size: 1.5rem; font-weight: 700; color: #dc2626;">฿35-45</div>
      <div style="font-size: 0.8rem; color: {TEXT_SECONDARY};">ต่อแก้ว</div>
    </div>
    <div style="border-left: 1px solid #e5e5e5; border-right: 1px solid #e5e5e5;">
      <div style="font-size: 0.9rem; color: {TEXT_SECONDARY}; margin-bottom: 0.5rem;">CoffeePortals Premium</div>
      <div style="font-size: 1.5rem; font-weight: 700; color: {SUCCESS};">฿22-28</div>
      <div style="font-size: 0.8rem; color: {SUCCESS}; font-weight: 600;">ประหยัด 25-35%</div>
    </div>
    <div>
      <div style="font-size: 0.9rem; color: {TEXT_SECONDARY}; margin-bottom: 0.5rem;">กำไรเพิ่มขึ้น</div>
      <div style="font-size: 1.5rem; font-weight: 700; color: {PRIMARY};">+฿15-20</div>
      <div style="font-size: 0.8rem; color: {PRIMARY};">ต่อแก้ว</div>
    </div>
  </div>
  <div style="text-align: center; margin-top: 1.5rem;">
    <a href="{PURCHASE_URL}" target="_blank" style="background: {PRIMARY}; color: white; padding: 0.8rem 2rem; border-radius: 25px; text-decoration: none; font-weight: 700; display: inline-block;">
      🛒 สั่งซื้อวัตถุดิบพรีเมียม
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 📊 สรุปผลการวิเคราะห์ (เปรียบเทียบ A/B/C)")

# Main KPIs
kpi_cols = st.columns(4)
kpi_metrics = [
    ("revenue", "💰 รายได้/เดือน", "บาท"),
    ("net", "💎 กำไรสุทธิ", "บาท"),
    ("gp_margin", "📈 อัตรากำไรขั้นต้น", "%"),
    ("payback", "⏰ Payback", "เดือน")
]

for i, (metric, title, unit) in enumerate(kpi_metrics):
    with kpi_cols[i]:
        st.markdown('<div class="kpi">', unsafe_allow_html=True)
        st.markdown(f'<div class="label">{title}</div>', unsafe_allow_html=True)

        for cid in CASE_IDS:
            val = results[cid][metric]
            if metric == "payback":
                val_str = f"{val:.1f}" if val != np.inf else "∞"
                benchmark = get_industry_benchmark("payback_months", val)
            elif metric == "gp_margin":
                val_str = f"{val * 100:.1f}%"
                benchmark = get_industry_benchmark("gross_margin", val)
            else:
                val_str = f"฿{val:,.0f}"
                benchmark = ""

            st.markdown(
                f'<div class="val">{val_str} <span style="font-size:0.7rem;color:{TEXT_SECONDARY};">({cid})</span></div>',
                unsafe_allow_html=True)
            if benchmark:
                st.markdown(f'<div style="font-size:0.7rem;margin-bottom:0.5rem;">{benchmark}</div>',
                            unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ===== DETAILED ANALYSIS FOR ACTIVE CASE =====
active = st.session_state.active_case
R = results[active]

st.markdown("---")
st.markdown(f"## 🎯 การวิเคราะห์เชิงลึก - Case {active}")

# Enhanced metrics row
met_cols = st.columns(3)
with met_cols[0]:
    bep_status = "✅ เกินจุดคุ้มทุน" if R["cups_day"] >= R["bep_day"] else "⚠️ ต่ำกว่าจุดคุ้มทุน"
    st.metric(
        "จุดคุ้มทุน vs ยอดจริง",
        f"{ceil(R['bep_day']) if np.isfinite(R['bep_day']) else 'N/A'} แก้ว/วัน",
        f"{R['cups_day'] - R['bep_day']:.0f} แก้ว" if np.isfinite(R['bep_day']) else "N/A",
        help=bep_status
    )

with met_cols[1]:
    roi_color = "normal" if R["roi_annual"] > 0.15 else "inverse"
    st.metric(
        "ROI ต่อปี",
        f"{R['roi_annual'] * 100:.1f}%",
        "ดีเยี่ยม" if R["roi_annual"] > 0.3 else ("ดี" if R["roi_annual"] > 0.15 else "ต้องปรับปรุง"),
        delta_color=roi_color
    )

with met_cols[2]:
    margin_color = "normal" if R["net_margin"] > 0.1 else "inverse"
    st.metric(
        "อัตรากำไรสุทธิ",
        f"{R['net_margin'] * 100:.1f}%",
        get_industry_benchmark("gross_margin", R["gp_margin"]),
        delta_color=margin_color
    )

# Enhanced Visualizations
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    # Interactive Break-even Gauge
    val = R["cups_day"]
    tgt = float(R["bep_day"]) if np.isfinite(R["bep_day"]) else 0
    max_range = max(1.0, val * 1.5, tgt * 1.5)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=val,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ยอดขาย vs จุดคุ้มทุน (แก้ว/วัน)", 'font': {'size': 16}},
        delta={'reference': tgt, 'increasing': {'color': SUCCESS}, 'decreasing': {'color': DANGER}},
        gauge={
            'axis': {'range': [None, max_range], 'tickwidth': 1, 'tickcolor': TEXT_SECONDARY},
            'bar': {'color': SECONDARY, 'thickness': 0.7},
            'steps': [
                {'range': [0, tgt], 'color': '#ffecec'},
                {'range': [tgt, max_range], 'color': '#ecffec'}
            ],
            'threshold': {
                'line': {'color': DANGER, 'width': 4},
                'thickness': 0.75,
                'value': tgt
            }
        }
    ))

    fig_gauge.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with viz_col2:
    # Enhanced Waterfall Chart
    categories = ["รายได้", "ต้นทุนผันแปร", "ต้นทุนคงที่", "กำไรก่อนภาษี", "ภาษี", "กำไรสุทธิ"]
    values = [R["revenue"], -R["var_total"], -R["fixed"], 0, -R["tax"], 0]
    measures = ["relative", "relative", "relative", "total", "relative", "total"]

    fig_waterfall = go.Figure(go.Waterfall(
        name="20", orientation="v",
        measure=measures,
        x=categories,
        textposition="outside",
        text=[f"฿{v:,.0f}" if v != 0 else f"฿{R['op']:,.0f}" if i == 3 else f"฿{R['net']:,.0f}" for i, v in
              enumerate(values)],
        y=values,
        connector={"line": {"color": TEXT_SECONDARY}},
        increasing={"marker": {"color": PRIMARY}},
        decreasing={"marker": {"color": DANGER}},
        totals={"marker": {"color": SECONDARY}}
    ))

    fig_waterfall.update_layout(
        title="โครงสร้างรายได้และกำไร",
        height=350,
        margin=dict(l=20, r=20, t=40, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

# ===== SCENARIO ANALYSIS =====
st.markdown("### 📈 การวิเคราะห์สถานการณ์แบบจำลอง")

scenario_col1, scenario_col2 = st.columns(2)

with scenario_col1:
    st.markdown("**🎯 Sensitivity Analysis: ยอดขาย vs กำไร**")

    range_input = st.text_input(
        "ช่วงการทดสอบ (แก้ว/วัน)",
        "50-400",
        help="เช่น 50-400 หรือ 100,200,300"
    )

    # Parse range
    if "-" in range_input:
        try:
            lo, hi = map(int, range_input.split("-"))
            test_range = np.linspace(lo, hi, 20)
        except:
            test_range = np.linspace(50, 400, 20)
    else:
        try:
            test_range = [int(x.strip()) for x in range_input.split(",")]
        except:
            test_range = np.linspace(50, 400, 20)

    # Calculate scenarios
    scenario_profits = []
    for cups in test_range:
        temp_case = st.session_state.cases[active].copy()
        temp_case["cups"] = str(cups)
        temp_result = calc_case(temp_case)
        scenario_profits.append(temp_result["net"])

    scenario_df = pd.DataFrame({
        "cups_per_day": test_range,
        "net_profit": scenario_profits
    })

    fig_scenario = px.line(
        scenario_df,
        x="cups_per_day",
        y="net_profit",
        markers=True,
        title="กำไรสุทธิเมื่อยอดขายเปลี่ยน"
    )

    fig_scenario.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="จุดคุ้มทุน")
    fig_scenario.add_vline(x=R["cups_day"], line_dash="dot", line_color=SECONDARY, annotation_text="ปัจจุบัน")

    fig_scenario.update_traces(line=dict(width=3, color=PRIMARY))
    fig_scenario.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_scenario, use_container_width=True)

with scenario_col2:
    st.markdown("**🏪 เปรียบเทียบต้นทุนคงที่**")

    # Cost breakdown pie chart
    cost_categories = ["ค่าเช่า", "พนักงาน", "สาธารณูปโภค", "การตลาด", "อื่นๆ"]
    cost_values = [
        parse_money(st.session_state.cases[active]["rent"]),
        parse_money(st.session_state.cases[active]["staff"]),
        parse_money(st.session_state.cases[active]["utils"]),
        parse_money(st.session_state.cases[active]["mkt"]),
        parse_money(st.session_state.cases[active]["others"])
    ]

    fig_costs = px.pie(
        values=cost_values,
        names=cost_categories,
        title="โครงสร้างต้นทุนคงที่",
        hole=0.4,
        color_discrete_sequence=[PRIMARY, SECONDARY, ACCENT_BLUE, SUCCESS, DANGER]
    )

    fig_costs.update_traces(textposition='inside', textinfo='percent+label')
    fig_costs.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_costs, use_container_width=True)

# ===== ENHANCED INSIGHTS & RECOMMENDATIONS =====
st.markdown("---")
st.markdown("## 🧠 AI Insights & คำแนะนำ")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("### 📋 การวิเคราะห์ปัจจุบัน")

    insights = []
    warnings = []
    recommendations = []

    # Profitability Analysis
    if R["net"] > 0:
        insights.append(f"✅ **กำไรได้** ฿{R['net']:,.0f}/เดือน ({R['net_margin'] * 100:.1f}%)")
    else:
        warnings.append(f"⚠️ **ขาดทุน** ฿{abs(R['net']):,.0f}/เดือน")
        recommendations.append("🎯 เพิ่มยอดขายหรือลดต้นทุน")

    # Break-even Analysis
    if np.isfinite(R["bep_day"]):
        if R["cups_day"] >= R["bep_day"]:
            insights.append(f"✅ **เกินจุดคุ้มทุน** {R['cups_day'] - R['bep_day']:.0f} แก้ว/วัน")
        else:
            warnings.append(f"⚠️ **ต่ำกว่าจุดคุ้มทุน** {R['bep_day'] - R['cups_day']:.0f} แก้ว/วัน")
            recommendations.append(f"🎯 เพิ่มยอดให้ถึง {ceil(R['bep_day'])} แก้ว/วัน")

    # Margin Analysis
    if R["gp_margin"] < 0.5:
        warnings.append(f"⚠️ **กำไรขั้นต้นต่ำ** {R['gp_margin'] * 100:.1f}%")
        recommendations.append("🎯 เปลี่ยนวัตถุดิบพรีเมียม → ลดต้นทุน 25%")
    elif R["gp_margin"] > 0.65:
        insights.append(f"✅ **กำไรขั้นต้นดี** {R['gp_margin'] * 100:.1f}%")

    # Payback Analysis
    if R["payback"] != np.inf:
        if R["payback"] <= 18:
            insights.append(f"✅ **คืนทุนเร็ว** {R['payback']:.1f} เดือน")
        elif R["payback"] <= 36:
            insights.append(f"🔶 **คืนทุนปานกลาง** {R['payback']:.1f} เดือน")
        else:
            warnings.append(f"⚠️ **คืนทุนช้า** {R['payback']:.1f} เดือน")
            recommendations.append("🎯 ลดเงินลงทุนเริ่มต้นหรือเพิ่มกำไร")

    # Display insights
    for insight in insights:
        st.success(insight)

    for warning in warnings:
        st.warning(warning)

with insights_col2:
    st.markdown("### 🚀 คำแนะนำปรับปรุง")

    for rec in recommendations:
        st.info(rec)

    # Additional strategic recommendations
    if R["revenue"] > 0:
        # Cost optimization with premium ingredients
        current_cogs = parse_money(st.session_state.cases[active]["cogs_thb"])
        if current_cogs > 25:
            potential_savings = (current_cogs - 22) * R["cups_day"] * R["days"]
            st.info(f"💰 **เปลี่ยนวัตถุดิบพรีเมียม** → ประหยัด ฿{potential_savings:,.0f}/เดือน")

        # Revenue optimization
        if R["contrib"] < 35:
            st.info("🌟 **วัตถุดิบคุณภาพสูง** → เพิ่มราคาได้ 10-15% ลูกค้ายอมจ่าย")

        # Product mix
        if R["gp_margin"] < 0.6:
            st.info("☕ **เมนูพิเศษจากวัตถุดิบพรีเมียม** → เพิ่มกำไรต่อแก้ว")

    # CTA for premium ingredients
    st.markdown(f"""
    <div style="background: {PRIMARY}; color: white; padding: 1rem; border-radius: 12px; text-align: center; margin-top: 1rem;">
        <div style="font-weight: 700; margin-bottom: 0.5rem;">🎯 ต้องการลดต้นทุนและเพิ่มคุณภาพ?</div>
        <a href="{PURCHASE_URL}" target="_blank" style="color: white; background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; text-decoration: none; font-weight: 600;">
            ดูวัตถุดิบพรีเมียม →
        </a>
    </div>
    """, unsafe_allow_html=True)

# ===== PRODUCT SHOWCASE =====
st.markdown("---")
st.markdown("## 🌟 วัตถุดิบพรีเมียม - CoffeePortals")

showcase_cols = st.columns(3)
products = [
    {
        "name": "เมล็ดกาแฟคั่วพรีเมียม",
        "price": "450-680 บาท/กก",
        "saving": "ประหยัด 25%",
        "desc": "คั่วสด ส่งตรงจากโรงงาน"
    },
    {
        "name": "นมสำหรับทำกาแฟ",
        "price": "45-65 บาท/ลิตร",
        "saving": "ประหยัด 20%",
        "desc": "คุณภาพ UHT นำเข้า"
    },
    {
        "name": "วัตถุดิบเซ็ตครบ",
        "price": "8,500-12,000 บาท",
        "saving": "ประหยัด 30%",
        "desc": "ชุดสำหรับร้านใหม่"
    }
]

for i, product in enumerate(products):
    with showcase_cols[i]:
        st.markdown(f"""
        <div style="background: white; border: 1px solid #e5e5e5; border-radius: 12px; padding: 1rem; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="color: {PRIMARY}; margin-bottom: 0.5rem;">{product['name']}</h4>
                <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">{product['price']}</div>
                <div style="color: {SUCCESS}; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">{product['saving']}</div>
                <div style="color: {TEXT_SECONDARY}; font-size: 0.85rem;">{product['desc']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align: center; margin: 2rem 0;">
    <a href="{PURCHASE_URL}" target="_blank" style="background: {PRIMARY}; color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: 700; font-size: 1.1rem; display: inline-block;">
        🛒 ดูสินค้าทั้งหมดและสั่งซื้อ
    </a>
    <div style="margin-top: 0.5rem; font-size: 0.9rem; color: {TEXT_SECONDARY};">
        🚚 ส่งฟรี! สั่งขั้นต่ำ 3,000 บาท | 📞 รับปรึกษาฟรี โทร 02-xxx-xxxx
    </div>
</div>
""", unsafe_allow_html=True)

# ===== PRODUCT SALES FUNNEL =====
if R["net"] > 0 and not st.session_state.get("product_viewed", False):
    st.markdown("---")

    # Calculate potential savings
    current_cogs = parse_money(st.session_state.cases[active]["cogs_thb"])
    premium_cogs = 25  # Our premium ingredient cost
    monthly_savings = max(0, (current_cogs - premium_cogs) * R["cups_day"] * R["days"])

    if monthly_savings > 1000:  # Show offer if significant savings
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {SUCCESS} 0%, {PRIMARY} 100%); 
                    color: white; border-radius: 20px; padding: 2rem; text-align: center; margin: 2rem 0;">
            <h3 style="margin-bottom: 1rem;">🎉 คุณสามารถประหยัดได้!</h3>
            <div style="font-size: 1.2rem; margin-bottom: 1rem;">
                <strong>฿{monthly_savings:,.0f}/เดือน</strong> ด้วยวัตถุดิบพรีเมียม
            </div>
            <div style="margin-bottom: 1.5rem; opacity: 0.9;">
                • คุณภาพสูงกว่า รสชาติดีกว่า<br>
                • ราคาโรงงาน ไม่ผ่านตัวกลาง<br>
                • ส่งตรงถึงร้าน บริการครบจบ
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛒 ดูสินค้าและราคา", type="primary", use_container_width=True):
                track_user_action("product_interest", {"potential_savings": monthly_savings})
                st.session_state.product_viewed = True
                # Redirect to purchase page
                st.markdown(f'<meta http-equiv="refresh" content="0;url={PURCHASE_URL}">', unsafe_allow_html=True)
                st.success("🔄 กำลังเปิดหน้าสั่งซื้อ...")

    else:
        st.info(f"💡 ดูวัตถุดิบพรีเมียมที่ [CoffeePortals.com]({PURCHASE_URL}) เพื่อเพิ่มคุณภาพและลดต้นทุน")

# ===== EXPORT & PRODUCT CATALOG =====
st.markdown("---")
st.markdown("### 📤 ผลลัพธ์และแคตตาล็อกสินค้า")

export_col1, export_col2, export_col3 = st.columns(3)

# ===== FOOTER WITH SOCIAL PROOF =====
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown(f"""
    **🛒 สั่งซื้อสินค้า**
    - 🌐 [ดูแคตตาล็อกเต็ม]({PURCHASE_URL})
    - 📞 ไลน์ไอดี: rathnagorn
    - 📧 อีเมล์ Coffeeportals@gmail.com
    """)

with footer_col2:
    st.markdown("""
    **☕ ผลิตภัณฑ์ยอดนิยม**
    - ✅ เมล็ดกาแฟคั่วพรีเมียม
    - ✅ ไซรัปสำหรับทำกาแฟ
    - ✅ วัตถุดิบครบเซ็ต
    """)

with footer_col3:
    st.markdown(f"""
    **📚 ข้อมูลเพิ่มเติม**
    - 📺 [วิดีโอแนะนำ]({YOUTUBE_URL})
    - 📊 เครื่องมือคำนวณ (หน้านี้)
    """)

st.markdown(f"""
<div style="text-align: center; padding: 2rem 0; color: {TEXT_SECONDARY}; border-top: 1px solid #e2e8f0; margin-top: 2rem;">
    <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">
        Made with ❤️ by <a href="{COFFEE_URL}" target="_blank" style="color: {PRIMARY}; font-weight: 600;">CoffeePortals Team</a>
    </div>
    <div style="font-size: 0.8rem;">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Version 1.0 Started
    </div>
</div>
""", unsafe_allow_html=True)