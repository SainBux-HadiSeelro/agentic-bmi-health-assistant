# 🧬 VitalAI - Technical & Clinical Specifications

**Document Version**: 2.0.0  
**Project**: VitalAI - Autonomous Health & BMI Intelligence Platform  
**Architecture Classification**: Agentic AI Biometric Decision Support System  

---

## 1. System Overview

**VitalAI** is an advanced, production-ready Health & Biometric Intelligence Platform engineered with modern **Agentic AI** design principles. It transitions traditional, static BMI calculators into an autonomous, context-aware health analytics copilot capable of:
1. Multi-metric anthropometric analysis.
2. Basal and active metabolic rate forecasting.
3. 24/7 autonomous conversational health guidance.
4. Exportable clinical-grade health dossiers.

```
                      ┌──────────────────────────────────────┐
                      │      User Biometric Inputs           │
                      │  (Metric / Imperial, Age, Sex, Goal) │
                      └──────────────────┬───────────────────┘
                                         │
                                         ▼
                      ┌──────────────────────────────────────┐
                      │    Clinical Calculation Pipeline     │
                      │   - Quetelet Body Mass Index (BMI)   │
                      │   - Mifflin-St Jeor BMR & TDEE       │
                      │   - Deurenberg Body Fat %            │
                      │   - WHO Stratification               │
                      └──────────────────┬───────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
      ┌─────────────────────────┐                 ┌─────────────────────────┐
      │  Interactive Dashboard  │                 │  24/7 VitalAI Agent     │
      │  - Visual Spectrum Bar  │                 │  - Live Context Memory  │
      │  - Macronutrient Table  │◄───────────────►│  - Intent Classifier    │
      │  - JSON / Text Export   │                 │  - Autonomous Engine    │
      └─────────────────────────┘                 └─────────────────────────┘
```

---

## 2. Anthropometric & Clinical Mathematical Specifications

### 2.1 Quetelet Body Mass Index (BMI)
BMI is determined via Adolphe Quetelet's standard metric index:
$$\text{BMI} = \frac{\text{Weight (kg)}}{\left(\frac{\text{Height (cm)}}{100}\right)^2}$$

### 2.2 World Health Organization (WHO) Stratification
The platform implements official WHO and CDC adult BMI categories:

| Index Range ($\text{kg/m}^2$) | WHO Classification | Comorbidity Health Risk Profile |
| :--- | :--- | :--- |
| $< 18.5$ | **Underweight** | Malnutrition, osteopenia, anemia, endocrine dysfunction |
| $18.5 - 24.9$ | **Normal Weight** | Baseline population risk |
| $25.0 - 29.9$ | **Overweight** | Elevated risk of cardiovascular disease, insulin resistance |
| $30.0 - 34.9$ | **Obese Class I** | Moderate risk of coronary artery disease, hypertension |
| $35.0 - 39.9$ | **Obese Class II** | High risk of type-2 diabetes, dyslipidemia, sleep apnea |
| $\ge 40.0$ | **Obese Class III** | Severe / extreme clinical risk; physician supervision advised |

### 2.3 Basal Metabolic Rate (BMR) - Mifflin-St Jeor Formulation
Extensively validated as the most accurate clinical formula for non-obese and obese adults:
- **Males**:
  $$\text{BMR}_{\text{male}} = 10 \times \text{Weight}_{\text{kg}} + 6.25 \times \text{Height}_{\text{cm}} - 5 \times \text{Age}_{\text{years}} + 5$$
- **Females**:
  $$\text{BMR}_{\text{female}} = 10 \times \text{Weight}_{\text{kg}} + 6.25 \times \text{Height}_{\text{cm}} - 5 \times \text{Age}_{\text{years}} - 161$$

### 2.4 Total Daily Energy Expenditure (TDEE) & Caloric Targets
Derived using the Harris-Benedict / Katch-McArdle physical activity multipliers:
- **Sedentary**: $1.20 \times \text{BMR}$
- **Lightly Active**: $1.375 \times \text{BMR}$
- **Moderately Active**: $1.55 \times \text{BMR}$
- **Very Active**: $1.725 \times \text{BMR}$
- **Extra Active**: $1.90 \times \text{BMR}$

Goal calibrations:
- **Fat Loss**: $\text{Target} = \max(1200, \text{TDEE} - 500 \text{ kcal})$
- **Maintenance**: $\text{Target} = \text{TDEE}$
- **Muscle Hypertrophy**: $\text{Target} = \text{TDEE} + 350 \text{ kcal}$

### 2.5 Adult Body Fat Percentage Estimation (Deurenberg Model)
$$\text{Body Fat } \% = (1.20 \times \text{BMI}) + (0.23 \times \text{Age}) - (10.8 \times \text{Sex}) - 5.4$$
*(where $\text{Sex} = 1$ for biological males, $0$ for biological females)*

---

## 3. Agentic AI Copilot Specifications (`agent.py`)

### 3.1 State Synchronization Engine
The AI Agent maintains an in-memory `UserHealthProfile` state synced across every interaction:
- **Biometric Bindings**: Live reactive updates on slider or unit changes.
- **Context Injection**: Every query received by the agent is injected with:
  - Exact BMI and WHO classification.
  - Basal rate vs target daily energy budget.
  - Projected weight variance from the ideal weight boundary.

### 3.2 24/7 Resilience & Zero-Downtime Architecture
- **Offline Autonomous Engine (`SmartAutonomousEngine`)**: Pattern-matching and medical heuristic engine that operates 100% locally with zero internet dependency, zero API cost, and zero latency.
- **Optional LLM Upgradability**: Compatible with Gemini or OpenAI models when API keys are configured, falling back smoothly to the autonomous engine on quota limits or network outages.
- **Safety Boundaries**: The agent strictly declines prescribing medical drugs or diagnostics, reinforcing standard health coaching and encouraging professional medical consultations for extreme outliers.

---

## 4. Privacy, Security & Data Protection Specifications

- **Zero Remote Storage**: User biometric inputs are processed purely within transient runtime session memory (`st.session_state`).
- **HIPAA / GDPR Ethical Alignment**: No personal identifiable health information (PII) is permanently saved, logged to disk, or sent to telemetry trackers without consent.
- **Export Integrity**: Generated JSON and Text exports are created client-side via in-memory buffers.

---

## 5. User Interface Specifications

- **Design System**: Glassmorphic Cyber-Dark (`#0f172a` canvas, `#1e293b` cards with `rgba(255,255,255,0.08)` borders).
- **Responsive Layout**: Fluid column grids that adapt seamlessly to desktop, tablet, and mobile browsers.
- **Unit Dual-Engine**: Bi-directional conversion support for Metric ($\text{kg}, \text{cm}$) and Imperial ($\text{lbs}, \text{ft}/\text{in}$).
- **Visual Spectrum Gauge**: High-contrast, color-coded visual indicator displaying user position relative to international benchmarks.

---

## 6. Verification & Quality Assurance

- **Unit Stability**: All calculations strictly enforce bounded domains (e.g. minimum heights, non-negative caloric floors).
- **Syntax Verification**: Strict Python 3.12+ compatibility verified with clean AST compilation (`py_compile`).
