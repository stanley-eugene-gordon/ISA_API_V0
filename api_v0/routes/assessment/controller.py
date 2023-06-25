from pydub import AudioSegment
from fastapi import UploadFile
from helpers.openai_connection import transcribe_audio,  generate_text

class AudioController:
    def __init__(self):
        pass

    async def process_audio(self, file: UploadFile):
        filename = file.filename.replace("\0", "")
        file_extension = filename.split('.')[-1]
        temp_file_path = f"temp_{filename}"

        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        if file_extension != 'mp3':
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
        language = language["choices"][0]["message"]["content"].lower()  # Extract language from response object

        input_prompt_en = f"""
        this were the questions asked: {questions}
        The language proficiency of this student is evaluated from their speech Please take note of any bad practices, unusual uses of verbs or poor sentence structures. Here is the speech for evaluation:\n{transcript["text"]}
        \nIn your analysis, please ensure to include the following structured response:
        1. Findings: List the notable observations such as bad practices, unusual uses of verbs, and flawed sentence structures. 
        2. Language Level: Determine and mention the student's proficiency in the language of the provided speech at the end of the evaluation. 
        3. Overall Summary: Provide an overall feedback paragraph, making it personal by using the student's name if provided, or using the term 'student' if not. 
        Ensure to return the feedback following this specific structure, making sure to refer to the language being evaluated (English) in your evaluation and add a list of homework tasks for the student to improve their language proficiency also use emojis to make the feedback more engaging.
        """

        input_prompt_fr = f"""
        es questions posées sont les suivantes: {questions}
        La compétence linguistique de cet étudiant est évaluée à partir de son discours. Veuillez prendre note de toute mauvaise pratique, utilisation inhabituelle des verbes ou structures de phrases médiocres. Voici le discours à évaluer :\n{transcript["text"]}
        \nDans votre analyse, veuillez inclure la réponse structurée suivante:
        1. Observations : Énumérez les observations notables comme les mauvaises pratiques, les usages inhabituels des verbes et les structures de phrases défectueuses.
        2. Niveau de langue : Déterminez et mentionnez la compétence de l'étudiant dans la langue du discours fourni à la fin de l'évaluation.
        3. Résumé global : Fournissez un paragraphe de feedback global, en le personnalisant en utilisant le nom de l'étudiant si fourni, ou en utilisant le terme 'étudiant' sinon.
        Assurez-vous de retourner le feedback en suivant cette structure spécifique, en vous assurant de vous référer à la langue évaluée (français) dans votre évaluation.
        """

        input_prompt_es = f"""
        Estas fueron las preguntas: {questions}
        La competencia lingüística de este estudiante se evalúa a partir de su discurso. Tenga en cuenta cualquier mala práctica, uso inusual de verbos o estructuras de frases pobres. Aquí está el discurso para la evaluación:\n{transcript["text"]}
        \nEn su análisis, asegúrese de incluir la siguiente respuesta estructurada:
        1. Hallazgos: Enumere las observaciones notables como malas prácticas, usos inusuales de verbos y estructuras de frases defectuosas.
        2. Nivel de lenguaje: Determine y mencione la competencia del estudiante en el lenguaje del discurso proporcionado al final de la evaluación.
        3. Resumen general: Proporcione un párrafo de feedback general, personalizándolo usando el nombre del estudiante si se proporciona, o usando el término 'estudiante' en caso contrario.
        Asegúrese de devolver el feedback siguiendo esta estructura específica, asegurándose de referirse al idioma que se evalúa (español) en su evaluación.
        """

        if  'english' in language:
            return {
                'language': 'english',
                'text': generate_text(input_prompt_en)
            }
        elif 'french' in language:
            return {
                'language': 'french',
                'text': generate_text(input_prompt_fr)
            }
        
        elif 'spanish' in language:
            return {
                'language': 'spanish',
                'text': generate_text(input_prompt_es)
            }
        