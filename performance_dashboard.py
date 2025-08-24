import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from math import ceil
from datetime import datetime
import re, html
from urllib.parse import urlencode

# ===== THEME =====
PRIMARY, SECONDARY, SUCCESS, DANGER = "#FABC3F", "#E85C0D", "#C7253E", "#821131"
BACKGROUND, CARD_BG = "#fffaf5", "#ffffff"
TEXT_PRIMARY, TEXT_SECONDARY = "#1e1e1e", "#5c5c5c"
COFFEE_URL  = "https://www.coffeeportals.com/"
COFFEE_LOGO = "https://coffeeportals.com/wp-content/uploads/2019/04/coffeeportals-1.png"
YOUTUBE_URL = "https://www.youtube.com/watch?v=aclyENOXMYU"

st.set_page_config(
    page_title="เจ๊งในกระดาษ ☕️ – Coffee Business",
    page_icon="☕️", layout="wide",
    initial_sidebar_state="collapsed"  # ซ่อน sidebar ไปเลย (เราใช้ textbox บนหน้า)
)

# ===== CSS =====
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
  .stApp {{ background:{BACKGROUND}; }}
  .main .block-container {{ padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1320px; }}
  .header {{
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
    color: #fff; border-radius: 16px; padding: 1.1rem 1.2rem; margin-bottom: .8rem;
    box-shadow: 0 10px 24px rgba(232,92,13,.25);
  }}
  .header-row {{ display:flex; align-items:center; justify-content:space-between; gap:.5rem; }}
  .title {{ font-size: 1.8rem; font-weight: 800; margin: 0; }}
  .sub  {{ font-size: .98rem; opacity: .95; }}
  .brand {{ display:flex; align-items:center; gap:.6rem; background: rgba(255,255,255,.15); padding:.42rem .7rem; border-radius:999px;
            text-decoration:none; color:#fff; border:1px solid rgba(255,255,255,.35); }}
  .brand img {{ height:30px; width:auto; border-radius:6px; background:#fff; padding:2px; }}

  .card {{ background:{CARD_BG}; border:1px solid rgba(0,0,0,.06); border-radius:16px; padding:1rem 1.2rem; box-shadow:0 4px 16px rgba(0,0,0,.06); }}
  .chart-container {{ background:{CARD_BG}; border:1px solid rgba(0,0,0,.06); border-radius:16px; padding:1rem 1.2rem; margin:.8rem 0; box-shadow:0 4px 16px rgba(0,0,0,.06); }}
  .chart-title {{ font-weight:700; color:{TEXT_PRIMARY}; margin-bottom:.65rem; display:flex; align-items:center; gap:.5rem; }}

  .kpi {{ background:{CARD_BG}; border:1px solid rgba(0,0,0,.05); border-radius:14px; padding:.9rem; }}
  .kpi .label {{ color:{TEXT_SECONDARY}; font-size:.85rem; }}
  .kpi .val {{ font-size:1.6rem; font-weight:800; color:{TEXT_PRIMARY}; }}

  .note {{ color:{TEXT_SECONDARY}; font-size:.85rem; }}

  .tt{{display:inline-flex;align-items:center;gap:.3rem}}
  .tt .tt-i{{ display:inline-block;width:18px;height:18px;line-height:18px;text-align:center;border-radius:50%;font-size:.75rem;font-weight:700;background:#fff3cf;color:#8a5a00;border:1px solid #f3d480; }}
  .tt .tt-box{{ visibility:hidden; opacity:0; transition:.15s ease; position:absolute; z-index:9999; background:#111827; color:#f9fafb; border-radius:10px; padding:.55rem .7rem; max-width:360px; font-size:.85rem; line-height:1.35; border:1px solid #334155; box-shadow:0 8px 24px rgba(0,0,0,.18) }}
  .tt:hover .tt-box{{ visibility:visible; opacity:1; }}
  .tt.top .tt-box{{ transform:translate(-10%, -8px); bottom:100%; }}
  .tt-wrap{{ position:relative; display:inline-block; }}

  #MainMenu {{visibility:hidden;}} footer {{visibility:hidden;}} header {{visibility:hidden;}}
</style>
""", unsafe_allow_html=True)

def TT(text):  # tooltip
    return f'<span class="tt top tt-wrap"><span class="tt-i">i</span><span class="tt-box">{html.escape(text)}</span></span>'

# ===== HEADER =====
st.markdown(f"""
<div class="header">
  <div class="header-row">
    <div>
      <div class="title">☕️ เจ๊งในกระดาษ – วิเคราะห์ธุรกิจร้านกาแฟ</div>
      <div class="sub">กรอกสมมติฐานผ่าน <b>Textbox</b> แล้วดูจุดคุ้มทุน/กำไร/แพย์แบ็คแบบเรียลไทม์ · อ้างอิงแนวคิดจาก <a href="{YOUTUBE_URL}" target="_blank" style="color:#fff;text-decoration:underline;">YouTube</a></div>
    </div>
    <a class="brand" href="{COFFEE_URL}" target="_blank" rel="noopener">
      <img src="{COFFEE_LOGO}" alt="CoffeePortals"/><span><b>coffeeportals.com</b></span>
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

# ===== Utils =====
def parse_money(s: str, default: float = 0.0) -> float:
    if s is None: return default
    s = str(s).strip()
    if s == "": return default
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg, s = True, s[1:-1]
    s = s.replace("฿","").replace(",","").replace(" ","")
    if s.endswith("%"):
        try:
            v = float(s[:-1]) / 100.0
            return -v if neg else v
        except: return default
    try:
        v = float(re.sub(r"[^0-9.\-]", "", s))
        return -v if neg else v
    except:
        return default

def pct_to_float(txt: str, default=0.0) -> float:
    v = parse_money(txt, default)
    return v if v <= 1 else v/100.0

# Defaults (string)
DEFAULTS = {
    "price":"75","cups":"180","days":"26",
    "cogs_thb":"28","cogs_pct":"0","pack":"2","app_fee_pct":"0",
    "rent":"35000","staff":"70000","utils":"12000","mkt":"8000","others":"5000",
    "capex":"280000","dep_years":"4","tax_pct":"0"
}

FIELDS = ["price","cups","days","cogs_thb","cogs_pct","pack","app_fee_pct",
          "rent","staff","utils","mkt","others","capex","dep_years","tax_pct"]

CASE_IDS = ["A","B","C"]

# ===== Permalink helpers =====
def get_qp():
    try:
        return dict(st.query_params)
    except Exception:
        return st.experimental_get_query_params()

def set_qp(d: dict):
    # Streamlit >=1.33
    try:
        st.query_params.clear()
        st.query_params.update(d)
    except Exception:
        st.experimental_set_query_params(**d)

def load_cases_from_qp() -> dict:
    qp = get_qp()
    cases = {}
    for c in CASE_IDS:
        obj = {}
        any_present = False
        for f in FIELDS:
            key = f"{f}{c}"
            if key in qp:
                v = qp[key] if isinstance(qp[key], str) else qp[key][0]
                obj[f] = v
                any_present = True
            else:
                obj[f] = DEFAULTS[f]
        if any_present:
            cases[c] = obj
    return cases

def build_qp_from_cases(cases: dict, active: str) -> dict:
    qp = {}
    for c in cases:
        for f in FIELDS:
            qp[f"{f}{c}"] = str(cases[c].get(f, DEFAULTS[f]))
    qp["active"] = active
    return qp

# ===== Session init =====
if "cases" not in st.session_state:
    st.session_state.cases = {cid: DEFAULTS.copy() for cid in CASE_IDS}
    # override from permalink if present
    loaded = load_cases_from_qp()
    st.session_state.cases.update(loaded)
if "active_case" not in st.session_state:
    act = get_qp().get("active", "")
    st.session_state.active_case = act if act in CASE_IDS else "A"

# ===== INPUT PANEL (Textbox on page) =====
st.markdown("## 🧮 กรอกสมมติฐาน (Textbox เท่านั้น)")

tabs = st.tabs([f"Case {cid}" for cid in CASE_IDS])

# quick copy buttons row
ccol1, ccol2, ccol3 = st.columns([1,1,2])
with ccol1:
    if st.button("คัดลอก A → B"):
        st.session_state.cases["B"] = st.session_state.cases["A"].copy()
with ccol2:
    if st.button("คัดลอก B → C"):
        st.session_state.cases["C"] = st.session_state.cases["B"].copy()
with ccol3:
    st.session_state.active_case = st.radio("เลือกเคสสำหรับกราฟละเอียด", CASE_IDS, horizontal=True, index=CASE_IDS.index(st.session_state.active_case))

def text_row(left_col, right_col, label, key_base, cid, default):
    with left_col:
        st.session_state.cases[cid][key_base] = st.text_input(
            f"{label}", value=st.session_state.cases[cid].get(key_base, default), key=f"{key_base}_{cid}"
        )

for i, cid in enumerate(CASE_IDS):
    with tabs[i]:
        col1, col2, col3, col4 = st.columns(4)
        st.markdown('<div class="note">พิมพ์ได้ทั้ง "75000", "฿75,000", "40%" หรือ "0.4"</div>', unsafe_allow_html=True)
        text_row(col1, col2, "ราคา/แก้ว (THB)",           "price", cid, DEFAULTS["price"])
        text_row(col2, col3, "ยอดขาย (แก้ว/วัน)",         "cups", cid, DEFAULTS["cups"])
        text_row(col3, col4, "วันเปิด/เดือน",             "days", cid, DEFAULTS["days"])

        st.divider()
        st.markdown("**ต้นทุนผันแปร/แก้ว**")
        text_row(col1, col2, "วัตถุดิบ/แก้ว (THB) – ถ้าว่างใช้ %", "cogs_thb", cid, DEFAULTS["cogs_thb"])
        text_row(col2, col3, "% วัตถุดิบจากราคา",         "cogs_pct", cid, DEFAULTS["cogs_pct"])
        text_row(col3, col4, "บรรจุภัณฑ์/แก้ว (THB)",      "pack", cid, DEFAULTS["pack"])
        text_row(col4, col1, "% ค่าช่องทางจากยอดขาย",      "app_fee_pct", cid, DEFAULTS["app_fee_pct"])

        st.divider()
        st.markdown("**ต้นทุนคงที่รายเดือน**")
        text_row(col1, col2, "ค่าเช่า",                 "rent", cid, DEFAULTS["rent"])
        text_row(col2, col3, "เงินเดือนพนักงานรวม",      "staff", cid, DEFAULTS["staff"])
        text_row(col3, col4, "ค่าสาธารณูปโภค",           "utils", cid, DEFAULTS["utils"])
        text_row(col4, col1, "งบการตลาด",                "mkt", cid, DEFAULTS["mkt"])
        text_row(col1, col2, "อื่น ๆ",                   "others", cid, DEFAULTS["others"])

        st.divider()
        st.markdown("**การลงทุน/ภาษี**")
        text_row(col2, col3, "เงินลงทุนตั้งต้น (CAPEX)", "capex", cid, DEFAULTS["capex"])
        text_row(col3, col4, "อายุการใช้งาน (ปี)",       "dep_years", cid, DEFAULTS["dep_years"])
        text_row(col4, col1, "% ภาษีจากกำไรสุทธิ",        "tax_pct", cid, DEFAULTS["tax_pct"])

# ===== Permalink controls =====
with st.expander("🔗 Permalink (เซฟค่าลง URL)"):
    if st.button("บันทึกค่าปัจจุบันทั้งหมดลง URL", type="primary"):
        qp = build_qp_from_cases(st.session_state.cases, st.session_state.active_case)
        set_qp(qp)
        # โชว์ query string ให้ก็อปได้ทันที
    qp_str = "?" + urlencode(build_qp_from_cases(st.session_state.cases, st.session_state.active_case))
    st.text_input("คัดลอกลิงก์ (ปรับเปลี่ยนจะอัปเดตใหม่ได้)", qp_str)

# ===== Core calculator =====
def calc_case(vals: dict) -> dict:
    price      = parse_money(vals["price"])
    cups_day   = parse_money(vals["cups"])
    days       = max(1, int(parse_money(vals["days"], 26)))

    cogs_thb   = parse_money(vals["cogs_thb"])
    cogs_pct   = pct_to_float(vals["cogs_pct"])
    pack       = parse_money(vals["pack"])
    app_fee    = pct_to_float(vals["app_fee_pct"])

    rent   = parse_money(vals["rent"])
    staff  = parse_money(vals["staff"])
    utils  = parse_money(vals["utils"])
    mkt    = parse_money(vals["mkt"])
    others = parse_money(vals["others"])

    capex     = parse_money(vals["capex"])
    dep_years = max(1, int(parse_money(vals["dep_years"], 4)))
    tax_pct   = pct_to_float(vals["tax_pct"])

    base_cogs = cogs_thb if str(vals["cogs_thb"]).strip() != "" else price * cogs_pct
    var_cup = base_cogs + pack + (price * app_fee)
    contrib = price - var_cup

    cups_month = cups_day * days
    revenue = price * cups_month
    var_total = var_cup * cups_month
    gp = revenue - var_total
    fixed = rent + staff + utils + mkt + others
    op = gp - fixed
    tax = max(0.0, op) * tax_pct
    net = op - tax
    depr = capex / (dep_years * 12)
    if contrib <= 0:
        bep_day = np.nan
    else:
        bep_day = fixed / contrib / days
    payback = (capex / net) if net > 0 else np.inf

    return dict(
        price=price, cups_day=cups_day, days=days, revenue=revenue, var_total=var_total, gp=gp,
        fixed=fixed, op=op, tax=tax, net=net, contrib=contrib, bep_day=bep_day, payback=payback,
        var_cup=var_cup, depr=depr
    )

# คำนวณทุกเคส
results = {cid: calc_case(st.session_state.cases[cid]) for cid in CASE_IDS}

# ===== KPI compare =====
st.markdown("## 📊 ตัวชี้วัดหลัก (เปรียบเทียบ A/B/C)")
def kpi_block(col, title, values_fmt):
    with col:
        st.markdown('<div class="kpi">', unsafe_allow_html=True)
        st.markdown(f'<div class="label">{title}</div>', unsafe_allow_html=True)
        st.markdown(values_fmt, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

cols = st.columns(3)
for i, metric in enumerate(["revenue","gp","fixed"]):
    col = cols[i]
    html_vals = " | ".join([f"<span style='font-weight:800;color:{TEXT_PRIMARY}'>฿{results[c]['%s'%metric]:,.0f}</span> <span class='note'>({c})</span>" for c in CASE_IDS])
    kpi_block(col, {"revenue":"รายได้/เดือน","gp":"กำไรขั้นต้น","fixed":"ต้นทุนคงที่/เดือน"}[metric], html_vals)

cols = st.columns(3)
kpi_block(cols[0], "กำไรสุทธิ/เดือน", " | ".join([f"<b>฿{results[c]['net']:,.0f}</b> <span class='note'>({c})</span>" for c in CASE_IDS]))
kpi_block(cols[1], "BEP แก้ว/วัน", " | ".join([f"<b>{'-' if np.isnan(results[c]['bep_day']) else ceil(results[c]['bep_day']):,}</b> <span class='note'>({c})</span>" for c in CASE_IDS]))
kpi_block(cols[2], "Payback (เดือน)", " | ".join([f"<b>{'∞' if results[c]['payback']==np.inf else f'{results[c]['payback']:.1f}'}</b> <span class='note'>({c})</span>" for c in CASE_IDS]))

# ===== ACTIVE CASE (รายละเอียด) =====
active = st.session_state.active_case
R = results[active]

st.markdown(f"### 🔎 รายละเอียดของ Case {active}")

# Gauge BEP
g1, g2 = st.columns([2,1])
with g1:
    val = R["cups_day"]
    tgt = float(R["bep_day"]) if np.isfinite(R["bep_day"]) else 0
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=val, title={'text': "แก้ว/วัน (Actual vs BEP)"},
        delta={'reference': tgt, 'increasing': {'color': SUCCESS}, 'decreasing': {'color': DANGER}},
        gauge={
            'axis': {'range': [0, max(1.0, val*1.5, tgt*1.5)], 'tickwidth': 1, 'tickcolor': '#777'},
            'bar': {'color': SECONDARY},
            'steps': [{'range':[0,tgt],'color':'#fff3cf'},{'range':[tgt,max(1.0,val*1.5,tgt*1.5)],'color':'#ffe39a'}],
            'threshold': {'line': {'color': DANGER, 'width': 4}, 'value': tgt}
        }
    ))
    fig.update_layout(height=300, margin=dict(l=10,r=10,t=20,b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
with g2:
    text_bep = "-" if np.isnan(R["bep_day"]) else f"{ceil(R['bep_day']):,} แก้ว/วัน"
    st.markdown(f"""
    <div class="card">
      <div class="chart-title">สรุป BEP (Case {active})</div>
      <div class="note">BEP = Fixed ÷ (ราคา − ต้นทุนผันแปร/แก้ว) ÷ วันเปิด/เดือน</div>
      <h3 style="margin:.4rem 0 0 0;">{text_bep}</h3>
      <div class="note">Contribution/แก้ว: ฿{R['contrib']:,.0f}</div>
      <div class="note">วันเปิด/เดือน: {int(results[active]['days'])} วัน</div>
    </div>
    """, unsafe_allow_html=True)

# Waterfall (รายได้→ต้นทุน→กำไร)
st.markdown("### 💧 โครงสร้างรายได้และกำไร (Waterfall)")
wf = pd.DataFrame({"label":["รายได้","ต้นทุนผันแปร","ต้นทุนคงที่","กำไรสุทธิ"],
                   "value":[R["revenue"], -R["var_total"], -R["fixed"], R["net"]]})
fig_wf = go.Figure(go.Waterfall(
    orientation="v", measure=["relative","relative","relative","total"], x=wf["label"],
    text=[f"฿{v:,.0f}" for v in wf["value"]], y=wf["value"],
    connector={"line":{"color":"#888"}}, increasing={"marker":{"color":PRIMARY}},
    decreasing={"marker":{"color":DANGER}}, totals={"marker":{"color":SECONDARY}}
))
fig_wf.update_layout(height=360, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_wf, use_container_width=True)

# Sensitivity: cups/day → net profit
st.markdown("### 📈 Sensitivity: กำไรสุทธิเมื่อยอดแก้ว/วันเปลี่ยน (Case " + active + ")")
range_txt = st.text_input("ช่วงแก้ว/วัน (เช่น 80-300 หรือ 120,240)", "80-300", key="sens_range")
def parse_range(txt, default=(50, 300)):
    txt = txt.strip()
    m = re.match(r"^\s*(\d+)\s*[-,]\s*(\d+)\s*$", txt)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return (a,b) if a <= b else (b,a)
    return default
lo, hi = parse_range(range_txt)
xs = np.linspace(lo, hi, 25)
ys = []
for x in xs:
    rev = results[active]["price"] * x * results[active]["days"]
    var = results[active]["var_cup"] * x * results[active]["days"]
    gp  = rev - var
    op  = gp - results[active]["fixed"]
    tax = max(0.0, op) * (parse_money(st.session_state.cases[active]["tax_pct"]) if "%" in st.session_state.cases[active]["tax_pct"] else pct_to_float(st.session_state.cases[active]["tax_pct"]))
    ys.append(op - tax)
df_sens = pd.DataFrame({"cups_per_day": xs, "net_profit": ys})
fig_s = px.line(df_sens, x="cups_per_day", y="net_profit", markers=True)
fig_s.update_traces(line=dict(width=3))
fig_s.add_vline(x=results[active]["cups_day"], line_dash="dash", line_color=SECONDARY, annotation_text="Actual")
if np.isfinite(results[active]["bep_day"]):
    fig_s.add_vline(x=results[active]["bep_day"], line_dash="dot", line_color=DANGER, annotation_text="BEP")
fig_s.update_layout(height=360, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_s, use_container_width=True)

# Pie: fixed breakdown
st.markdown("### 🧾 Breakdown ต้นทุนคงที่ (Case " + active + ")")
vals = st.session_state.cases[active]
fixed_df = pd.DataFrame({
    "รายการ":["ค่าเช่า","พนักงาน","สาธารณูปโภค","มาร์เก็ตติ้ง","อื่น ๆ"],
    "มูลค่า":[parse_money(vals["rent"]), parse_money(vals["staff"]), parse_money(vals["utils"]), parse_money(vals["mkt"]), parse_money(vals["others"])]
})
fig_p = px.pie(fixed_df, names="รายการ", values="มูลค่า", hole=.45)
fig_p.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10))
st.plotly_chart(fig_p, use_container_width=True)

# Insights
st.markdown("## 🧠 อินไซต์อัตโนมัติ")
ins = []
gm_rate = (R["gp"]/R["revenue"]) if R["revenue"]>0 else 0
if gm_rate < 0.55:
    ins.append("✅ GM ต่ำกว่า 55% — ลองลดวัตถุดิบ/แพ็กเกจจิ้ง หรือตั้งราคาให้เหมาะกว่าเดิม")
if np.isfinite(R["bep_day"]) and R["cups_day"] < R["bep_day"]:
    ins.append(f"⚠️ ยอดแก้ว/วันต่ำกว่า BEP ~ {ceil(R['bep_day']):,} แก้ว/วัน — เพิ่มยอดเฉลี่ย/อัปเซลล์/ปรับราคา")
if R["payback"] != np.inf and R["payback"] > 24:
    ins.append(f"ℹ️ ระยะคืนทุน ~ {R['payback']:.1f} เดือน (ค่อนข้างยาว) — ทบทวน CAPEX หรือผลักดันยอด")
if not ins:
    st.success("ภาพรวมดีมาก 🎉 โครงสร้างต้นทุน/ยอดขายสมเหตุสมผล")
else:
    for x in ins: st.markdown(f"- {x}")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;color:{TEXT_SECONDARY};padding:.6rem 0;">
  <div style="font-size:.9rem;">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
  <div style="font-size:.85rem;margin-top:.35rem;">© <a href="{COFFEE_URL}" target="_blank" rel="noopener">coffeeportals.com</a></div>
</div>
""", unsafe_allow_html=True)
