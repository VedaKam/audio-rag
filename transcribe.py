from speechmatics.models import ConnectionSettings, BatchTranscriptionConfig
from speechmatics.batch_client import BatchClient
from httpx import HTTPStatusError
import os
from dotenv import load_dotenv

load_dotenv()

settings = ConnectionSettings(
    url="https://asr.api.speechmatics.com/v2",
    auth_token=os.getenv("SPEECHMATICS_API_KEY"),
)

transcription_config = BatchTranscriptionConfig(
    language="en",
    diarization="speaker",
)

def transcribe(audio_path):
    with BatchClient(settings) as client:
        try:
            job_id = client.submit_job(audio=audio_path, transcription_config=transcription_config)
        except HTTPStatusError as e:
            print("Speechmatics error response:", e.response.text)
            raise
        print(f"Job submitted: {job_id}, waiting for completion...")
        transcript = client.wait_for_completion(job_id, transcription_format="txt")
        return transcript

if __name__ == "__main__":
    transcript_text = transcribe("input_audio.mp3")
    with open("transcript.txt", "w") as f:
        f.write(transcript_text)
    print("Saved transcript.txt")