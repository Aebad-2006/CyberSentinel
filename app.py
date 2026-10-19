"""
CyberSentinel v3.0
Enterprise-Grade Web & API Security Posture Auditor
"""

import json
import socket
import ssl
import datetime
from urllib.parse import urlparse

import requests
import streamlit as st
import urllib3

# Disable insecure request warnings for cleaner terminal output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --------------------------------------------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="CyberSentinel v3.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------------------
# CUSTOM CSS - STRICTLY PROFESSIONAL ENTERPRISE DARK THEME
# --------------------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* ---------- Base & Typography ---------- */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .stApp {
        background-color: #0B0F19;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }

    h1, h2, h3, h4 { color: #FFFFFF !important; font-weight: 600; letter-spacing: -0.01em; }
    p, span, div { color: #94A3B8; }

    /* ---------- Brand Header ---------- */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 16px;
        padding-bottom: 20px;
        border-bottom: 1px solid #1E293B;
        margin-bottom: 30px;
    }
    .brand-logo {
        width: 48px; height: 48px;
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px;
    }
    .brand-title {
        font-size: 24px; font-weight: 700; color: #FFFFFF; line-height: 1.2;
    }
    .brand-title span { color: #00F0FF; font-weight: 800; }
    .brand-sub {
        font-size: 12px; color: #64748B; text-transform: uppercase; 
        letter-spacing: 0.1em; font-weight: 600; margin-top: 4px;
    }

    /* ---------- Text Input ---------- */
    .stTextInput > div > div > input {
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00F0FF !important;
        box-shadow: 0 0 0 1px #00F0FF !important;
    }
    .stTextInput label { 
        color: #94A3B8 !important; font-size: 12px !important; 
        font-weight: 600 !important; text-transform: uppercase !important; 
        letter-spacing: 0.05em !important;
    }

    /* ---------- Primary Button (FIXED & PROFESSIONAL) ---------- */
    div.stButton > button {
        background-color: #00F0FF !important;
        color: #0B0F19 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 0.05em !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        width: 100%;
        transition: all 0.2s ease !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2) !important;
    }
    div.stButton > button:hover {
        background-color: #00D8E6 !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4) !important;
        transform: translateY(-1px);
        color: #0B0F19 !important;
    }
    div.stButton > button:active { transform: translateY(0); }

    /* ---------- Download Buttons ---------- */
    div.stDownloadButton > button {
        background-color: #1E293B !important;
        color: #E2E8F0 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 10px 16px !important;
        width: 100%;
        transition: all 0.2s ease !important;
    }
    div.stDownloadButton > button:hover {
        border-color: #00F0FF !important;
        color: #00F0FF !important;
    }

    /* ---------- Metric Cards ---------- */
    .metric-card {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        min-height: 140px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-label {
        font-size: 11px; color: #64748B; font-weight: 600; 
        text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px; font-weight: 700; color: #F8FAFC; line-height: 1.2;
    }
    .metric-value-sm { font-size: 20px; }
    .metric-sub { 
        font-size: 12px; color: #64748B; margin-top: 8px; 
        font-family: 'Inter', sans-serif;
    }

    /* ---------- Badges ---------- */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.05em;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-pass { background: rgba(0, 255, 102, 0.1); color: #00FF66; border: 1px solid rgba(0, 255, 102, 0.2); }
    .badge-fail { background: rgba(255, 77, 106, 0.1); color: #FF4D6A; border: 1px solid rgba(255, 77, 106, 0.2); }
    .badge-warn { background: rgba(255, 176, 32, 0.1); color: #FFB020; border: 1px solid rgba(255, 176, 32, 0.2); }
    .badge-info { background: rgba(0, 240, 255, 0.1); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.2); }

    /* ---------- Grade Box ---------- */
    .grade-box {
        display: inline-flex; align-items: center; justify-content: center;
        width: 56px; height: 56px; border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px; font-weight: 700;
    }

    /* ---------- Header Audit Rows ---------- */
    .hdr-row {
        display: flex; align-items: center; justify-content: space-between;
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-left: 3px solid #00F0FF;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .hdr-name {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px; font-weight: 600; color: #F8FAFC;
    }
    .hdr-detail {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px; color: #64748B; margin-top: 4px; word-break: break-all;
    }

    /* ---------- Section Titles ---------- */
    .section-title {
        font-size: 12px; color: #94A3B8; text-transform: uppercase;
        letter-spacing: 0.1em; font-weight: 700;
        margin: 24px 0 16px 0; padding-bottom: 8px; border-bottom: 1px solid #1E293B;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background: transparent; border-bottom: 1px solid #1E293B;
    }
    .stTabs [data-baseweb="tab"] {
        background: #0F172A; border: 1px solid #1E293B;
        border-bottom: none; border-radius: 6px 6px 0 0;
        color: #94A3B8 !important; font-weight: 600; font-size: 13px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: #0B0F19 !important; color: #00F0FF !important;
        border-color: #00F0FF !important; border-bottom-color: #0B0F19 !important;
    }
    
    /* ---------- Code Blocks ---------- */
    .stCode, pre, code {
        background-color: #0F172A !important; color: #00FF66 !important;
        border: 1px solid #1E293B !important; border-radius: 8px !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------------------
# CONFIGURATION & CONSTANTS
# --------------------------------------------------------------------------------------
SECURITY_HEADERS = {
    "Strict-Transport-Security": {"description": "Forces HTTPS.", "weight": 20},
    "Content-Security-Policy": {"description": "Mitigates XSS.", "weight": 25},
    "X-Frame-Options": {"description": "Prevents Clickjacking.", "weight": 15},
    "X-Content-Type-Options": {"description": "Blocks MIME-sniffing.", "weight": 10},
    "Referrer-Policy": {"description": "Controls referrer leakage.", "weight": 10},
}

WAF_SIGNATURES = {
    "Cloudflare": ["cloudflare", "__cfduid", "cf-ray", "cf-cache-status", "server: cloudflare"],
    "Akamai": ["akamai", "akamai-ghost", "akamaighost", "x-akamai"],
    "AWS WAF": ["awswaf", "x-amzn-waf", "aws-waf", "x-amz-cf-id"],
    "Imperva": ["imperva", "incapsula", "x-iinfo", "visid_incap"],
    "Sucuri": ["sucuri", "x-sucuri"],
    "F5 BIG-IP": ["big-ip", "bigip", "f5-"],
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CyberSentinel/3.0"
REQUEST_TIMEOUT = 15

# --------------------------------------------------------------------------------------
# HELPER: NORMALIZE TARGET URL
# --------------------------------------------------------------------------------------
def normalize_target(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    if "#" in raw:
        raw = raw.split("#")[0]
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    return raw


# --------------------------------------------------------------------------------------
# CORE AUDIT ENGINE
# --------------------------------------------------------------------------------------
def perform_audit(target_url: str) -> dict:
    result = {
        "target": target_url,
        "audit_timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "reachable": False,
        "error": None,
        "http": {"status_code": None, "reason": None, "server": None, "elapsed_ms": None},
        "headers_present": {},
        "headers_audit": {},
        "tls": {"valid": False, "issuer": None, "subject": None, "not_before": None, "not_after": None, "days_remaining": None, "protocol": None, "cipher": None, "error": None},
        "waf": {"detected": "None Identified", "evidence": []},
        "cors": {"acao": None, "acac": None, "wildcard": False, "risk": "UNKNOWN", "details": []},
        "score": 0, "grade": "F", "risk_surface": {},
    }

    parsed = urlparse(target_url)
    hostname = parsed.hostname
    if not hostname:
        result["error"] = "Unable to parse hostname."
        return result

    # 1. HTTP REQUEST
    response = None
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT, "Accept": "*/*"})
        response = session.get(target_url, timeout=REQUEST_TIMEOUT, allow_redirects=True, verify=False)
        result["reachable"] = True
        result["http"]["status_code"] = response.status_code
        result["http"]["reason"] = response.reason
        result["http"]["elapsed_ms"] = int(response.elapsed.total_seconds() * 1000)
    except Exception as exc:
        result["error"] = f"Connection failure: {str(exc)}"

    # 2. SECURITY HEADERS
    headers = {}
    if response is not None:
        headers = {k.lower(): v for k, v in response.headers.items()}
        result["http"]["server"] = headers.get("server", "Not Disclosed")

    total_weight = 0
    earned_weight = 0
    for header_name, meta in SECURITY_HEADERS.items():
        value = headers.get(header_name.lower())
        present = value is not None and str(value).strip() != ""
        result["headers_audit"][header_name] = {
            "present": present,
            "value": value if present else None,
            "description": meta["description"],
        }
        if present: result["headers_present"][header_name] = value
        total_weight += meta["weight"]
        if present: earned_weight += meta["weight"]

    header_score = (earned_weight / total_weight) * 100 if total_weight else 0

    # 3. TLS / SSL INSPECTION
    port = parsed.port if parsed.port else (443 if parsed.scheme == "https" else 80)
    tls_score = 0
    
    if parsed.scheme == "https" or port == 443:
        try:
            context = ssl.create_default_context()
            try:
                with socket.create_connection((hostname, port), timeout=REQUEST_TIMEOUT) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        protocol = ssock.version()
                        cipher = ssock.cipher()
            except ssl.SSLCertVerificationError:
                context = ssl._create_unverified_context()
                with socket.create_connection((hostname, port), timeout=REQUEST_TIMEOUT) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        protocol = ssock.version()
                        cipher = ssock.cipher()

            result["tls"]["valid"] = True
            result["tls"]["protocol"] = protocol
            if cipher:
                result["tls"]["cipher"] = f"{cipher[0]} ({cipher[1]})"

            if cert:
                issuer_parts = [val for rdn in cert.get("issuer", ()) for key, val in rdn if key in ("organizationName", "commonName")]
                result["tls"]["issuer"] = " / ".join(issuer_parts) if issuer_parts else "Unknown"
                subject_parts = [val for rdn in cert.get("subject", ()) for key, val in rdn if key == "commonName"]
                result["tls"]["subject"] = " / ".join(subject_parts) if subject_parts else hostname
                
                not_after_str = cert.get("notAfter")
                result["tls"]["not_before"] = cert.get("notBefore")
                result["tls"]["not_after"] = not_after_str

                if not_after_str:
                    expiry = datetime.datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=datetime.timezone.utc)
                    days_remaining = (expiry - datetime.datetime.now(datetime.timezone.utc)).days
                    result["tls"]["days_remaining"] = days_remaining

                    if days_remaining > 90: tls_score = 100
                    elif days_remaining > 30: tls_score = 85
                    elif days_remaining > 0: tls_score = 55
                else:
                    tls_score = 40
            else:
                tls_score = 40
        except Exception as exc:
            result["tls"]["error"] = f"TLS inspection failed: {str(exc)}"
            tls_score = 0

    # 4. WAF IDENTIFICATION
    haystack = " ".join([f"{k}:{v}" for k, v in headers.items()] + [str(result["http"]["server"] or "")]).lower()
    for waf_name, signatures in WAF_SIGNATURES.items():
        if any(sig.lower() in haystack for sig in signatures):
            result["waf"]["detected"] = waf_name
            result["waf"]["evidence"].append(f"Matched signature for {waf_name}")
            break
    waf_score = 100 if result["waf"]["detected"] != "None Identified" else 30

    # 5. CORS POLICY
    acao = headers.get("access-control-allow-origin")
    acac = headers.get("access-control-allow-credentials")
    result["cors"]["acao"] = acao
    result["cors"]["acac"] = acac
    
    cors_score = 70
    if acao:
        if acao.strip() == "*":
            result["cors"]["wildcard"] = True
            if str(acac).lower() == "true":
                result["cors"]["risk"] = "CRITICAL"
                result["cors"]["details"].append("Wildcard origin combined with credentials enabled.")
                cors_score = 0
            else:
                result["cors"]["risk"] = "HIGH"
                result["cors"]["details"].append("Wildcard '*' origin permits any domain.")
                cors_score = 25
        else:
            result["cors"]["risk"] = "INFORMATIONAL"
            result["cors"]["details"].append(f"Explicit origin policy configured: {acao}")
            cors_score = 100
    else:
        result["cors"]["risk"] = "NOT CONFIGURED"
        result["cors"]["details"].append("No Access-Control-Allow-Origin header detected.")
        cors_score = 70

    # 6. COMPOSITE SCORE
    composite = (header_score * 0.50) + (tls_score * 0.25) + (waf_score * 0.10) + (cors_score * 0.15)
    if not result["reachable"]: composite = 0
    composite = max(0, min(100, round(composite, 1)))
    result["score"] = composite

    if composite >= 95: grade = "A+"
    elif composite >= 90: grade = "A"
    elif composite >= 80: grade = "B"
    elif composite >= 70: grade = "C"
    elif composite >= 60: grade = "D"
    else: grade = "F"
    result["grade"] = grade

    # 7. RISK SURFACE
    result["risk_surface"] = {
        "Missing Headers": round(100 - header_score, 1),
        "TLS Weakness": round(100 - tls_score, 1),
        "WAF Gap": round(100 - waf_score, 1),
        "CORS Risk": round(100 - cors_score, 1),
    }

    return result


# --------------------------------------------------------------------------------------
# HTML REPORT GENERATOR
# --------------------------------------------------------------------------------------
def build_html_report(audit: dict) -> str:
    def badge(present: bool) -> str:
        return '<span class="badge badge-pass">PASS</span>' if present else '<span class="badge badge-fail">FAIL</span>'
    
    grade = audit["grade"]
    grade_color = {"A+": "#00FF66", "A": "#00FF66", "B": "#00F0FF", "C": "#FFB020", "D": "#FF8A3D", "F": "#FF4D6A"}.get(grade, "#FF4D6A")

    header_rows = ""
    for name, meta in audit["headers_audit"].items():
        val = meta["value"] if meta["value"] else "Not Present"
        header_rows += f"""
        <tr>
          <td style="font-family:monospace;font-weight:700;">{name}</td>
          <td>{badge(meta['present'])}</td>
          <td style="font-family:monospace;font-size:12px;color:#94A3B8;word-break:break-all;">{val}</td>
          <td style="font-size:12.5px;color:#94A3B8;">{meta['description']}</td>
        </tr>"""

    tls = audit["tls"]
    days = tls["days_remaining"]
    days_display = f"{days} days" if days is not None else "N/A"
    cors = audit["cors"]
    risk_color = {"CRITICAL": "#FF4D6A", "HIGH": "#FF4D6A", "INFORMATIONAL": "#00FF66", "NOT CONFIGURED": "#FFB020", "UNKNOWN": "#94A3B8"}.get(cors["risk"], "#94A3B8")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CyberSentinel v3.0 | Executive Report</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0B0F19; color:#F8FAFC; font-family:'Inter',sans-serif; padding:40px 24px; line-height:1.55; }}
  .wrap {{ max-width:1000px; margin:0 auto; }}
  .header {{ display:flex; align-items:center; gap:16px; border-bottom:1px solid #1E293B; padding-bottom:20px; margin-bottom:30px; }}
  .logo {{ width:48px; height:48px; border-radius:10px; background:#1E293B; display:flex; align-items:center; justify-content:center; font-size:24px; }}
  h1 {{ font-size:24px; color:#FFF; }}
  h1 span {{ color:#00F0FF; }}
  .sub {{ font-size:12px; color:#64748B; text-transform:uppercase; font-weight:600; letter-spacing:0.1em; }}
  .target {{ background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:16px; margin-bottom:30px; font-family:monospace; font-size:14px; color:#00F0FF; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; margin-bottom:30px; }}
  .card {{ background:#0F172A; border:1px solid #1E293B; border-radius:12px; padding:20px; }}
  .card .label {{ font-size:11px; color:#64748B; text-transform:uppercase; font-weight:700; margin-bottom:10px; }}
  .card .value {{ font-family:monospace; font-size:24px; font-weight:700; color:#FFF; }}
  .grade {{ font-size:36px; font-weight:800; font-family:monospace; color:{grade_color}; }}
  h2 {{ font-size:13px; color:#94A3B8; text-transform:uppercase; font-weight:700; margin:30px 0 15px 0; padding-bottom:8px; border-bottom:1px solid #1E293B; }}
  table {{ width:100%; border-collapse:collapse; font-size:13.5px; }}
  th {{ text-align:left; padding:12px; background:#0F172A; color:#94A3B8; font-size:11px; text-transform:uppercase; border-bottom:1px solid #1E293B; }}
  td {{ padding:12px; border-bottom:1px solid #1E293B; }}
  .badge {{ display:inline-block; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:700; font-family:monospace; }}
  .badge-pass {{ background:rgba(0,255,102,0.1); color:#00FF66; border:1px solid rgba(0,255,102,0.2); }}
  .badge-fail {{ background:rgba(255,77,106,0.1); color:#FF4D6A; border:1px solid rgba(255,77,106,0.2); }}
  .kv {{ display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #1E293B; }}
  .kv .k {{ color:#94A3B8; }}
  .kv .v {{ font-family:monospace; color:#FFF; text-align:right; max-width:60%; }}
  .footer {{ margin-top:40px; padding-top:20px; border-top:1px solid #1E293B; font-size:12px; color:#64748B; text-align:center; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <div class="logo">🛡️</div>
    <div>
      <h1>CyberSentinel <span>v3.0</span></h1>
      <div class="sub">Executive Security Posture Report</div>
    </div>
  </div>
  <div class="target">TARGET: {audit['target']}</div>
  <div class="grid">
    <div class="card"><div class="label">Security Grade</div><div class="grade">{grade}</div><div style="font-size:12px;color:#64748B;margin-top:4px;">Score: {audit['score']} / 100</div></div>
    <div class="card"><div class="label">HTTP Response</div><div class="value">{audit['http']['status_code'] if audit['http']['status_code'] else 'N/A'}</div><div style="font-size:12px;color:#64748B;margin-top:4px;">{audit['http']['reason'] or 'Unreachable'}</div></div>
    <div class="card"><div class="label">TLS Expiration</div><div class="value">{days_display}</div><div style="font-size:12px;color:#64748B;margin-top:4px;">{tls['issuer'] or 'Unknown'}</div></div>
    <div class="card"><div class="label">WAF Detection</div><div class="value" style="color:#00F0FF;">{audit['waf']['detected']}</div></div>
  </div>
  <h2>HTTP Security Headers</h2>
  <table><thead><tr><th>Header</th><th>Status</th><th>Observed Value</th><th>Purpose</th></tr></thead><tbody>{header_rows}</tbody></table>
  <h2>SSL/TLS Cryptographic Profile</h2>
  <div class="card">
    <div class="kv"><span class="k">TLS Validity</span><span class="v">{'VALID' if tls['valid'] else 'INVALID'}</span></div>
    <div class="kv"><span class="k">Protocol</span><span class="v">{tls['protocol'] or 'N/A'}</span></div>
    <div class="kv"><span class="k">Cipher Suite</span><span class="v">{tls['cipher'] or 'N/A'}</span></div>
    <div class="kv"><span class="k">Issuer</span><span class="v">{tls['issuer'] or 'N/A'}</span></div>
    <div class="kv"><span class="k">Valid Until</span><span class="v">{tls['not_after'] or 'N/A'}</span></div>
  </div>
  <h2>CORS Policy</h2>
  <div class="card">
    <div class="kv"><span class="k">Allow-Origin</span><span class="v">{cors['acao'] or 'Not Configured'}</span></div>
    <div class="kv"><span class="k">Allow-Credentials</span><span class="v">{cors['acac'] or 'Not Configured'}</span></div>
    <div class="kv"><span class="k">Risk Classification</span><span class="v" style="color:{risk_color};">{cors['risk']}</span></div>
  </div>
  <div class="footer">Generated by CyberSentinel v3.0 &nbsp;•&nbsp; {audit['audit_timestamp_utc']} &nbsp;•&nbsp; Confidential</div>
</div>
</body>
</html>"""
    return html


# --------------------------------------------------------------------------------------
# UI LAYOUT
# --------------------------------------------------------------------------------------
st.markdown(
    """
    <div class="brand-wrap">
        <div class="brand-logo">🛡️</div>
        <div>
            <div class="brand-title">CyberSentinel <span>v3.0</span></div>
            <div class="brand-sub">Web &amp; API Security Posture Auditor</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

input_col, button_col = st.columns([5, 1.4], gap="medium")
with input_col:
    target_input = st.text_input(
        "TARGET FQDN OR API ENDPOINT",
        value="",
        placeholder="https://api.example.com",
    )
with button_col:
    st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)
    execute = st.button("EXECUTE AUDIT", use_container_width=True)

if execute:
    normalized = normalize_target(target_input)
    if not normalized:
        st.error("Audit aborted: a valid target URL or FQDN must be supplied.")
    else:
        with st.spinner("Executing live security posture assessment..."):
            try:
                audit = perform_audit(normalized)
                st.session_state["audit_result"] = audit
            except Exception as exc:
                st.session_state.pop("audit_result", None)
                st.error(f"Fatal audit error: {exc}")

if "audit_result" in st.session_state:
    audit = st.session_state["audit_result"]

    if audit.get("error") and not audit.get("reachable"):
        st.warning(f"AUDIT NOTICE — {audit['error']}")
        st.info("Limited results may still be displayed below where data is available.")

    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

    grade = audit["grade"]
    grade_color = {"A+": "#00FF66", "A": "#00FF66", "B": "#00F0FF", "C": "#FFB020", "D": "#FF8A3D", "F": "#FF4D6A"}.get(grade, "#FF4D6A")

    days_remaining = audit["tls"]["days_remaining"]
    if days_remaining is None:
        days_value, days_color = "N/A", "#94A3B8"
    elif days_remaining <= 0:
        days_value, days_color = "EXPIRED", "#FF4D6A"
    elif days_remaining <= 30:
        days_value, days_color = f"{days_remaining} d", "#FF4D6A"
    elif days_remaining <= 90:
        days_value, days_color = f"{days_remaining} d", "#FFB020"
    else:
        days_value, days_color = f"{days_remaining} d", "#00FF66"

    http_code = audit["http"]["status_code"]
    http_reason = audit["http"]["reason"] or "Unreachable"
    http_color = "#00FF66" if http_code and http_code < 400 else "#FF4D6A"

    waf_name = audit["waf"]["detected"]
    waf_color = "#00FF66" if waf_name != "None Identified" else "#FFB020"

    m1, m2, m3, m4 = st.columns(4, gap="medium")

    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Security Grade</div>
                <div class="grade-box" style="color:{grade_color};border:1px solid {grade_color};">{grade}</div>
                <div class="metric-sub">Score: {audit['score']} / 100</div>
            </div>
            """, unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">HTTP Response</div>
                <div class="metric-value" style="color:{http_color};">{http_code if http_code else 'N/A'}</div>
                <div class="metric-sub">{http_reason}</div>
            </div>
            """, unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">TLS Expiration</div>
                <div class="metric-value" style="color:{days_color};">{days_value}</div>
                <div class="metric-sub">{audit['tls']['issuer'] or 'Issuer Unknown'}</div>
            </div>
            """, unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">WAF Detection</div>
                <div class="metric-value metric-value-sm" style="color:{waf_color};">{waf_name}</div>
                <div class="metric-sub">{'Signature Confirmed' if waf_name != 'None Identified' else 'No Signature Match'}</div>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Deep Analysis</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["HTTP SECURITY HEADERS", "SSL/TLS & WAF PROFILE", "API SECURITY & CORS", "RISK SURFACE CHART"])

    with tab1:
        if not audit["headers_audit"]:
            st.info("No HTTP header data is available for this target.")
        else:
            for name, meta in audit["headers_audit"].items():
                badge_html = '<span class="badge badge-pass">PASS</span>' if meta["present"] else '<span class="badge badge-fail">FAIL</span>'
                value_display = meta["value"] if meta["value"] else "Not Present"
                st.markdown(
                    f"""
                    <div class="hdr-row">
                        <div style="flex:1;">
                            <div class="hdr-name">{name}</div>
                            <div class="hdr-detail">{value_display}</div>
                            <div class="hdr-detail" style="color:#475569;">{meta['description']}</div>
                        </div>
                        <div style="margin-left:20px;">{badge_html}</div>
                    </div>
                    """, unsafe_allow_html=True
                )

    with tab2:
        tls = audit["tls"]
        st.markdown('<div class="section-title" style="margin-top:8px;">SSL/TLS Cryptographic Profile</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2, gap="medium")
        with col_a:
            st.markdown(
                f"""
                <div class="metric-card" style="min-height:auto;">
                    <div class="metric-label">TLS Validity</div>
                    <div class="metric-value metric-value-sm">{'VALID' if tls['valid'] else 'INVALID'}</div>
                    <div class="metric-sub">Protocol: {tls['protocol'] or 'N/A'}</div>
                    <div class="metric-sub">Cipher: {tls['cipher'] or 'N/A'}</div>
                </div>
                """, unsafe_allow_html=True
            )
        with col_b:
            days_display = f"{tls['days_remaining']} days" if tls["days_remaining"] is not None else "N/A"
            st.markdown(
                f"""
                <div class="metric-card" style="min-height:auto;">
                    <div class="metric-label">Certificate Expiration</div>
                    <div class="metric-value metric-value-sm">{days_display}</div>
                    <div class="metric-sub">Issuer: {tls['issuer'] or 'N/A'}</div>
                    <div class="metric-sub">Subject: {tls['subject'] or 'N/A'}</div>
                </div>
                """, unsafe_allow_html=True
            )

        if tls["not_before"] or tls["not_after"]:
            st.markdown(
                f"""
                <div class="metric-card" style="min-height:auto;margin-top:14px;">
                    <div class="metric-label">Certificate Validity Window</div>
                    <div class="metric-sub">Valid From: <span style="font-family:monospace;color:#F8FAFC;">{tls['not_before'] or 'N/A'}</span></div>
                    <div class="metric-sub">Valid Until: <span style="font-family:monospace;color:#F8FAFC;">{tls['not_after'] or 'N/A'}</span></div>
                </div>
                """, unsafe_allow_html=True
            )

        if tls["error"]:
            st.warning(f"TLS INSPECTION NOTE — {tls['error']}")

        st.markdown('<div class="section-title">WAF Identification</div>', unsafe_allow_html=True)
        waf_name = audit["waf"]["detected"]
        waf_badge = '<span class="badge badge-pass">DETECTED</span>' if waf_name != "None Identified" else '<span class="badge badge-warn">NOT DETECTED</span>'
        st.markdown(
            f"""
            <div class="metric-card" style="min-height:auto;">
                <div class="metric-label">Detected Web Application Firewall</div>
                <div class="metric-value metric-value-sm" style="color:#00F0FF;">{waf_name}</div>
                <div style="margin-top:10px;">{waf_badge}</div>
            </div>
            """, unsafe_allow_html=True
        )
        if audit["waf"]["evidence"]:
            for ev in audit["waf"]["evidence"]:
                st.markdown(f"- `{ev}`")

        st.markdown('<div class="section-title">Observed Server Header</div>', unsafe_allow_html=True)
        st.code(audit["http"]["server"] or "Not Disclosed", language="text")

    with tab3:
        cors = audit["cors"]
        risk_badge_class = {"CRITICAL": "badge-fail", "HIGH": "badge-fail", "INFORMATIONAL": "badge-pass", "NOT CONFIGURED": "badge-warn", "UNKNOWN": "badge-info"}.get(cors["risk"], "badge-info")
        st.markdown('<div class="section-title" style="margin-top:8px;">CORS Policy Assessment</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.markdown(
                f"""
                <div class="metric-card" style="min-height:auto;">
                    <div class="metric-label">Access-Control-Allow-Origin</div>
                    <div class="metric-value metric-value-sm" style="font-size:16px;">{cors['acao'] or 'Not Configured'}</div>
                </div>
                """, unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f"""
                <div class="metric-card" style="min-height:auto;">
                    <div class="metric-label">Allow-Credentials</div>
                    <div class="metric-value metric-value-sm" style="font-size:16px;">{cors['acac'] or 'Not Configured'}</div>
                </div>
                """, unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div class="metric-card" style="min-height:auto;margin-top:14px;">
                <div class="metric-label">Risk Classification</div>
                <div style="margin-top:6px;"><span class="badge {risk_badge_class}">{cors['risk']}</span></div>
                <div class="metric-sub" style="margin-top:12px;">Wildcard Origin Detected: <strong style="color:#F8FAFC;">{'YES' if cors['wildcard'] else 'NO'}</strong></div>
            </div>
            """, unsafe_allow_html=True
        )

        if cors["details"]:
            st.markdown('<div class="section-title">Assessment Notes</div>', unsafe_allow_html=True)
            for detail in cors["details"]:
                st.markdown(f"- {detail}")

        if cors["wildcard"]:
            st.error("CRITICAL FINDING — The target responds with a wildcard '*' Access-Control-Allow-Origin. Any external origin can read cross-origin responses.")

    with tab4:
        st.markdown('<div class="section-title" style="margin-top:8px;">Interactive Risk Surface</div>', unsafe_allow_html=True)
        st.bar_chart(audit["risk_surface"], use_container_width=True, height=380)
        st.caption("Higher bars indicate greater residual risk exposure across each audited security domain.")

    st.markdown('<div class="section-title">Reporting &amp; SIEM Export</div>', unsafe_allow_html=True)

    export_col1, export_col2 = st.columns(2, gap="medium")

    with export_col1:
        html_report = build_html_report(audit)
        st.download_button(
            label="⬇  DOWNLOAD EXECUTIVE HTML REPORT",
            data=html_report,
            file_name=f"cybersentinel_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True,
        )

    with export_col2:
        siem_payload = {
            "event_type": "SECURITY_POSTURE_AUDIT",
            "engine": "CyberSentinel v3.0",
            "timestamp_utc": audit["audit_timestamp_utc"],
            "target": audit["target"],
            "reachable": audit["reachable"],
            "error": audit["error"],
            "security_grade": audit["grade"],
            "composite_score": audit["score"],
            "http": audit["http"],
            "headers": audit["headers_audit"],
            "tls": audit["tls"],
            "waf": audit["waf"],
            "cors": audit["cors"],
            "risk_surface": audit["risk_surface"],
        }
        st.download_button(
            label="⬇  DOWNLOAD RAW SIEM LOG (JSON)",
            data=json.dumps(siem_payload, indent=2, default=str),
            file_name=f"cybersentinel_siem_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )

else:
    st.markdown(
        """
        <div class="metric-card" style="text-align:center;padding:48px 24px;margin-top:20px;">
            <div style="font-size:32px;margin-bottom:16px;">🛡️</div>
            <div class="metric-value metric-value-sm">AWAITING TARGET</div>
            <div class="metric-sub" style="max-width:520px;margin:12px auto 0 auto;">
                Enter a fully qualified domain name or API endpoint above and select
                <strong style="color:#00F0FF;">EXECUTE AUDIT</strong> to initiate a live
                security posture assessment.
            </div>
        </div>
        """, unsafe_allow_html=True
    )