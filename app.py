"""
app.py

Flask API layer for the VoiceMind AI voice assistant.

Frontend:
    index.html

Backend:
    Flask API

AI Pipeline:
    Audio → Whisper → Language Detection → Cohere → gTTS → Audio
"""

import os
import base64
import uuid

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from assistant_core import (
    transcribe_audio,
    get_ai_reply,
    synthesize_speech,
    reset_conversation,
)


# =========================
# 1. Flask App
# =========================

app = Flask(__name__)

# Allow the frontend to communicate with the API
CORS(app)


# =========================
# 2. Temporary Audio Folder
# =========================

UPLOAD_DIR = "temp_audio"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# =========================
# 3. Health Check
# =========================

@app.route("/api/health", methods=["GET"])
def health():
    """
    Check whether the VoiceMind AI backend is running.
    """

    return jsonify({
        "status": "Voice assistant backend is running"
    })


# =========================
# 4. Voice Chat API
# =========================

@app.route("/api/voice-chat", methods=["POST"])
def voice_chat():

    # Make sure an audio file was received
    if "audio" not in request.files:
        return jsonify({
            "error": "No audio file received (expected field 'audio')"
        }), 400


    audio_file = request.files["audio"]


    # =========================
    # Create Unique File Names
    # =========================

    session_id = uuid.uuid4().hex

    input_path = os.path.join(
        UPLOAD_DIR,
        f"input_{session_id}.webm"
    )

    output_path = os.path.join(
        UPLOAD_DIR,
        f"response_{session_id}.mp3"
    )


    # Save uploaded audio
    audio_file.save(input_path)


    try:

        # =========================
        # 1. Speech-to-Text
        # =========================

        user_text, language = transcribe_audio(
            input_path
        )


        # If Whisper didn't hear anything
        if not user_text:

            return jsonify({
                "transcript": "",
                "reply": "I didn't hear you. Please try again.",
                "audio_base64": "",
                "language": language
            })


        # =========================
        # 2. AI Response
        # =========================

        answer = get_ai_reply(
            user_text,
            language
        )


        # =========================
        # 3. Text-to-Speech
        # =========================

        synthesize_speech(
            answer,
            output_path,
            language
        )


        # =========================
        # 4. Convert Audio to Base64
        # =========================

        with open(
            output_path,
            "rb"
        ) as f:

            audio_b64 = base64.b64encode(
                f.read()
            ).decode("utf-8")


        # =========================
        # 5. Return Result
        # =========================

        return jsonify({

            "transcript": user_text,

            "reply": answer,

            "audio_base64": audio_b64,

            "language": language

        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


    finally:

        # =========================
        # Clean Temporary Files
        # =========================

        for path in (
            input_path,
            output_path
        ):

            if os.path.exists(path):

                try:
                    os.remove(path)

                except Exception:
                    pass


# =========================
# 5. Frontend
# =========================

@app.route("/")
def home():

    return send_file(
        "index.html"
    )


# =========================
# 6. Reset Conversation
# =========================

@app.route(
    "/api/reset",
    methods=["POST"]
)
def reset():

    reset_conversation()

    return jsonify({
        "status": "conversation reset"
    })


# =========================
# 7. Run Flask
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )