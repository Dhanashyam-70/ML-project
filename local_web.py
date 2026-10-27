"""Small local HTML front end for the SMS spam model."""

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR / "vendor"))

import joblib

MODEL = joblib.load(PROJECT_DIR / "spam_model.joblib")
PRIZE_PHRASES = (
    "you have won",
    "you've won",
    "won an iphone",
    "win an iphone",
    "claim your prize",
    "free prize",
)

PAGE = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Inbox Guardian | SMS checker</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
    * { box-sizing: border-box; }
    body { margin:0; min-height:100vh; padding:34px 18px; color:#14253d; font-family:'DM Sans',Arial,sans-serif; background:radial-gradient(ellipse at 10% 0%,#e7f5ff 0,transparent 40%),linear-gradient(160deg,#f8fbff,#f4f7fb); }
    main { max-width:850px; margin:0 auto; }
    .hero { background:linear-gradient(125deg,#102c4e,#174f71 62%,#18a6a0); color:white; padding:36px 40px; border-radius:24px; box-shadow:0 18px 45px #14375922; margin-bottom:24px; }
    .eyebrow { text-transform:uppercase; letter-spacing:.16em; color:#75e0d0; font-size:.75rem; font-weight:800; }
    h1 { font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,6vw,2.7rem); margin:8px 0; }
    .hero p { color:#d6e9f3; font-size:1.05rem; margin:0; }
    h2 { font-family:'Space Grotesk',sans-serif; margin:0 0 8px; }
    .hint { color:#62748a; line-height:1.55; }
    .card { background:white; border:1px solid #e6edf4; border-radius:18px; padding:24px; box-shadow:0 8px 24px #193a5a0b; }
    label { display:block; font-weight:700; margin:20px 0 8px; }
    textarea { display:block; width:100%; min-height:150px; padding:14px 15px; border:1px solid #cbd7e4; border-radius:12px; background:#fff; color:#14253d; font:16px/1.5 'DM Sans',Arial,sans-serif; resize:vertical; cursor:text; user-select:text; -webkit-user-select:text; }
    textarea:focus { outline:3px solid #9be4dc; border-color:#118b83; }
    .actions { display:flex; align-items:center; gap:14px; flex-wrap:wrap; margin-top:15px; }
    button { border:0; border-radius:12px; padding:12px 20px; color:white; background:#118b83; font-weight:800; font-size:1rem; cursor:pointer; }
    button:hover { background:#0b716c; }
    button:disabled { opacity:.65; cursor:wait; }
    .try { color:#62748a; font-size:.92rem; }
    #result { display:none; margin-top:18px; padding:16px; border-radius:12px; font-weight:700; }
    #result.spam { display:block; color:#912b29; background:#fff0ef; border:1px solid #f3c4c1; }
    #result.ham { display:block; color:#176345; background:#eaf8f1; border:1px solid #bde7cf; }
    #result.error { display:block; color:#805400; background:#fff8e6; border:1px solid #f0d896; }
    .how { margin-top:20px; color:#62748a; line-height:1.6; }
    footer { color:#8291a3; text-align:center; font-size:.82rem; margin:24px 0; }
  </style>
</head>
<body>
  <main>
    <header class="hero"><div class="eyebrow">Machine Learning · SMS Safety</div><h1>Inbox Guardian</h1><p>Check a text message for common spam signals in seconds.</p></header>
    <section class="card">
      <h2>Check a message</h2>
      <div class="hint">Type or paste any SMS below, then check the prediction.</div>
      <form id="sms-form">
        <label for="message">SMS message</label>
        <textarea id="message" name="message" placeholder="Example: You have won an iPhone!" autocomplete="off" spellcheck="false" required></textarea>
        <div class="actions"><button id="check" type="submit">Check message</button><span class="try">Try: Are we still meeting at 5 today?</span></div>
      </form>
      <div id="result" role="status" aria-live="polite"></div>
      <div class="how"><b>How it works</b><br>TF-IDF converts words into weighted numbers. A Linear SVM classifies the message, with a small prize-scam phrase check as an extra safeguard.</div>
    </section>
    <footer>SMS Spam Detector · ML Lab Project</footer>
  </main>
  <script>
    const form = document.getElementById('sms-form');
    const box = document.getElementById('message');
    const button = document.getElementById('check');
    const result = document.getElementById('result');
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = box.value.trim();
      if (!message) { box.focus(); return; }
      button.disabled = true;
      button.textContent = 'Checking…';
      result.className = '';
      result.style.display = 'none';
      try {
        const response = await fetch('/predict', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({message}) });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Could not check this message.');
        result.className = data.label === 'spam' ? 'spam' : 'ham';
        result.textContent = data.label === 'spam' ? '🚨 Likely SPAM — be careful with links, requests, and unknown numbers.' : '✅ Likely HAM — the model considers this a normal message.';
        result.style.display = 'block';
        if (data.rule) result.textContent += ' Flagged by the prize-scam phrase check.';
      } catch (error) {
        result.className = 'error';
        result.textContent = error.message;
        result.style.display = 'block';
      } finally {
        button.disabled = false;
        button.textContent = 'Check message';
      }
    });
    document.addEventListener('keydown', (event) => { if (event.ctrlKey && event.key === 'Enter') form.requestSubmit(); });
  </script>
</body>
</html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/_stcore/health") or self.path == "/health":
            body = b"ok"
            content_type = "text/plain; charset=utf-8"
        elif self.path == "/" or self.path.startswith("/?"):
            body = PAGE.encode("utf-8")
            content_type = "text/html; charset=utf-8"
        else:
            body = b"Not found"
            self.send_response(404)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/predict":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            message = str(payload.get("message", "")).strip()
            if not message:
                raise ValueError("Enter a message first.")
            normalized = " ".join(message.lower().split())
            rule_hit = any(phrase in normalized for phrase in PRIZE_PHRASES)
            label = "spam" if rule_hit else str(MODEL.predict([message])[0])
            response = {"label": label, "rule": rule_hit}
            status = 200
        except Exception as error:
            response = {"error": str(error)}
            status = 400
        body = json.dumps(response).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Do not write message text or local requests to a persistent access log.
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8501), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
