from gtts import gTTS

def gtts_test(text: str) -> None:
    tts = gTTS(text)
    tts.save(f"{text}.mp3")


test_text = "안녕하세요"
gtts_test(test_text)