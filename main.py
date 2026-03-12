import os
import time
import wave
import anthropic
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- 1. API KEYS (Pulled safely from the environment) ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not GOOGLE_API_KEY or not ANTHROPIC_API_KEY:
    raise ValueError("Missing API Keys. Please set GOOGLE_API_KEY and ANTHROPIC_API_KEY in your .env file.")

def run_royal_debate_paced():
    client = genai.Client(api_key=GOOGLE_API_KEY)
    claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # --- MODELS (Verified March 2026) ---
    GEMINI_BRAIN = "gemini-2.5-flash" 
    CLAUDE_BRAIN = "claude-sonnet-4-6" 
    GEMINI_VOICE = "gemini-2.5-flash-preview-tts"

    all_audio = bytearray()
    history = ""

    # Step 1: Text-to-Speech Engine
    def synthesize_speech(text, voice_name):
        response = client.models.generate_content(
            model=GEMINI_VOICE,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
                    )
                )
            )
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                return part.inline_data.data
        return b""

    # Step 2: The Paced AI Turn
    def ai_turn(actor, prompt, voice, is_claude=False, sys_instr=None):
        print(f"🧠 {actor} is thinking...")
        
        if is_claude:
            c_resp = claude_client.messages.create(
                model=CLAUDE_BRAIN, max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            generated_text = c_resp.content[0].text
        else:
            config = types.GenerateContentConfig(system_instruction=sys_instr) if sys_instr else None
            g_resp = client.models.generate_content(
                model=GEMINI_BRAIN,
                contents=prompt,
                config=config
            )
            generated_text = g_resp.text
            
        print(f"🎙️ {actor} says: '{generated_text.strip()}'")
        
        audio_bytes = synthesize_speech(generated_text, voice)
        return audio_bytes, generated_text

    print("🔌 Starting humiin-OSS Audio Pipeline (Respecting 3 RPM Limit)...")

    try:
        # 1. Butler Introduction 
        print("\n🕴️ Butler: Announcing...")
        butler_text = "Her Majesty is seated. Presenting Gemini and Claude to discuss Yann LeCun's AMI Labs."
        print(f"🎙️ Butler says: '{butler_text}'")
        all_audio.extend(synthesize_speech(butler_text, "Charon"))
        history += f"Butler: {butler_text}\n"

        print("⏳ Sipping tea for 21 seconds to avoid API rate limits...")
        time.sleep(21)

        # 2. Queen Command
        q_prompt = f"Context: {history}\nCommand: 'Gentlemen, explain AMI Labs. Is it true LLMs are dead ends?' Keep it brief."
        audio, text = ai_turn("Queen", q_prompt, "Puck", sys_instr="You are Queen Charlotte. Imperious judge.")
        all_audio.extend(audio)
        history += f"Queen: {text}\n"

        print("⏳ Sipping tea for 21 seconds...")
        time.sleep(21)

        # 3. Gemini Defense
        g_prompt = f"Context: {history}\nIntroduce yourself. Defend LLMs as the foundation of reasoning. Maximum 2 sentences."
        audio, text = ai_turn("Gemini", g_prompt, "Aoede", sys_instr="You are Gemini. Defend LLMs elegantly.")
        all_audio.extend(audio)
        history += f"Gemini: {text}\n"

        print("⏳ Sipping tea for 21 seconds...")
        time.sleep(21)

        # 4. Claude Reasoning 
        c_prompt = f"Context: {history}\nRespond as Claude. Support LeCun's World Models. Keep it Regency-flavored. Maximum 2 sentences."
        audio, text = ai_turn("Claude", c_prompt, "Fenrir", is_claude=True)
        all_audio.extend(audio)
        history += f"Claude: {text}\n"

        print("⏳ Sipping tea for 21 seconds...")
        time.sleep(21)

        # 5. THE FINALE: Queen's Dismissal
        q_final_prompt = f"Context: {history}\nRespond: 'World Models or Word Models, I prefer Diamond Models. Butler, more tea. Dismissed!' Make it final."
        audio, text = ai_turn("Queen", q_final_prompt, "Puck", sys_instr="You are Queen Charlotte.")
        all_audio.extend(audio)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return

    # Save to disk
    filename = "bridgerton_debate_humiin.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000) 
        wf.writeframes(all_audio)
    
    print(f"\n🎧 Court Adjourned! File saved: {filename}")

if __name__ == "__main__":
    run_royal_debate_paced()
