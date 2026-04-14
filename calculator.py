import streamlit as st

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Web Calculator",
    page_icon="🧮",
    layout="centered"
)

# ─── CUSTOM STYLING ───────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Dark background */
.stApp { background-color: #0a0a0f; }

/* Hide Streamlit default header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* Display screen */
.display-box {
    background: #08080f;
    border: 1px solid #2a2a3d;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    min-height: 100px;
}
.expr-text {
    color: #555570;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    margin: 0;
    min-height: 20px;
}
.result-text {
    color: #e8e8f0;
    font-family: 'Courier New', monospace;
    font-size: 44px;
    font-weight: bold;
    text-align: right;
    margin: 0;
    word-break: break-all;
}
.result-error {
    color: #ff4d6d;
    font-size: 20px;
    font-family: 'Courier New', monospace;
    text-align: right;
}
.title-label {
    color: #555570;
    font-size: 11px;
    letter-spacing: 4px;
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 20px;
    font-family: sans-serif;
}
.footer-label {
    color: #555570;
    font-size: 11px;
    letter-spacing: 1px;
    text-align: center;
    margin-top: 16px;
    font-family: sans-serif;
}

/* Button styling */
div.stButton > button {
    width: 100%;
    padding: 18px 0px;
    background-color: #1a1a28;
    color: #e8e8f0;
    border: 1px solid #2a2a3d;
    border-radius: 10px;
    font-size: 18px;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
    transition: all 0.1s;
    cursor: pointer;
}
div.stButton > button:hover {
    background-color: #22223a;
    border-color: #3a3a55;
    color: #ffffff;
}
div.stButton > button:active {
    transform: scale(0.95);
}

/* Operator buttons - cyan */
div[data-testid="column"]:nth-child(4) div.stButton > button,
.op-btn div.stButton > button {
    background-color: #1e1e35;
    color: #00e5ff;
    border-color: rgba(0,229,255,0.25);
}

/* Function buttons - gray */
.fn-btn div.stButton > button {
    background-color: #1c1c2e;
    color: #aaaacc;
}

/* Equal button */
.eq-btn div.stButton > button {
    background-color: #00e5ff;
    color: #0a0a0f;
    border: none;
    font-size: 22px;
    box-shadow: 0 4px 20px rgba(0,229,255,0.3);
}
div.stButton > button:focus {
    box-shadow: none;
    outline: none;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE (memory between button clicks) ─────────────────────────────
# Streamlit reruns top-to-bottom on every button click.
# st.session_state persists values across reruns — this is our "memory".

if "expression" not in st.session_state:
    st.session_state.expression = ""        # the math string being built

if "display" not in st.session_state:
    st.session_state.display = "0"          # what shows on screen

if "just_calculated" not in st.session_state:
    st.session_state.just_calculated = False  # did we just press "=" ?

if "error" not in st.session_state:
    st.session_state.error = False

# ─── PURE PYTHON LOGIC FUNCTIONS ─────────────────────────────────────────────

def press_number(n: str):
    """Append a digit to the expression."""
    if st.session_state.just_calculated:
        st.session_state.expression = ""
        st.session_state.just_calculated = False
    st.session_state.expression += n
    st.session_state.display = st.session_state.expression
    st.session_state.error = False


def press_operator(op: str):
    """Append an operator (+, -, *, /)."""
    st.session_state.just_calculated = False
    expr = st.session_state.expression
    # Prevent double operators
    if expr and expr[-1] in "+-*/":
        expr = expr[:-1]
    st.session_state.expression = expr + op
    st.session_state.display = st.session_state.expression
    st.session_state.error = False


def press_dot():
    """Add decimal point (only if current number doesn't have one)."""
    import re
    parts = re.split(r"[\+\-\*\/]", st.session_state.expression)
    if "." not in parts[-1]:
        press_number(".")


def press_clear():
    """AC — reset everything."""
    st.session_state.expression = ""
    st.session_state.display = "0"
    st.session_state.just_calculated = False
    st.session_state.error = False


def press_toggle_sign():
    """Flip positive/negative."""
    expr = st.session_state.expression
    if not expr:
        return
    if expr.startswith("-(") and expr.endswith(")"):
        st.session_state.expression = expr[2:-1]   # remove wrapping -(...)
    else:
        st.session_state.expression = f"-({expr})"
    st.session_state.display = st.session_state.expression


def press_percent():
    """Divide current expression by 100."""
    if not st.session_state.expression:
        return
    st.session_state.expression = f"({st.session_state.expression})/100"
    st.session_state.display = st.session_state.expression


def press_equals():
    """
    THE KEY PYTHON FUNCTION — evaluates the math expression.
    This runs on Python server, not in the browser.
    """
    expr = st.session_state.expression
    if not expr:
        return
    try:
        # Restrict eval to math only — no builtins allowed
        result = eval(expr, {"__builtins__": {}})

        # Check for division by zero result
        if not isinstance(result, (int, float)):
            raise ValueError("Invalid result type")

        # Format nicely: remove trailing zeros from floats
        if isinstance(result, float):
            formatted = f"{result:.10f}".rstrip("0").rstrip(".")
        else:
            formatted = str(result)

        st.session_state.display = formatted
        st.session_state.expression = formatted
        st.session_state.just_calculated = True
        st.session_state.error = False

    except ZeroDivisionError:
        st.session_state.display = "Cannot divide by zero"
        st.session_state.error = True

    except Exception:
        st.session_state.display = "Invalid expression"
        st.session_state.error = True


# ─── UI LAYOUT ────────────────────────────────────────────────────────────────

st.markdown('<div class="title-label">Web Calculator</div>', unsafe_allow_html=True)

# Display screen
expr_line = st.session_state.expression if st.session_state.expression else "—"
result_class = "result-error" if st.session_state.error else "result-text"

st.markdown(f"""
<div class="display-box">
    <p class="expr-text">{expr_line}</p>
    <p class="{result_class}">{st.session_state.display}</p>
</div>
""", unsafe_allow_html=True)

# ── Button Grid (4 columns) ───────────────────────────────────────────────────
# Row 1: AC  +/-  %  ÷
r1 = st.columns(4)
with r1[0]: st.button("AC",  on_click=press_clear,              use_container_width=True)
with r1[1]: st.button("+/−", on_click=press_toggle_sign,        use_container_width=True)
with r1[2]: st.button("%",   on_click=press_percent,            use_container_width=True)
with r1[3]: st.button("÷",   on_click=press_operator, args=("/",), use_container_width=True)

# Row 2: 7  8  9  ×
r2 = st.columns(4)
with r2[0]: st.button("7", on_click=press_number, args=("7",), use_container_width=True)
with r2[1]: st.button("8", on_click=press_number, args=("8",), use_container_width=True)
with r2[2]: st.button("9", on_click=press_number, args=("9",), use_container_width=True)
with r2[3]: st.button("×", on_click=press_operator, args=("*",), use_container_width=True)

# Row 3: 4  5  6  −
r3 = st.columns(4)
with r3[0]: st.button("4", on_click=press_number, args=("4",), use_container_width=True)
with r3[1]: st.button("5", on_click=press_number, args=("5",), use_container_width=True)
with r3[2]: st.button("6", on_click=press_number, args=("6",), use_container_width=True)
with r3[3]: st.button("−", on_click=press_operator, args=("-",), use_container_width=True)

# Row 4: 1  2  3  +
r4 = st.columns(4)
with r4[0]: st.button("1", on_click=press_number, args=("1",), use_container_width=True)
with r4[1]: st.button("2", on_click=press_number, args=("2",), use_container_width=True)
with r4[2]: st.button("3", on_click=press_number, args=("3",), use_container_width=True)
with r4[3]: st.button("+", on_click=press_operator, args=("+",), use_container_width=True)

# Row 5: 0 (wide)  .  =
r5 = st.columns([2, 1, 1])
with r5[0]: st.button("0",  on_click=press_number,  args=("0",), use_container_width=True)
with r5[1]: st.button(".",  on_click=press_dot,                  use_container_width=True)
with r5[2]: st.button("=",  on_click=press_equals,               use_container_width=True)

st.markdown('<div class="footer-label">100% Python · Built with Streamlit</div>', unsafe_allow_html=True)
