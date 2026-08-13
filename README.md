# VoiceMind — AI Voice Assistant
A voice-to-voice AI assistant integrating Speech-to-Text, LLM-based response generation, and Text-to-Speech to enable seamless, intelligent voice interaction.

## Overview

VoiceMind is an AI-powered voice assistant that allows users to communicate with an AI through voice.

The system combines Speech-to-Text, AI response generation, and Text-to-Speech to provide a natural voice interaction experience.

VoiceMind supports **Arabic and English** with automatic language detection.

## Technologies

- Python
- Whisper
- Cohere
- gTTS
- Flask
- HTML
- CSS
- JavaScript

## How It Works

```text
User Speech
    ↓
Whisper
    ↓
Speech-to-Text + Language Detection
    ↓
Cohere
    ↓
AI Response
    ↓
gTTS
    ↓
Voice Response

Features

* Voice-based interaction
* Arabic and English support
* Automatic language detection
* AI-generated responses
* Voice responses
* Conversation memory
* New conversation option
* Light and Dark mode

Main Components

Whisper

Used for Speech-to-Text and automatic language detection.

Cohere

Used to generate AI responses based on the user’s speech.

gTTS

Converts the AI-generated text into speech.

Flask

Connects the AI processing with the web application.

Example

English

User:
How are you?

VoiceMind:
I’m doing well! How can I help you?

Arabic

User:
كيف حالك؟

VoiceMind:
أنا بخير! كيف يمكنني مساعدتك؟

Future Improvements

* Real-time voice interaction
* Additional language support
* More voice options
* Persistent conversation history
* Cloud deployment
* Improved speech recognition

