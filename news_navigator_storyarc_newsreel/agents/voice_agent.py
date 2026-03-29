from gtts import gTTS
import os

def generate_voice(script, news_id):
    output_path = f"output/audio/{news_id}.mp3"
    
    # Text to speech conversion
    tts = gTTS(text=script, lang='en')
    tts.save(output_path)
    
    return output_path