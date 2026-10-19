# 🛡️ CyberSentinel: Web & API Security Posture Suite

CyberSentinel is an automated, lightweight, non-intrusive security posture inspection suite built with Python and Streamlit. It audits Web Applications and REST APIs against OWASP security configuration standards, SSL certificate validity, and WAF signatures.

---

## 🚀 Key Features

- **HTTP Security Headers Audit:** Evaluates `Strict-Transport-Security` (HSTS), `Content-Security-Policy` (CSP), `X-Frame-Options`, `X-Content-Type-Options`, and `Referrer-Policy`.
- **CORS Policy Inspection:** Identifies dangerous wildcard (`*`) access controls[cite: 1].
- **SSL/TLS & WAF Detector:** Validates certificate trust chains, expiration windows, and detects Cloudflare, AWS WAF, or Akamai signatures[cite: 1].
- **Automated Scorecard Engine:** Translates configuration posture into an enterprise letter grade (A+ to F)[cite: 1].
- **Dark Executive HTML Reports:** Generates downloadable, dark-themed HTML assessment reports[cite: 1].

---

## 🛠️ Installation & Setup

```bash
# Clone the repository
git clone [https://github.com/YOUR_GITHUB_USERNAME/CyberSentinel.git](https://github.com/YOUR_GITHUB_USERNAME/CyberSentinel.git)

# Navigate to project directory
cd CyberSentinel

# Install required dependencies
pip install streamlit requests

# Launch the Application
streamlit run app.py

📊 Live Benchmark ResultsTarget DomainSecurity GradeSecurity ScoreKey FindingsPinterestA+100 / 100Full HSTS preloading, strict CSP, valid TLS 1.3   Daraz.pkC65 / 100Missing CSP and Referrer-Policy headers   👨‍💻 Developer & Program DetailsDeveloper: Aebad[cite: 1]Internship: Cyberfox Society Cybersecurity R&D Internship[cite: 1]Domain: Web & API Security[cite: 1]