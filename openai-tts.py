from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI


def tts(_client, _input, _model='tts-1', _voice='alloy', _file_path='./speech.mp3'):
    """
    The Audio API provides a speech endpoint based on our TTS (text-to-speech) model. It comes with 6 built-in voices
    and can be used to:
        Narrate a written blog post
        Produce spoken audio in multiple languages
        Give real time audio output using streaming
    :param _client: OpenAI client
    :param _input: text
    :param _model: tts-1, tts-1-hd
    :param _voice: alloy, echo, fable, onyx, nova, and shimmer
    :param _file_path: output file save path, default='./speech.mp3'
    :return:
    """
    response = _client.audio.speech.create(model=_model, voice=_voice, input=_input)
    response.stream_to_file(_file_path)
    return


if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()
    input_text = "Today is a wonderful day to build something people love!"
    # speech_file_path = Path(__file__).parent / "speech.mp3"
    tts(client, input_text)
