import os
from fish_audio_sdk import Session, TTSRequest
from dotenv import load_dotenv
from generate import generate_answer

load_dotenv()

session = Session(os.getenv("FISHAUDIO_API_KEY"))

def speak_answer(query_text, output_path="answer.mp3"):
    answer = generate_answer(query_text)
    print("Answer:\n", answer)

    with open(output_path, "wb") as f:
        for chunk in session.tts(TTSRequest(text=answer, format="mp3"), backend="s2.1-pro-free"):
            f.write(chunk)

    print(f"Saved spoken answer to {output_path}")
    return answer, output_path

if __name__ == "__main__":
    query = "what did they say about neural networks"
    speak_answer(query)