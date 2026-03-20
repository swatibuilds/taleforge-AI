from gtts import gTTS
from io import BytesIO


# Map common language names to gTTS codes
LANGUAGE_MAP = {
    "english": "en",
    "hindi": "hi",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "russian": "ru",
    "japanese": "ja",
    "korean": "ko",
    "chinese": "zh-cn",
    "arabic": "ar",
}


def narrate_story(story_text: str, language: str = "english"):
    """
    Convert a story into speech using gTTS.

    Parameters
    ----------
    story_text : str
        The generated story text.
    language : str
        Language of the story (e.g., English, Hindi, Spanish).

    Returns
    -------
    BytesIO
        Audio buffer containing narration.
    """

    try:
        # Normalize language
        lang_key = language.lower().strip()

        # Get gTTS language code
        lang_code = LANGUAGE_MAP.get(lang_key, "en")

        # Generate TTS
        tts = gTTS(
            text=story_text,
            lang=lang_code,
            slow=False
        )

        # Save audio to memory
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)

        # Reset pointer
        audio_buffer.seek(0)

        return audio_buffer

    except Exception as e:

        raise RuntimeError(
            f"Narration generation failed: {str(e)}"
        )