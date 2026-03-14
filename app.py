from flask import Flask, render_template, request
from google import genai
from google.genai import types
import vertexai
from google.cloud import texttospeech
import os
import re
import time

app = Flask(__name__)

PROJECT_ID = "project-1fb03e0b-cd2f-4d0e-a48"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def format_case_study(text):
    lines = text.split('\n')
    output = []
    in_ol = False
    in_ul = False

    for line in lines:
        line = line.strip()
        if not line:
            if in_ul: output.append('</ul>'); in_ul = False
            if in_ol: output.append('</ol>'); in_ol = False
            continue

        if line.lower().startswith('title:'):
            title = line[6:].strip()
            title = re.sub(r'\*\*(.*?)\*\*', r'\1', title)
            output.append(f'<span class="case-title">{title}</span>')

        elif re.match(r'^\*?\*?(the problem|discussion questions?|hints?|your task|the challenge|background)[:\*]*', line, re.IGNORECASE):
            clean = re.sub(r'\*', '', line).replace(':', '').strip()
            output.append(f'<h2>{clean}</h2>')

        elif re.match(r'^\*\*.+\*\*:?$', line):
            clean = re.sub(r'\*\*(.*?)\*\*', r'\1', line).replace(':', '').strip()
            output.append(f'<h3>{clean}</h3>')

        elif re.match(r'^\d+\.', line):
            if in_ul: output.append('</ul>'); in_ul = False
            if not in_ol: output.append('<ol>'); in_ol = True
            clean = re.sub(r'^\d+\.\s*', '', line)
            clean = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean)
            output.append(f'<li>{clean}</li>')

        elif line.startswith('* ') or line.startswith('- '):
            if in_ol: output.append('</ol>'); in_ol = False
            if not in_ul: output.append('<ul>'); in_ul = True
            clean = line[2:]
            clean = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean)
            output.append(f'<li>{clean}</li>')

        else:
            if in_ul: output.append('</ul>'); in_ul = False
            if in_ol: output.append('</ol>'); in_ol = False
            clean = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            output.append(f'<p>{clean}</p>')

    if in_ul: output.append('</ul>')
    if in_ol: output.append('</ol>')

    return '\n'.join(output)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    grade = request.form["grade"]
    subject = request.form["subject"]
    context = request.form["context"]
    include_image = request.form.get("include_image") == "yes"
    include_audio = request.form.get("include_audio") == "yes"

    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    # --- GENERATE CASE STUDY TEXT ---
    prompt = f"""
    You are EduCase, an AI that creates immersive case studies for K-12 students.

    Create an engaging case study for:
    - Grade: {grade}
    - Subject: {subject}
    - Classroom context: {context}

    The case study should include:
    1. A catchy title (on its own line, prefixed with "Title:")
    2. A vivid narrative story that pulls students in (2-3 paragraphs)
    3. A clear problem for students to solve
    4. 3 discussion questions

    Make it feel like a story, not a worksheet. Use real characters, real stakes, and real emotions.
    """

    text_response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt
    )
    case_study_text = format_case_study(text_response.text)

    # --- GENERATE IMAGE (optional) ---
    image_filename = None
    if include_image:
        try:
            image_prompt_request = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"""Based on this case study, write a single sentence describing a warm,
                    colorful storybook illustration that captures the setting and key objects from the story.
                    Do NOT include any people or characters in the description at all.
                    Focus only on the environment, objects, food, animals, and mood.
                    The illustration must contain NO text, words, numbers, or letters of any kind.
                    Case study: {text_response.text[:500]}

                    Reply with only the image description, nothing else."""
            )
            image_prompt = image_prompt_request.text.strip() + "Storybook illustration style, warm colors, no text, no words, no numbers, no letters."
            print(f"IMAGE PROMPT: {image_prompt}")

            image_response = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=image_prompt,
                config=types.GenerateImagesConfig(number_of_images=1)
            )
            if image_response.generated_images:
                timestamp = int(time.time())
                image_filename = f"case_study_image_{timestamp}.png"
                with open(f"static/{image_filename}", "wb") as f:
                    f.write(image_response.generated_images[0].image.image_bytes)
                print(f"IMAGE SAVED: {image_filename}")
            else:
                print("IMAGE ERROR: No images returned from Imagen")
        except Exception as e:
            print(f"IMAGE ERROR: {e}")
            image_filename = None

    # --- GENERATE AUDIO (optional) ---
    audio_filename = None
    if include_audio:
        try:
            tts_client = texttospeech.TextToSpeechClient()
            clean_text = re.sub(r'<[^>]+>', '', case_study_text)
            synthesis_input = texttospeech.SynthesisInput(text=clean_text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Journey-D",
                ssml_gender=texttospeech.SsmlVoiceGender.MALE
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            audio_response = tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            timestamp = int(time.time())
            audio_filename = f"case_study_audio_{timestamp}.mp3"
            with open(f"static/{audio_filename}", "wb") as f:
                f.write(audio_response.audio_content)
            print(f"AUDIO SAVED: {audio_filename}")
        except Exception as e:
            print(f"AUDIO ERROR: {e}")
            audio_filename = None

    return render_template("result.html",
        case_study=case_study_text,
        grade=grade,
        subject=subject,
        include_image=include_image,
        include_audio=include_audio,
        image_filename=image_filename,
        audio_filename=audio_filename
    )

if __name__ == "__main__":
    app.run(debug=True)