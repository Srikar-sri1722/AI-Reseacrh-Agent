import textwrap
import datetime
import streamlit as st

from agents import build_search_agent, build_scraping_agent, writer_chain, critic_chain

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

def html(s: str) -> str:
    """Dedent + strip so Streamlit's markdown parser never mistakes indented
    HTML for a code block (the cause of raw-HTML leaking into the page)."""
    return textwrap.dedent(s).strip()

# ----------------------------------------------------------------------------
# GLOBAL STYLE + ANIMATED AURORA BACKGROUND
# ----------------------------------------------------------------------------
st.markdown(
    html(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {{
        --bg:      #05060B;
        --panel:   rgba(255,255,255,0.045);
        --panel-b: rgba(255,255,255,0.09);
        --text:    #F2F4FB;
        --muted:   #8890A6;

        --c-search: #22D3EE;
        --c-reader: #A78BFA;
        --c-writer: #F472B6;
        --c-editor: #FBBF24;
    }}

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    #MainMenu, footer, header {{visibility: hidden;}}

    .stApp {{
        background: var(--bg);
        color: var(--text);
    }}

    /* aurora blobs, fixed behind content */
    .aurora {{
        position: fixed; inset: 0; z-index: 0; overflow: hidden; pointer-events: none;
    }}
    .aurora span {{
        position: absolute; border-radius: 50%; filter: blur(90px); opacity: 0.28;
    }}
    .aurora .b1 {{ width: 480px; height: 480px; background: var(--c-search); top: -160px; left: -100px; animation: float1 22s ease-in-out infinite; }}
    .aurora .b2 {{ width: 520px; height: 520px; background: var(--c-writer); bottom: -200px; right: -140px; animation: float2 26s ease-in-out infinite; }}
    .aurora .b3 {{ width: 380px; height: 380px; background: var(--c-reader); top: 30%; right: 20%; animation: float3 30s ease-in-out infinite; }}
    @keyframes float1 {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(60px,40px); }} }}
    @keyframes float2 {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(-50px,-30px); }} }}
    @keyframes float3 {{ 0%,100% {{ transform: translate(0,0) scale(1); }} 50% {{ transform: translate(-40px,50px) scale(1.08); }} }}

    section.main > div.block-container {{ position: relative; z-index: 1; padding-top: 1.4rem; }}

    h1, h2, h3 {{ font-family: 'Sora', sans-serif !important; }}

    /* ---------- HEADER ---------- */
    .topbar {{
        display: flex; align-items: center; justify-content: space-between;
        padding: 1.1rem 1.6rem; margin-bottom: 1.3rem; border-radius: 16px;
        background: var(--panel); border: 1px solid var(--panel-b);
        backdrop-filter: blur(18px);
    }}
    .brand {{ display: flex; align-items: center; gap: 0.8rem; }}
    .brand-dot {{
        width: 12px; height: 12px; border-radius: 50%;
        background: radial-gradient(circle, #fff, var(--c-search));
        box-shadow: 0 0 14px var(--c-search); animation: pulse-dot 2s infinite;
    }}
    @keyframes pulse-dot {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
    .brand-title {{
        font-family: 'Sora', sans-serif; font-weight: 800; font-size: 1.5rem; margin: 0;
        background: linear-gradient(90deg, #fff 10%, var(--c-search) 55%, var(--c-reader) 100%);
        -webkit-background-clip: text; background-clip: text; color: transparent;
        letter-spacing: -0.01em;
    }}
    .brand-sub {{ color: var(--muted); font-size: 0.82rem; margin-top: 0.15rem; }}
    .topbar-meta {{
        font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--muted);
        text-align: right; line-height: 1.5;
    }}

    /* ---------- STATS STRIP ---------- */
    .stats {{ display: flex; gap: 0.9rem; margin-bottom: 1.3rem; }}
    .stat {{
        flex: 1; background: var(--panel); border: 1px solid var(--panel-b);
        border-radius: 14px; padding: 0.9rem 1.1rem; backdrop-filter: blur(14px);
    }}
    .stat-label {{ font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); }}
    .stat-value {{ font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.3rem; margin-top: 0.2rem; color: var(--text); }}

    /* ---------- AGENT CARDS ---------- */
    .agentcard {{
        background: var(--panel); border: 1px solid var(--panel-b); border-radius: 16px;
        padding: 1.2rem 1.4rem; margin-bottom: 1.1rem; backdrop-filter: blur(16px);
        border-left: 3px solid var(--edge, #666); animation: rise 0.5s ease both;
    }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .agentcard-head {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.7rem; }}
    .agentcard-name {{ font-family: 'Sora', sans-serif; font-weight: 700; font-size: 0.95rem; color: var(--edge, #fff); }}
    .agentcard-time {{ font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--muted); }}
    .agentcard-body {{
        font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; line-height: 1.6;
        color: #C9CFE3; max-height: 240px; overflow-y: auto; white-space: pre-wrap;
    }}

    /* ---------- REPORT ---------- */
    .report {{
        background: linear-gradient(180deg, rgba(244,114,182,0.07), rgba(255,255,255,0.03));
        border: 1px solid rgba(244,114,182,0.35); border-radius: 18px;
        padding: 1.8rem 2.1rem; margin-bottom: 1.2rem; backdrop-filter: blur(18px);
        animation: rise 0.6s ease both;
    }}
    .report-kicker {{
        font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--c-writer);
        text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;
    }}
    .report-title {{ font-family: 'Sora', sans-serif; font-weight: 800; font-size: 1.6rem; margin-bottom: 1rem; color: #fff; }}
    .report-body {{ font-size: 0.98rem; line-height: 1.8; color: #E4E7F2; }}

    .critic {{
        background: linear-gradient(180deg, rgba(251,191,36,0.09), rgba(255,255,255,0.03));
        border: 1px solid rgba(251,191,36,0.4); border-radius: 18px;
        padding: 1.4rem 1.7rem; margin-bottom: 1.2rem; backdrop-filter: blur(18px);
        animation: rise 0.7s ease both;
    }}
    .critic-tag {{
        font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--c-editor);
        text-transform: uppercase; letter-spacing: 0.1em; display: block; margin-bottom: 0.5rem;
    }}
    .critic-body {{ font-size: 0.94rem; line-height: 1.7; color: #F1E6C8; }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{ background: rgba(255,255,255,0.02); border-right: 1px solid var(--panel-b); }}
    .side-title {{ font-family:'Sora',sans-serif; font-weight:800; font-size:1.05rem; color:var(--text); }}
    .side-note  {{ color: var(--muted); font-size: 0.82rem; line-height:1.5; }}
    .history-row {{ font-size: 0.78rem; color: var(--muted); padding: 0.3rem 0; border-bottom: 1px solid var(--panel-b); }}

    div.stButton > button {{
        background: linear-gradient(90deg, var(--c-search), var(--c-reader));
        color: #06121A; font-weight: 700; font-family: 'Sora', sans-serif;
        border: none; border-radius: 10px; padding: 0.65rem 1rem; width: 100%;
        box-shadow: 0 6px 18px rgba(34,211,238,0.25);
    }}
    div.stButton > button:hover {{ filter: brightness(1.08); }}
    div[data-testid="stDownloadButton"] > button {{
        background: linear-gradient(90deg, var(--c-writer), var(--c-editor));
        color: #1A0B12; font-weight: 700; border: none; border-radius: 10px;
    }}
    </style>

    <div class="aurora"><span class="b1"></span><span class="b2"></span><span class="b3"></span></div>
    """),
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "state" not in st.session_state:
    st.session_state.state = None
if "stage" not in st.session_state:
    st.session_state.stage = -1

AGENTS = [
    {"key": "search", "name": "Search Agent",  "color": "#22D3EE", "verb": "scanning the web for sources"},
    {"key": "reader", "name": "Reader Agent",  "color": "#A78BFA", "verb": "reading the lead source in depth"},
    {"key": "writer", "name": "Writer Chain",  "color": "#F472B6", "verb": "drafting the report"},
    {"key": "editor", "name": "Critic Chain",  "color": "#FBBF24", "verb": "reviewing the report"},
]

# ----------------------------------------------------------------------------
# SIGNAL DECK — animated node-and-line component (self-contained HTML/CSS/SVG,
# rendered via components.html so it never runs into markdown parsing quirks)
# ----------------------------------------------------------------------------
def signal_deck(active: int) -> str:
    n = len(AGENTS)
    # fixed pixel coordinate space (viewBox), scaled uniformly - no stretch
    VB_W, VB_H = 1000, 90
    MARGIN = 110
    span = VB_W - 2 * MARGIN
    xs = [MARGIN + i * (span / (n - 1)) for i in range(n)]
    cy = VB_H / 2
    r = 24

    node_svg, label_html = "", ""
    for i, a in enumerate(AGENTS):
        x = xs[i]
        if active == -1:
            state = "pending"
        elif active == 4 or i < active:
            state = "done"
        elif i == active:
            state = "active"
        else:
            state = "pending"

        glow = a["color"] if state in ("active", "done") else "#3A3F52"
        fill = "#0B0E18" if state != "pending" else "#12141F"
        pulse_class = "pulse" if state == "active" else ""
        check = "&#10003;" if state == "done" else str(i + 1)

        node_svg += f"""
        <g class="{pulse_class}" style="color:{glow}">
          <circle cx="{x}" cy="{cy}" r="{r}" fill="{fill}" stroke="{glow}" stroke-width="2.5" />
          <text x="{x}" y="{cy}" text-anchor="middle" dominant-baseline="central"
                font-size="18" font-family="JetBrains Mono, monospace" fill="{glow}">{check}</text>
        </g>
        """
        left_pct = (x / VB_W) * 100
        status_text = a["verb"] if state == "active" else ("done" if state == "done" else "queued")
        label_html += f"""
        <div class="sd-label" style="left:{left_pct}%; --c:{glow}">
          <div class="sd-name">{a['name']}</div>
          <div class="sd-verb">{status_text}</div>
        </div>
        """

    segs = ""
    for i in range(n - 1):
        x1, x2 = xs[i] + r, xs[i + 1] - r
        lit = (active == 4) or (i < active)
        is_flowing = active not in (-1, 4) and i == active - 1
        color = AGENTS[i + 1]["color"] if (lit or is_flowing) else "#2A2E40"
        dash = "" if lit else 'stroke-dasharray="6 6"'
        anim_class = "flow" if is_flowing else ""
        segs += f'<line x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}" stroke="{color}" stroke-width="2.5" {dash} class="{anim_class}" />'

    return f"""
    <html>
    <head>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      body {{ background: transparent; font-family: 'Inter', sans-serif; overflow: hidden; }}
      .sd-wrap {{ position: relative; width: 100%; height: 170px; }}
      svg.sd-svg {{ display: block; width: 100%; height: 100px; overflow: visible; }}
      .pulse circle {{ animation: sdpulse 1.4s ease-in-out infinite; }}
      @keyframes sdpulse {{
        0%,100% {{ filter: drop-shadow(0 0 2px currentColor); }}
        50% {{ filter: drop-shadow(0 0 10px currentColor); }}
      }}
      line.flow {{ stroke-dasharray: 5 7; animation: dashmove 0.6s linear infinite; }}
      @keyframes dashmove {{ to {{ stroke-dashoffset: -24; }} }}
      .sd-label {{
        position: absolute; top: 106px; transform: translateX(-50%); width: 160px; text-align: center;
      }}
      .sd-name {{ font-family: 'Sora', sans-serif; font-weight: 700; font-size: 13px; color: var(--c); }}
      .sd-verb {{ font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #7C84A0; margin-top: 3px; }}
    </style>
    </head>
    <body>
      <div class="sd-wrap">
        <svg class="sd-svg" viewBox="0 0 {VB_W} {VB_H}" preserveAspectRatio="xMidYMid meet">
          {segs}
          {node_svg}
        </svg>
        {label_html}
      </div>
    </body>
    </html>
    """

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="side-title">✦ Signal Deck</div>', unsafe_allow_html=True)
    st.markdown(
        html("""
        <div class="side-note">Give the deck a topic. Four agents relay it —
        search, read, write, critique — and you watch the signal move between
        them live.</div>
        """),
        unsafe_allow_html=True,
    )
    st.markdown("---")
    topic = st.text_area(
        "Research topic",
        placeholder="e.g. Impact of small modular nuclear reactors on grid stability",
        height=100,
    )
    run_clicked = st.button("⚡ Run the deck", use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="side-title" style="font-size:0.95rem;">Run history</div>', unsafe_allow_html=True)
    if st.session_state.history:
        rows = "".join(
            f'<div class="history-row">#{len(st.session_state.history)-i:02d} · {h["topic"]} '
            f'<span style="opacity:0.5;">({h["timestamp"]})</span></div>'
            for i, h in enumerate(reversed(st.session_state.history[-8:]))
        )
        st.markdown(html(rows), unsafe_allow_html=True)
    else:
        st.markdown('<div class="side-note">No runs yet.</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
run_no = len(st.session_state.history)
now_str = datetime.datetime.now().strftime("%d %b %Y · %H:%M")
st.markdown(
    html(f"""
    <div class="topbar">
      <div class="brand">
        <div class="brand-dot"></div>
        <div>
          <p class="brand-title">AI Research Agent</p>
          <p class="brand-sub">Search → Read → Write → Critique, running as a live multi-agent relay</p>
        </div>
      </div>
      <div class="topbar-meta">RUN #{run_no:03d}<br>{now_str}</div>
    </div>
    """),
    unsafe_allow_html=True,
)

deck_slot = st.empty()
stats_slot = st.empty()

def render_deck(active: int):
    with deck_slot:
        st.iframe(signal_deck(active), height=180)

def render_stats(state: dict | None, active: int):
    src_chars = len(state["search_results"]) if state and "search_results" in state else 0
    scraped_chars = len(state["scraped_content"]) if state and "scraped_content" in state else 0
    report_words = len(state["report"].split()) if state and "report" in state else 0
    status = "Idle" if active == -1 else ("Complete" if active == 4 else "Running")
    stats_slot.markdown(
        html(f"""
        <div class="stats">
          <div class="stat"><div class="stat-label">Status</div><div class="stat-value">{status}</div></div>
          <div class="stat"><div class="stat-label">Search chars</div><div class="stat-value">{src_chars:,}</div></div>
          <div class="stat"><div class="stat-label">Scraped chars</div><div class="stat-value">{scraped_chars:,}</div></div>
          <div class="stat"><div class="stat-label">Report words</div><div class="stat-value">{report_words:,}</div></div>
        </div>
        """),
        unsafe_allow_html=True,
    )

render_deck(st.session_state.stage)
render_stats(st.session_state.state, st.session_state.stage)

search_slot = st.container()
reader_slot = st.container()
report_slot = st.container()
critic_slot = st.container()

# ----------------------------------------------------------------------------
# RENDER HELPERS
# ----------------------------------------------------------------------------
def render_agent_card(container, name, color, body, timestamp):
    with container:
        st.markdown(
            html(f"""
            <div class="agentcard" style="--edge:{color}">
              <div class="agentcard-head">
                <span class="agentcard-name">{name}</span>
                <span class="agentcard-time">{timestamp}</span>
              </div>
              <div class="agentcard-body">{body}</div>
            </div>
            """),
            unsafe_allow_html=True,
        )

def render_report(container, topic, report):
    with container:
        st.markdown(
            html(f"""
            <div class="report">
              <div class="report-kicker">Writer Chain · Final Draft</div>
              <div class="report-title">{topic}</div>
              <div class="report-body">{report}</div>
            </div>
            """),
            unsafe_allow_html=True,
        )

def render_critic(container, feedback):
    with container:
        st.markdown(
            html(f"""
            <div class="critic">
              <span class="critic-tag">◆ Critic chain — review notes</span>
              <div class="critic-body">{feedback}</div>
            </div>
            """),
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# PIPELINE EXECUTION
# ----------------------------------------------------------------------------
def run_pipeline_with_live_ui(topic: str):
    state = {}
    now = lambda: datetime.datetime.now().strftime("%H:%M:%S")

    st.session_state.stage = 0
    render_deck(0); render_stats(state, 0)
    with st.spinner("Search agent is looking for sources..."):
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
    state["search_results"] = search_result["messages"][-1].content
    render_agent_card(search_slot, "Search Agent", "#22D3EE", state["search_results"], now())
    render_stats(state, 0)

    st.session_state.stage = 1
    render_deck(1); render_stats(state, 1)
    with st.spinner("Reader agent is scraping the top source..."):
        reader_agent = build_scraping_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
    state["scraped_content"] = reader_result["messages"][-1].content
    render_agent_card(reader_slot, "Reader Agent", "#A78BFA", state["scraped_content"], now())
    render_stats(state, 1)

    st.session_state.stage = 2
    render_deck(2); render_stats(state, 2)
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    with st.spinner("Writer chain is drafting the report..."):
        state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
    render_report(report_slot, topic, state["report"])
    render_stats(state, 2)

    st.session_state.stage = 3
    render_deck(3); render_stats(state, 3)
    with st.spinner("Critic chain is reviewing the report..."):
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
    render_critic(critic_slot, state["feedback"])

    st.session_state.stage = 4
    render_deck(4); render_stats(state, 4)
    return state

# ----------------------------------------------------------------------------
# MAIN TRIGGER
# ----------------------------------------------------------------------------
if run_clicked:
    if not topic or not topic.strip():
        st.warning("Enter a topic before running the deck.")
    else:
        st.session_state.history.append({
            "topic": topic.strip(),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        })
        try:
            result = run_pipeline_with_live_ui(topic.strip())
            st.session_state.state = result
            st.success("Run complete — report reviewed and ready.")
            st.download_button(
                "⬇ Download report (.md)",
                data=result["report"],
                file_name=f"research_report_{datetime.date.today()}.md",
                mime="text/markdown",
            )
        except Exception as e:
            st.session_state.stage = -1
            render_deck(-1); render_stats(None, -1)
            st.error(f"The pipeline hit an error: {e}")

elif st.session_state.state:
    state = st.session_state.state
    render_deck(4); render_stats(state, 4)
    render_agent_card(search_slot, "Search Agent", "#22D3EE", state["search_results"], "—")
    render_agent_card(reader_slot, "Reader Agent", "#A78BFA", state["scraped_content"], "—")
    render_report(report_slot, st.session_state.history[-1]["topic"] if st.session_state.history else "Report", state["report"])
    render_critic(critic_slot, state["feedback"])
    st.download_button(
        "⬇ Download report (.md)",
        data=state["report"],
        file_name=f"research_report_{datetime.date.today()}.md",
        mime="text/markdown",
    )
else:
    st.info("👈 Enter a topic in the sidebar and press **Run the deck** to send the agents to work.")
