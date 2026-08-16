#!/usr/bin/env python
"""
Goal Compilation Video Creator
Downloads YouTube clips and compiles them with narration

USAGE:
1. Find YouTube videos of Messi goals
2. Download them using this script
3. Run compilation to create final video with narration
"""

import os
import sys
import subprocess
from pathlib import Path


def download_goal_clip(youtube_url: str, goal_name: str, start_time: str = None, duration: int = 15):
    """
    Download a specific goal clip from YouTube
    
    Args:
        youtube_url: Full YouTube video URL
        goal_name: Name for the clip (e.g., "messi_getafe_2007")
        start_time: Start time in format "MM:SS" (e.g., "2:30")
        duration: Length of clip in seconds (default 15)
    
    Example:
        download_goal_clip("https://youtube.com/watch?v=...", "messi_getafe_2007", "2:30", 15)
    """
    clips_dir = Path("backend/static/videos/clips")
    clips_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = clips_dir / f"{goal_name}.mp4"
    
    print(f"\n{'='*60}")
    print(f"Downloading: {goal_name}")
    print(f"URL: {youtube_url}")
    print(f"{'='*60}\n")
    
    # Build yt-dlp command
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]",
        "--merge-output-format", "mp4",
    ]
    
    # Add time trimming if specified
    if start_time and duration:
        # Download full video first, then trim with ffmpeg
        temp_file = clips_dir / f"temp_{goal_name}.mp4"
        cmd.extend(["-o", str(temp_file), youtube_url])
        
        print("Downloading full video...")
        try:
            subprocess.run(cmd, check=True)
            
            # Trim with ffmpeg
            print(f"Trimming from {start_time} for {duration} seconds...")
            trim_cmd = [
                "ffmpeg", "-i", str(temp_file),
                "-ss", start_time,
                "-t", str(duration),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-y",
                str(output_path)
            ]
            subprocess.run(trim_cmd, check=True)
            
            # Remove temp file
            temp_file.unlink()
            print(f"✓ Saved to: {output_path}\n")
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Download/trim failed: {e}")
            return None
    else:
        # Download full clip
        cmd.extend(["-o", str(output_path), youtube_url])
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ Saved to: {output_path}\n")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            print(f"✗ Download failed: {e}")
            return None


def list_available_clips():
    """List all downloaded clips"""
    clips_dir = Path("backend/static/videos/clips")
    if not clips_dir.exists():
        print("No clips directory found. Download some clips first!")
        return []
    
    clips = list(clips_dir.glob("*.mp4"))
    if not clips:
        print("No clips downloaded yet.")
        return []
    
    print("\n" + "="*60)
    print("AVAILABLE CLIPS:")
    print("="*60)
    for clip in clips:
        size_mb = clip.stat().st_size / (1024 * 1024)
        print(f"• {clip.name} ({size_mb:.2f} MB)")
    print("="*60 + "\n")
    
    return [str(c) for c in clips]


# Pre-defined Messi goal videos to download
MESSI_GOALS = {
    "getafe_2007": {
        "name": "Messi vs Getafe 2007 - Maradona Goal",
        "search_terms": "Messi Getafe 2007 solo goal HD",
        "description": "The famous solo run beating 5 defenders"
    },
    "real_madrid_2011": {
        "name": "Messi vs Real Madrid 2011 - Champions League",
        "search_terms": "Messi Real Madrid 2011 Champions League semi final goals",
        "description": "Two goals at Bernabeu in CL semi-final"
    },
    "boateng_2015": {
        "name": "Messi vs Boateng 2015",
        "search_terms": "Messi Boateng chip Neuer Bayern Munich 2015",
        "description": "Sending Boateng to the ground + chip over Neuer"
    },
    "bilbao_2015": {
        "name": "Messi Copa del Rey Final 2015",
        "search_terms": "Messi Athletic Bilbao Copa del Rey final 2015 solo goal",
        "description": "70-meter solo run in the final"
    },
    "arsenal_2010": {
        "name": "Messi vs Arsenal 2010",
        "search_terms": "Messi 4 goals Arsenal 2010 Champions League",
        "description": "Four goals in Champions League quarter-final"
    }
}


def print_download_instructions():
    """Print instructions for downloading clips"""
    print("\n" + "="*70)
    print("HOW TO DOWNLOAD MESSI GOAL CLIPS")
    print("="*70)
    print("\n📺 MANUAL METHOD (Recommended):")
    print("1. Go to YouTube and search for the goal")
    print("2. Copy the video URL")
    print("3. Run this command:")
    print("   python backend/compile_goals.py --download <URL> <clip_name>\n")
    print("Example:")
    print('   python backend/compile_goals.py --download "https://youtube.com/watch?v=..." messi_getafe_2007\n')
    
    print("\n⏱️ TO TRIM A SPECIFIC SECTION:")
    print("   python backend/compile_goals.py --download <URL> <clip_name> --start 2:30 --duration 15")
    print("   (This downloads starting at 2:30 for 15 seconds)\n")
    
    print("\n📋 SUGGESTED CLIPS TO DOWNLOAD:\n")
    for key, info in MESSI_GOALS.items():
        print(f"• {info['name']}")
        print(f"  Search: {info['search_terms']}")
        print(f"  Clip name: {key}")
        print()
    
    print("="*70)
    print("\n⚠️  LEGAL NOTICE:")
    print("• Only download videos you have permission to use")
    print("• Consider fair use for educational/commentary purposes")
    print("• Always credit original sources in your final video")
    print("• This tool is for personal/educational use only")
    print("="*70 + "\n")


def main():
    if len(sys.argv) < 2:
        print_download_instructions()
        list_available_clips()
        return
    
    if sys.argv[1] == "--download":
        if len(sys.argv) < 4:
            print("Usage: python compile_goals.py --download <URL> <clip_name> [--start MM:SS] [--duration SECONDS]")
            return
        
        url = sys.argv[2]
        clip_name = sys.argv[3]
        
        # Check for optional time parameters
        start_time = None
        duration = 15
        
        if "--start" in sys.argv:
            start_idx = sys.argv.index("--start")
            start_time = sys.argv[start_idx + 1]
        
        if "--duration" in sys.argv:
            dur_idx = sys.argv.index("--duration")
            duration = int(sys.argv[dur_idx + 1])
        
        download_goal_clip(url, clip_name, start_time, duration)
    
    elif sys.argv[1] == "--list":
        list_available_clips()
    
    else:
        print_download_instructions()


if __name__ == "__main__":
    main()
