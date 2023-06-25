from fastapi import APIRouter, UploadFile, File, Form
import os
from .controller import AudioController, TranscriptController, TextGenerationController
from helpers.openai_connection import generate_text

router = APIRouter(tags=["assessment"])

audio_controller = AudioController()
transcript_controller = TranscriptController()
text_generation_controller = TextGenerationController()

@router.post("/evaluate-speech")
async def evaluate_speech(file: UploadFile = File(...), questions: str = Form(...)):
    audio_file_path = await audio_controller.process_audio(file)
    transcript = transcript_controller.transcribe_audio(audio_file_path)
    language = generate_text(f"What language is this:{transcript}")

    response = text_generation_controller.generate_text(transcript, language, questions)

    if os.path.exists(audio_file_path):
        with open(audio_file_path, 'r') as file:
            os.close(file.fileno())
        os.remove(audio_file_path)

    return response


@router.post("/generate-text")
async def generate_text_api(text: str = Form(...)):
    return generate_text(input_prompt=text)
