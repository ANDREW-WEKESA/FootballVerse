"""Enhanced video rendering with cinematic effects and multiple formats"""
import glob
import logging
import time
from pathlib import Path
from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, VideoClip
)
import numpy as np

from .tts_service import TTSService
from .scene_generator import SceneGenerator

logger = logging.getLogger(__name__)


class EnhancedVideoRenderer:
    """Enhanced video renderer with cinematic transitions and multiple formats"""
    
    def __init__(self):
        self.tts = TTSService()
        self.scene_gen = SceneGenerator(resolution=(1920, 1080))  # Full HD
        self.output_dir = Path("static/videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def crossfade_transition(self, clip1, clip2, duration=0.5):
        """Create crossfade transition between clips"""
        def make_frame(t):
            if t < duration:
                alpha = t / duration
                frame1 = clip1.get_frame(clip1.duration - duration + t)
                frame2 = clip2.get_frame(t)
                return (1 - alpha) * frame1 + alpha * frame2
            else:
                return clip2.get_frame(t)
        
        return VideoClip(make_frame, duration=clip2.duration)
    
    def fade_in(self, clip, duration=0.5):
        """Add fade in effect to clip"""
        def apply_fade(get_frame, t):
            if t < duration:
                alpha = t / duration
                return (alpha * get_frame(t)).astype('uint8')
            return get_frame(t)
        
        return clip.fl(lambda gf, t: apply_fade(gf, t))
    
    def fade_out(self, clip, duration=0.5):
        """Add fade out effect to clip"""
        def apply_fade(get_frame, t):
            if t > clip.duration - duration:
                alpha = (clip.duration - t) / duration
                return (alpha * get_frame(t)).astype('uint8')
            return get_frame(t)
        
        return clip.fl(lambda gf, t: apply_fade(gf, t))
    
    def render_short_reel(self, story_id: int, title: str, script: str, 
                         target_duration: int = 60) -> dict:
        """
        Render short-form content (15-60 seconds) for social media
        Optimized for Instagram Reels, TikTok, YouTube Shorts
        """
        try:
            clips = []
            
            # 1. Quick title card (2 seconds)
            title_img = self.scene_gen.create_cinematic_title_card(
                title, "A FootballVerse Short", story_id
            )
            title_clip = ImageClip(title_img).set_duration(2)
            title_clip = self.fade_in(title_clip, 0.3)
            clips.append(title_clip)
            
            # 2. Main content - truncate script to fit target duration
            if script.strip():
                # Limit script length for short format
                max_chars = min(len(script), 400)
                short_script = script[:max_chars]
                if len(script) > max_chars:
                    short_script = short_script.rsplit('.', 1)[0] + '.'
                
                narration_path = self.tts.generate_narration(short_script, story_id)
                audio_duration = self.tts.get_audio_duration(narration_path)
                
                # Create dynamic text scene
                script_img = self.scene_gen.create_text_scene(
                    short_script[:300] if len(short_script) > 300 else short_script,
                    story_id,
                    1
                )
                script_clip = ImageClip(script_img).set_duration(audio_duration)
                audio = AudioFileClip(narration_path)
                script_clip = script_clip.set_audio(audio)
                clips.append(script_clip)
            
            # 3. Quick end card (1.5 seconds)
            end_img = self.scene_gen.create_end_card(story_id)
            end_clip = ImageClip(end_img).set_duration(1.5)
            end_clip = self.fade_out(end_clip, 0.5)
            clips.append(end_clip)
            
            # Concatenate with smooth transitions
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Export for social media (vertical format optional)
            output_filename = f"reel_{story_id}_{int(time.time())}.mp4"
            output_path = self.output_dir / output_filename
            
            final_video.write_videofile(
                str(output_path),
                fps=30,  # Higher FPS for smooth social media playback
                codec='libx264',
                audio_codec='aac',
                bitrate='3000k',
                preset='fast'
            )
            
            file_size = output_path.stat().st_size
            duration = final_video.duration
            final_video.close()
            self._cleanup_temp_files(story_id)
            
            return {
                "output_path": str(output_path),
                "duration": duration,
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "format": "short_reel"
            }
            
        except Exception as e:
            logger.error(f"Reel rendering failed for story {story_id}: {e}")
            self._cleanup_temp_files(story_id)
            raise
    
    def render_full_episode(self, story_id: int, title: str, chapters: list,
                           stats: list = None) -> dict:
        """
        Render full documentary-style episode (3-5 minutes) with chapters
        
        chapters: list of dicts with 'title', 'narration', 'duration'
        stats: list of dicts with 'label', 'value'
        """
        try:
            clips = []
            
            # 1. Opening title (4 seconds)
            title_img = self.scene_gen.create_cinematic_title_card(
                title, "A FootballVerse Documentary", story_id
            )
            title_clip = ImageClip(title_img).set_duration(4)
            title_clip = self.fade_in(title_clip, 0.5)
            clips.append(title_clip)
            
            # 2. Content disclaimer (4 seconds)
            disclaimer_img = self.scene_gen.create_parody_disclaimer(story_id)
            disclaimer_clip = ImageClip(disclaimer_img).set_duration(4)
            clips.append(disclaimer_clip)
            
            # 3. Render each chapter
            for idx, chapter in enumerate(chapters, 1):
                # Chapter card (2 seconds)
                chapter_img = self.scene_gen.create_chapter_card(
                    chapter['title'], idx, story_id
                )
                chapter_clip = ImageClip(chapter_img).set_duration(2)
                clips.append(chapter_clip)
                
                # Chapter narration
                narration = chapter['narration']
                narration_path = self.tts.generate_narration(narration, 
                                                            story_id * 100 + idx)
                audio_duration = self.tts.get_audio_duration(narration_path)
                
                # Create scene
                scene_img = self.scene_gen.create_text_scene(
                    narration[:350] if len(narration) > 350 else narration,
                    story_id,
                    idx
                )
                scene_clip = ImageClip(scene_img).set_duration(audio_duration)
                audio = AudioFileClip(narration_path)
                scene_clip = scene_clip.set_audio(audio)
                clips.append(scene_clip)
            
            # 4. Statistics overlays (if provided)
            if stats:
                for idx, stat in enumerate(stats, 1):
                    stat_img = self.scene_gen.create_stat_overlay(
                        stat['label'], stat['value'], story_id, idx * 10
                    )
                    stat_clip = ImageClip(stat_img).set_duration(2.5)
                    clips.append(stat_clip)
            
            # 5. End card (3 seconds)
            end_img = self.scene_gen.create_end_card(story_id)
            end_clip = ImageClip(end_img).set_duration(3)
            end_clip = self.fade_out(end_clip, 0.8)
            clips.append(end_clip)
            
            # Concatenate all
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Export high quality
            output_filename = f"episode_{story_id}_{int(time.time())}.mp4"
            output_path = self.output_dir / output_filename
            
            final_video.write_videofile(
                str(output_path),
                fps=24,
                codec='libx264',
                audio_codec='aac',
                bitrate='4000k',  # Higher bitrate for quality
                preset='medium'
            )
            
            file_size = output_path.stat().st_size
            duration = final_video.duration
            final_video.close()
            self._cleanup_temp_files(story_id)
            
            return {
                "output_path": str(output_path),
                "duration": duration,
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "format": "full_episode",
                "chapters": len(chapters)
            }
            
        except Exception as e:
            logger.error(f"Episode rendering failed for story {story_id}: {e}")
            self._cleanup_temp_files(story_id)
            raise
    
    def _cleanup_temp_files(self, story_id: int):
        """Clean up temporary files after rendering"""
        patterns = [
            f"temp/narration_{story_id}*.*",
            f"temp/title_{story_id}.*",
            f"temp/scene_{story_id}_*.*",
            f"temp/chapter_{story_id}_*.*",
            f"temp/stat_{story_id}_*.*",
            f"temp/disclaimer_{story_id}.*",
            f"temp/endcard_{story_id}.*"
        ]
        for pattern in patterns:
            for file in glob.glob(pattern):
                try:
                    Path(file).unlink()
                    logger.debug(f"Cleaned up: {file}")
                except Exception as e:
                    logger.warning(f"Failed to clean up {file}: {e}")
