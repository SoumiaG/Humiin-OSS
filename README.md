# 👑 humiin-OSS: Multi-Agent Audio Orchestrator (The High Tech Court Debate)

Welcome to the **humiin-OSS** repository! This project demonstrates how to orchestrate a multi-agent AI debate (featuring Gemini and Claude) and output it as a high-fidelity, native audio `.wav` file, entirely bypassing common WebSocket lockouts and Free-Tier rate limits.

## 🚀 The Tech Stack
* **The Brains (Reasoning):** Gemini 2.5 Flash & Claude Sonnet 4.6
* **The Voice (TTS):** Gemini 2.5 Flash Preview TTS
* **The Architecture:** A hybrid pipeline that splits the LLM text generation from the audio synthesis, bypassing `bidiGenerateContent` restrictions.
* **The Pacing:** Built-in sleep intervals (21s) to safely navigate Google's 3 RPM Free-Tier limits (Say goodbye to `429 RESOURCE_EXHAUSTED`!).

## 🛠️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_NAME/humiin-OSS.git](https://github.com/YOUR_GITHUB_NAME/humiin-OSS.git)
   cd humiin-OSS
