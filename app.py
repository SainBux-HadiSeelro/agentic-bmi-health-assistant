"""
🧬 VitalAI - Smart Health & BMI Intelligence Platform
Simple, aesthetic, and designed for everyone (technical and non-technical).
Features real-time biometrics, visual health meters, and an aesthetic floating corner AI Chatbot.
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
# Modern Aesthetic & Floating Corner Chatbot Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(99, 102, 241, 0.15) 50%, rgba(168, 85, 247, 0.15) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 24px 30px;
        margin-bottom: 24px;
        backdrop-filter: blur(14px);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.35);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.98rem;
        line-height: 1.5;
    }

    /* Card Containers */
    .simple-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.25);
    }

    /* Big Metric Result Card */
    .result-hero-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }

    .bmi-number {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 6px 0;
    }

    .category-pill {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-top: 6px;
    }

    /* Visual Spectrum Gauge */
    .gauge-container {
        margin: 18px 0;
    }

    .gauge-track {
        display: flex;
        height: 16px;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .gauge-seg-under { background: #38bdf8; width: 18.5%; }
    .gauge-seg-norm { background: #22c55e; width: 25%; }
    .gauge-seg-over { background: #eab308; width: 20%; }
    .gauge-seg-obese1 { background: #f97316; width: 18%; }
    .gauge-seg-obese2 { background: #ef4444; width: 18.5%; }

    .gauge-marker-row {
        position: relative;
        height: 14px;
        margin-top: 2px;
    }

    .gauge-marker {
        position: absolute;
        transform: translateX(-50%);
        color: #f8fafc;
        font-size: 13px;
        font-weight: bold;
    }

    .gauge-legend {
        display: flex;
        justify-content: space-between;
        color: #94a3b8;
        font-size: 0.75rem;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Mini Stat Cards */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 14px;
    }

    .stat-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }

    .stat-title {
        font-size: 0.75rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    .stat-val {
        font-size: 1.35rem;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 3px;
    }

    .stat-desc {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 2px;
    }

    /* Friendly Advice Box */
    .friendly-box {
        background: rgba(99, 102, 241, 0.09);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 16px 0;
        font-size: 0.92rem;
        color: #e2e8f0;
        line-height: 1.5;
    }

    /* ---------------------------------------------
       Aesthetic Floating Corner Chatbot
       --------------------------------------------- */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 999999 !important;
    }

    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #0284c7 0%, #6366f1 50%, #a855f7 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 9999px !important;
        padding: 12px 22px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.6), 0 0 18px rgba(168, 85, 247, 0.4) !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-testid="stPopover"] > button:hover {
        transform: translateY(-3px) scale(1.04) !important;
        box-shadow: 0 14px 30px -5px rgba(99, 102, 241, 0.8), 0 0 22px rgba(168, 85, 247, 0.6) !important;
    }

    div[data-testid="stPopoverBody"] {
        width: 390px !important;
        max-width: 92vw !important;
        max-height: 560px !important;
        border-radius: 20px !important;
        background: #0f172a !important;
        border: 1px solid rgba(99, 102, 241, 0.35) !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.85), 0 0 20px rgba(99, 102, 241, 0.2) !important;
        padding: 16px !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Hero Banner (Attractive for new visitors)
# ---------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
            <div class="hero-badge">✨ AI-Powered Health Intelligence</div>
            <div class="hero-title">Simple & Smart BMI Health Calculator</div>
            <div class="hero-subtitle">
                Enter your details to get your instant BMI score, ideal weight range, daily calorie target, 
                and personalized health tips. Non-technical & easy for everyone!
            </div>
        </div>
        <div style="background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 9999px; padding: 6px 14px; font-size: 0.82rem; font-weight: 600; color: #4ade80;">
            🟢 24/7 AI Health Coach Ready
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Two-Column Clean Dashboard Layout
# ---------------------------------------------------------
col_input, col_result = st.columns([1, 1.25], gap="large")

with col_input:
    st.markdown("### 📝 Enter Your Details")
    st.caption("Change any value below to see instant results")

    # Friendly Unit Selector
    unit_mode = st.radio(
        "Choose Your Measurement Units:",
        ["Metric (kg & cm)", "Imperial (lbs & feet/inches)"],
        horizontal=True
    )

    # Gender & Age
    c_gen, c_age = st.columns(2)
    with c_gen:
        gender = st.selectbox("Your Gender", ["Male", "Female"])
    with c_age:
        age = st.number_input("Your Age (Years)", min_value=10, max_value=120, value=25, step=1)

    # Weight & Height based on unit mode
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

        # Convert to Metric for calculation
        weight_kg = weight_lbs * 0.45359237
        height_cm = ((height_ft * 12) + height_in) * 2.54

    st.markdown("---")
    st.markdown("### 🎯 Your Goal & Routine")

    # Simple goal selection
    goal_options = {
        "🥗 Lose Fat / Weight (Calorie Deficit)": -500,
        "⚖️ Stay Healthy & Fit (Maintain Weight)": 0,
        "💪 Build Lean Muscle (Calorie Surplus)": 350
    }
    user_goal = st.selectbox("What is your main health goal?", list(goal_options.keys()), index=0)
    calorie_offset = goal_options[user_goal]

    # Simple activity selection
    activity_options = {
        "Desk Job / Little Exercise (Sedentary)": 1.2,
        "Light Exercise (1 to 3 days a week)": 1.375,
        "Moderate Exercise (3 to 5 days a week)": 1.55,
        "Very Active (Gym / Sports 6 days a week)": 1.725
    }
    user_activity = st.selectbox("How active are you during the week?", list(activity_options.keys()), index=1)
    act_multiplier = activity_options[user_activity]


# ---------------------------------------------------------
# Calculations
# ---------------------------------------------------------
height_m = max(height_cm / 100.0, 0.5)
bmi = round(weight_kg / (height_m ** 2), 2)

# WHO Categories & Friendly Styling
if bmi < 18.5:
    category = "Underweight"
    cat_color = "#38bdf8"
    cat_bg = "rgba(56, 189, 248, 0.15)"
    friendly_msg = "You are currently underweight. Focus on eating nutrient-dense foods (eggs, milk, nuts, protein) and light strength training to reach a healthy weight."
elif 18.5 <= bmi < 25.0:
    category = "Healthy & Normal"
    cat_color = "#22c55e"
    cat_bg = "rgba(34, 197, 94, 0.15)"
    friendly_msg = "Awesome! Your body weight is in the ideal healthy zone. Keep eating balanced home-cooked meals and stay consistently active!"
elif 25.0 <= bmi < 30.0:
    category = "Slightly Overweight"
    cat_color = "#eab308"
    cat_bg = "rgba(234, 179, 8, 0.15)"
    friendly_msg = "You are slightly above your ideal weight range. A small daily calorie reduction (-500 kcal) with 30 minutes of brisk walking will bring you into the normal range."
elif 30.0 <= bmi < 35.0:
    category = "Obese (Class 1)"
    cat_color = "#f97316"
    cat_bg = "rgba(249, 115, 22, 0.15)"
    friendly_msg = "Your BMI indicates obesity. Prioritize reducing sugary drinks, processed foods, and start with light daily walks. You can safely achieve great progress step-by-step!"
else:
    category = "Obese (High Risk)"
    cat_color = "#ef4444"
    cat_bg = "rgba(239, 68, 68, 0.15)"
    friendly_msg = "Your weight is in a high-risk category. We strongly recommend speaking with a doctor or registered dietitian to guide your health journey safely."

# Ideal Weight Range (WHO 18.5 - 24.9)
ideal_min = round(18.5 * (height_m ** 2), 1)
ideal_max = round(24.9 * (height_m ** 2), 1)

# BMR & Daily Calories (Mifflin-St Jeor)
if gender == "Male":
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    gender_factor = 1
else:
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    gender_factor = 0

tdee = bmr * act_multiplier
daily_calories = max(1200, int(tdee + calorie_offset))

# Water intake in Liters & Glasses
water_liters = round((weight_kg * 0.035) + (0.5 if act_multiplier >= 1.55 else 0), 1)
water_glasses = round(water_liters * 4)

# Estimated Body Fat %
body_fat = max(4.0, round((1.20 * bmi) + (0.23 * age) - (10.8 * gender_factor) - 5.4, 1))

# Initialize Health Profile for AI Agent
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
# Right Column: Visual Result Card
# ---------------------------------------------------------
with col_result:
    st.markdown("### 📊 Your Health Report")

    # Big Result Hero Card
    st.markdown(f"""
    <div class="result-hero-card">
        <div style="font-size: 0.85rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Your Body Mass Index (BMI)</div>
        <div class="bmi-number" style="color: {cat_color};">{bmi}</div>
        <div class="category-pill" style="background: {cat_bg}; color: {cat_color}; border: 1px solid {cat_color}40;">
            ● {category}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Visual Spectrum Gauge
    pos_pct = max(0.0, min(100.0, ((bmi - 15) / (40 - 15)) * 100))
    st.markdown(f"""
    <div class="gauge-container">
        <div class="gauge-track">
            <div class="gauge-seg-under" title="Underweight (<18.5)"></div>
            <div class="gauge-seg-norm" title="Normal (18.5 - 24.9)"></div>
            <div class="gauge-seg-over" title="Overweight (25 - 29.9)"></div>
            <div class="gauge-seg-obese1" title="Obese 1 (30 - 34.9)"></div>
            <div class="gauge-seg-obese2" title="Obese 2+ (≥35)"></div>
        </div>
        <div class="gauge-marker-row">
            <div class="gauge-marker" style="left: {pos_pct}%;">▲ You ({bmi})</div>
        </div>
        <div class="gauge-legend">
            <span>Underweight</span>
            <span style="color: #22c55e;">Healthy Range</span>
            <span>Overweight</span>
            <span>Obese</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Big Key Stat Boxes
    diff_kg = round(weight_kg - ideal_max if weight_kg > ideal_max else (ideal_min - weight_kg if weight_kg < ideal_min else 0), 1)
    diff_text = f"~{diff_kg} kg away" if diff_kg > 0 else "In Healthy Zone!"

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-box">
            <div class="stat-title">Ideal Weight</div>
            <div class="stat-val" style="color: #38bdf8;">{ideal_min}-{ideal_max} <span style="font-size: 0.8rem;">kg</span></div>
            <div class="stat-desc">{diff_text}</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">Daily Calories</div>
            <div class="stat-val" style="color: #a78bfa;">{daily_calories} <span style="font-size: 0.8rem;">kcal</span></div>
            <div class="stat-desc">For your goal</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">Daily Water</div>
            <div class="stat-val" style="color: #34d399;">{water_liters} <span style="font-size: 0.8rem;">L</span></div>
            <div class="stat-desc">~{water_glasses} glasses</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Friendly Plain Advice Box
    st.markdown(f"""
    <div class="friendly-box">
        💡 <b>AI Health Coach Tip:</b><br/>
        {friendly_msg}
    </div>
    """, unsafe_allow_html=True)

    # Simple 1-Click Download Button
    summary_txt = f"""--- VITALAI HEALTH SUMMARY ---
Date: {datetime.now().strftime('%Y-%m-%d')}
Weight: {weight_kg:.1f} kg | Height: {height_cm:.1f} cm
BMI: {bmi} ({category})
Ideal Weight: {ideal_min} - {ideal_max} kg
Daily Calorie Target: {daily_calories} kcal/day
Daily Water Intake: {water_liters} Liters (~{water_glasses} glasses)
Goal: {user_goal}
------------------------------"""

    st.download_button(
        label="📥 Download My Health Summary",
        data=summary_txt,
        file_name="My_Health_Summary.txt",
        mime="text/plain",
        use_container_width=True
    )


# ---------------------------------------------------------
# CORNER FLOATING AESTHETIC CHATBOT (Web-style in corner)
# ---------------------------------------------------------
# Session state initialization for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": f"Hi there! 👋 I am your **AI Health Coach**.\n\nI see your BMI is **{bmi} ({category})** and daily target is **{daily_calories} kcal**.\n\nHow can I help you? Ask me for an easy meal plan, home workout, or tips to reach your ideal weight!"
        }
    ]

if "agent" not in st.session_state:
    st.session_state.agent = HealthAgent()

# Floating Corner Chat Popover
with st.popover("💬 Chat with AI Coach 🟢", use_container_width=False):
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; margin-bottom: 12px;">
            <div>
                <b style="font-size: 1rem; color: #f8fafc;">🧬 VitalAI Health Assistant</b><br/>
                <span style="font-size: 0.75rem; color: #22c55e;">● Online 24/7 (Live Biometrics Synced)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Quick 1-click suggestion chips inside the corner chat
    st.caption("Quick Questions:")
    q_col1, q_col2 = st.columns(2)
    chip_question = None

    with q_col1:
        if st.button("🥗 7-Day Meal Plan", key="chip_diet", use_container_width=True):
            chip_question = "What should I eat? Give me an easy 7-day meal plan."
        if st.button("🎯 Reach Ideal Weight", key="chip_ideal", use_container_width=True):
            chip_question = "How soon can I reach my ideal weight safely?"
    with q_col2:
        if st.button("🏋️ Workout Schedule", key="chip_gym", use_container_width=True):
            chip_question = "Suggest an easy weekly workout plan for me."
        if st.button("💧 Daily Water & Habits", key="chip_water", use_container_width=True):
            chip_question = "Tell me water and healthy recovery habits for my body."

    # Render previous messages
    for msg in st.session_state.chat_history[-6:]:  # show recent messages for clean scroll
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input in corner popup
    chat_prompt = st.chat_input("Ask anything (e.g. diet, exercise, weight)...")
    final_query = chip_question if chip_question else chat_prompt

    if final_query:
        st.session_state.chat_history.append({"role": "user", "content": final_query})
        with st.chat_message("user"):
            st.markdown(final_query)

        # Get response from AI Agent with live profile
        reply = st.session_state.agent.respond(final_query, profile)

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
