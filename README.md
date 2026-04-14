# 🧮 Web Calculator — 100% Python (Streamlit)

A fully Python-based web calculator. Zero HTML, zero JavaScript — all logic and UI built entirely in Python using Streamlit.

🔗 **Live Demo**: [your-app.streamlit.app](https://your-app.streamlit.app)

---

## 🐍 Why This is 100% Python

| What it does | How it's done | Language |
|---|---|---|
| Button layout | `st.columns()` + `st.button()` | Python |
| Memory between clicks | `st.session_state` | Python |
| Math evaluation | `eval()` with restricted builtins | Python |
| Error handling | `try / except ZeroDivisionError` | Python |
| UI styling | `st.markdown()` with CSS | Python |

---

## 📁 Project Structure

```
streamlit-calculator/
├── calculator.py       ← entire app in one Python file
└── requirements.txt    ← streamlit dependency
```

---

## ⚙️ Run Locally

```bash
pip install streamlit
streamlit run calculator.py
```

---

## 🚀 Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub → select repo → set main file: `calculator.py`
4. Click Deploy → get a live URL instantly

---

## 🧠 Key Concept: st.session_state

Streamlit reruns the entire script on every button click.  
`st.session_state` is a Python dictionary that **persists values across reruns** — it acts as the calculator's memory.

```python
if "expression" not in st.session_state:
    st.session_state.expression = ""   # initialize once

# Later, any button click updates it:
st.session_state.expression += "7"    # persists to next rerun
```

---

## 👤 Author

**Himanshu Kala** — AI QA Engineer  
🌐 [himanshukala.co.in](https://himanshukala.co.in) · 🐙 [github.com/Hkala402](https://github.com/Hkala402)
