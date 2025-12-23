# Smart Login Automation 🤖

An AI-assisted UI automation framework that intelligently adapts to DOM changes
by learning the most reliable selectors over time.

Built with **Python + Playwright**, inspired by modern self-healing test systems.

---

## ✨ Key Features
- 🧠 Self-healing selectors with weight learning
- 🤖 AI-assisted decision making (ML-ready)
- 🧪 Robust UI automation with Playwright
- 🔁 Fallback strategies for unstable DOMs
- 🌐 Works with React-based applications
- 📈 Selector reliability tracking

---

## 🧰 Tech Stack
- Python 3.11
- Playwright (sync API)
- scikit-learn
- NumPy
- JSON-based persistence

---

## 🧠 How It Works
1. Attempts selectors based on learned weights
2. Updates selector reliability after success
3. Falls back to generic DOM strategies
4. Persists learning across test runs

---

## 🚀 Run the Demo

```bash
pip install -r requirements.txt
python src/main.py
