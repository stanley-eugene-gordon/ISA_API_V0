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
       As an AI teacher known for your friendliness and proficiency, you are assigned to critique a set of evaluation questions and their respective answers, specifically focused on teaching English idioms. You are tasked to carefully analyze the assessment results, offer valuable insights on the credibility and effectiveness of the questions and their respective answers, taking into account the learner's English proficiency level (e.g., B1, B2, etc.). Provide an overall summary of their performance, and suggest relevant homework assignments that align with their current proficiency level.
In your assessment, consider the clarity and accuracy of the questions and answers. Also, assess whether the questions accurately gauge the learners' comprehension and knowledge of English idioms, considering their English proficiency level. Review if the answers given are both correct and comprehensive.
Moreover, suggest improvements or modifications to the assessment responses that could enhance their effectiveness. Your critique should be detailed and offer constructive feedback that aids in the refinement of the assessment's overall quality.
English Proficiency Level: {level}
Questions for Assessment: {questions}
Please extract answers from the following transcript: {transcript}
For instance, your feedback might resemble:
Feedback: At the {level} proficiency level, the learner has made an error in the use of 'Its'. The corrected sentence should read: "It's raining cats and dogs." This is because 'it's' is a contraction of 'it is', making it suitable in this context. For their level, it is crucial to understand such contractions. The homework task could involve practicing such commonly confused contractions.
        """
        input_prompt_fr = f"""
        En tant que professeur d'IA reconnu pour votre amabilité et votre compétence, vous êtes chargé de critiquer un ensemble de questions d'évaluation et leurs réponses respectives, axées spécifiquement sur l'enseignement des idiomes anglais. Votre tâche consiste à analyser minutieusement les résultats de l'évaluation, à offrir des informations précieuses sur la crédibilité et l'efficacité des questions et de leurs réponses respectives, en tenant compte du niveau de compétence en anglais de l'apprenant (par exemple, B1, B2, etc.). Fournissez un résumé global de leurs performances et suggérez des devoirs pertinents qui correspondent à leur niveau de compétence actuel.

        Dans votre évaluation, prenez en compte la clarté et l'exactitude des questions et des réponses. De plus, évaluez si les questions mesurent correctement la compréhension et la connaissance des idiomes anglais de l'apprenant, en tenant compte de leur niveau de compétence en anglais. Examinez si les réponses données sont à la fois correctes et complètes.

        De plus, suggérez des améliorations ou des modifications aux réponses d'évaluation qui pourraient augmenter leur efficacité. Votre critique doit être détaillée et offrir un retour constructif qui aide à affiner la qualité globale de l'évaluation.

        Niveau de compétence en anglais : {level}
        Questions pour évaluation : {questions}
        Veuillez extraire les réponses du transcript suivant : {transcript}

        Par exemple, votre feedback pourrait ressembler à :

        Feedback : Au niveau de compétence {level}, l'apprenant a commis une erreur dans l'utilisation de 'Its'. La phrase corrigée devrait se lire : "It's raining cats and dogs." C'est parce que 'it's' est une contraction de 'it is', le rendant approprié dans ce contexte. Pour leur niveau, il est crucial de comprendre de telles contractions. La tâche à domicile pourrait impliquer de pratiquer de telles contractions couramment confondues.
        """

        input_prompt_es = f"""
        Como profesor de IA conocido por tu amabilidad y competencia, se te ha asignado la tarea de criticar un conjunto de preguntas de evaluación y sus respectivas respuestas, enfocadas específicamente en la enseñanza de los idiomas inglés. Se te pide que analices cuidadosamente los resultados de la evaluación, que ofrezcas valiosos conocimientos sobre la credibilidad y eficacia de las preguntas y sus respectivas respuestas, teniendo en cuenta el nivel de competencia en inglés del aprendiz (por ejemplo, B1, B2, etc.). Proporciona un resumen general de su rendimiento y sugiere tareas de casa relevantes que se alineen con su nivel de competencia actual.

        En tu evaluación, considera la claridad y precisión de las preguntas y respuestas. Además, evalúa si las preguntas miden con precisión la comprensión y el conocimiento de los idiomas ingleses del aprendiz, teniendo en cuenta su nivel de competencia en inglés. Revisa si las respuestas dadas son correctas y completas.

        Además, sugiere mejoras o modificaciones a las respuestas de la evaluación que podrían mejorar su efectividad. Tu crítica debe ser detallada y

        ofrecer retroalimentación constructiva que ayude a perfeccionar la calidad general de la evaluación.

        Nivel de competencia en inglés: {level}
        Preguntas para evaluación: {questions}
        Por favor extrae las respuestas del siguiente transcripción: {transcript}

        Por ejemplo, tu feedback podría ser algo como:

        Feedback: En el nivel de competencia {level}, el aprendiz ha cometido un error en el uso de 'Its'. La frase corregida debería ser: "It's raining cats and dogs". Esto se debe a que 'it's' es una contracción de 'it is', lo que lo hace adecuado en este contexto. Para su nivel, es crucial entender tales contracciones. La tarea de casa podría involucrar la práctica de tales contracciones comúnmente confundidas.
        """
        if "english" in language:
            return {"language": "english", "text": generate_text(input_prompt_en)}
        elif "french" in language:
            return {"language": "french", "text": generate_text(input_prompt_fr)}

        elif "spanish" in language:
            return {"language": "spanish", "text": generate_text(input_prompt_es)}
