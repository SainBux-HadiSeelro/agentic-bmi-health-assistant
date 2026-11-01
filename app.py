"""
🧬 VitalAI - Agentic Health & BMI Intelligence Platform
Engineered by an Agentic AI Developer.
Combines precision clinical anthropometrics, metabolic forecasting,
and a 24/7 Context-Aware Autonomous AI Health Copilot.
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
    page_title="VitalAI | Agentic Health & BMI Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern Styling (Glassmorphism & Cybernetic Dark)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Gradient Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.12) 0%, rgba(99, 102, 241, 0.12) 50%, rgba(168, 85, 247, 0.12) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.02rem;
        margin-bottom: 12px;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.84rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 4px;
    }
    .metric-subtext {
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Gauge Visual Bar */
    .gauge-wrapper {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin: 20px 0;
    }
    .gauge-bar {
        display: flex;
        height: 18px;
        border-radius: 9px;
        overflow: hidden;
        margin: 14px 0 8px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .gauge-underweight { background: #38bdf8; width: 18.5%; }
    .gauge-normal { background: #22c55e; width: 25%; }
    .gauge-overweight { background: #eab308; width: 20%; }
    .gauge-obese1 { background: #f97316; width: 18%; }
    .gauge-obese2 { background: #ef4444; width: 18.5%; }

    .gauge-labels {
        display: flex;
        justify-content: space-between;
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Chat Context Header */
    .chat-context-box {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 16px;
        font-size: 0.88rem;
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Sidebar Controls & User Biometric Inputs
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Biometric Input Engine")
    st.caption("Precision parameters for metabolic calculations")

    unit_system = st.radio("Measurement System", ["Metric (kg, cm)", "Imperial (lbs, ft & in)"], horizontal=True)

    col_g, col_a = st.columns(2)
    with col_g:
        gender = st.selectbox("Biological Sex", ["Male", "Female"])
    with col_a:
        age = st.number_input("Age (years)", min_value=10, max_value=120, value=25, step=1)

    if "Metric" in unit_system:
        weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=350.0, value=70.0, step=0.5)
        height_cm = st.number_input("Height (cm)", min_value=80.0, max_value=250.0, value=170.0, step=0.5)
    else:
        weight_lbs = st.number_input("Weight (lbs)", min_value=44.0, max_value=770.0, value=154.0, step=1.0)
        col_ft, col_in = st.columns(2)
        with col_ft:
            height_ft = st.number_input("Height (ft)", min_value=2, max_value=8, value=5, step=1)
        with col_in:
            height_in = st.number_input("Height (in)", min_value=0.0, max_value=11.9, value=7.0, step=0.5)

        # Conversions to Metric standard
        weight_kg = weight_lbs * 0.45359237
        total_inches = (height_ft * 12) + height_in
        height_cm = total_inches * 2.54

    st.markdown("---")
    st.markdown("### 🎯 Lifestyle & Target")

    activity_levels = {
        "Sedentary (Little/no exercise, desk job)": 1.2,
        "Lightly Active (Exercise 1-3 days/week)": 1.375,
        "Moderately Active (Exercise 3-5 days/week)": 1.55,
        "Very Active (Hard exercise 6-7 days/week)": 1.725,
        "Extra Active (Intense daily training / athlete)": 1.9,
    }
    selected_activity = st.selectbox("Activity Level", list(activity_levels.keys()), index=2)
    activity_multiplier = activity_levels[selected_activity]

    goals = {
        "Fat Loss (-500 kcal deficit)": -500,
        "Maintain Weight (Equilibrium)": 0,
        "Lean Muscle Gain (+350 kcal surplus)": 350
    }
    selected_goal = st.selectbox("Primary Health Goal", list(goals.keys()), index=0)
    calorie_offset = goals[selected_goal]

    st.markdown("---")
    st.markdown("### 🤖 Agent Connectivity")
    st.markdown("""
        <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.5;">
            ✅ <b>24/7 Autonomous Agent</b>: Active<br>
            🧠 <b>Zero-Latency Engine</b>: Synced<br>
            🔒 <b>Privacy Sandbox</b>: 100% Local
        </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# Mathematical & Clinical Analytics Core
# ---------------------------------------------------------
height_m = max(height_cm / 100.0, 0.5)
bmi = round(weight_kg / (height_m ** 2), 2)

# WHO Standard Categorization & Styling
if bmi < 18.5:
    category = "Underweight"
    cat_color = "#38bdf8"
    cat_desc = "Nutrient density & structured strength training recommended"
elif 18.5 <= bmi < 25.0:
    category = "Normal weight"
    cat_color = "#22c55e"
    cat_desc = "Optimal biometric range for cardiovascular and metabolic health"
elif 25.0 <= bmi < 30.0:
    category = "Overweight"
    cat_color = "#eab308"
    cat_desc = "Moderate risk. Gradual caloric deficit & zone 2 cardio advised"
elif 30.0 <= bmi < 35.0:
    category = "Obese Class I"
    cat_color = "#f97316"
    cat_desc = "Elevated metabolic risk. Structured lifestyle intervention recommended"
elif 35.0 <= bmi < 40.0:
    category = "Obese Class II"
    cat_color = "#ef4444"
    cat_desc = "High cardiovascular risk. Clinical consultation advised"
else:
    category = "Obese Class III"
    cat_color = "#c084fc"
    cat_desc = "Critical risk tier. Immediate professional medical guidance recommended"

# Ideal Body Weight Range (WHO 18.5 - 24.9 standard)
ideal_min_kg = round(18.5 * (height_m ** 2), 1)
ideal_max_kg = round(24.9 * (height_m ** 2), 1)

# Basal Metabolic Rate (BMR) - Mifflin-St Jeor Equation
if gender == "Male":
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    gender_factor = 1
else:
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    gender_factor = 0

# Total Daily Energy Expenditure (TDEE) & Goal Target
tdee = round(bmr * activity_multiplier, 0)
target_calories = max(1200, round(tdee + calorie_offset, 0))

# Daily Water Intake (35ml per kg base + activity bonus)
water_liters = round((weight_kg * 0.035) + (0.5 if activity_multiplier >= 1.55 else 0), 1)

# Body Fat % Estimation (Deurenberg Formula)
estimated_body_fat = round((1.20 * bmi) + (0.23 * age) - (10.8 * gender_factor) - 5.4, 1)
estimated_body_fat = max(4.0, estimated_body_fat)

# Initialize User Health Profile for Agent
user_profile = UserHealthProfile(
    weight_kg=weight_kg,
    height_cm=height_cm,
    age=age,
    gender=gender,
    bmi=bmi,
    category=category,
    ideal_weight_min=ideal_min_kg,
    ideal_weight_max=ideal_max_kg,
    bmr=bmr,
    tdee=tdee,
    target_calories=target_calories,
    water_liters=water_liters,
    body_fat_pct=estimated_body_fat,
    activity_level=selected_activity.split(" (")[0],
    goal=selected_goal.split(" (")[0]
)


# ---------------------------------------------------------
# Header & Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
            <div class="hero-title">
                <span>🧬 VitalAI</span>
                <span style="font-size: 1.2rem; font-weight: 500; color: #94a3b8; -webkit-text-fill-color: initial;">| Biometric & Agentic Health Platform</span>
            </div>
            <div class="hero-subtitle">
                Autonomous clinical analytics, metabolic forecasting, and a 24/7 Context-Aware AI Health Agent.
            </div>
        </div>
        <div>
            <div class="status-badge">
                <span class="status-dot"></span>
                <span>24/7 Health Agent Active</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Main Navigation Tabs
# ---------------------------------------------------------
tab_dashboard, tab_agent, tab_specs = st.tabs([
    "📊 Biometric Dashboard",
    "🤖 24/7 Live AI Health Agent",
    "📋 Clinical Specifications & Architecture"
])


# =========================================================
# TAB 1: Biometric Dashboard
# =========================================================
with tab_dashboard:
    # Top 4 Primary Metric Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Body Mass Index (BMI)</div>
            <div class="metric-value" style="color: {cat_color};">{bmi}</div>
            <div class="metric-subtext" style="color: {cat_color};">● {category}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        diff_ideal = round(weight_kg - ideal_max_kg if weight_kg > ideal_max_kg else (ideal_min_kg - weight_kg if weight_kg < ideal_min_kg else 0), 1)
        sub_txt = f"{diff_ideal} kg to range" if diff_ideal > 0 else "Within target band"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Ideal Weight Range</div>
            <div class="metric-value">{ideal_min_kg} - {ideal_max_kg} <span style="font-size: 1rem; color: #94a3b8;">kg</span></div>
            <div class="metric-subtext" style="color: #38bdf8;">{sub_txt}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Daily Calorie Target</div>
            <div class="metric-value">{int(target_calories)} <span style="font-size: 1rem; color: #94a3b8;">kcal</span></div>
            <div class="metric-subtext" style="color: #a78bfa;">TDEE: {int(tdee)} kcal</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Estimated Body Fat</div>
            <div class="metric-value">{estimated_body_fat}%</div>
            <div class="metric-subtext" style="color: #34d399;">Hydration: {water_liters} L/day</div>
        </div>
        """, unsafe_allow_html=True)

    # Visual BMI Range Gauge
    # Clamp visual indicator between 15 and 45 BMI scale
    indicator_pct = max(0.0, min(100.0, ((bmi - 15) / (42 - 15)) * 100))
    st.markdown(f"""
    <div class="gauge-wrapper">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 700; color: #e2e8f0; font-size: 0.95rem;">BMI Visual Spectrum (WHO Benchmark)</span>
            <span style="font-size: 0.85rem; color: {cat_color}; font-weight: 600;">Current: {bmi} ({category})</span>
        </div>
        <div class="gauge-bar">
            <div class="gauge-underweight" title="Underweight (<18.5)"></div>
            <div class="gauge-normal" title="Normal (18.5 - 24.9)"></div>
            <div class="gauge-overweight" title="Overweight (25.0 - 29.9)"></div>
            <div class="gauge-obese1" title="Obese Class I (30.0 - 34.9)"></div>
            <div class="gauge-obese2" title="Obese Class II+ (≥35.0)"></div>
        </div>
        <div style="position: relative; height: 16px; margin-bottom: 4px;">
            <div style="position: absolute; left: {indicator_pct}%; transform: translateX(-50%); font-size: 14px;">▲</div>
        </div>
        <div class="gauge-labels">
            <span>15.0</span>
            <span>18.5 (Normal)</span>
            <span>25.0 (Overweight)</span>
            <span>30.0 (Obese)</span>
            <span>42.0+</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Deep Analytics Columns
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("⚡ Autonomous Agentic Diagnosis")
        st.markdown(f"""
        > **Primary Evaluation**: Based on your biometrics, your body mass index indicates **{category}**.
        > {cat_desc}.
        """)

        # Macronutrient allocation based on target calories
        protein_g = int(weight_kg * (1.8 if "Muscle" in selected_goal else 1.4))
        fats_g = int((target_calories * 0.25) / 9)
        carbs_g = max(50, int((target_calories - (protein_g * 4) - (fats_g * 9)) / 4))

        st.markdown(f"#### 🍽️ Recommended Daily Macronutrient Breakdown ({int(target_calories)} kcal)")
        macro_df = pd.DataFrame({
            "Nutrient": ["Protein (Tissue repair)", "Complex Carbs (Energy)", "Healthy Fats (Hormones)"],
            "Grams (g)": [protein_g, carbs_g, fats_g],
            "Calories (kcal)": [protein_g * 4, carbs_g * 4, fats_g * 9],
            "Ratio (%)": [
                round((protein_g * 4 / target_calories) * 100, 1),
                round((carbs_g * 4 / target_calories) * 100, 1),
                round((fats_g * 9 / target_calories) * 100, 1)
            ]
        })
        st.dataframe(macro_df, hide_index=True, use_container_width=True)

    with col_right:
        st.subheader("📋 Complete Biometric Profile")
        profile_data = {
            "Parameter": [
                "Biological Sex", "Age", "Recorded Weight", "Recorded Height",
                "Quetelet BMI", "BMI Classification", "Ideal Weight Band",
                "Basal Metabolic Rate (BMR)", "Total Daily Energy (TDEE)",
                "Prescribed Daily Intake", "Estimated Body Fat", "Daily Water Goal"
            ],
            "Value": [
                gender, f"{age} years", f"{weight_kg:.1f} kg ({weight_kg*2.20462:.1f} lbs)",
                f"{height_cm:.1f} cm ({int(height_cm//30.48)}' {int((height_cm%30.48)//2.54)}\")",
                f"{bmi}", category, f"{ideal_min_kg} - {ideal_max_kg} kg",
                f"{int(bmr)} kcal/day", f"{int(tdee)} kcal/day",
                f"{int(target_calories)} kcal/day ({selected_goal.split(' (')[0]})",
                f"{estimated_body_fat}%", f"{water_liters} Liters"
            ]
        }
        st.table(pd.DataFrame(profile_data))

    st.markdown("---")

    # Export Health Report Engine
    st.subheader("📥 Export Comprehensive Health Report")
    st.caption("Generate a structured JSON or clinical summary document for your personal records or physician consultation.")

    export_payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_profile": {
            "gender": gender,
            "age": age,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "activity_level": selected_activity,
            "goal": selected_goal
        },
        "anthropometric_results": {
            "bmi": bmi,
            "category": category,
            "ideal_weight_range_kg": [ideal_min_kg, ideal_max_kg],
            "estimated_body_fat_pct": estimated_body_fat
        },
        "metabolic_results": {
            "bmr_kcal": int(bmr),
            "tdee_kcal": int(tdee),
            "target_calories_kcal": int(target_calories),
            "water_liters": water_liters,
            "macros": {
                "protein_g": protein_g,
                "carbs_g": carbs_g,
                "fats_g": fats_g
            }
        }
    }

    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            label="📄 Download JSON Health Dossier",
            data=json.dumps(export_payload, indent=4),
            file_name=f"VitalAI_Health_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )
    with col_exp2:
        text_report = f"""==================================================
🧬 VITALAI BIOMETRIC HEALTH & METABOLIC REPORT
Generated: {export_payload['generated_at']}
==================================================

1. BIOMETRICS
- Sex: {gender} | Age: {age}
- Weight: {weight_kg:.1f} kg | Height: {height_cm:.1f} cm
- BMI: {bmi} ({category})
- Ideal Weight Range: {ideal_min_kg} kg - {ideal_max_kg} kg
- Body Fat (est): {estimated_body_fat}%

2. METABOLIC PROFILE
- Basal Metabolic Rate (BMR): {int(bmr)} kcal/day
- Total Daily Energy Expenditure (TDEE): {int(tdee)} kcal/day
- Target Daily Caloric Intake: {int(target_calories)} kcal/day
- Health Goal: {selected_goal}
- Recommended Hydration: {water_liters} Liters/day

3. MACRONUTRIENT ALLOCATION
- Protein: {protein_g}g (~{protein_g*4} kcal)
- Carbs: {carbs_g}g (~{carbs_g*4} kcal)
- Fats: {fats_g}g (~{fats_g*9} kcal)

==================================================
Engineered by VitalAI Autonomous Health Copilot
==================================================
"""
        st.download_button(
            label="📝 Download Text Health Summary",
            data=text_report,
            file_name=f"VitalAI_Summary_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# TAB 2: 24/7 Live AI Health Agent
# =========================================================
with tab_agent:
    st.markdown("""
    <div class="chat-context-box">
        <b>🤖 VitalAI Live Health Copilot</b>: Synced in real-time with your biometrics.
        Ask questions about your meal plans, workout splits, weight targets, or clinical interpretations.
    </div>
    """, unsafe_allow_html=True)

    # Initialize Session State for Chat History & Agent
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    f"Hello! I am **VitalAI**, your 24/7 autonomous Health & Fitness Copilot. "
                    f"I have synchronized your live profile: **BMI {bmi} ({category})**, "
                    f"Daily Target: **{int(target_calories)} kcal**, and Goal: **{selected_goal.split(' (')[0]}**.\n\n"
                    f"How can I assist you right now? Feel free to click one of the suggested prompts below or ask any question!"
                )
            }
        ]

    if "agent_instance" not in st.session_state:
        st.session_state.agent_instance = HealthAgent()

    # Quick Suggestion Chips
    st.caption("Quick Inquiries:")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    suggested_prompt = None

    with col_q1:
        if st.button("🥗 7-Day Meal Plan", use_container_width=True):
            suggested_prompt = "Generate a personalized 7-day meal plan for my calorie target."
    with col_q2:
        if st.button("🏋️ Workout Schedule", use_container_width=True):
            suggested_prompt = "What is the best weekly workout split for my goal and BMI?"
    with col_q3:
        if st.button("🎯 Ideal Weight Roadmap", use_container_width=True):
            suggested_prompt = "How soon can I reach my ideal weight safely?"
    with col_q4:
        if st.button("⚠️ Explain My Health Risks", use_container_width=True):
            suggested_prompt = "Explain my BMI category and potential health risks."

    # Display Chat History
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input handler (manual or via chip)
    user_input = st.chat_input("Ask VitalAI anything about your diet, workouts, or health goals...")

    active_prompt = suggested_prompt if suggested_prompt else user_input

    if active_prompt:
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        # Generate response using 24/7 Agent with updated biometric profile
        agent_reply = st.session_state.agent_instance.respond(
            message=active_prompt,
            profile=user_profile,
            history=st.session_state.chat_messages
        )

        # Display and record assistant message
        with st.chat_message("assistant"):
            st.markdown(agent_reply)
        st.session_state.chat_messages.append({"role": "assistant", "content": agent_reply})


# =========================================================
# TAB 3: Clinical Specifications & Architecture
# =========================================================
with tab_specs:
    st.subheader("📐 System Architecture & Clinical Algorithms")
    st.markdown("""
    This platform demonstrates production-grade **Agentic AI Engineering** principles:

    ### 1. Mathematical Formulas
    - **Quetelet Body Mass Index (BMI)**:
      $$\\text{BMI} = \\frac{\\text{Weight (kg)}}{\\text{Height (m)}^2}$$

    - **Mifflin-St Jeor Equation (Basal Metabolic Rate - BMR)**:
      - *Men*: $\\text{BMR} = 10 \\times \\text{weight (kg)} + 6.25 \\times \\text{height (cm)} - 5 \\times \\text{age} + 5$
      - *Women*: $\\text{BMR} = 10 \\times \\text{weight (kg)} + 6.25 \\times \\text{height (cm)} - 5 \\times \\text{age} - 161$

    - **Total Daily Energy Expenditure (TDEE)**:
      $$\\text{TDEE} = \\text{BMR} \\times \\text{Physical Activity Factor}$$

    - **Deurenberg Adult Body Fat Percentage Estimation**:
      $$\\text{Body Fat \\%} = (1.20 \\times \\text{BMI}) + (0.23 \\times \\text{Age}) - (10.8 \\times \\text{Sex}) - 5.4$$
      *(Sex = 1 for males, 0 for females)*

    ---

    ### 2. World Health Organization (WHO) BMI Classifications
    | Classification | BMI Range ($\\text{kg/m}^2$) | Risk of Comorbidities |
    | :--- | :--- | :--- |
    | **Underweight** | $< 18.5$ | Low (risk of other clinical issues) |
    | **Normal range** | $18.5 - 24.9$ | Average |
    | **Overweight** | $25.0 - 29.9$ | Increased |
    | **Obese Class I** | $30.0 - 34.9$ | Moderate |
    | **Obese Class II** | $35.0 - 39.9$ | Severe |
    | **Obese Class III** | $\\ge 40.0$ | Very Severe |

    ---

    ### 3. Agentic AI Copilot Architecture
    - **State Synchronization**: Live parameter binding between Streamlit UI reactive inputs and agent context memory.
    - **Offline-First Resilience**: Heuristic clinical engine guarantees zero downtime 24/7 without external API limits.
    - **Privacy Protection**: Zero client health data transmitted across untrusted external networks without explicit configuration.
    """)
