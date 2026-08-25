import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Roast My Form",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_KEY = os.environ.get("GEMINI_API_KEY", st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else "")

PREFERRED_MODELS = [
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-flash-latest",
]

@st.cache_resource
def get_client(api_key: str):
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def get_model_diagnostics(client):
    """Returns (model_name_or_none, available_list, error_message)"""
    if client is None:
        return None, [], "No API key provided."
    try:
        models = list(client.models.list())
        available = [m.name.replace("models/", "") for m in models]
    except Exception as e:
        return None, [], f"models.list() failed: {e}"

    if not available:
        return None, [], "models.list() succeeded but returned zero models."

    for name in PREFERRED_MODELS:
        if name in available:
            return name, available, None

    return available[0], available, None

CLIENT = get_client(API_KEY)
MODEL_NAME, AVAILABLE_MODELS, MODEL_ERROR = get_model_diagnostics(CLIENT)

EXERCISES = ["Pushup", "Squat"]

CHECKPOINTS = {
    "Pushup": ["Hand placement", "Elbow angle", "Hip sag / pike", "Neck & spine alignment", "Core bracing"],
    "Squat": ["Foot stance", "Knee tracking", "Hip depth", "Back angle / spine neutrality", "Weight distribution"],
}

if "history" not in st.session_state:
    st.session_state.history = []
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

def analyze_form(image: Image.Image, exercise: str):
    checkpoints = ", ".join(CHECKPOINTS[exercise])

    system_prompt = (
        "You are a blunt, funny but genuinely knowledgeable strength coach analyzing a "
        "single starting-posture photo for a bodyweight exercise. You roast bad form with "
        "sharp one-liners, but every roast must be backed by a real, specific biomechanical "
        "observation — never vague. You always end with clear corrective cues, not just criticism."
    )

    user_prompt = f"""
The photo shows the STARTING POSITION for a {exercise}.
Evaluate these specific checkpoints: {checkpoints}.

Respond in this exact structure:

### Form Score
A single integer 0-100 representing overall form quality, on its own line, formatted exactly as:
SCORE: <number>

### The Roast
2-3 punchy sentences roasting the worst 1-2 flaws you actually see in the photo. If the form
genuinely looks solid, roast something minor or just hype them up — don't invent flaws.

### Checkpoint Breakdown
A short bullet per checkpoint ({checkpoints}), marked ✅ if it looks correct or ⚠️ if it needs work,
with one specific corrective cue for each ⚠️.
"""

    if CLIENT is None:
        return {
            "score": 0,
            "roast": "⚠️ No GEMINI_API_KEY found in environment/secrets — this is a placeholder response.",
            "breakdown": "1. Set GEMINI_API_KEY in Streamlit Cloud secrets.\n2. Re-run the app.",
            "raw": "",
        }

    if not MODEL_NAME:
        return {
            "score": 0,
            "roast": f"⚠️ {MODEL_ERROR or 'No compatible Gemini model found.'}",
            "breakdown": "Check API key validity and that the Generative Language API is enabled for your project.",
            "raw": "",
        }

    try:
        response = CLIENT.models.generate_content(
            model=MODEL_NAME,
            contents=[user_prompt, image],
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
        text = response.text
    except Exception as e:
        return {
            "score": 0,
            "roast": f"⚠️ Gemini couldn't process this request: {e}",
            "breakdown": "Try again in a moment, or take a new photo — this is usually a transient API issue, not a bug in the app.",
            "raw": "",
        }

    score = 50
    for line in text.splitlines():
        if line.strip().upper().startswith("SCORE:"):
            try:
                score = int("".join(c for c in line if c.isdigit()))
            except ValueError:
                pass
            break

    roast, breakdown = text, ""
    if "### Checkpoint Breakdown" in text:
        roast_part, breakdown = text.split("### Checkpoint Breakdown", 1)
        roast = roast_part.split("### The Roast")[-1].strip() if "### The Roast" in roast_part else roast_part.strip()
        breakdown = breakdown.strip()

    return {"score": score, "roast": roast.strip(), "breakdown": breakdown, "raw": text}

with st.sidebar:
    st.title("🏋️ Roast My Form")
    st.caption("Snap your starting posture. Get roasted. Get corrected.")

    exercise = st.selectbox("Exercise", EXERCISES)
    st.markdown(f"**Checkpoints for {exercise}:**")
    for cp in CHECKPOINTS[exercise]:
        st.write(f"- {cp}")

    st.divider()
    with st.expander("🔧 Model diagnostics", expanded=False):
        if MODEL_NAME:
            st.success(f"Using: `{MODEL_NAME}`")
            st.caption(f"{len(AVAILABLE_MODELS)} models available to this key")
        else:
            st.error(MODEL_ERROR or "No model resolved.")

    st.caption("Built with Streamlit + Gemini Vision • MirAI School of Technology Capstone")


st.title("Roast My Form")
st.caption("AI-powered biomechanics feedback for your starting posture — no gym buddy required.")

col_cam, col_result = st.columns([1, 1.4])

with col_cam:
    st.subheader("📸 Capture your posture")
    photo = st.camera_input(f"Get in your {exercise.lower()} starting position and take a photo")

    if photo is not None:
        image = Image.open(photo)
        if st.button("Roast My Form", use_container_width=True):
            with st.spinner("Gemini is judging your biomechanics..."):
                result = analyze_form(image, exercise)
                st.session_state.last_analysis = result
                st.session_state.history.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Exercise": exercise,
                    "Score": result["score"],
                })

with col_result:
    st.subheader("📊 Results")
    result = st.session_state.last_analysis

    if result is None:
        st.info("Take a photo and hit **Roast My Form** to see your breakdown here.")
    else:
        score = result["score"]
        delta_label = "solid form" if score >= 75 else ("needs work" if score >= 50 else "danger zone")
        st.metric("Form Score", f"{score}/100", delta=delta_label,
                   delta_color="normal" if score >= 75 else "inverse")

        st.error(result["roast"])

        with st.expander("🔍 Checkpoint Breakdown", expanded=True):
            st.markdown(result["breakdown"])

st.divider()

# --- PROGRESS TRACKING ---
st.subheader("📈 Progress Over Time")
if st.session_state.history:
    hist_df = pd.DataFrame(st.session_state.history)
    chart_col, table_col = st.columns([2, 1])

    with chart_col:
        chart_data = hist_df.copy()
        chart_data["Attempt"] = range(1, len(chart_data) + 1)
        st.line_chart(chart_data.set_index("Attempt")["Score"])

    with table_col:
        st.write(f"**Attempts logged:** {len(hist_df)}")
        st.write(f"**Best score:** {hist_df['Score'].max()}")
        st.write(f"**Average score:** {hist_df['Score'].mean():.1f}")

    with st.expander("📋 Full session log", expanded=False):
        edited_hist = st.data_editor(hist_df, num_rows="dynamic", use_container_width=True)
        st.session_state.history = edited_hist.to_dict("records")
else:
    st.caption("No attempts logged yet — your history will build up as you roast more sets.")
