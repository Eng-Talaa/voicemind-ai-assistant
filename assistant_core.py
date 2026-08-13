"""
assistant_core.py

Voice AI core for the Flask web application.

Supports automatic Arabic / English language detection:
Speech -> Whisper -> Language Detection -> Cohere -> gTTS
"""

import os
import whisper
import cohere
from dotenv import load_dotenv
from gtts import gTTS


# =========================
# 1. Load API Key
# =========================

load_dotenv()

co = cohere.ClientV2(
    api_key=os.getenv("COHERE_API_KEY")
)


# =========================
# 2. Load Whisper
# =========================

whisper_model = whisper.load_model("tiny")


# =========================
# 3. Conversation Memory
# =========================

messages = [
    {
        "role": "system",
        "content": (
            "You are a friendly voice assistant. "
            "Have natural and short conversations with the user. "
            "Keep your answers concise because your responses will be spoken aloud. "
            "Ask a simple follow-up question when appropriate. "
            "Always respond in the same language as the user's latest message. "
            "If the user speaks Arabic, respond in Arabic. "
            "If the user speaks English, respond in English."
        )
    }
]


# =========================
# 4. Speech-to-Text
# =========================

def transcribe_audio(audio_path: str):

    result = whisper_model.transcribe(
        audio_path,
        fp16=False
    )

    user_text = result["text"].strip()

    # Get language detected by Whisper
    detected_language = result.get(
        "language",
        "en"
    )

    # Print language in Terminal for testing
    print(
        "Detected language:",
        detected_language
    )

    # Support Arabic and English
    if detected_language == "ar":
        language = "ar"
    else:
        language = "en"

    print(
        "Using response language:",
        language
    )

    print(
        "Transcription:",
        user_text
    )

    return user_text, language


# =========================
# 5. AI Response
# =========================

def get_ai_reply(
    user_text: str,
    language: str
) -> str:

    messages.append({
        "role": "user",
        "content": user_text
    })

    # Tell Cohere which language to use
    if language == "ar":
        language_instruction = (
            "Respond in Arabic. "
            "Use clear and natural Arabic."
        )
    else:
        language_instruction = (
            "Respond in English. "
            "Use clear and natural English."
        )

    response = co.chat(
        model="command-a-03-2025",
        messages=[
            *messages,
            {
                "role": "system",
                "content": language_instruction
            }
        ]
    )

    answer = next(
        item.text
        for item in response.message.content
        if item.type == "text"
    )

    messages.append({
        "role": "assistant",
        "content": answer
    })

    return answer


# =========================
# 6. Text-to-Speech
# =========================

def synthesize_speech(
    text: str,
    output_path: str,
    language: str = "en"
) -> str:

    # Arabic voice
    if language == "ar":
        tts_language = "ar"

    # English voice
    else:
        tts_language = "en"

    print(
        "TTS language:",
        tts_language
    )

    tts = gTTS(
        text=text,
        lang=tts_language
    )

    if os.path.exists(output_path):
        os.remove(output_path)

    tts.save(output_path)

    return output_path


# =========================
# 7. Reset Conversation
# =========================

def reset_conversation():

    global messages

    messages = messages[:1]