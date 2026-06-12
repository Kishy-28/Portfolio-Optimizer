APP_CSS = """
    <style>
    /* ---------------------------------------------------------------
       Fonts & global typography
       --------------------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,300..500,0..1,-50..200&display=block');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

    html,
    body,
    body *,
    [class*="css"],
    [class*="st-"],
    [data-testid],
    [data-baseweb] {
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
    }

    .stMarkdown,
    .stMarkdown *,
    .stCaptionContainer,
    .stCaptionContainer *,
    .stAlert,
    .stAlert *,
    .stButton button,
    .stDownloadButton button,
    .stTextInput *,
    .stNumberInput *,
    .stDateInput *,
    .stSelectbox *,
    .stDataFrame *,
    .stTable *,
    .stMetric *,
    .js-plotly-plot,
    .js-plotly-plot * {
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
    }

    .material-icons,
    .material-icons-outlined,
    .material-icons-round,
    .material-icons-sharp,
    .material-symbols-outlined,
    .material-symbols-rounded,
    .material-symbols-sharp,
    [class*="material-icons"],
    [class*="material-symbols"] {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: 400 !important;
        font-style: normal !important;
        font-size: 1rem !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: 'liga' !important;
    }

    /* ---------------------------------------------------------------
       App background & base layout
       --------------------------------------------------------------- */
    .stApp {
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
        background:
            linear-gradient(180deg, #02070D 0%, #07111D 44%, #08131F 100%);
        color: #F9FAFB;
        letter-spacing: 0.005em;
    }

    .block-container {
        padding-top: 0.55rem;
        padding-bottom: 1.7rem;
        max-width: 1480px;
        border-left: 1px solid rgba(56, 189, 248, 0.12);
        border-right: 1px solid rgba(56, 189, 248, 0.12);
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.78rem !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    h1 {
        font-size: 2.18rem !important;
        font-weight: 560 !important;
        letter-spacing: 0.005em !important;
        color: #F9FAFB !important;
        margin-bottom: 0.48rem !important;
    }

    h2 {
        font-size: 1.34rem !important;
        font-weight: 540 !important;
        letter-spacing: 0.006em !important;
        color: #F9FAFB !important;
    }

    h3 {
        font-size: 1.02rem !important;
        font-weight: 520 !important;
        letter-spacing: 0.006em !important;
        color: #F9FAFB !important;
    }

    p, li, span, div {
        color: inherit;
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
        font-weight: 400;
    }

    span.material-icons,
    span.material-icons-outlined,
    span.material-icons-round,
    span.material-icons-sharp,
    span.material-symbols-outlined,
    span.material-symbols-rounded,
    span.material-symbols-sharp,
    span[class*="material-icons"],
    span[class*="material-symbols"],
    i[class*="material-icons"],
    i[class*="material-symbols"],
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] * {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: 400 !important;
        font-size: 1rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        font-feature-settings: 'liga' !important;
    }

    /* ---------------------------------------------------------------
       Sidebar
       --------------------------------------------------------------- */
    button,
    input,
    textarea,
    label,
    [data-testid="stSidebar"],
    [data-testid="stDataFrame"],
    [data-testid="stTable"],
    [data-baseweb="tab"],
    [data-baseweb="input"],
    [data-baseweb="select"] {
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #030A12 0%, #06111D 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.18);
        box-shadow: inset -1px 0 0 rgba(15, 23, 42, 0.8);
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.56rem !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #F9FAFB !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #CBD5E1 !important;
    }

    [data-testid="stSidebar"] input {
        background-color: #0B1220 !important;
        color: #F9FAFB !important;
        border: 1px solid rgba(148, 163, 184, 0.20) !important;
        border-radius: 7px !important;
        min-height: 2rem !important;
        font-size: 0.82rem !important;
        line-height: 1.1 !important;
    }

    [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        background-color: #0B1220 !important;
        color: #F9FAFB !important;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div {
        background-color: #0B1220 !important;
        border-color: rgba(148, 163, 184, 0.20) !important;
        border-radius: 7px !important;
        min-height: 2rem !important;
    }

    [data-testid="stWidgetLabel"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stTextInput"] label,
    [data-testid="stDateInput"] label {
        font-size: 0.76rem !important;
        margin-bottom: 0.16rem !important;
    }

    [data-testid="stNumberInput"] input {
        text-align: right !important;
        font-variant-numeric: tabular-nums !important;
    }

    [data-baseweb="menu"] li {
        background-color: #0B1220 !important;
        color: #E5E7EB !important;
    }

    [data-testid="stSidebar"] button {
        border-radius: 8px !important;
        min-height: 2.38rem !important;
        font-weight: 520 !important;
        background: linear-gradient(135deg, #1D4ED8, #0891B2) !important;
        color: white !important;
        border: 1px solid rgba(56, 189, 248, 0.42) !important;
        box-shadow: 0 10px 24px rgba(14, 165, 233, 0.18);
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] button {
        width: 1.45rem !important;
        min-width: 1.45rem !important;
        height: 1.45rem !important;
        min-height: 1.45rem !important;
        padding: 0 !important;
        border-radius: 6px !important;
        background: rgba(15, 23, 42, 0.72) !important;
        border: 1px solid rgba(100, 116, 139, 0.18) !important;
        color: #64748B !important;
        box-shadow: none !important;
        font-size: 0.72rem !important;
        font-weight: 400 !important;
        line-height: 1 !important;
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover {
        background: rgba(30, 41, 59, 0.72) !important;
        border-color: rgba(100, 116, 139, 0.28) !important;
        color: #94A3B8 !important;
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] button svg,
    [data-testid="stSidebar"] [data-testid="stNumberInput"] button span {
        width: 0.72rem !important;
        height: 0.72rem !important;
        font-size: 0.72rem !important;
        color: #64748B !important;
    }

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    button[aria-label="Open sidebar"],
    button[aria-label="Close sidebar"] {
        position: fixed !important;
        top: 0.52rem !important;
        left: 0.58rem !important;
        width: 1.65rem !important;
        height: 1.65rem !important;
        min-width: 1.65rem !important;
        max-width: 1.65rem !important;
        overflow: hidden !important;
        font-size: 0 !important;
        color: transparent !important;
        line-height: 0 !important;
        z-index: 999999 !important;
    }

    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] *,
    button[aria-label="Open sidebar"] *,
    button[aria-label="Close sidebar"] * {
        display: none !important;
        font-size: 0 !important;
        color: transparent !important;
        line-height: 0 !important;
    }

    [data-testid="stSidebarCollapseButton"]::before,
    [data-testid="collapsedControl"]::before,
    button[aria-label="Open sidebar"]::before,
    button[aria-label="Close sidebar"]::before {
        content: "\\2039";
        display: grid;
        place-items: center;
        width: 1.65rem;
        height: 1.65rem;
        border-radius: 7px;
        color: #7B8AA0;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(100, 116, 139, 0.18);
        font-size: 1rem;
        line-height: 1;
    }

    .sidebar-brand {
        padding: 0.05rem 0 0.35rem 0;
        display: grid;
        grid-template-columns: 1fr auto;
        align-items: center;
        gap: 0.56rem;
    }

    .sidebar-kicker {
        color: #AAB6C5;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 500;
        line-height: 1.05;
    }

    .sidebar-title {
        color: #F8FAFC;
        font-size: 0.94rem;
        font-weight: 650;
        letter-spacing: 0.07em;
        line-height: 1.05;
        text-transform: uppercase;
        margin-top: 0;
    }

    /* ---------------------------------------------------------------
       Top bar / header
       --------------------------------------------------------------- */
    .top-shell {
        min-height: 50px;
        margin: 0 -1rem 1.05rem;
        padding: 0 1rem;
        display: grid;
        grid-template-columns: minmax(190px, 0.64fr) minmax(0, 1.7fr);
        gap: 1rem;
        align-items: center;
        background: rgba(2, 8, 15, 0.92);
        border-bottom: 1px solid rgba(148, 163, 184, 0.16);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
    }

    .top-brand {
        display: flex;
        align-items: center;
        gap: 0.72rem;
        min-width: 0;
    }

    .brand-text {
        color: #F8FAFC;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-size: 0.88rem;
        line-height: 1.08;
        font-weight: 650;
    }

    .brand-text div:nth-child(2) {
        color: #AAB6C5;
        font-size: 0.66rem;
        letter-spacing: 0.18em;
        font-weight: 500;
    }

    .live-pill {
        color: #4ADE80;
        background: rgba(34, 197, 94, 0.16);
        border: 1px solid rgba(34, 197, 94, 0.24);
        border-radius: 5px;
        padding: 0.12rem 0.34rem;
        font-size: 0.6rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    .top-meta {
        display: grid;
        grid-template-columns: repeat(4, minmax(116px, 1fr));
        align-items: center;
        gap: 0;
        min-width: 0;
        border-left: 1px solid rgba(148, 163, 184, 0.22);
    }

    .meta-item {
        min-width: 0;
        padding: 0.25rem 0.86rem;
        border-right: 1px solid rgba(148, 163, 184, 0.18);
    }

    .meta-item span {
        display: block;
        color: #7DD3FC;
        font-size: 0.58rem;
        font-weight: 600;
        margin-bottom: 0.12rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        white-space: nowrap;
    }

    .meta-item strong {
        display: block;
        color: #D7E0EA;
        font-size: 0.74rem;
        font-weight: 460;
        line-height: 1.24;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* ---------------------------------------------------------------
       Hero / mode strip
       --------------------------------------------------------------- */
    .hero-card {
        width: min(100%, 1180px);
        padding: 0.2rem 0 0.58rem;
        border-radius: 0;
        background: transparent;
        border: 0;
        margin: 0 auto 0.72rem;
        box-shadow: none;
        position: relative;
    }

    .hero-card::before {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        display: none;
    }

    .hero-title {
        font-size: clamp(1.88rem, 3vw, 2.72rem);
        font-weight: 700;
        color: #F9FAFB;
        margin-bottom: 0.2rem;
        letter-spacing: 0;
        line-height: 1.12;
    }

    .hero-subtitle {
        font-size: 0.98rem;
        color: #C6D0DD;
        max-width: 920px;
        line-height: 1.38;
        font-weight: 380;
        letter-spacing: 0.01em;
    }

    .hero-card .section-label {
        margin-bottom: 0.5rem;
        color: #7DD3FC;
    }

    .mode-strip {
        width: min(100%, 1180px);
        margin: 0 auto 0.76rem;
        display: flex;
        align-items: center;
        gap: 0.45rem;
        color: #AAB6C5;
        font-size: 0.74rem;
    }

    .mode-strip span {
        width: 0.45rem;
        height: 0.45rem;
        border-radius: 999px;
        background: #22C55E;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.36);
    }

    /* ---------------------------------------------------------------
       Section cards & metric cards
       --------------------------------------------------------------- */
    .section-card {
        padding: 0.86rem 1rem;
        border-radius: 8px;
        background: rgba(12, 18, 31, 0.76);
        border: 1px solid rgba(148, 163, 184, 0.14);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
        margin-bottom: 0.78rem;
    }

    .section-label {
        font-size: 0.64rem;
        color: #38BDF8;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        margin-bottom: 0.44rem;
        font-weight: 500;
    }

    .section-title {
        font-size: 1.08rem;
        line-height: 1.34;
        color: #F9FAFB;
        font-weight: 520;
        letter-spacing: 0.006em;
        margin-bottom: 0.35rem;
    }

    .section-description {
        font-size: 0.86rem;
        color: #AAB6C5;
        line-height: 1.5;
        font-weight: 380;
    }

    .metric-card {
        min-height: 72px;
        padding: 0.64rem 0.82rem;
        border-radius: 8px;
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(8, 13, 24, 0.88));
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.27);
        margin-bottom: 0.52rem;
        position: relative;
        overflow: hidden;
    }

    .metric-card::after {
        content: "";
        position: absolute;
        right: 0.9rem;
        bottom: 0.82rem;
        width: 4rem;
        height: 1rem;
        opacity: 0.82;
        background:
            linear-gradient(135deg, transparent 12%, currentColor 13%, currentColor 16%, transparent 17%),
            linear-gradient(45deg, transparent 30%, currentColor 31%, currentColor 34%, transparent 35%);
        clip-path: polygon(0 76%, 16% 56%, 29% 62%, 43% 39%, 58% 50%, 73% 24%, 86% 35%, 100% 5%, 100% 16%, 86% 48%, 73% 36%, 58% 64%, 43% 53%, 30% 77%, 16% 69%, 0 90%);
    }

    .metric-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #94A3B8;
        font-weight: 500;
        margin-bottom: 0.28rem;
    }

    .metric-value {
        font-size: 1.14rem;
        line-height: 1.15;
        font-weight: 540;
        letter-spacing: 0.004em;
        margin-bottom: 0.26rem;
        overflow-wrap: anywhere;
    }

    .metric-caption {
        font-size: 0.72rem;
        color: #AAB6C5;
        font-weight: 380;
        line-height: 1.5;
    }

    .metric-blue .metric-value { color: #3B82F6; }
    .metric-green .metric-value { color: #22C55E; }
    .metric-purple .metric-value { color: #A855F7; }
    .metric-cyan .metric-value { color: #22D3EE; }
    .metric-yellow .metric-value { color: #FACC15; }
    .metric-red .metric-value { color: #EF4444; }
    .metric-blue { color: #1687FF; }
    .metric-green { color: #22C55E; }
    .metric-purple { color: #A855F7; }
    .metric-cyan { color: #22D3EE; }
    .metric-yellow { color: #FACC15; }
    .metric-red { color: #EF4444; }

    /* ---------------------------------------------------------------
       Reference overview: dashboard panels, performance chart,
       allocation breakdown, and risk list
       --------------------------------------------------------------- */
    .reference-grid {
        width: min(100%, 1180px);
        margin: 0 auto 0.78rem;
        display: grid;
        grid-template-columns: minmax(0, 1.55fr) minmax(280px, 0.9fr);
        gap: 0.74rem;
    }

    .dashboard-panel {
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(8, 18, 31, 0.92), rgba(4, 11, 20, 0.9));
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.24);
        padding: 0.84rem 0.92rem;
        overflow: hidden;
    }

    .performance-panel {
        grid-row: span 2;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.62rem;
    }

    .panel-header span {
        color: #F8FAFC;
        text-transform: none;
        font-size: 0.82rem;
        letter-spacing: 0;
        font-weight: 600;
    }

    .performance-chart {
        width: 100%;
        height: 220px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        background:
            linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
        background-size: 100% 25%, 16.66% 100%;
    }

    .performance-chart-placeholder {
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0 1.5rem;
        color: #7B8AA0;
        font-size: 0.82rem;
    }

    .performance-stats {
        display: grid;
        grid-template-columns: repeat(5, minmax(88px, 1fr));
        gap: 0;
        padding-top: 0.62rem;
        overflow-x: auto;
    }

    .performance-stats div {
        min-width: 0;
        padding: 0 0.7rem;
        border-left: 1px solid rgba(148, 163, 184, 0.16);
    }

    .performance-stats div:first-child {
        border-left: 0;
    }

    .performance-stats span,
    .risk-list span {
        display: block;
        color: #AAB6C5;
        font-size: clamp(0.58rem, 0.78vw, 0.68rem);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.3rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .performance-stats strong {
        display: block;
        font-size: clamp(1rem, 1.45vw, 1.18rem);
        font-weight: 600;
        white-space: nowrap;
        line-height: 1.15;
    }

    .positive { color: #22C55E !important; }
    .negative { color: #EF4444 !important; }
    .blue { color: #1687FF !important; }
    .purple { color: #A855F7 !important; }
    .yellow { color: #FACC15 !important; }
    .cyan { color: #22D3EE !important; }

    .allocation-body {
        display: grid;
        grid-template-columns: minmax(112px, 132px) minmax(0, 1fr);
        align-items: center;
        gap: 0.85rem;
    }

    .allocation-ring {
        width: clamp(112px, 11vw, 132px);
        height: clamp(112px, 11vw, 132px);
        border-radius: 999px;
        background: conic-gradient(#1687FF 0 40%, #23C7C9 40% 100%);
        display: grid;
        place-items: center;
        position: relative;
        color: #FFFFFF;
        font-size: 0.8rem;
    }

    .allocation-ring::after {
        content: "";
        width: 58px;
        height: 58px;
        border-radius: 999px;
        background: #06111D;
        position: absolute;
    }

    .allocation-ring span {
        position: relative;
        z-index: 1;
    }

    .allocation-legend {
        display: grid;
        gap: 0.78rem;
        min-width: 0;
    }

    .allocation-legend div,
    .risk-list div {
        display: grid;
        grid-template-columns: auto minmax(0, 1fr) auto;
        gap: 0.48rem;
        align-items: center;
        color: #D6DEE9;
        font-size: clamp(0.76rem, 0.95vw, 0.85rem);
        min-width: 0;
        white-space: nowrap;
    }

    .allocation-legend strong,
    .risk-list strong {
        white-space: nowrap;
        justify-self: end;
    }

    .allocation-legend i {
        width: 0.72rem;
        height: 0.72rem;
        border-radius: 999px;
    }

    .blue-dot { background: #1687FF; }
    .cyan-dot { background: #23C7C9; }

    .risk-list {
        display: grid;
        gap: 0.48rem;
    }

    .risk-list div {
        grid-template-columns: 1fr auto;
        padding-bottom: 0.36rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.10);
    }

    .risk-list span {
        display: inline-flex;
        align-items: center;
        gap: 0.42rem;
    }

    .risk-dot {
        width: 0.48rem;
        height: 0.48rem;
        border-radius: 999px;
        display: inline-block;
        flex: 0 0 auto;
    }

    .red-dot { background: rgba(239, 68, 68, 0.72); }
    .slate-dot { background: rgba(148, 163, 184, 0.72); }
    .yellow-dot { background: rgba(250, 204, 21, 0.82); }

    .risk-list div:last-child {
        border-bottom: 0;
        padding-bottom: 0;
    }

    .conclusion-panel p,
    .insight-panel li {
        color: #C6D0DD;
        font-size: 0.8rem;
        line-height: 1.46;
    }

    .insight-panel ul {
        display: grid;
        gap: 0.54rem;
        padding-left: 1.1rem;
        margin: 0;
    }

    /* ---------------------------------------------------------------
       Responsive layout
       --------------------------------------------------------------- */
    @media (max-width: 1100px) {
        .top-shell,
        .reference-grid {
            grid-template-columns: 1fr;
        }

        .top-meta {
            display: none;
        }

        .performance-stats {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.8rem;
        }
    }

    /* ---------------------------------------------------------------
       Native Streamlit widget overrides (metrics, dataframes, tables,
       charts, buttons, tabs, alerts)
       --------------------------------------------------------------- */
    div[data-testid="stMetric"] {
        border: 1px solid rgba(148, 163, 184, 0.15);
        padding: 0.82rem;
        border-radius: 8px;
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(8, 13, 24, 0.88));
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.27);
    }

    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        font-weight: 500;
    }

    div[data-testid="stMetricValue"] {
        color: #F9FAFB !important;
        font-weight: 540;
        letter-spacing: 0.004em;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(148, 163, 184, 0.14) !important;
        border-radius: 8px !important;
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.84), rgba(8, 13, 24, 0.78));
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.24);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.16);
        background: #0B1220 !important;
        color: #D6DEE9 !important;
        font-size: 0.82rem !important;
    }

    div[data-testid="stDataFrame"] div {
        background-color: transparent !important;
        color: #D6DEE9 !important;
    }

    div[data-testid="stDataFrame"] [role="grid"],
    div[data-testid="stDataFrame"] [data-testid="stTable"],
    div[data-testid="stDataFrame"] canvas {
        background-color: #0B1220 !important;
        color: #D6DEE9 !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"],
    div[data-testid="stDataFrame"] [role="rowheader"] {
        background-color: #101827 !important;
        color: #E5E7EB !important;
        font-weight: 500 !important;
    }

    div[data-testid="stDataFrame"] [role="gridcell"] {
        background-color: #0B1220 !important;
        color: #D6DEE9 !important;
    }

    div[data-testid="stTable"],
    div[data-testid="stTable"] table,
    div[data-testid="stTable"] thead,
    div[data-testid="stTable"] tbody,
    div[data-testid="stTable"] tr,
    div[data-testid="stTable"] th,
    div[data-testid="stTable"] td {
        background-color: #0B1220 !important;
        color: #D6DEE9 !important;
        border-color: rgba(148, 163, 184, 0.14) !important;
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
    }

    div[data-testid="stTable"] th {
        background-color: #101827 !important;
        color: #E5E7EB !important;
        font-weight: 500 !important;
    }

    div[data-testid="stPlotlyChart"] {
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 8px;
        padding: 0.38rem;
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.78), rgba(8, 13, 24, 0.72));
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 8px;
        min-height: 2.38rem;
        font-weight: 520;
        letter-spacing: 0.01em;
        background: linear-gradient(135deg, #1D4ED8, #0891B2);
        color: white;
        border: 1px solid rgba(56, 189, 248, 0.42);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.28rem;
        background: rgba(5, 10, 20, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 8px;
        padding: 0.26rem;
        margin-bottom: 0.82rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 34px;
        border-radius: 7px;
        color: #CBD5E1;
        font-weight: 430;
        letter-spacing: 0.01em;
        padding: 0 0.72rem;
        font-size: 0.82rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(29, 78, 216, 0.88), rgba(8, 145, 178, 0.78));
        color: #FFFFFF !important;
        font-weight: 520 !important;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.18);
    }

    .stAlert {
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    hr {
        border-color: rgba(148, 163, 184, 0.12);
    }
    </style>
"""
