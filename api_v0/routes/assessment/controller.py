from pydub import AudioSegment
from fastapi import UploadFile
from helpers.openai_connection import transcribe_audio, generate_text


class AudioController:
    def __init__(self):
        pass

    async def process_audio(self, file: UploadFile):
        filename = file.filename.replace("\0", "")
        file_extension = filename.split(".")[-1]
        temp_file_path = f"temp_{filename}"

        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        if file_extension != "mp3":
            audio = AudioSegment.from_file(temp_file_path)
            temp_file_path = f"temp_{filename.split('.')[0]}.mp3"
            audio.export(temp_file_path, format="mp3")

        return temp_file_path


class TranscriptController:
    def __init__(self):
        pass

    def transcribe_audio(self, audio_file_path):
        return transcribe_audio(audio_file_path)


class TextGenerationController:
    def __init__(self):
        pass

    def generate_text(self, transcript, language, questions):
        level = "B1"
        language = language["choices"][0]["message"][
            "content"
        ].lower()  # Extract language from response object

        input_prompt_en = f"""
        As an AI English tutor, you're to critique a set of English idiom questions and answers, analyze their credibility, effectiveness, and alignment with the learner's proficiency level (e.g., B1, B2). Summarize performance, offer homework aligning with their level. Evaluate the clarity, accuracy, comprehension, and knowledge gauge of the idiom questions. Review correctness and comprehensiveness of answers.
Propose improvement to responses to enhance their effectiveness. Your critique should offer detailed, constructive feedback.

English Proficiency Level: {level}
Questions for Assessment: {questions}
Extract answers from: {transcript}

Feedback example:
Feedback: At the {level}, an error in 'Its' usage. Corrected: "It's raining cats and dogs." For their level, understanding such contractions is crucial. Homework: practice common contractions.

Structural example:

{
"trainee_performance": "Clear, accurate responses. Needs complexity, accuracy improvement.",
"assessment_details": [
{
"question": "Favorite food?",
"answer": "Pasta, love for Italian culture.",
"feedback": "Adequate understanding, English use for B1. Reason for preference is clear."
},
{
"question": "Age?",
"answer": "19.",
"feedback": "Accurate, straightforward, meets B1 expectations."
},
{
"question": "Residence?",
"answer": "Nicaragua, Central America.",
"feedback": "Clear response, good vocabulary."
}
],
"homework_suggestions": [
{
"assignment": "Practice food, pasta vocabulary for detail enhancement."
},
{
"assignment": "Write structured paragraph about favorite food."
},
{
"assignment": "Write an essay about a location for complex description practice."
}
],
"overall_feedback": "Good command of B1. Suggested tasks for consolidation, fluency, accuracy improvement."
}
        """
        input_prompt_fr = f"""
      En tant que tuteur d'anglais IA, vous devez critiquer un ensemble de questions et de réponses sur les idiomes anglais, analyser leur crédibilité, leur efficacité et leur adéquation avec le niveau de compétence de l'apprenant (par exemple, B1, B2). Résumez la performance, proposez des devoirs adaptés au niveau de l'apprenant. Évaluer la clarté, la précision, la compréhension et le niveau de connaissance des questions sur les expressions idiomatiques. Examinez l'exactitude et l'exhaustivité des réponses.

Proposez des améliorations aux réponses afin d'accroître leur efficacité. Votre critique doit être détaillée et constructive.

Niveau de compétence en anglais : {level}
Questions pour l'évaluation : {questions}
Extraire les réponses de : {transcript}

Exemple de retour d'information :
Feedback : Au {level}, une erreur dans l'utilisation de 'Son'. Corrigé : "Il pleut des cordes". Pour leur niveau, la compréhension de ces contractions est cruciale. Devoir : pratiquez les contractions courantes.

Exemple de structure :

{
"trainee_performance" : "Réponses claires et précises. Nécessite une amélioration de la complexité et de la précision,
"assessment_details" : [
{
"question" : "Nourriture préférée ?",
"answer" : "Pasta, amour de la culture italienne",
"feedback" : "Compréhension adéquate, utilisation de l'anglais pour le niveau B1. La raison de la préférence est claire."
},
{
"question" : "Age ?",
"answer" : "19.",
"feedback" : "Précis, direct, répond aux attentes de B1."
},
{
"question" : "Résidence ?",
"answer" : "Nicaragua, Amérique centrale",
"feedback" : "Réponse claire, bon vocabulaire".
}
],
"devoirs_suggestions" : [
{
"assignation" : "Pratiquer le vocabulaire de la nourriture et des pâtes pour améliorer les détails".
},
{
"mission" : "Rédiger un paragraphe structuré sur son plat préféré."
},
{
"mission" : "Rédiger un essai sur un lieu de pratique de description complexe."
}
],
"overall_feedback" : "Bonne maîtrise de B1. Tâches suggérées pour la consolidation, l'amélioration de la fluidité et de la précision."
}
        """

        input_prompt_es = f"""
Como tutor de inglés de AI, debes criticar un conjunto de preguntas y respuestas sobre expresiones idiomáticas en inglés, analizar su credibilidad, eficacia y alineación con el nivel de competencia del alumno (por ejemplo, B1, B2). Resumir el rendimiento, proponer deberes acordes con su nivel. Evaluar la claridad, la precisión, la comprensión y el nivel de conocimiento de las preguntas idiomáticas. Revisar la corrección y exhaustividad de las respuestas.

Proponer mejoras en las respuestas para aumentar su eficacia. Su crítica debe ofrecer comentarios detallados y constructivos.

Nivel de dominio del inglés: {level}
Preguntas para la evaluación: {questions}
Extraiga las respuestas de: {transcript}

Ejemplo de retroalimentación:
Feedback: En el {level}, un error en el uso de 'Su'. Corregido: "Está lloviendo a cántaros". Para su nivel, la comprensión de este tipo de contracciones es crucial. Deberes: practicar las contracciones más comunes.

Ejemplo estructural:

{
"trainee_performance": "Respuestas claras y precisas. Necesita mejorar complejidad, precisión",
"assessment_details": [
{
"question": "¿Comida favorita?",
"answer": "Pasta, amor por la cultura italiana",
"feedback": "Comprensión adecuada, uso del inglés para B1. Motivo de preferencia claro".
},
{
"question": "¿Edad?",
"answer": "19.",
"valoración": "Preciso, directo, cumple con las expectativas B1".
},
{
"pregunta": "¿Residencia?",
"answer": "Nicaragua, América Central",
"feedback": "Respuesta clara, buen vocabulario".
}
],
"homework_suggestions": [
{
"tarea": "Practicar vocabulario de comida, pasta para mejorar detalles".
},
{
"assignment": "Escribir párrafo estructurado sobre comida favorita".
},
{
"assignment": "Escribe un ensayo sobre un lugar para la práctica de descripción compleja".
}
],
"overall_feedback": "Buen dominio del B1. Tareas sugeridas para consolidación, fluidez, mejora de la precisión."
}
        """
        if "english" in language:
            return {"language": "english", "text": generate_text(input_prompt_en)}
        elif "french" in language:
            return {"language": "french", "text": generate_text(input_prompt_fr)}

        elif "spanish" in language:
            return {"language": "spanish", "text": generate_text(input_prompt_es)}
