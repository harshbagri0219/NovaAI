from voice.interfaces import VoiceInput, VoiceOutput


def test_voice_input_protocol():
    class Input:
        def listen(self):
            return "hello"

    assert isinstance(Input(), VoiceInput)


def test_voice_output_protocol():
    class Output:
        def speak(self, text):
            pass

    assert isinstance(Output(), VoiceOutput)


def test_voice_input_rejects_missing_listen():
    class BadInput:
        pass

    assert not isinstance(BadInput(), VoiceInput)


def test_voice_output_rejects_missing_speak():
    class BadOutput:
        pass

    assert not isinstance(BadOutput(), VoiceOutput)
