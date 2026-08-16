"""Text-to-speech narration generator"""
import logging
from pathlib import Path
from gtts import gTTS
from moviepy.editor import AudioFileClip

logger = logging.getLogger(__name__)


class TTSService:
    """Text-to-speech narration generator"""
    
    def __init__(self, output_dir: str = "temp"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_narration(self, text: str, story_id: int) -> str:
        """Generate audio narration from script text"""
        if not text.strip():
            return None
        
        output_path = self.output_dir / f"narration_{story_id}.mp3"
        
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(output_path))
            logger.info(f"Generated narration for story {story_id}")
            return str(output_path)
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise
    
    def get_audio_duration(self, audio_path: str) -> float:
        """Get duration of audio file in seconds"""
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        return duration
