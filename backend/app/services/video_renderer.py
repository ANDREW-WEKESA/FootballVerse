"""Main video rendering orchestrator"""
import glob
import logging
import time
from pathlib import Path
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

from .tts_service import TTSService
from .scene_generator import SceneGenerator

logger = logging.getLogger(__name__)


class VideoRenderer:
    """Main video rendering orchestrator"""
    
    def __init__(self):
        self.tts = TTSService()
        self.scene_gen = SceneGenerator()
        self.output_dir = Path("static/videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def render_story(self, story_id: int, title: str, script: str) -> dict:
        """
        Render a complete story video
        Returns: {"output_path": str, "duration": float, "file_size": int}
        """
        try:
            clips = []
            
            # 1. Title card (3 seconds)
            logger.info(f"Rendering story {story_id}: Creating title card")
            title_img = self.scene_gen.create_title_card(title, story_id)
            title_clip = ImageClip(title_img).set_duration(3)
            clips.append(title_clip)
            
            # 2. Parody disclaimer (5 seconds)
            logger.info(f"Rendering story {story_id}: Creating disclaimer")
            disclaimer_img = self.scene_gen.create_parody_disclaimer(story_id)
            disclaimer_clip = ImageClip(disclaimer_img).set_duration(5)
            clips.append(disclaimer_clip)
            
            # 3. Generate narration
            narration_path = None
            if script.strip():
                logger.info(f"Rendering story {story_id}: Generating narration")
                narration_path = self.tts.generate_narration(script, story_id)
                audio_duration = self.tts.get_audio_duration(narration_path)
                
                # Create text scene for duration of narration
                script_img = self.scene_gen.create_text_scene(
                    script[:200] + "..." if len(script) > 200 else script,
                    story_id,
                    1
                )
                script_clip = ImageClip(script_img).set_duration(audio_duration)
                
                # Add audio to clip
                audio = AudioFileClip(narration_path)
                script_clip = script_clip.set_audio(audio)
                clips.append(script_clip)
            
            # 4. Concatenate all clips
            logger.info(f"Rendering story {story_id}: Composing video")
            final_video = concatenate_videoclips(clips, method="compose")
            
            # 5. Export video
            output_filename = f"story_{story_id}_{int(time.time())}.mp4"
            output_path = self.output_dir / output_filename
            
            logger.info(f"Rendering story {story_id}: Writing video file")
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                bitrate='2000k',
                preset='medium',
                logger=None  # Suppress moviepy progress logging
            )
            
            # 6. Get file info
            file_size = output_path.stat().st_size
            duration = final_video.duration
            
            # 7. Cleanup
            final_video.close()
            self._cleanup_temp_files(story_id)
            
            logger.info(f"Successfully rendered story {story_id}: {output_filename}")
            return {
                "output_path": str(output_path),
                "duration": duration,
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Video rendering failed for story {story_id}: {e}")
            self._cleanup_temp_files(story_id)
            raise
    
    def _cleanup_temp_files(self, story_id: int):
        """Clean up temporary files after rendering"""
        patterns = [
            f"temp/narration_{story_id}.*",
            f"temp/title_{story_id}.*",
            f"temp/scene_{story_id}_*.*",
            f"temp/disclaimer_{story_id}.*"
        ]
        for pattern in patterns:
            for file in glob.glob(pattern):
                try:
                    Path(file).unlink()
                    logger.debug(f"Cleaned up temp file: {file}")
                except Exception as e:
                    logger.warning(f"Failed to clean up {file}: {e}")
