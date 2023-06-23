from fastapi import APIRouter, UploadFile, File
import os
import openai
from .controller import AudioController, TranscriptController, TextGenerationController
from helpers.openai_connection import generate_text

router = APIRouter(tags=["assessment"])

audio_controller = AudioController()
transcript_controller = TranscriptController()
text_generation_controller = TextGenerationController()

@router.post("/generate_text")
async def generate_text_api(file: UploadFile = File(...)):    
    audio_file_path = await audio_controller.process_audio(file)
    transcript = transcript_controller.transcribe_audio(audio_file_path)
    language = generate_text(f"What language is this:{transcript}")

    response = text_generation_controller.generate_text(transcript, language)

    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)

    return response