# 📚 EduCase — AI-Powered Case Studies for K-12 Classrooms

> **Gemini Live Agent Challenge Submission — Creative Storyteller Category**

EduCase is an AI agent that transforms any classroom topic into an immersive, multimedia case study — in just a few minutes! Teachers input their grade level, subject, and classroom context, and EduCase generates a narrative-driven case study complete with a scene illustration and audio narration.

**Live Demo:** https://educase-39686368932.us-central1.run.app

---

## 🎯 The Problem

Case-based learning is one of the most effective pedagogical approaches for K-12 students — but it's massively underutilized because creating good case studies takes hours. Most teachers rely on textbook problems that feel disconnected from students' lives.

EduCase changes that. A teacher can go from idea to classroom-ready material in the time it takes to make a coffee.

---

## ✨ Features

- **AI-Generated Case Studies** — Gemini 2.0 Flash generates immersive, story-driven case studies tailored to the teacher's grade level, subject, and classroom context. 
- **Dynamic Scene Illustrations** — Imagen 3 generates a custom storybook-style illustration based on the actual story content
- **Audio Narration** — Google Cloud Text-to-Speech reads the full case study aloud, making content accessible to struggling readers
- **Smart Formatting** — Case studies are structured with clear narrative, problem statement, and discussion questions
- **Responsive Layout** — Two-column reading experience optimized for classroom projectors and large screens

---

## 🏗️ Architecture

```
Teacher Input (Grade, Subject, Context)
        ↓
   Flask Backend (Python)
        ↓
   Gemini 2.0 Flash ──→ Case Study Text
        ↓
   Gemini 2.0 Flash ──→ Custom Image Prompt
        ↓
   Imagen 3 ──→ Scene Illustration
        ↓
   Google Cloud Text-to-Speech ──→ Audio Narration
        ↓
   Result Page (Two-column layout with scrollable text)
```

**Google Technologies Used:**
- Gemini 2.0 Flash (via Vertex AI) — case study generation + image prompt generation
- Imagen 3 (imagen-3.0-generate-002) — scene illustration
- Google Cloud Text-to-Speech (en-US-Journey-D) — audio narration
- Google Cloud Run — deployment
- Google Cloud Artifact Registry — container storage

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Google Cloud account with billing enabled
- APIs enabled: Vertex AI, Cloud Text-to-Speech, Cloud Run

### Local Setup

1. **Clone the repo**
```bash
git clone https://github.com/chumki-das/educase.git
cd educase
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Authenticate with Google Cloud**
```bash
gcloud auth application-default login
```

5. **Run the app**
```bash
python3 app.py
```

6. **Visit** `http://127.0.0.1:5000`

### Deploy to Cloud Run

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

| Grade | Subject | Output |
|-------|---------|--------|
| Grade 4 | Math – Fractions | A bear and rabbit argue over cake slices |
| Grade 7 | Science – Ecosystems | A polluted river mystery to investigate |
| Grade 8 | History – Industrial Revolution | A factory worker's moral dilemma in 1842 |

---

## 🌱 Built By

**Chumki Das** — Solo project built for the Google Gemini Live Agent Challenge, March 2026.
