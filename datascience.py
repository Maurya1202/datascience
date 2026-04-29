import streamlit as st
import pandas as pd
from supabase import create_client, Client
import datetime

# --- CONFIGURATION ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
ADMIN_USER = st.secrets["ADMIN_USER"]
ADMIN_PASS = st.secrets["ADMIN_PASS"]

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_supabase()

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Data Science Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize theme in session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- ULTIMATE CSS STYLING WITH DARK/LIGHT MODE ---
st.markdown(f"""
<style>
    /* IMPORT MODERN FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    * {{
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    /* THEME VARIABLES */
    :root {{
        --bg-primary: {'#0f0f23' if st.session_state.dark_mode else '#f8f9fa'};
        --bg-secondary: {'#1a1a2e' if st.session_state.dark_mode else '#ffffff'};
        --bg-card: {'#16213e' if st.session_state.dark_mode else '#ffffff'};
        --text-primary: {'#ffffff' if st.session_state.dark_mode else '#1a1a2e'};
        --text-secondary: {'#b8b8d4' if st.session_state.dark_mode else '#64748b'};
        --accent-primary: #667eea;
        --accent-secondary: #764ba2;
        --shadow-color: {'rgba(0, 0, 0, 0.5)' if st.session_state.dark_mode else 'rgba(0, 0, 0, 0.1)'};
    }}
    
    /* HIDE DEFAULT ELEMENTS */
    [data-testid="stSidebar"] {{ display: none; }} 
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    [data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    .stApp > header {{ display: none !important; }}
    [data-testid="stDecoration"] {{ display: none !important; }}
    
    /* Remove top padding */
    .main .block-container {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    
    section[data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    div[data-testid="stStatusWidget"] {{
        display: none !important;
    }}
    
    /* SMOOTH SCROLLING */
    html {{
        scroll-behavior: smooth;
    }}
    
    /* BASE APP STYLING */
    .stApp {{
        background: var(--bg-primary);
        transition: background 0.3s ease;
    }}
    
    /* ANIMATED BACKGROUND PARTICLES */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(102, 126, 234, 0.05) 0%, transparent 50%);
        animation: particleFloat 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }}
    
    @keyframes particleFloat {{
        0%, 100% {{ transform: translate(0, 0) scale(1); }}
        33% {{ transform: translate(30px, -30px) scale(1.1); }}
        66% {{ transform: translate(-20px, 20px) scale(0.9); }}
    }}
    
    /* MAIN CONTAINER */
    .main-container {{
        background: var(--bg-secondary);
        backdrop-filter: blur(20px);
        padding: 25px;
        margin: 90px auto 20px auto;
        max-width: 1400px;
        animation: containerFadeIn 0.6s ease;
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }}
    
    @keyframes containerFadeIn {{
        from {{
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}
    
    /* NAVIGATION BAR */
    .nav-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
        box-shadow: 0 5px 30px rgba(102, 126, 234, 0.4);
        animation: navSlideDown 0.6s ease;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        overflow: hidden;
    }}
    
    .nav-bar::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: navShine 3s infinite;
    }}
    
    @keyframes navShine {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    @keyframes navSlideDown {{
        from {{
            opacity: 0;
            transform: translateY(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .nav-logo {{
        font-size: 32px;
        font-weight: 900;
        color: white;
        text-decoration: none;
        letter-spacing: -1px;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        position: relative;
        z-index: 1;
    }}
    
    .nav-logo:hover {{
        transform: scale(1.05) rotate(-2deg);
        filter: drop-shadow(0 0 20px rgba(255,255,255,0.5));
    }}
    
    /* WATERMARK STYLING */
    .watermark {{
        position: absolute;
        top: -22px;
        left: 0;
        font-size: 0.75rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.7);
        letter-spacing: 1px;
        text-transform: uppercase;
        z-index: 2;
    }}
    
    .nav-controls {{
        display: flex;
        gap: 15px;
        align-items: center;
        position: relative;
        z-index: 1;
    }}
    
    /* THEME TOGGLE BUTTON */
    .theme-toggle {{
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        color: white;
        border-radius: 50px;
        padding: 10px 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }}
    
    .theme-toggle:hover {{
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    
    /* HERO SECTION */
    .hero-box {{
        text-align: center;
        padding: 100px 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 30px;
        margin-bottom: 50px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        animation: heroAppear 1s ease;
    }}
    
    @keyframes heroAppear {{
        from {{
            opacity: 0;
            transform: scale(0.9);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    /* Animated gradient background */
    .hero-box::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(
            from 0deg,
            transparent,
            rgba(255,255,255,0.1),
            transparent 60deg
        );
        animation: heroRotate 8s linear infinite;
    }}
    
    @keyframes heroRotate {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .hero-content {{
        position: relative;
        z-index: 1;
    }}
    
    .hero-title {{
        font-size: 4.5rem;
        font-weight: 900;
        color: white;
        margin: 0;
        text-shadow: 0 5px 30px rgba(0, 0, 0, 0.3);
        animation: titleFloat 3s ease-in-out infinite;
        line-height: 1.2;
    }}
    
    @keyframes titleFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .hero-subtitle {{
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(45deg, #fff, #ffd700, #fff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 15px;
        animation: gradientFlow 3s ease infinite;
    }}
    
    @keyframes gradientFlow {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    
    .hero-text {{
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.95);
        margin-top: 30px;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.8;
        animation: fadeInUp 1s ease 0.3s both;
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .hero-cta {{
        display: inline-flex;
        gap: 20px;
        margin-top: 40px;
        animation: fadeInUp 1s ease 0.6s both;
    }}
    
    .cta-button {{
        padding: 15px 40px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
        display: inline-flex;
        align-items: center;
        gap: 10px;
    }}
    
    .cta-primary {{
        background: white;
        color: #667eea;
        box-shadow: 0 5px 20px rgba(255,255,255,0.3);
    }}
    
    .cta-primary:hover {{
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(255,255,255,0.5);
    }}
    
    .cta-secondary {{
        background: rgba(255,255,255,0.2);
        color: white;
        border: 2px solid rgba(255,255,255,0.5);
        backdrop-filter: blur(10px);
    }}
    
    .cta-secondary:hover {{
        background: rgba(255,255,255,0.3);
        transform: translateY(-3px) scale(1.05);
    }}
    
    /* SECTION TITLES */
    .section-title {{
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 40px;
        text-align: center;
        position: relative;
        animation: fadeIn 1s ease;
    }}
    
    .section-title::after {{
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 2px;
        animation: expandWidth 1s ease;
    }}
    
    @keyframes expandWidth {{
        from {{ width: 0; }}
        to {{ width: 100px; }}
    }}
    
    /* SUBJECT CARDS GRID */
    .cards-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 30px;
        margin-top: 50px;
        animation: fadeIn 1s ease;
    }}
    
    .subject-card {{
        background: var(--bg-card);
        padding: 45px 35px;
        border-radius: 25px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px var(--shadow-color);
        border: 2px solid transparent;
        animation: cardAppear 0.6s ease both;
    }}
    
    .subject-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        opacity: 0;
        transition: opacity 0.4s ease;
        z-index: 0;
    }}
    
    .subject-card:hover::before {{
        opacity: 1;
    }}
    
    .subject-card:hover {{
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
        border-color: var(--accent-primary);
    }}
    
    .subject-card:hover .card-content {{
        color: white;
    }}
    
    .card-content {{
        position: relative;
        z-index: 1;
        transition: color 0.4s ease;
    }}
    
    .card-icon {{
        font-size: 80px;
        margin-bottom: 25px;
        display: inline-block;
        animation: iconBounce 2s ease-in-out infinite;
        filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.2));
        transition: transform 0.4s ease;
    }}
    
    .subject-card:hover .card-icon {{
        transform: scale(1.2) rotate(5deg);
        animation: iconSpin 0.6s ease;
    }}
    
    @keyframes iconSpin {{
        0% {{ transform: rotate(0deg) scale(1); }}
        50% {{ transform: rotate(180deg) scale(1.2); }}
        100% {{ transform: rotate(360deg) scale(1.2); }}
    }}
    
    @keyframes iconBounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-15px); }}
    }}
    
    .card-title {{
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        transition: color 0.3s ease;
    }}
    
    .card-desc {{
        font-size: 1rem;
        color: var(--text-secondary);
        margin-top: 10px;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.4s ease;
    }}
    
    .subject-card:hover .card-desc {{
        opacity: 1;
        transform: translateY(0);
        color: rgba(255,255,255,0.9);
    }}
    
    /* Staggered animation for cards */
    .subject-card:nth-child(1) {{ animation-delay: 0.1s; }}
    .subject-card:nth-child(2) {{ animation-delay: 0.2s; }}
    .subject-card:nth-child(3) {{ animation-delay: 0.3s; }}
    .subject-card:nth-child(4) {{ animation-delay: 0.4s; }}
    .subject-card:nth-child(5) {{ animation-delay: 0.5s; }}
    .subject-card:nth-child(6) {{ animation-delay: 0.6s; }}
    
    @keyframes cardAppear {{
        from {{
            opacity: 0;
            transform: translateY(50px) scale(0.9);
        }}
        to {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}
    
    /* RESOURCE ITEMS */
    .resource-item {{
        background: var(--bg-card);
        border: 2px solid transparent;
        border-radius: 20px;
        padding: 25px 30px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
        animation: slideInLeft 0.5s ease both;
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 20px var(--shadow-color);
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-50px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    .resource-item::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 5px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }}
    
    .resource-item:hover::before {{
        transform: scaleY(1);
    }}
    
    .resource-item:hover {{
        transform: translateX(10px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        border-color: var(--accent-primary);
    }}
    
    .res-icon {{
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        margin-right: 25px;
        transition: all 0.4s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }}
    
    .resource-item:hover .res-icon {{
        transform: rotate(360deg) scale(1.15);
    }}
    
    .res-info {{
        flex: 1;
    }}
    
    .res-title {{
        font-weight: 700;
        font-size: 1.2rem;
        color: var(--text-primary);
        margin-bottom: 5px;
        transition: color 0.3s ease;
    }}
    
    .res-date {{
        font-size: 0.9rem;
        color: var(--text-secondary);
        transition: color 0.3s ease;
    }}
    
    .res-link-btn {{
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white !important;
        text-decoration: none !important;
        padding: 12px 30px;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }}
    
    .res-link-btn::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }}
    
    .res-link-btn:hover::before {{
        width: 300px;
        height: 300px;
    }}
    
    .res-link-btn:hover {{
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }}
    
    /* PAGE HEADER */
    .page-header {{
        padding: 80px 40px;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 50px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        animation: headerAppear 0.8s ease;
    }}
    
    @keyframes headerAppear {{
        from {{
            opacity: 0;
            transform: translateY(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .page-header h1 {{
        margin: 0;
        font-size: 4rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 5px 30px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }}
    
    /* BACK BUTTON */
    .back-btn {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 12px 28px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white !important;
        text-decoration: none !important;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        font-size: 1rem;
    }}
    
    .back-btn:hover {{
        transform: translateX(-5px) scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }}
    
    /* STREAMLIT ELEMENTS STYLING */
    .stButton > button {{
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }}
    
    .stTextInput > div > div > input {{
        border-radius: 12px !important;
        border: 2px solid {'#444' if st.session_state.dark_mode else '#d0d0d0'} !important;
        padding: 12px 20px !important;
        transition: all 0.25s ease !important;
        background: transparent !important;
        color: var(--text-primary) !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        background: transparent !important;
    }}
    
    /* TEXT VISIBILITY FIXES WITH SMOOTH TRANSITIONS */
    .main-container p,
    .main-container span,
    .main-container div,
    .main-container label,
    .main-container h1,
    .main-container h2,
    .main-container h3,
    .main-container h4,
    .main-container h5,
    .main-container h6 {{
        color: var(--text-primary) !important;
        transition: color 0.3s ease !important;
    }}
    
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *,
    .element-container,
    .element-container * {{
        color: var(--text-primary) !important;
        transition: color 0.3s ease !important;
    }}
    
    /* Ensure all Streamlit text elements adapt */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span,
    .stTextInput label, .stTextInput p,
    label[data-testid="stWidgetLabel"],
    .stAlert {{
        color: var(--text-primary) !important;
        transition: color 0.3s ease !important;
    }}
    
    /* Card text transitions */
    .card-title,
    .res-title,
    .res-date {{
        transition: color 0.3s ease !important;
    }}
    
    /* Input placeholders */
    ::placeholder {{
        color: var(--text-secondary) !important;
        opacity: 0.7 !important;
    }}
    
    /* Info/Success/Warning messages */
    .stAlert {{
        border-radius: 12px !important;
        animation: alertSlide 0.5s ease !important;
    }}
    
    @keyframes alertSlide {{
        from {{ transform: translateX(-20px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3) !important;
        transform: scale(1.02) !important;
    }}
    
    .streamlit-expanderContent {{
        background: var(--bg-card) !important;
        border-radius: 0 0 12px 12px !important;
    }}
    
    /* Admin Popover */
    [data-testid="stPopover"] > button {{
        background: rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    [data-testid="stPopover"] > button:hover {{
        background: rgba(255, 255, 255, 0.3) !important;
        transform: scale(1.05) !important;
    }}
    
    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar {{
        width: 14px;
        height: 14px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--bg-primary);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 10px;
        border: 3px solid var(--bg-primary);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
    }}
    
    /* RESPONSIVE DESIGN */
    @media (max-width: 1024px) {{
        .hero-title {{ font-size: 3.5rem; }}
        .hero-subtitle {{ font-size: 2.2rem; }}
        .cards-grid {{ grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .nav-bar {{ padding: 15px 25px; }}
        .watermark {{ font-size: 0.7rem; }}
    }}
    
    @media (max-width: 768px) {{
        .hero-title {{ font-size: 2.5rem; }}
        .hero-subtitle {{ font-size: 1.8rem; }}
        .hero-text {{ font-size: 1.1rem; }}
        .hero-box {{ padding: 60px 20px; }}
        .nav-logo {{ font-size: 20px; }}
        .nav-bar {{ padding: 12px 15px; }}
        .main-container {{ margin-top: 80px; padding: 15px; }}
        .cards-grid {{ grid-template-columns: 1fr; }}
        .section-title {{ font-size: 2rem; }}
        .page-header h1 {{ font-size: 3rem; }}
        .resource-item {{ flex-direction: column; gap: 15px; text-align: center; }}
        .res-icon {{ margin-right: 0; }}
        .watermark {{ font-size: 0.65rem; top: -20px; }}
    }}
    
    @media (max-width: 480px) {{
        .hero-title {{ font-size: 2rem; }}
        .hero-subtitle {{ font-size: 1.5rem; }}
        .hero-text {{ font-size: 1rem; }}
        .nav-logo {{ font-size: 18px; }}
        .nav-bar {{ padding: 10px 12px; }}
        .main-container {{ margin-top: 75px; padding: 12px; }}
        .hero-cta {{ flex-direction: column; gap: 10px; }}
        .cta-button {{ width: 100%; justify-content: center; padding: 12px 20px; font-size: 0.95rem; }}
        .watermark {{ font-size: 0.6rem; top: -18px; }}
    }}
    
    /* FADE IN ANIMATION */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    /* LINKS */
    a {{
        text-decoration: none !important;
        transition: all 0.3s ease;
    }}
    
    /* NO SELECT ON DECORATIVE ELEMENTS */
    .hero-box::before,
    .nav-bar::before,
    .subject-card::before {{
        user-select: none;
        pointer-events: none;
    }}
</style>
""", unsafe_allow_html=True)

# --- DATA FUNCTIONS ---
def load_data():
    """Load all resources from Supabase"""
    try:
        response = supabase.table('resources').select("*").order('date_added', desc=True).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            return pd.DataFrame(columns=["id", "title", "category", "link", "date_added"])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=["id", "title", "category", "link", "date_added"])

def add_resource(title, category, link):
    """Add a new resource to Supabase"""
    try:
        data = {
            "title": title,
            "category": category,
            "link": link,
            "date_added": str(datetime.date.today())
        }
        response = supabase.table('resources').insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error adding resource: {e}")
        return False

def delete_resource(resource_id):
    """Delete a resource from Supabase"""
    try:
        response = supabase.table('resources').delete().eq('id', resource_id).execute()
        return True
    except Exception as e:
        st.error(f"Error deleting resource: {e}")
        return False

# --- CUSTOM CSS (ADD THIS FIRST) ---
st.markdown("""
<style>

/* Force white text in buttons */
div.stButton > button {
    color: white !important;
    font-weight: 600;
}

/* Keep white on hover also */
div.stButton > button:hover {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# --- NAVIGATION ---
query_params = st.query_params
current_page = query_params.get("page", "Home")

# --- NAVIGATION BAR ---
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)

# Adjusted layout (more space for controls)
col_logo, col_spacer, col_controls = st.columns([3, 4, 3])

# --- LOGO ---
with col_logo:
    st.markdown('''
        <div style="position: relative;">
            <div class="watermark">Avanish Maurya</div>
            <a href="?page=Home" class="nav-logo">🎓 DataSci Hub</a>
        </div>
    ''', unsafe_allow_html=True)

# --- SPACER ---
with col_spacer:
    st.markdown('')

# --- CONTROLS ---
with col_controls:
    # Give Job button more width
    subcol1, subcol2, subcol3 = st.columns([2, 1, 1])
    
    # --- JOB SEARCH BUTTON ---
    with subcol1:
        if st.button("Job Search", key="job_btn", help="Open Job Search"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://www.google.com">',
                unsafe_allow_html=True
            )

    # --- THEME TOGGLE ---
    with subcol2:
        if "dark_mode" not in st.session_state:
            st.session_state.dark_mode = False

        theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        if st.button(theme_icon, key="theme_toggle", help="Toggle Theme"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # --- ADMIN LOGIN ---
    with subcol3:
        with st.popover("👤", help="Admin Access"):
            st.markdown("### 🔐 Admin Login")

            if "is_admin" not in st.session_state:
                st.session_state.is_admin = False

            if not st.session_state.is_admin:
                with st.form("login"):
                    u = st.text_input("Username")
                    p = st.text_input("Password", type="password")

                    if st.form_submit_button("🚀 Login"):
                        if u == ADMIN_USER and p == ADMIN_PASS:
                            st.session_state.is_admin = True
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials")
            else:
                st.success("✅ Logged In")
                if st.button("🚪 Logout"):
                    st.session_state.is_admin = False
                    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
# --- WRAPPED CONTENT ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- MAIN CONTENT ---
if current_page == "Home":
    # Enhanced Hero Section
    st.markdown("""
        <div class="hero-box">
            <div class="hero-content">
                <h1 class="hero-title">🚀 Master Data Science</h1>
                <h1 class="hero-subtitle">All Resources in One Place</h1>
                <p class="hero-text">
                    Unlock your potential with our comprehensive collection of curated learning resources. 
                    From Python programming to Machine Learning, we've got everything you need to excel 
                    in the world of data science.
                </p>
                <div class="hero-cta">
                    <a href="#explore" class="cta-button cta-primary">
                        <span>📚 Explore Now</span>
                    </a>
                    <a href="?page=Python" class="cta-button cta-secondary">
                        <span>🐍 Start with Python</span>
                    </a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Subject Cards with descriptions
    st.markdown('<h2 class="section-title" id="explore">📚 Explore Subjects</h2>', unsafe_allow_html=True)
    
    subjects = [
        ("Python", "🐍", "Master programming fundamentals and advanced concepts"),
        ("MySQL", "🗄️", "Learn database management and SQL queries"),
        ("Power BI", "📊", "Create stunning data visualizations and dashboards"),
        ("Machine Learning", "🤖", "Build intelligent systems and AI models"),
        ("Descriptive Statistics", "📈", "Understand data analysis and statistical methods"),
        ("Other", "📚", "Explore additional resources and tools")
    ]
    
    # Create 3 columns for cards
    for i in range(0, len(subjects), 3):
        cols = st.columns(3)
        for j, (title, icon, desc) in enumerate(subjects[i:i+3]):
            with cols[j]:
                st.markdown(f"""
                    <a href="?page={title}" target="_self">
                        <div class="subject-card">
                            <div class="card-content">
                                <div class="card-icon">{icon}</div>
                                <div class="card-title">{title}</div>
                                <div class="card-desc">{desc}</div>
                            </div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)

else:
    # --- SUBJECT PAGE ---
    
    # Page Header with specific gradient
    gradients = {
        "Python": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "MySQL": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "Power BI": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "Machine Learning": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "Descriptive Statistics": "linear-gradient(135deg, #30cfd0 0%, #330867 100%)",
        "Other": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
    }
    bg = gradients.get(current_page, "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
    
    icons = {
        "Python": "🐍",
        "MySQL": "🗄️",
        "Power BI": "📊",
        "Machine Learning": "🤖",
        "Descriptive Statistics": "📈",
        "Other": "📚"
    }
    icon = icons.get(current_page, "📚")
    
    st.markdown(f"""
        <div class="page-header" style="background:{bg};">
            <h1>{icon} {current_page}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Admin Add Section
    if st.session_state.get("is_admin"):
        with st.expander(f"➕ Add New {current_page} Resource", expanded=False):
            with st.form("add_res_top"):
                c_add1, c_add2 = st.columns([1, 2])
                t = c_add1.text_input("📝 Resource Title")
                l = c_add2.text_input("🔗 Drive Link")
                if st.form_submit_button("✨ Upload Resource"):
                    if t and l:
                        if add_resource(t, current_page, l):
                            st.success("✅ Resource added successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to add resource")
                    else:
                        st.warning("⚠️ Please fill in all fields")

    # Navigation & Search
    col_nav, col_search = st.columns([1, 4])
    with col_nav:
        st.markdown('<a href="?page=Home" target="_self" class="back-btn">← Back Home</a>', unsafe_allow_html=True)
    with col_search:
        search_q = st.text_input("🔍 Search", placeholder="Find resources...", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # List Resources
    df = load_data()
    filtered = df[df['category'] == current_page]
    if search_q:
        filtered = filtered[filtered['title'].str.contains(search_q, case=False, na=False)]

    if filtered.empty:
        st.info(f"📭 No resources in {current_page} yet. Check back soon!")
    else:
        for idx, row in filtered.iterrows():
            date_val = row.get('date_added', 'N/A')
            title_val = row.get('title', '')
            link_val = row.get('link', '')
            id_val = row.get('id', idx)
            
            col1, col2 = st.columns([10, 2])
            with col1:
                st.markdown(f"""
                <div class="resource-item">
                    <div style="display:flex; align-items:center;">
                        <div class="res-icon">📄</div>
                        <div class="res-info">
                            <div class="res-title">{title_val}</div>
                            <div class="res-date">📅 Added: {date_val}</div>
                        </div>
                    </div>
                    <a href="{link_val}" target="_blank" class="res-link-btn">View Resource →</a>
                </div>
                """, unsafe_allow_html=True)
            
            # Admin Delete Button
            with col2:
                if st.session_state.get("is_admin"):
                    if st.button("🗑️", key=f"del_{id_val}", help="Delete this resource"):
                        if delete_resource(id_val):
                            st.success("✅ Deleted!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete")

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
