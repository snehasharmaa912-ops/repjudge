<div align="center">

```
██████╗  ██████╗  █████╗ ███████╗████████╗
██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝
██████╔╝██║   ██║███████║███████╗   ██║
██╔══██╗██║   ██║██╔══██║╚════██║   ██║
██║  ██║╚██████╔╝██║  ██║███████║   ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝
        M Y   F O R M
```

### AI biomechanics coach that roasts your pushups & squats — then fixes them

[![Live App](https://img.shields.io/badge/🚀_Live_App-repjudge--capstone.streamlit.app-FF4B4B?style=for-the-badge)](https://repjudge-capstone.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.62-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini_3.6_Flash-Vision_API-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev)

</div>

---

> `$ streamlit run app.py`
> `> Opening camera...`
> `> Sending frame to Gemini Vision...`
> `> Analyzing biomechanics...`
> `> Prepare to be roasted.`

<br>

## `>` About

**RepJudge** captures a photo of your starting posture for a pushup or squat
and sends it to **Gemini Vision**, which acts as a blunt-but-competent
strength coach. It roasts real biomechanical flaws — hip sag, knee tracking,
spine alignment — in a witty one-liner, scores your form 0–100, and gives a
checkpoint-by-checkpoint breakdown with corrective cues. Every attempt is
logged so progress over time is visible on a chart.

Built for the **MirAI School of Technology Capstone Program**.

<br>

## `>` Features

| | |
|---|---|
| 📸 **Live camera capture** | Browser-based photo capture via `st.camera_input` — works on phone or laptop |
| 🎯 **Exercise-aware checkpoints** | Pushup and squat each get their own biomechanical checklist |
| 🔥 **AI-generated roast** | Gemini Vision critiques real flaws in the photo, not generic advice |
| ✅ **Structured feedback** | Score + roast + per-checkpoint breakdown, cleanly parsed into UI |
| 📈 **Progress tracking** | Session history with a score trend chart and editable log |
| 🔐 **Key-safe by design** | API key never touches the repo — read from environment/secrets only |

<br>

## `>` Architecture

```
┌──────────────┐   st.camera_input   ┌───────────────────┐
│   Browser     │ ───────────────────▶│   Streamlit App    │
│  (camera)     │                     │      app.py         │
└──────────────┘                     └─────────┬──────────┘
                                                │
                                    PIL.Image   │  exercise + checkpoints
                                                ▼
                                     ┌────────────────────┐
                                     │  Gemini Vision API   │
                                     │ system_instruction + │
                                     │ image + f-string      │
                                     │ checkpoint prompt      │
                                     └─────────┬──────────┘
                                                │ SCORE / Roast / Breakdown
                                                ▼
                                     ┌────────────────────┐
                                     │  st.metric, st.error, │
                                     │  st.expander UI        │
                                     └─────────┬──────────┘
                                                │ append to history
                                                ▼
                                     ┌────────────────────┐
                                     │ st.session_state.hist │
                                     │ → line_chart + data_  │
                                     │   editor progress log  │
                                     └────────────────────┘
```

<br>

## `>` Tech Stack

<div align="center">

| Layer | Technology |
|:---|:---|
| **UI / Dashboard** | Streamlit — columns, expanders, `st.metric`, `st.camera_input`, `st.data_editor` |
| **Image Handling** | Pillow |
| **Data Pipeline** | Pandas — session history → progress chart |
| **AI** | Google Gemini Vision (`google-genai`) |
| **Deployment** | Streamlit Community Cloud |

</div>

<br>

## `>` Setup

```bash
git clone https://github.com/snehasharmaa912-ops/repjudge.git
cd repjudge
pip install -r requirements.txt

# add your key
cp secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml with your real GEMINI_API_KEY

streamlit run app.py
```

<br>

## `>` Deployment

Deployed on **Streamlit Community Cloud**, connected directly to the `main` branch.

🔗 **Live app:** [repjudge-capstone.streamlit.app](https://repjudge-capstone.streamlit.app/)

<details>
<summary><strong>Deploy your own copy</strong></summary>
<br>

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io), connect the repo
3. In **App Settings → Secrets**, paste the contents of `secrets.toml.example` with your real key
4. Deploy

</details>

<br>

## `>` How It Works

1. Pick **Pushup** or **Squat** in the sidebar — checkpoints update automatically
2. Take a photo of your starting position with `st.camera_input`
3. Hit **Roast My Form** — Gemini Vision scores it, roasts the worst flaw(s), and breaks down each checkpoint
4. Every attempt is logged so you can track score trends over a session

<br>

## `>` Capstone Notes

Submitted for the **MirAI School of Technology** Streamlit + Gemini AI Capstone.
See [`SYSTEM_DESIGN.md`](./SYSTEM_DESIGN.md) for the full data flow and prompt
engineering strategy.

<div align="center">

---

Built with 🔥 by **Sneha Sharma** · [GitHub](https://github.com/snehasharmaa912-ops) · [LinkedIn](https://linkedin.com/in/snehasharmaa2006)

</div>
