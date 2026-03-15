# 📚 EduCase — AI-Powered Case Studies for K-12 Classrooms

> **Gemini Live Agent Challenge Submission — Creative Storyteller Category**

Case-based learning is one of the most effective pedagogical approaches for K-12 students. But creating a good case study takes hours — time teachers simply don't have. EduCase changes that. Teachers input a grade level, subject, and classroom context, and EduCase generates a narrative-driven multimedia case study complete with a custom scene illustration and audio narration — all in one cohesive output.

**Live Demo:** https://educase-39686368932.us-central1.run.app

---

## ✨ Features

- **AI-Generated Case Studies** — Gemini 2.5 Flash generates immersive, story-driven case studies tailored to the teacher's grade level, subject, and classroom context
- **Classroom Context Field** — teachers describe their students in plain language (gifted class, ESL classroom, recent curriculum topics, student interests) and EduCase adapts the case study accordingly
- **Dynamic Scene Illustrations** — Imagen 3 generates a custom storybook-style illustration based on the actual story content via a two-step Gemini prompt pipeline
- **Audio Narration** — Google Cloud Text-to-Speech reads the full case study aloud, making content accessible to all learners
- **Optional Multimedia** — illustration and audio are both optional, giving teachers control over what their classroom needs
- **Projector-Ready Layout** — two-column result page optimized for classroom display

---

## 🏗️ Architecture

```
Teacher Input (Grade, Subject, Classroom Context)
        ↓
   Flask Backend (Python · Gunicorn · Cloud Run)
        ↓
   Gemini 2.5 Flash ──────────────→ Case Study Text
        ↓
   Gemini 2.5 Flash ──────────────→ Custom Image Prompt
        ↓
   Imagen 3 ──────────────────────→ Scene Illustration (PNG)
        ↓
   Google Cloud Text-to-Speech ───→ Audio Narration (MP3)
        ↓
   Result Page (Text + Illustration + Audio)
```

**Google Technologies Used:**
- Gemini 2.5 Flash (via Vertex AI) — case study generation + image prompt generation
- Imagen 3 (imagen-3.0-generate-002) — scene illustration
- Google Cloud Text-to-Speech (en-US-Journey-D) — audio narration
- Google Cloud Run — deployment
- Google Cloud Build — container build pipeline
- Google Cloud Artifact Registry — container image storage

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Google Cloud account with billing enabled
- Google Cloud project with the following APIs enabled:
  - Vertex AI API
  - Cloud Text-to-Speech API
  - Cloud Run API
  - Cloud Build API

### Local Setup

**1. Clone the repo**
```bash
git clone https://github.com/chumki-das/educase.git
cd educase
```

**2. Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Authenticate with Google Cloud**
```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

**5. Run the app**
```bash
python3 app.py
```

**6. Visit** `http://127.0.0.1:5000`

---

## 🧪 Reproducible Testing

Once the app is running locally at `http://127.0.0.1:5000`, use the following test cases to verify all features are working:

**Test 1 — Text only (fastest)**
- Grade: Grade 5
- Subject: Math — Fractions
- Classroom context: Students are struggling with fractions, keep it simple and visual
- Enable illustration: No
- Enable audio: No
- Expected: A formatted case study with title, narrative, problem statement, and 3 discussion questions

**Test 2 — With illustration**
- Grade: Grade 7
- Subject: Science — Ecosystems
- Classroom context: Gifted class, push them to think critically about human impact
- Enable illustration: Yes
- Enable audio: No
- Expected: Case study + a storybook-style scene illustration related to the story

**Test 3 — Full multimedia**
- Grade: Grade 8
- Subject: History — Industrial Revolution
- Classroom context: We just finished reading a chapter on factory conditions in 1840s England
- Enable illustration: Yes
- Enable audio: Yes
- Expected: Full case study with matching illustration and audio narration player

**What to check in terminal output:**
- `IMAGE PROMPT:` — confirms Gemini generated a custom image description
- `IMAGE SAVED:` — confirms Imagen 3 returned an image successfully
- `AUDIO SAVED:` — confirms Text-to-Speech generated the MP3

---

## ☁️ Deploy to Cloud Run

```bash
gcloud run deploy educase \
  --source . \
  --project=YOUR_PROJECT_ID \
  --region=us-central1 \
  --allow-unauthenticated \
  --timeout=300 \
  --memory=1Gi
```

---

## 📁 Project Structure

```
educase/
├── app.py              # Flask backend — generation logic
├── templates/
│   ├── index.html      # Teacher input form
│   └── result.html     # Case study results page
├── static/             # Generated images and audio (runtime)
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
└── .dockerignore
```

---

## 💡 Example Use Cases

| Grade | Subject | Classroom Context | Output |
|-------|---------|-------------------|--------|
| Grade 4 | Math – Fractions | ESL classroom, keep language simple | Simple story with fraction problem |
| Grade 7 | Science – Ecosystems | Gifted class, push harder than grade level | Complex environmental case with data |
| Grade 8 | History – Industrial Revolution | Just finished a unit on factory conditions | Character-driven historical dilemma |

---

## 🌱 What's Next

- **Shareable links** — persistent URLs so teachers can share cases with students including audio
- **Curriculum standard alignment** — tag cases to Common Core or provincial standards
- **Real-world data grounding** — connect to subject-relevant datasets for richer outputs
- **Student-facing interactive mode** — students read, listen, and submit responses
- **Saved case library** — teacher accounts with history of generated cases

---

## 👤 Built By

**Chumki Das** — Solo project built for the Google Gemini Live Agent Challenge, March 2026.