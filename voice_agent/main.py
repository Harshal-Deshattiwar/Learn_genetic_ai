from urllib import response
import asyncio
from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI,AsyncOpenAI

from openai.helpers import LocalAudioPlayer

load_dotenv()
client = OpenAI()
async_client = AsyncOpenAI()

async def tts(speech:str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Speak in a friendly and clear manner, suitable for a voice assistant. Keep responses concise and engaging.",  
        input= speech,
        response_format="pcm",
    )as response:
        await LocalAudioPlayer().play(response)

def main():
    r = sr.Recognizer()
    print("Voice agent started. Say 'quit' or 'exit' to stop.\n")


    SYSTEM_PROMT = f"""
            You're an expense voice agent. You are given the transcribed text of a user's voice input. You need to output as if you are an  voice agent and whatever you speak will be converted to audio using AI and played back to user
    """

    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            r.pause_threshold = 5
            messages = [
                 {"role": "system", "content": SYSTEM_PROMT},
            ]
            while True:
                print("Say something! (timeout: 10 seconds)")
                try:
                    audio = r.listen(source, timeout=10, phrase_time_limit=5)
                except sr.WaitTimeoutError:
                    print("Timeout: No speech detected.")
                    print("If you're on macOS, grant microphone access to VS Code in:")
                    print("  System Settings → Privacy & Security → Microphone")
                    return

                print("Processing audio...(STT)")
                stt = r.recognize_google(audio)
                print("You said:", stt)

                messages.append({"role": "user", "content": stt})
                response= client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=messages,
                )   

                print("Agent response:", response.choices[0].message.content)
                # Convert the agent's response to speech
                asyncio.run(tts(response.choices[0].message.content))

    except OSError as e:
        print(f"Microphone error: {e}")
        print("Grant microphone access to VS Code/Terminal in System Settings → Privacy & Security → Microphone")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Google STT request failed: {e}")

   

main()