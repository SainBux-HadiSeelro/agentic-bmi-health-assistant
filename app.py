"""
🧬 VitalAI - Smart Health & BMI Intelligence Platform
Clean, aesthetic, high-contrast, and intuitive for everyone.
Includes precision biometrics, visual WHO spectrum meter,
and a 24/7 Live AI Health Assistant anchored to the bottom-right corner
with bottom quick-question options and a custom question input box.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from agent import HealthAgent, UserHealthProfile

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="VitalAI | Smart Health & BMI Calculator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# High-Contrast Cyber-Glassmorphic Dark Theme Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
    }

    /* Container: Centered with comfortable bottom clearance */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 110px !important;
        max-width: 1040px !important;
        margin: 0 auto !important;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 18px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.5);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.25);
        color: #c7d2fe;
        border: 1px solid rgba(99, 102, 241, 0.4);
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .hero-title {
        font-size: 1.95rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 0.92rem;
        line-height: 1.4;
    }

    /* Section Headers */
    .section-title {
        font-size: 1.18rem;
        font-weight: 700;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 2px;
    }

    .section-caption {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-bottom: 14px;
    }

    /* Big Hero Result Card */
    .result-hero-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
    }

    .bmi-score {
        font-size: 3.1rem;
        font-weight: 800;
        line-height: 1.05;
        margin: 4px 0;
    }

    .status-pill {
        display: inline-block;
        padding: 5px 18px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 4px;
        letter-spacing: 0.3px;
    }

    /* Visual Spectrum Gauge */
    .gauge-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 14px 18px;
        margin: 14px 0;
    }

    .gauge-bar-track {
        display: flex;
        height: 14px;
        border-radius: 7px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin: 8px 0 6px 0;
    }

    .gauge-seg-under { background: #38bdf8; width: 18.5%; }
    .gauge-seg-norm { background: #22c55e; width: 25%; }
    .gauge-seg-over { background: #eab308; width: 20%; }
    .gauge-seg-obese1 { background: #f97316; width: 18%; }
    .gauge-seg-obese2 { background: #ef4444; width: 18.5%; }

    .gauge-marker-wrap {
        position: relative;
        height: 16px;
    }

    .gauge-pointer {
        position: absolute;
        transform: translateX(-50%);
        color: #ffffff;
        font-size: 12px;
        font-weight: 800;
        background: #6366f1;
        padding: 2px 7px;
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    }

    .gauge-text-legend {
        display: flex;
        justify-content: space-between;
        color: #cbd5e1;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 6px;
    }

    /* Key Stat Triplet Cards */
    .triplet-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 14px 0;
    }

    .triplet-item {
        background: rgba(21, 28, 44, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 8px;
        text-align: center;
    }

    .triplet-label {
        font-size: 0.72rem;
        color: #94a3b8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .triplet-number {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        margin: 3px 0 1px 0;
    }

    .triplet-caption {
        font-size: 0.74rem;
        font-weight: 600;
    }

    /* Friendly Advice Banner */
    .advice-banner {
        background: rgba(99, 102, 241, 0.12);
        border-left: 4px solid #818cf8;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 14px 0;
        color: #f1f5f9;
        font-size: 0.88rem;
        line-height: 1.45;
    }

    /* --------------------------------------------------
       FIXED CORNER FLOATING CHATBOT BUTTON (Bottom-Right Anchor)
       -------------------------------------------------- */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 9999999 !important;
    }

    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%) !important;
        color: #ffffff !important;
        border: 1.5px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 9999px !important;
        padding: 11px 20px !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 10px 25px -4px rgba(124, 58, 237, 0.75), 0 0 18px rgba(219, 39, 119, 0.5) !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        cursor: pointer !important;
    }

    div[data-testid="stPopover"] > button:hover {
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 16px 32px -4px rgba(124, 58, 237, 0.95), 0 0 24px rgba(219, 39, 119, 0.7) !important;
    }

    div[data-testid="stPopoverBody"] {
        width: 390px !important;
        max-width: 92vw !important;
        border-radius: 18px !important;
        background: #111827 !important;
        border: 1.5px solid rgba(124, 58, 237, 0.45) !important;
        box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.95) !important;
        padding: 12px 14px !important;
        color: #f8fafc !important;
    }

    /* Message bubble styling */
    .chat-bubble-ai {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 10px;
        padding: 8px 10px;
        font-size: 0.82rem;
        line-height: 1.35;
        margin-bottom: 6px;
        color: #f8fafc;
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 10px;
        padding: 7px 10px;
        font-size: 0.82rem;
        line-height: 1.3;
        margin-bottom: 6px;
        color: #ffffff;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Top Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
            <div class="hero-badge">✨ AI-Powered Health Intelligence</div>
            <div class="hero-title">Smart & Simple BMI Health Calculator</div>
            <div class="hero-subtitle">
                Accurate clinical insights made clear and simple. Discover your ideal weight, daily calories, 
                hydration target, and get instant guidance from your 24/7 AI Health Coach.
            </div>
        </div>
        <div style="background: rgba(34, 197, 94, 0.2); border: 1px solid rgba(34, 197, 94, 0.4); border-radius: 9999px; padding: 6px 14px; font-size: 0.82rem; font-weight: 700; color: #4ade80;">
            ● 24/7 AI Health Coach Active
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Dual-Column Main Dashboard Layout
# ---------------------------------------------------------
col_left, col_right = st.columns([1, 1.25], gap="large")

with col_left:
    st.markdown('<div class="section-title">📝 Enter Your Details</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Instant calculations update as you adjust any value</div>', unsafe_allow_html=True)

    # Unit switch
    unit_mode = st.radio(
        "Measurement System:",
        ["Metric (kg & cm)", "Imperial (lbs & feet/inches)"],
        horizontal=True
    )

    # Gender & Age
    c1, c2 = st.columns(2)
    with c1:
        gender = st.selectbox("Biological Sex", ["Male", "Female"])
    with c2:
        age = st.number_input("Age (Years)", min_value=10, max_value=120, value=25, step=1)

    # Weight & Height
    if "Metric" in unit_mode:
        weight_kg = st.number_input("Weight (in kg)", min_value=20.0, max_value=350.0, value=70.0, step=0.5)
        height_cm = st.number_input("Height (in cm)", min_value=80.0, max_value=250.0, value=170.0, step=0.5)
    else:
        weight_lbs = st.number_input("Weight (in lbs)", min_value=45.0, max_value=750.0, value=154.0, step=1.0)
        c_ft, c_in = st.columns(2)
        with c_ft:
            height_ft = st.number_input("Height (Feet)", min_value=2, max_value=8, value=5, step=1)
        with c_in:
            height_in = st.number_input("Inches", min_value=0.0, max_value=11.9, value=7.0, step=0.5)

        weight_kg = weight_lbs * 0.45359237
        height_cm = ((height_ft * 12) + height_in) * 2.54

    st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 14px 0;'/>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Goal & Lifestyle</div>', unsafe_allow_html=True)

    # Goals
    goal_map = {
        "🥗 Lose Fat / Weight (Calorie Deficit)": -500,
        "⚖️ Maintain Healthy Weight (Equilibrium)": 0,
        "💪 Build Lean Muscle (Calorie Surplus)": 350
    }
    user_goal = st.selectbox("What is your primary health goal?", list(goal_map.keys()), index=0)
    cal_offset = goal_map[user_goal]

    # Activity
    activity_map = {
        "Desk Job / Little Exercise (Sedentary)": 1.2,
        "Light Exercise (1 to 3 days a week)": 1.375,
        "Moderate Exercise (3 to 5 days a week)": 1.55,
        "Very Active (Hard training 6 days a week)": 1.725
    }
    user_activity = st.selectbox("How active are you weekly?", list(activity_map.keys()), index=1)
    act_mult = activity_map[user_activity]


# ---------------------------------------------------------
# Mathematical & Health Calculations Core
# ---------------------------------------------------------
height_m = max(height_cm / 100.0, 0.5)
bmi = round(weight_kg / (height_m ** 2), 2)

# WHO Standard Stratification & Styling
if bmi < 18.5:
    category = "Underweight"
    cat_color = "#38bdf8"
    cat_bg = "rgba(56, 189, 248, 0.18)"
    coach_advice = "You are currently underweight. Focus on eating nutrient-dense whole foods (eggs, oats, dairy, nuts) and light strength training to reach a healthy weight safely."
elif 18.5 <= bmi < 25.0:
    category = "Healthy & Normal"
    cat_color = "#22c55e"
    cat_bg = "rgba(34, 197, 94, 0.18)"
    coach_advice = "Outstanding! Your weight is in the ideal clinical zone. Maintain your balanced nutrition, stay active, and drink plenty of water daily!"
elif 25.0 <= bmi < 30.0:
    category = "Slightly Overweight"
    cat_color = "#eab308"
    cat_bg = "rgba(234, 179, 8, 0.18)"
    coach_advice = "You are slightly above your ideal weight range. A moderate caloric deficit (-500 kcal) with daily brisk walking or cardio will bring you back into the green zone."
elif 30.0 <= bmi < 35.0:
    category = "Obese (Class 1)"
    cat_color = "#f97316"
    cat_bg = "rgba(249, 115, 22, 0.18)"
    coach_advice = "Your BMI falls in the obesity bracket. Small consistent steps like cutting sugary drinks, walking 8,000 steps, and portion control will create massive health improvements!"
else:
    category = "Obese (High Risk)"
    cat_color = "#ef4444"
    cat_bg = "rgba(239, 68, 68, 0.18)"
    coach_advice = "Your weight poses elevated health risks. We strongly recommend consulting with a healthcare physician or certified nutritionist for a structured medical plan."

# Ideal Weight Range (WHO 18.5 - 24.9)
ideal_min = round(18.5 * (height_m ** 2), 1)
ideal_max = round(24.9 * (height_m ** 2), 1)

# Basal Metabolic Rate (BMR) - Mifflin-St Jeor
if gender == "Male":
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    gender_factor = 1
else:
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    gender_factor = 0

tdee = bmr * act_mult
daily_calories = max(1200, int(tdee + cal_offset))

# Hydration & Body Fat
water_liters = round((weight_kg * 0.035) + (0.5 if act_mult >= 1.55 else 0), 1)
water_glasses = round(water_liters * 4)
body_fat = max(4.0, round((1.20 * bmi) + (0.23 * age) - (10.8 * gender_factor) - 5.4, 1))

# Initialize Active User Profile for AI Chatbot
profile = UserHealthProfile(
    weight_kg=weight_kg,
    height_cm=height_cm,
    age=age,
    gender=gender,
    bmi=bmi,
    category=category,
    ideal_weight_min=ideal_min,
    ideal_weight_max=ideal_max,
    bmr=bmr,
    tdee=tdee,
    target_calories=daily_calories,
    water_liters=water_liters,
    body_fat_pct=body_fat,
    activity_level=user_activity.split(" (")[0],
    goal=user_goal.split(" (")[0]
)


# ---------------------------------------------------------
# Right Column: Visual Health Dashboard
# ---------------------------------------------------------
with col_right:
    st.markdown('<div class="section-title">📊 Your Health Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Real-time biometric evaluation based on WHO standards</div>', unsafe_allow_html=True)

    # Hero BMI Result Card
    st.markdown(f"""
    <div class="result-hero-box">
        <div style="font-size: 0.82rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Body Mass Index (BMI)</div>
        <div class="bmi-score" style="color: {cat_color};">{bmi}</div>
        <div class="status-pill" style="background: {cat_bg}; color: {cat_color}; border: 1.5px solid {cat_color}50;">
            ● {category}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Visual Spectrum Gauge
    pos_pct = max(0.0, min(100.0, ((bmi - 15) / (40 - 15)) * 100))
    st.markdown(f"""
    <div class="gauge-card">
        <div style="display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 700; color: #f8fafc;">
            <span>WHO Weight Spectrum</span>
            <span style="color: {cat_color};">Current: {bmi}</span>
        </div>
        <div class="gauge-bar-track">
            <div class="gauge-seg-under" title="Underweight (<18.5)"></div>
            <div class="gauge-seg-norm" title="Healthy Range (18.5 - 24.9)"></div>
            <div class="gauge-seg-over" title="Overweight (25 - 29.9)"></div>
            <div class="gauge-seg-obese1" title="Obese 1 (30 - 34.9)"></div>
            <div class="gauge-seg-obese2" title="Obese 2+ (≥35)"></div>
        </div>
        <div class="gauge-marker-wrap">
            <div class="gauge-pointer" style="left: {pos_pct}%;">▲ You ({bmi})</div>
        </div>
        <div class="gauge-text-legend">
            <span style="color: #38bdf8;">Underweight</span>
            <span style="color: #22c55e;">Healthy Normal</span>
            <span style="color: #eab308;">Overweight</span>
            <span style="color: #ef4444;">Obese</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Stat Cards Triplet
    diff_kg = round(weight_kg - ideal_max if weight_kg > ideal_max else (ideal_min - weight_kg if weight_kg < ideal_min else 0), 1)
    diff_sub = f"~{diff_kg} kg to reach" if diff_kg > 0 else "In Target Band"

    st.markdown(f"""
    <div class="triplet-grid">
        <div class="triplet-item">
            <div class="triplet-label">Ideal Weight</div>
            <div class="triplet-number" style="color: #38bdf8;">{ideal_min}-{ideal_max} <span style="font-size: 0.75rem; color: #94a3b8;">kg</span></div>
            <div class="triplet-caption" style="color: #38bdf8;">{diff_sub}</div>
        </div>
        <div class="triplet-item">
            <div class="triplet-label">Daily Calories</div>
            <div class="triplet-number" style="color: #c084fc;">{daily_calories} <span style="font-size: 0.75rem; color: #94a3b8;">kcal</span></div>
            <div class="triplet-caption" style="color: #c084fc;">For {user_goal.split(' (')[0]}</div>
        </div>
        <div class="triplet-item">
            <div class="triplet-label">Daily Hydration</div>
            <div class="triplet-number" style="color: #34d399;">{water_liters} <span style="font-size: 0.75rem; color: #94a3b8;">L</span></div>
            <div class="triplet-caption" style="color: #34d399;">~{water_glasses} glasses/day</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Friendly Coach Advice Banner
    st.markdown(f"""
    <div class="advice-banner">
        💡 <b>AI Coach Advice for You:</b><br/>
        {coach_advice}
    </div>
    """, unsafe_allow_html=True)

    # Download summary button
    summary_report = f"""=======================================
🧬 VITALAI HEALTH & BIOMETRIC DOSSIER
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
=======================================
- Biological Sex: {gender} | Age: {age} yrs
- Weight: {weight_kg:.1f} kg | Height: {height_cm:.1f} cm
- BMI Score: {bmi} ({category})
- Ideal Weight Range: {ideal_min} kg - {ideal_max} kg
- Estimated Body Fat: {body_fat}%
- Daily Calorie Target: {daily_calories} kcal/day
- Target Goal: {user_goal}
- Recommended Hydration: {water_liters} Liters (~{water_glasses} glasses)
=======================================
"""
    st.download_button(
        label="📥 Download My Health Summary",
        data=summary_report,
        file_name=f"VitalAI_Report_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True
    )


# ---------------------------------------------------------
# CORNER FLOATING AI CHATBOT (Bottom-Right Anchor)
# ---------------------------------------------------------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": f"Hi! 👋 Synced: **BMI {bmi} ({category})**, Target: **{daily_calories} kcal/day**. How can I help you?"
        }
    ]

if "agent_engine" not in st.session_state:
    st.session_state.agent_engine = HealthAgent()

# Popover anchored strictly in bottom-right corner
with st.popover("💬 Chat with AI Coach 🟢", use_container_width=False):
    # Chat Header
    st.markdown("""
        <div style="border-bottom: 1px solid rgba(255,255,255,0.12); padding-bottom: 6px; margin-bottom: 8px;">
            <b style="font-size: 0.98rem; color: #ffffff;">🧬 VitalAI Health Assistant</b><br/>
            <span style="font-size: 0.74rem; color: #4ade80; font-weight: 600;">● Online 24/7 (Live Biometrics Synced)</span>
        </div>
    """, unsafe_allow_html=True)

    # 1. Message Stream Area (Compact Scrollable)
    st.markdown('<div style="max-height: 100px; overflow-y: auto; padding-right: 4px; margin-bottom: 8px;">', unsafe_allow_html=True)
    for m in st.session_state.chat_messages[-4:]:
        if m["role"] == "assistant":
            st.markdown(f'<div class="chat-bubble-ai">🤖 <b>VitalAI:</b><br/>{m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-user">👤 <b>You:</b><br/>{m["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Options for questions to ask (Neeche Options)
    st.markdown('<div style="font-size: 0.72rem; font-weight: 700; color: #94a3b8; margin-bottom: 4px; text-transform: uppercase;">💡 Quick Questions (Click to Ask):</div>', unsafe_allow_html=True)
    q_c1, q_c2 = st.columns(2)
    selected_option = None

    with q_c1:
        if st.button("🥗 7-Day Meal Plan", key="opt_diet", use_container_width=True):
            selected_option = "Give me an easy 7-day meal plan for my calorie target."
        if st.button("🎯 Reach Ideal Weight", key="opt_target", use_container_width=True):
            selected_option = "How soon can I reach my ideal weight safely?"
    with q_c2:
        if st.button("🏋️ Workout Schedule", key="opt_workout", use_container_width=True):
            selected_option = "What is the best weekly workout plan for my body and goal?"
        if st.button("💧 Daily Water & Habits", key="opt_water", use_container_width=True):
            selected_option = "What are the best hydration and daily recovery habits?"

    # 3. Custom Question Input Form (Neeche question poochhne ke lie)
    st.markdown('<div style="margin-top: 6px;"></div>', unsafe_allow_html=True)
    with st.form("user_chat_form", clear_on_submit=True):
        custom_query = st.text_input(
            "Apna sawal yahan likhein (Ask your question):",
            placeholder="Type your question here...",
            key="custom_user_input",
            label_visibility="collapsed"
        )
        submit_btn = st.form_submit_button("Ask Question 🚀", use_container_width=True)

    # Process action
    active_prompt = None
    if selected_option:
        active_prompt = selected_option
    elif submit_btn and custom_query.strip():
        active_prompt = custom_query.strip()

    if active_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": active_prompt})
        bot_reply = st.session_state.agent_engine.respond(active_prompt, profile)
        st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()
