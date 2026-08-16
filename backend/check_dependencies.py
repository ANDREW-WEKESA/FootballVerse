#!/usr/bin/env python
"""Quick dependency checker for FootballVerse"""
import subprocess
import sys

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🔍 FootballVerse Dependency Check\n")
    
    # Check ffmpeg
    if check_ffmpeg():
        print("✅ ffmpeg: INSTALLED")
    else:
        print("❌ ffmpeg: NOT FOUND")
        print("   Install: https://ffmpeg.org/download.html")
    
    # Check Python version
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python: {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"⚠️  Python: {version.major}.{version.minor}.{version.micro} (3.11+ recommended)")
    
    print("\n✨ Check complete!")

if __name__ == "__main__":
    main()
