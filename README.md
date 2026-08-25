```
██████╗  ██████╗  █████╗ ███████╗████████╗
██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝
██████╔╝██║   ██║███████║███████╗   ██║
██╔══██╗██║   ██║██╔══██║╚════██║   ██║
██║  ██║╚██████╔╝██║  ██║███████║   ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝
     MY FORM — a Gemini Vision workout form coach
```

> `$ streamlit run app.py`
> `> Opening camera...`
> `> Sending frame to Gemini Vision...`
> `> Analyzing biomechanics...`
> `> Prepare to be roasted.`

## `> about`

**Roast My Form** captures a photo of your starting posture for a pushup or
squat and sends it to **Gemini Vision**, which acts as a blunt-but-competent
strength coach: it roasts real biomechanical flaws (hip sag, knee tracking,
spine alignment) in a witty one-liner, scores your form 0–100, and gives a
checkpoint-by-checkpoint breakdown with corrective cues. Attempts are logged
so progress over time is visible on a chart.

Built for the **MirAI School of Technology Capstone Program**.

## `> architecture`

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

## `> tech stack`

| Layer         | Tech                                            |
|---------------|--------------------------------------------------|
| UI/Dashboard  | Streamlit (columns, expanders, `st.metric`, `st.camera_input`, `st.data_editor`) |
| Image handling| Pillow                                            |
| Data pipeline | Pandas (session history → progress chart)         |
| AI            | Google Gemini Vision (`google-generativeai`)      |
| Deployment    | Streamlit Community Cloud                         |

## `> setup`

```bash
git clone https://github.com/snehasharmaa912-ops/roast-my-form.git
cd roast-my-form
pip install -r requirements.txt

# add your key
cp secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml with your real GEMINI_API_KEY

streamlit run app.py
```

## `> deployment`

Deployed on **Streamlit Community Cloud**.
🔗 **Live app:** `<ADD_YOUR_LIVE_LINK_HERE>`

To deploy your own copy:
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io), connect the repo
3. In **App Settings → Secrets**, paste the contents of `secrets.toml.example` with your real key
4. Deploy

## `> how it works`

1. Pick **Pushup** or **Squat** in the sidebar — checkpoints update automatically
2. Take a photo of your starting position with `st.camera_input`
3. Hit **Roast My Form** — Gemini Vision scores it, roasts the worst flaw(s), and breaks down each checkpoint
4. Every attempt is logged so you can track score trends over a session

## `> capstone notes`

Submitted for the MirAI School of Technology Streamlit + Gemini AI Capstone.
See `SYSTEM_DESIGN.md` for the full data flow and prompt engineering strategy.
