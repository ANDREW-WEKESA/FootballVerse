"""Visual scene generator for video rendering"""
import logging
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class SceneGenerator:
    """Generate visual scenes for video"""
    
    def __init__(self, resolution=(1280, 720)):
        self.width, self.height = resolution
        self.output_dir = Path("temp")
        self.output_dir.mkdir(exist_ok=True)
    
    def create_title_card(self, title: str, story_id: int) -> str:
        """Create opening title card"""
        img = Image.new('RGB', (self.width, self.height), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Try to load font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 72)
            subtitle_font = ImageFont.truetype("arial.ttf", 36)
        except Exception:
            # Fallback to a reasonable default size
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 72)
                subtitle_font = ImageFont.truetype("DejaVuSans.ttf", 36)
            except Exception:
                font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
        
        # Draw title (centered)
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((self.width - text_width) // 2, 
                   (self.height - text_height) // 2 - 50)
        draw.text(position, title, fill='white', font=font)
        
        # Draw subtitle
        subtitle = "A FootballVerse Story"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sub_width = bbox[2] - bbox[0]
        sub_position = ((self.width - sub_width) // 2, 
                       position[1] + text_height + 30)
        draw.text(sub_position, subtitle, fill='#aaaaaa', font=subtitle_font)
        
        # Save
        output_path = self.output_dir / f"title_{story_id}.png"
        img.save(output_path)
        logger.info(f"Created title card for story {story_id}")
        return str(output_path)
    
    def create_text_scene(self, text: str, story_id: int, scene_num: int) -> str:
        """Create scene with text overlay"""
        img = Image.new('RGB', (self.width, self.height), color='#16213e')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except Exception:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 48)
            except Exception:
                font = ImageFont.load_default()
        
        # Wrap text to fit width
        margin = 100
        wrapped_lines = textwrap.wrap(text, width=40)
        
        # Draw text lines
        y_offset = (self.height - len(wrapped_lines) * 60) // 2
        for line in wrapped_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (self.width - line_width) // 2
            draw.text((x, y_offset), line, fill='white', font=font)
            y_offset += 60
        
        output_path = self.output_dir / f"scene_{story_id}_{scene_num}.png"
        img.save(output_path)
        logger.info(f"Created text scene {scene_num} for story {story_id}")
        return str(output_path)
    
    def create_parody_disclaimer(self, story_id: int) -> str:
        """Create parody disclaimer card"""
        img = Image.new('RGB', (self.width, self.height), color='#000000')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except Exception:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", 32)
            except Exception:
                font = ImageFont.load_default()
        
        disclaimer = [
            "PARODY DISCLAIMER",
            "",
            "This content is a fictional parody for entertainment purposes.",
            "Any resemblance to actual events or persons is coincidental.",
            "Sources: TheSportsDB and publicly available football data."
        ]
        
        y_offset = 200
        for line in disclaimer:
            if line:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                x = (self.width - line_width) // 2
                color = 'yellow' if 'PARODY' in line else 'white'
                draw.text((x, y_offset), line, fill=color, font=font)
            y_offset += 50
        
        output_path = self.output_dir / f"disclaimer_{story_id}.png"
        img.save(output_path)
        logger.info(f"Created parody disclaimer for story {story_id}")
        return str(output_path)
