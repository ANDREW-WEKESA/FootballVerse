"""
Compilation Video Renderer
Combines real YouTube goal clips with AI narration
"""
import glob
import logging
import time
from pathlib import Path
from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, 
    concatenate_videoclips, CompositeVideoClip
)

from .tts_service import TTSService
from .scene_generator import SceneGenerator

logger = logging.getLogger(__name__)


class CompilationRenderer:
    """Render compilation videos with real goal footage + narration"""
    
    def __init__(self):
        self.tts = TTSService()
        self.scene_gen = SceneGenerator(resolution=(1920, 1080))
        self.output_dir = Path("static/videos")
        self.clips_dir = Path("static/videos/clips")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.clips_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def render_goal_compilation(
        self,
        story_id: int,
        title: str,
        goals: list
    ) -> dict:
        """
        Render a compilation of multiple goals with narration
        
        Args:
            story_id: Story ID
            title: Overall compilation title
            goals: List of dicts with:
                - clip_path: Path to goal video file
                - title: Goal title (e.g., "vs Getafe 2007")
                - narration: Text to narrate before/after goal
                - trim_start: Optional seconds to trim from start
                - trim_end: Optional seconds to trim from end
        
        Example:
            goals = [
                {
                    "clip_path": "static/videos/clips/messi_getafe_2007.mp4",
                    "title": "The Maradona Goal - vs Getafe 2007",
                    "narration": "April 18, 2007. Messi picks up the ball and begins an impossible run.",
                    "trim_start": 2,
                    "trim_end": 1
                },
                ...
            ]
        """
        try:
            all_clips = []
            
            # 1. Opening title card (4 seconds)
            logger.info(f"Creating title card for compilation {story_id}")
            title_img = self.scene_gen.create_cinematic_title_card(
                title,
                f"{len(goals)} Iconic Moments",
                story_id
            )
            title_clip = ImageClip(title_img).set_duration(4)
            all_clips.append(title_clip)
            
            # 2. Disclaimer (3 seconds)
            disclaimer_img = self.scene_gen.create_parody_disclaimer(story_id)
            disclaimer_clip = ImageClip(disclaimer_img).set_duration(3)
            all_clips.append(disclaimer_clip)
            
            # 3. Process each goal
            for idx, goal in enumerate(goals, 1):
                logger.info(f"Processing goal {idx}/{len(goals)}: {goal['title']}")
                
                # Check if clip exists
                clip_path = Path(goal['clip_path'])
                if not clip_path.exists():
                    logger.warning(f"Clip not found: {clip_path}, skipping...")
                    continue
                
                # a) Goal title card (2 seconds)
                goal_title_img = self.scene_gen.create_chapter_card(
                    goal['title'],
                    idx,
                    story_id
                )
                goal_title_clip = ImageClip(goal_title_img).set_duration(2)
                all_clips.append(goal_title_clip)
                
                # b) Pre-goal narration (if provided)
                if goal.get('narration'):
                    narration_path = self.tts.generate_narration(
                        goal['narration'],
                        story_id * 100 + idx
                    )
                    audio_duration = self.tts.get_audio_duration(narration_path)
                    
                    # Create narration scene
                    narration_img = self.scene_gen.create_text_scene(
                        goal['narration'][:300],
                        story_id,
                        idx * 10
                    )
                    narration_clip = ImageClip(narration_img).set_duration(audio_duration)
                    audio = AudioFileClip(narration_path)
                    narration_clip = narration_clip.set_audio(audio)
                    all_clips.append(narration_clip)
                
                # c) The actual goal clip!
                logger.info(f"Loading goal video: {clip_path}")
                goal_video = VideoFileClip(str(clip_path))
                
                # Trim if specified
                trim_start = goal.get('trim_start', 0)
                trim_end = goal.get('trim_end', 0)
                
                if trim_start > 0 or trim_end > 0:
                    end_time = goal_video.duration - trim_end if trim_end > 0 else goal_video.duration
                    goal_video = goal_video.subclip(trim_start, end_time)
                
                # Resize to 1080p if needed
                if goal_video.h != 1080:
                    goal_video = goal_video.resize(height=1080)
                
                all_clips.append(goal_video)
                
                # d) Slow-motion replay (optional - last 3 seconds in slow-mo)
                if goal.get('add_slowmo', False) and goal_video.duration > 3:
                    slowmo_start = max(0, goal_video.duration - 3)
                    slowmo_clip = goal_video.subclip(slowmo_start, goal_video.duration)
                    slowmo_clip = slowmo_clip.fx(lambda clip: clip.speedx(0.5))  # 50% speed
                    
                    # Add "REPLAY" text overlay using ImageClip instead
                    from PIL import Image, ImageDraw, ImageFont
                    
                    # Create replay text image
                    replay_img = Image.new('RGBA', (300, 100), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(replay_img)
                    
                    try:
                        font = ImageFont.truetype("arialbd.ttf", 60)
                    except:
                        font = ImageFont.load_default()
                    
                    # Draw text with shadow
                    draw.text((4, 4), "REPLAY", fill=(0, 0, 0, 200), font=font)
                    draw.text((2, 2), "REPLAY", fill=(255, 255, 255, 255), font=font)
                    
                    # Save temp image
                    replay_img_path = self.temp_dir / f"replay_{story_id}_{idx}.png"
                    replay_img.save(replay_img_path)
                    
                    # Create overlay clip
                    txt_clip = ImageClip(str(replay_img_path)).set_duration(slowmo_clip.duration).set_position(('right', 'top'))
                    
                    slowmo_with_text = CompositeVideoClip([slowmo_clip, txt_clip])
                    all_clips.append(slowmo_with_text)
            
            # 4. End card (3 seconds)
            end_img = self.scene_gen.create_end_card(story_id)
            end_clip = ImageClip(end_img).set_duration(3)
            all_clips.append(end_clip)
            
            # 5. Concatenate everything
            logger.info(f"Concatenating {len(all_clips)} clips...")
            final_video = concatenate_videoclips(all_clips, method="compose")
            
            # 6. Export
            output_filename = f"compilation_{story_id}_{int(time.time())}.mp4"
            output_path = self.output_dir / output_filename
            
            logger.info(f"Exporting compilation to {output_path}")
            final_video.write_videofile(
                str(output_path),
                fps=30,
                codec='libx264',
                audio_codec='aac',
                bitrate='5000k',  # High quality for real footage
                preset='medium'
            )
            
            # 7. Get stats
            file_size = output_path.stat().st_size
            duration = final_video.duration
            
            # Cleanup
            final_video.close()
            for clip in all_clips:
                try:
                    clip.close()
                except:
                    pass
            self._cleanup_temp_files(story_id)
            
            logger.info(f"Compilation complete: {output_filename}")
            return {
                "output_path": str(output_path),
                "duration": duration,
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "goals_count": len(goals),
                "format": "compilation"
            }
            
        except Exception as e:
            logger.error(f"Compilation rendering failed: {e}", exc_info=True)
            self._cleanup_temp_files(story_id)
            raise
    
    def _cleanup_temp_files(self, story_id: int):
        """Clean up temporary files"""
        patterns = [
            f"temp/narration_{story_id}*.*",
            f"temp/*_{story_id}.*",
        ]
        for pattern in patterns:
            for file in glob.glob(pattern):
                try:
                    Path(file).unlink()
                except Exception:
                    pass
