import os
import streamlit as st

DEFAULT_MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct"

st.set_page_config(page_title="HF Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&family=Nunito+Mono:wght@400;600&display=swap');

:root {
    --bg:           #12131a;
    --surface:      #1c1e2e;
    --surface2:     #252840;
    --border:       #303458;
    --coral:        #ff6b6b;
    --coral-glow:   rgba(255,107,107,0.18);
    --mint:         #43e6b5;
    --mint-glow:    rgba(67,230,181,0.15);
    --lavender:     #c084fc;
    --lavender-glow:rgba(192,132,252,0.15);
    --sun:          #fbbf24;
    --sky:          #38bdf8;
    --user-bg:      #2a1f2e;
    --user-border:  #7c3f5e;
    --bot-bg:       #1a2a2a;
    --bot-border:   #2d5a50;
    --text:         #edeef5;
    --text-muted:   #7b7fa0;
    --font:         'Nunito', sans-serif;
    --mono:         'Nunito Mono', monospace;
    --radius:       18px;
    --radius-sm:    10px;
}

html, body, [class*="css"] { font-family: var(--font) !important; }
.stApp { background: var(--bg); color: var(--text); }

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--coral), var(--lavender), var(--mint), var(--sky), var(--sun), var(--coral));
    background-size: 300% 100%;
    animation: gradientSlide 5s linear infinite;
    z-index: 9999;
}
@keyframes gradientSlide {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

.chat-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 24px 0 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
}
.chat-header .avatar {
    width: 52px; height: 52px;
    border-radius: 16px;
    background: linear-gradient(135deg, var(--coral), var(--lavender));
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    box-shadow: 0 4px 20px var(--coral-glow), 0 0 0 1px rgba(255,107,107,0.2);
    animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 4px 20px var(--coral-glow), 0 0 0 1px rgba(255,107,107,0.2); }
    50%       { box-shadow: 0 4px 30px rgba(192,132,252,0.35), 0 0 0 1px rgba(192,132,252,0.3); }
}
.chat-header .title-block h1 {
    margin: 0 !important; padding: 0 !important;
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, var(--coral), var(--lavender));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}
.chat-header .title-block .sub {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 3px;
    font-weight: 500;
}
.chat-header .status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: var(--mint);
    border-radius: 50%;
    margin-right: 5px;
    box-shadow: 0 0 6px var(--mint);
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity: 1; } 50% { opacity: 0.4; }
}

[data-testid="stChatMessage"] {
    padding: 14px 18px !important;
    border-radius: var(--radius) !important;
    margin-bottom: 14px !important;
    border: 1px solid transparent;
    animation: popIn 0.28s cubic-bezier(0.34,1.56,0.64,1) both;
}
@keyframes popIn {
    from { opacity: 0; transform: scale(0.95) translateY(10px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
}
div[class*="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--user-bg) !important;
    border-color: var(--user-border) !important;
    border-left: 3px solid var(--coral) !important;
}
div[class*="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: var(--bot-bg) !important;
    border-color: var(--bot-border) !important;
    border-left: 3px solid var(--mint) !important;
}

[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, var(--coral), #ff9a9a) !important;
    border-radius: 10px !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, var(--mint), #38d9a9) !important;
    border-radius: 10px !important;
}
[data-testid="chatAvatarIcon-user"] svg,
[data-testid="chatAvatarIcon-assistant"] svg { fill: #fff !important; }

[data-testid="stChatMessage"] p {
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    color: var(--text) !important;
    font-weight: 400 !important;
}

/* ── FIXED: Chat input text visibility ── */
[data-testid="stChatInput"] {
    border-radius: var(--radius) !important;
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--lavender) !important;
    box-shadow: 0 0 0 3px var(--lavender-glow) !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus,
[data-testid="stChatInput"] textarea:active,
[data-testid="stChatInput"] textarea::placeholder,
div[data-testid="stChatInputTextArea"] textarea,
div[data-testid="stChatInputTextArea"] textarea:focus,
.stChatInput textarea {
    color: #edeef5 !important;
    -webkit-text-fill-color: #edeef5 !important;
    caret-color: #edeef5 !important;
    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    background: transparent !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #7b7fa0 !important;
    -webkit-text-fill-color: #7b7fa0 !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .sidebar-title {
    font-size: 0.72rem;
    font-family: var(--mono);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--lavender);
    font-weight: 600;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 6px;
}
[data-testid="stSidebar"] label {
    font-size: 0.83rem !important;
    color: var(--text-muted) !important;
    font-weight: 600 !important;
}

.model-badge {
    background: linear-gradient(135deg, rgba(67,230,181,0.1), rgba(56,189,248,0.08));
    border: 1px solid rgba(67,230,181,0.25);
    border-radius: var(--radius-sm);
    padding: 9px 13px;
    font-family: var(--mono);
    font-size: 0.71rem;
    color: var(--mint);
    margin-top: 6px;
    word-break: break-all;
    line-height: 1.5;
}

.stat-row { display: flex; gap: 8px; margin: 16px 0 4px; }
.stat-chip {
    flex: 1;
    border-radius: var(--radius-sm);
    padding: 10px 6px;
    text-align: center;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-muted);
}
.stat-chip.coral { background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.2); }
.stat-chip.mint  { background: rgba(67,230,181,0.08);  border: 1px solid rgba(67,230,181,0.2); }
.stat-chip.sun   { background: rgba(251,191,36,0.08);  border: 1px solid rgba(251,191,36,0.2); }
.stat-chip span  { display: block; font-size: 1.15rem; font-weight: 800; margin-bottom: 1px; }
.stat-chip.coral span { color: var(--coral); }
.stat-chip.mint  span { color: var(--mint); }
.stat-chip.sun   span { color: var(--sun); }

.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 14px 0;
}

[data-testid="stSidebar"] button {
    background: rgba(255,107,107,0.06) !important;
    border: 1.5px dashed rgba(255,107,107,0.3) !important;
    color: rgba(255,107,107,0.7) !important;
    border-radius: var(--radius-sm) !important;
    font-size: 0.83rem !important;
    font-weight: 700 !important;
    font-family: var(--font) !important;
    width: 100% !important;
    transition: all 0.2s !important;
    padding: 8px !important;
}
[data-testid="stSidebar"] button:hover {
    background: rgba(255,107,107,0.14) !important;
    border-color: var(--coral) !important;
    color: var(--coral) !important;
    transform: translateY(-1px);
}

.stSpinner > div { border-top-color: var(--lavender) !important; }

.empty-state {
    text-align: center;
    padding: 70px 24px 40px;
}
.empty-state .emoji-stack {
    font-size: 2.8rem;
    margin-bottom: 16px;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
.empty-state h3 {
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 8px;
}
.empty-state p {
    font-size: 0.88rem;
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 300px;
    margin: 0 auto;
}
.suggestion-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 22px;
}
.chip {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 7px 15px;
    font-size: 0.8rem;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.18s;
    font-weight: 600;
}
.chip:hover {
    border-color: var(--lavender);
    color: var(--lavender);
    background: rgba(192,132,252,0.08);
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--lavender); }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="🔧 Loading model weights…")
def get_llm(model_id):
    from transformers import AutoTokenizer, pipeline
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    text_generator = pipeline(
        "text-generation",
        model=model_id,
        tokenizer=tokenizer,
    )
    return text_generator, tokenizer


def build_prompt(messages, tokenizer):
    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        return tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    parts = []
    for m in messages:
        role = "User" if m["role"] == "user" else "Assistant"
        parts.append(f"{role}: {m['content']}")
    parts.append("Assistant:")
    return "\n".join(parts)


def generate_response(messages, model_id, max_new_tokens, temperature):
    llm, tokenizer = get_llm(model_id)
    prompt = build_prompt(messages, tokenizer)
    out = llm(
        prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=temperature > 0,
        return_full_text=False,
        pad_token_id=tokenizer.eos_token_id,
    )
    text = out[0]["generated_text"].strip()
    return text, messages + [{"role": "assistant", "content": text}]


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ &nbsp;Settings</div>', unsafe_allow_html=True)
    model_id = st.text_input(
        "Model ID",
        value=os.getenv("HF_MODEL_ID", DEFAULT_MODEL),
        help="Any Hugging Face text-generation or instruct model.",
    )
    st.markdown(f'<div class="model-badge">🟢 &nbsp;{model_id}</div>', unsafe_allow_html=True)
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    max_new_tokens = st.slider("Max new tokens", 32, 512, 160, 16)
    temperature    = st.slider("Temperature",    0.0, 1.5, 0.7, 0.1)
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    n_turns = len([m for m in st.session_state.messages if m["role"] == "user"])
    n_words = sum(len(m["content"].split()) for m in st.session_state.messages)
    n_chars = sum(len(m["content"]) for m in st.session_state.messages)
    st.markdown(f"""
        <div class="stat-row">
            <div class="stat-chip coral"><span>{n_turns}</span>turns</div>
            <div class="stat-chip mint"><span>{n_words}</span>words</div>
            <div class="stat-chip sun"><span>{n_chars}</span>chars</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️  Clear chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown("""
<div class="chat-header">
  <div class="avatar">🤖</div>
  <div class="title-block">
    <h1>HF Chatbot</h1>
    <div class="sub">
      <span class="status-dot"></span>Ready · Powered by Hugging Face Transformers
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
      <div class="emoji-stack">🌟</div>
      <h3>Hey there! Let's chat 👋</h3>
      <p>Ask me anything — I'm running locally on your machine, fully private.</p>
      <div class="suggestion-chips">
        <div class="chip">💡 Explain quantum computing</div>
        <div class="chip">✍️ Write a short poem</div>
        <div class="chip">🐍 Help me with Python</div>
        <div class="chip">🌍 Fun world facts</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type something… I'm listening 👂")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                reply, updated = generate_response(
                    st.session_state.messages, model_id, max_new_tokens, temperature
                )
            except Exception as exc:
                reply = f"⚠️ Oops! Model error: {exc}"
                updated = st.session_state.messages + [{"role": "assistant", "content": reply}]
        st.markdown(reply)

    st.session_state.messages = updated
