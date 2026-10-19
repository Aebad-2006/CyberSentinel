# 🛡️ CyberSentinel - Web & API Security Posture Suite

**CyberSentinel** is an automated, lightweight, and non-intrusive security inspection tool designed to evaluate the real-time security posture of Web Applications and REST APIs. It audits defensive configurations, SSL/TLS certificates, Web Application Firewall (WAF) signatures, and HTTP security headers without causing operational disruption.

---

## 📌 Project Overview & Core Features

### 1. 🛡️ Defensive HTTP Security Headers Audit
Evaluates whether mandatory defensive HTTP response headers are implemented according to OWASP guidelines:
- **Strict-Transport-Security (HSTS):** Enforces mandatory HTTPS connections.
- **Content-Security-Policy (CSP):** Mitigates Cross-Site Scripting (XSS) and data injection attacks.
- **X-Frame-Options:** Blocks UI Clickjacking exploits.
- **X-Content-Type-Options:** Prevents MIME-type sniffing vulnerabilities.
- **Referrer-Policy:** Controls sensitive URL metadata leakage.

### 2. 🔒 SSL/TLS & Cryptographic Inspector
- **X.509 Certificate Inspection:** Validates certificate authenticity, issuing authority (CA), and TLS protocol versions (TLS 1.2/1.3).
- **Expiration Tracking:** Calculates exact remaining days before certificate expiration to prevent unexpected downtime.

### 3. 🌐 API Security & CORS Boundary Assessor
- Audits Cross-Origin Resource Sharing (CORS) policies.
- Identifies hazardous wildcard (`*`) origins that risk exposing sensitive authenticated session data across domains.

### 4. ⚡ Cloud WAF Signature Detection
- Inspects edge HTTP response headers to identify major Web Application Firewalls (WAF):
  - Cloudflare WAF
  - Akamai Edge
  - AWS WAF
  - Imperva / Incapsula

### 5. 📊 Algorithmic Risk Scorecard & Grading
- Automatically calculates a normalized numerical score (0–100) and assigns an enterprise security grade (**A+ to F**) based on weighted OWASP misconfiguration penalties.

### 6. 📄 Executive Reports & SIEM Exporters
- **Dark Executive HTML Report:** Generates a standalone, dark-themed HTML report suitable for offline archival and leadership briefs.
- **Raw SIEM Logs (JSON):** Exports structured audit telemetry in JSON format for SIEM log ingestion.

---

## 🛠️ Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/Aebad-2006)

# 2. Navigate to the project directory
cd CyberSentinel

# 3. Install required dependencies
pip install streamlit requests

# 4. Launch the application
streamlit run app.py


👤 Developer & Program Metadata
Developer: Aebad

Domain: Web & API Security

Organization: Cyberfox Society Cybersecurity R&D Internship
