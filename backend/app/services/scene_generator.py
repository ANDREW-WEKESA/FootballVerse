"""Visual scene generator for video rendering"""
import logging
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

logger = logging.getLogger(__name__)


class SceneGenerator:
    """Generate visual scenes for video"""
    
    def __init__(self, resolution=(1920, 1080)):  # Full HD for cinematic quality
        self.width, self.height = resolution
        self.output_dir = Path("temp")
        self.output_dir.mkdir(exist_ok=True)
        
        # Cinematic color palette
        self.colors = {
            'primary': '#00D9FF',      # Bright cyan
            'secondary': '#FF6B35',    # Vibrant orange
            'dark': '#0A0E27',         # Deep navy
            'darker': '#050814',       # Almost black
            'gold': '#FFD700',         # Gold
            'silver': '#C0C0C0',       # Silver
            'text': '#FFFFFF',         # White
            'subtitle': '#B8C5D6'      # Light blue-grey
        }
    
    def _get_font(self, size, bold=False):
        """Load font with fallbacks"""
        font_names = [
            "arialbd.ttf" if bold else "arial.ttf",
            "Arial Bold.ttf" if bold else "Arial.ttf",
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        ]
        
        for font_name in font_names:
            try:
                return ImageFont.truetype(font_name, size)
            except Exception:
                continue
        
        # Fallback to default
        return ImageFont.load_default()
    
    def create_cinematic_title_card(self, title: str, subtitle: str, story_id: int) -> str:
        """Create cinematic opening title card with gradient and effects"""
        img = Image.new('RGB', (self.width, self.height), color=self.colors['darker'])
        draw = ImageDraw.Draw(img)
        
        # Add gradient overlay
        for y in range(self.height):
            opacity = int(255 * (y / self.height) * 0.3)
            color = (10 + opacity // 2, 14 + opacity // 2, 39 + opacity // 2)
            draw.rectangle([(0, y), (self.width, y + 1)], fill=color)
        
        # Draw accent bars
        bar_height = 4
        draw.rectangle([(0, self.height // 3), (self.width, self.height // 3 + bar_height)], 
                      fill=self.colors['primary'])
        draw.rectangle([(0, self.height * 2 // 3), (self.width, self.height * 2 // 3 + bar_height)], 
                      fill=self.colors['secondary'])
        
        # Title
        font_title = self._get_font(120, bold=True)
        
        # Wrap title if too long
        max_width = self.width - 200
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font_title)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw title lines
        total_height = len(lines) * 140
        start_y = (self.height - total_height) // 2 - 80
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_title)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            y = start_y + (i * 140)
            
            # Shadow
            draw.text((x + 4, y + 4), line, fill='#000000', font=font_title)
            # Main text with gradient effect (gold)
            draw.text((x, y), line, fill=self.colors['gold'], font=font_title)
        
        # Subtitle
        font_subtitle = self._get_font(48)
        bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        sub_width = bbox[2] - bbox[0]
        sub_x = (self.width - sub_width) // 2
        sub_y = start_y + total_height + 40
        draw.text((sub_x, sub_y), subtitle, fill=self.colors['subtitle'], font=font_subtitle)
        
        # FootballVerse branding
        brand_font = self._get_font(36, bold=True)
        brand_text = "FOOTBALLVERSE"
        bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_width = bbox[2] - bbox[0]
        brand_x = (self.width - brand_width) // 2
        brand_y = self.height - 120
        draw.text((brand_x, brand_y), brand_text, fill=self.colors['primary'], font=brand_font)
        
        output_path = self.output_dir / f"title_{story_id}.png"
        img.save(output_path)
        logger.info(f"Created cinematic title card for story {story_id}")
        return str(output_path)
    
    def create_chapter_card(self, chapter_title: str, chapter_number: int, story_id: int) -> str:
        """Create chapter transition card"""
        img = Image.new('RGB', (self.width, self.height), color=self.colors['dark'])
        draw = ImageDraw.Draw(img)
        
        # Chapter number (large)
        chapter_font = self._get_font(200, bold=True)
        chapter_text = f"CHAPTER {chapter_number}"
        bbox = draw.textbbox((0, 0), chapter_text, font=chapter_font)
        ch_width = bbox[2] - bbox[0]
        ch_x = (self.width - ch_width) // 2
        ch_y = self.height // 2 - 150
        
        # Shadow
        draw.text((ch_x + 3, ch_y + 3), chapter_text, fill='#000000', font=chapter_font)
        # Main
        draw.text((ch_x, ch_y), chapter_text, fill=self.colors['secondary'], font=chapter_font)
        
        # Chapter title
        title_font = self._get_font(64)
        bbox = draw.textbbox((0, 0), chapter_title, font=title_font)
        title_width = bbox[2] - bbox[0]
        title_x = (self.width - title_width) // 2
        title_y = ch_y + 220
        draw.text((title_x, title_y), chapter_title, fill=self.colors['text'], font=title_font)
        
        # Accent line
        line_width = 400
        line_x = (self.width - line_width) // 2
        line_y = title_y + 90
        draw.rectangle([(line_x, line_y), (line_x + line_width, line_y + 3)], 
                      fill=self.colors['primary'])
        
        output_path = self.output_dir / f"chapter_{story_id}_{chapter_number}.png"
        img.save(output_path)
        logger.info(f"Created chapter {chapter_number} card for story {story_id}")
        return str(output_path)
    
    def create_stat_overlay(self, stat_text: str, stat_value: str, story_id: int, scene_num: int) -> str:
        """Create statistics overlay scene"""
        img = Image.new('RGB', (self.width, self.height), color=self.colors['darker'])
        draw = ImageDraw.Draw(img)
        
        # Large stat value
        value_font = self._get_font(220, bold=True)
        bbox = draw.textbbox((0, 0), stat_value, font=value_font)
        val_width = bbox[2] - bbox[0]
        val_x = (self.width - val_width) // 2
        val_y = self.height // 2 - 180
        
        # Glow effect
        draw.text((val_x, val_y), stat_value, fill=self.colors['gold'], font=value_font)
        
        # Stat description
        text_font = self._get_font(56)
        bbox = draw.textbbox((0, 0), stat_text, font=text_font)
        text_width = bbox[2] - bbox[0]
        text_x = (self.width - text_width) // 2
        text_y = val_y + 240
        draw.text((text_x, text_y), stat_text, fill=self.colors['subtitle'], font=text_font)
        
        output_path = self.output_dir / f"stat_{story_id}_{scene_num}.png"
        img.save(output_path)
        logger.info(f"Created stat overlay for story {story_id}")
        return str(output_path)
    
    def create_text_scene(self, text: str, story_id: int, scene_num: int, style='default') -> str:
        """Create scene with text overlay - cinematic style"""
        # Dark gradient background
        img = Image.new('RGB', (self.width, self.height), color=self.colors['dark'])
        draw = ImageDraw.Draw(img)
        
        # Add subtle gradient
        for y in range(self.height):
            opacity = int(40 * (1 - y / self.height))
            color = (10 + opacity, 14 + opacity, 39 + opacity)
            draw.rectangle([(0, y), (self.width, y + 1)], fill=color)
        
        # Side accent bars
        draw.rectangle([(0, 0), (8, self.height)], fill=self.colors['primary'])
        draw.rectangle([(self.width - 8, 0), (self.width, self.height)], fill=self.colors['secondary'])
        
        font = self._get_font(58)
        
        # Wrap text to fit width
        margin = 200
        max_width = self.width - (2 * margin)
        wrapped_lines = textwrap.wrap(text, width=50)
        
        # Draw text lines with animation-ready positioning
        line_height = 85
        total_height = len(wrapped_lines) * line_height
        y_offset = (self.height - total_height) // 2
        
        for line in wrapped_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (self.width - line_width) // 2
            
            # Shadow for depth
            draw.text((x + 2, y_offset + 2), line, fill='#000000', font=font)
            # Main text
            draw.text((x, y_offset), line, fill=self.colors['text'], font=font)
            y_offset += line_height
        
        output_path = self.output_dir / f"scene_{story_id}_{scene_num}.png"
        img.save(output_path)
        logger.info(f"Created text scene {scene_num} for story {story_id}")
        return str(output_path)
    
    def create_parody_disclaimer(self, story_id: int) -> str:
        """Create parody disclaimer card with legal notice"""
        img = Image.new('RGB', (self.width, self.height), color='#000000')
        draw = ImageDraw.Draw(img)
        
        title_font = self._get_font(64, bold=True)
        text_font = self._get_font(42)
        
        disclaimer = [
            ("CONTENT NOTICE", self.colors['gold'], title_font, True),
            ("", None, None, False),
            ("This is an educational documentary-style narrative", self.colors['text'], text_font, False),
            ("combining factual information with creative storytelling.", self.colors['text'], text_font, False),
            ("", None, None, False),
            ("Player statistics sourced from TheSportsDB public API.", self.colors['subtitle'], text_font, False),
            ("Narration generated by AI for educational purposes.", self.colors['subtitle'], text_font, False),
            ("", None, None, False),
            ("For entertainment and educational use only.", self.colors['secondary'], text_font, False),
        ]
        
        y_offset = 280
        for line, color, font, is_title in disclaimer:
            if not line:
                y_offset += 30
                continue
            
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (self.width - line_width) // 2
            
            if is_title:
                # Underline for title
                draw.rectangle([(x, y_offset + 75), (x + line_width, y_offset + 80)], 
                             fill=self.colors['primary'])
            
            draw.text((x, y_offset), line, fill=color, font=font)
            y_offset += 65 if is_title else 55
        
        output_path = self.output_dir / f"disclaimer_{story_id}.png"
        img.save(output_path)
        logger.info(f"Created disclaimer for story {story_id}")
        return str(output_path)
    
    def create_end_card(self, story_id: int) -> str:
        """Create ending card with call to action"""
        img = Image.new('RGB', (self.width, self.height), color=self.colors['darker'])
        draw = ImageDraw.Draw(img)
        
        # Gradient overlay
        for y in range(self.height):
            opacity = int(50 * (y / self.height))
            color = (5 + opacity // 3, 8 + opacity // 3, 20 + opacity // 3)
            draw.rectangle([(0, y), (self.width, y + 1)], fill=color)
        
        # Main text
        title_font = self._get_font(96, bold=True)
        text = "FOOTBALLVERSE"
        bbox = draw.textbbox((0, 0), text, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        y = self.height // 2 - 100
        
        draw.text((x, y), text, fill=self.colors['primary'], font=title_font)
        
        # Subtitle
        subtitle_font = self._get_font(48)
        subtitle = "Where Football Stories Come Alive"
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sub_width = bbox[2] - bbox[0]
        sub_x = (self.width - sub_width) // 2
        sub_y = y + 120
        draw.text((sub_x, sub_y), subtitle, fill=self.colors['subtitle'], font=subtitle_font)
        
        # Call to action
        cta_font = self._get_font(38)
        cta = "More Episodes Coming Soon"
        bbox = draw.textbbox((0, 0), cta, font=cta_font)
        cta_width = bbox[2] - bbox[0]
        cta_x = (self.width - cta_width) // 2
        cta_y = sub_y + 100
        draw.text((cta_x, cta_y), cta, fill=self.colors['gold'], font=cta_font)
        
        output_path = self.output_dir / f"endcard_{story_id}.png"
        img.save(output_path)
        logger.info(f"Created end card for story {story_id}")
        return str(output_path)
