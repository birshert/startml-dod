import os

import openai

openai.api_key = os.environ.get("OPENAI_KEY", None)

API_ERROR = openai.OpenAIError


def transcribe(filename: str) -> tuple[str, str]:
    with open(filename, "rb") as audio:
        original = openai.Audio.transcribe("whisper-1", audio, response_format="text")

    with open(filename, "rb") as audio:
        english = openai.Audio.translate("whisper-1", audio, response_format="text")

    return original, english


def ask_gpt(user_message: str, system_prompt: str = None, model: str = "gpt-3.5-turbo", temperature: int = 0) -> str:
    messages = []

    if system_prompt is not None:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        messages=messages,
    )

    return response["choices"][0]["message"]["content"]


def generate_corrected_transcript(transcript: str) -> str:
    system_prompt = (
        "You are a helpful assistant for the company Raiffeisen Bank. Your task is to correct any "
        "spelling discrepancies in the transcribed text. Make sure that the names of the following "
        "products are spelled correctly: Raiffeisen Direct, Premium Savings Account, Gold Credit Card, "
        "Raiffeisen Mortgage, BusinessPlus Loan, FlexiDeposit, e-Raiffeisen Online, SecurePay Gateway, "
        "Wealth Management Pro, Retirement Planner, SME Business Package. Only add necessary punctuation "
        "such as periods, commas, and capitalization, and use only the context provided. Keep the original language."
    )

    return ask_gpt(user_message=transcript, system_prompt=system_prompt)


def answer_question_about_transcription(
    transcript: str, question: str = "Write short summary", model: str = "gpt-3.5-turbo"
) -> str:
    user_message = f"""Here is a transcript marked by triple quotes. 
Answer the question in the end based on this transcript.

```
{transcript}
```

Question: {question}"""

    return ask_gpt(user_message=user_message, model=model)


def process_audio_file(filename: str) -> dict[str, str]:
    original_transcript, english_transcript = transcribe(filename)

    english_transcript = generate_corrected_transcript(english_transcript)

    english_summary = answer_question_about_transcription(english_transcript)

    return {
        "original_transcript": original_transcript,
        "transcript": english_transcript,
        "summary": english_summary,
    }
