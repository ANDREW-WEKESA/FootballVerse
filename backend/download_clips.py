#!/usr/bin/env python
"""
Helper script to download YouTube clips for educational/fair use purposes.

IMPORTANT: 
- Only download videos you have permission to use
- Ensure compliance with YouTube Terms of Service
- Use for educational/commentary purposes under fair use
- Always credit original sources
"""

import os
import subprocess
import sys

# Messi goal clips with YouTube search terms
CLIPS = {
    "messi_getafe_2007": {
        "search": "Messi vs Getafe 2007 goal",
        "description": "Messi's iconic solo goal similar to Maradona",
        "duration": "0:15-0:30"  # Download 15 second clip
    },
    "messi_madrid_2011": {
        "search": "Messi vs Real Madrid Champions League 2011",
        "description": "Messi goals at Bernabeu",
        "duration": "0:10-0:25"
    },
    "messi_freekick": {
        "search": "Messi best free kick goal",
        "description": "Messi free kick compilation",
        "duration": "0:05-0:20"
    },
    "messi_boateng_2015": {
        "search": "Messi vs Boateng Bayern Munich 2015",
        "description": "Messi sending Boateng to ground",
        "duration": "0:10-0:25"
    },
    "messi_bilbao_2015": {
        "search": "Messi Copa del Rey final 2015 solo goal",
        "description": "70-meter solo run",
        "duration": "0:10-0:30"
    },
    "messi_arsenal_2010": {
        "search": "Messi 4 goals vs Arsenal 2010",
        "description": "Messi destroys Arsenal",
        "duration": "0:15-0:35"
    },
    "messi_worldcup_2022": {
        "search": "Messi World Cup 2022 final goals",
        "description": "World Cup glory",
        "duration": "0:10-0:30"
    }
}


def download_clip(clip_name, search_term, output_dir="backend/static/videos/clips"):
    """
    Download a YouTube clip using yt-dlp
    
    NOTE: You must manually find the video URL first, then pass it to this function.
    This script does NOT automatically search and download.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{clip_name}.mp4")
    
    print(f"\n{'='*60}")
    print(f"Clip: {clip_name}")
    print(f"Search: {search_term}")
    print(f"{'='*60}")
    print("\nMANUAL STEPS:")
    print(f"1. Search YouTube for: {search_term}")
    print("2. Copy the video URL")
    print(f"3. Run: yt-dlp -f 'bestvideo[height<=720]+bestaudio/best[height<=720]' -o '{output_path}' <URL>")
    print("\nOR use this script with URL:")
    print(f"   python download_clips.py --url <YOUTUBE_URL> --clip {clip_name}")
    print()


def download_from_url(url, clip_name, output_dir="backend/static/videos/clips"):
    """Download specific clip from provided URL"""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{clip_name}.mp4")
    
    # yt-dlp command for 720p max, 15-20 second clips
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "--merge-output-format", "mp4",
        "-o", output_path,
        url
    ]
    
    print(f"Downloading {clip_name}...")
    try:
        subprocess.run(cmd, check=True)
        print(f"✓ Downloaded: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to download: {e}")
        return None
    except FileNotFoundError:
        print("✗ yt-dlp not found. Install: pip install yt-dlp")
        return None


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--url":
        # Download mode
        if len(sys.argv) < 5:
            print("Usage: python download_clips.py --url <YOUTUBE_URL> --clip <CLIP_NAME>")
            sys.exit(1)
        
        url = sys.argv[2]
        clip_name = sys.argv[4]
        download_from_url(url, clip_name)
    else:
        # Info mode - show what needs to be downloaded
        print("\n" + "="*60)
        print("MESSI CLIPS TO DOWNLOAD")
        print("="*60)
        print("\nThis script helps you download YouTube clips for your videos.")
        print("You must manually find videos and provide URLs due to copyright.")
        print("\nAvailable clips:\n")
        
        for clip_name, info in CLIPS.items():
            print(f"• {clip_name}")
            print(f"  Search: {info['search']}")
            print(f"  Description: {info['description']}")
            print(f"  Duration needed: {info['duration']}")
            print()
        
        print("\nTo download a clip:")
        print("1. Search YouTube and copy the video URL")
        print("2. Run: python download_clips.py --url <URL> --clip <clip_name>")
        print("\nExample:")
        print("  python download_clips.py --url https://youtube.com/watch?v=... --clip messi_getafe_2007")
        print("\n" + "="*60)
        print("LEGAL NOTICE:")
        print("• Only download videos you have rights to use")
        print("• Consider fair use doctrine for educational/commentary")
        print("• Always credit original sources")
        print("• Respect YouTube Terms of Service")
        print("="*60 + "\n")


if __name__ == "__main__":
    main()
