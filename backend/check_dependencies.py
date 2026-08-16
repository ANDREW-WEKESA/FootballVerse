#!/usr/bin/env python
"""Quick dependency checker for FootballVerse"""
import subprocess
import sys
import shutil

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    if shutil.which("ffmpeg"):
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"✅ ffmpeg: {version}")
                return True
        except Exception:
            pass
    print("❌ ffmpeg: NOT FOUND")
    print("   Install: https://ffmpeg.org/download.html")
    print("   Windows: choco install ffmpeg")
    print("   macOS: brew install ffmpeg")
    print("   Linux: apt install ffmpeg")
    return False

def check_pip_packages():
    """Check if required pip packages are installed"""
    required = [
        ("Pillow", "PIL"),
        ("gTTS", "gtts"),
        ("moviepy", "moviepy")
    ]
    all_installed = True
    
    for display_name, import_name in required:
        try:
            __import__(import_name)
            print(f"✅ {display_name}: INSTALLED")
        except ImportError:
            print(f"❌ {display_name}: NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\n   Install missing packages:")
        print("   pip install Pillow gTTS moviepy")
    
    return all_installed

def main():
    print("🔍 FootballVerse Dependency Check\n")
    
    # Check Python version
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python: {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python: {version.major}.{version.minor}.{version.micro} (3.8+ required)")
    
    print()
    
    # Check pip packages
    packages_ok = check_pip_packages()
    
    print()
    
    # Check ffmpeg
    ffmpeg_ok = check_ffmpeg()
    
    print("\n" + "="*50)
    if packages_ok and ffmpeg_ok:
        print("✨ All dependencies installed! Ready to render videos.")
    else:
        print("⚠️  Some dependencies missing. Install them to enable video rendering.")
    
    return 0 if (packages_ok and ffmpeg_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
