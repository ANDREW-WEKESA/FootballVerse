# YouTube Goal Compilation Guide

## Create Real Goal Compilation Videos with AI Narration

This guide shows you how to download real Messi goal videos from YouTube and compile them with AI narration into professional highlight reels.

---

## 📋 Prerequisites

```bash
# Install yt-dlp (YouTube downloader)
pip install yt-dlp

# Verify ffmpeg is available
ffmpeg -version
```

---

## 🎬 Step-by-Step Workflow

### Step 1: Find Goal Videos on YouTube

Search YouTube for Messi goals. Recommended videos:
- "Messi vs Getafe 2007 HD"
- "Messi Copa del Rey final 2015 solo goal"
- "Messi vs Boateng Bayern Munich 2015"
- "Messi hat-trick Real Madrid"

### Step 2: Download Goal Clips

Use the download script to get clips:

```bash
# Download full goal video
python backend/compile_goals.py --download "https://youtube.com/watch?v=VIDEO_ID" messi_getafe_2007

# Download and trim to specific section (starts at 2:30, lasts 15 seconds)
python backend/compile_goals.py --download "https://youtube.com/watch?v=VIDEO_ID" messi_getafe_2007 --start 2:30 --duration 15
```

**Clips are saved to:** `backend/static/videos/clips/`

### Step 3: List Downloaded Clips

```bash
python backend/compile_goals.py --list
```

### Step 4: Create Compilation via API

Once you have 2-3 goal clips downloaded, create a compilation:

**Login first:**
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@footballverse.com","password":"admin123"}'
```

**Create compilation:**
```bash
curl -X POST "http://127.0.0.1:8000/videos/compile?story_id=100" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Messi Top 3 Solo Goals",
    "goals": [
      {
        "clip_path": "static/videos/clips/messi_getafe_2007.mp4",
        "title": "The Maradona Goal - vs Getafe 2007",
        "narration": "April 18, 2007. Camp Nou. A 19-year-old Messi picks up the ball near halfway and begins an impossible journey. Five defenders, all beaten. The finish, clinical. This is the goal that announced his arrival.",
        "trim_start": 0,
        "trim_end": 0,
        "add_slowmo": true
      },
      {
        "clip_path": "static/videos/clips/messi_bilbao_2015.mp4",
        "title": "Copa Final Solo Run - vs Athletic Bilbao 2015",
        "narration": "Copa del Rey final. Messi receives the ball in his own half. What follows is a 70-meter masterclass in speed, skill, and determination. The trophy-winning goal.",
        "add_slowmo": true
      },
      {
        "clip_path": "static/videos/clips/messi_boateng_2015.mp4",
        "title": "The Boateng Moment - vs Bayern Munich 2015",
        "narration": "Champions League semi-final. Jerome Boateng, one of the world's best defenders, stands in Messi's way. A subtle shift of weight, and Boateng collapses. The chip over Neuer is pure genius.",
        "add_slowmo": true
      }
    ]
  }'
```

---

## 🎥 What Gets Created

The compilation video includes:

1. **Opening Title Card** (4s)
   - Your custom title
   - "X Iconic Moments" subtitle
   - Cinematic branding

2. **Content Disclaimer** (3s)
   - Legal notice about educational use

3. **For Each Goal:**
   - **Chapter Card** (2s) - Goal title and number
   - **AI Narration Scene** (10-15s) - Dramatic storytelling
   - **Real Goal Footage** (10-20s) - Actual YouTube clip
   - **Slow-Motion Replay** (5-10s, optional) - Last 3 seconds in 50% speed

4. **End Card** (3s)
   - FootballVerse branding
   - "More compilations coming soon"

**Total Duration:** ~2-4 minutes depending on number of goals

---

## 📊 Example Compilation Structures

### Short Compilation (3 goals)
```
├── Title Card (4s)
├── Disclaimer (3s)
├── Goal 1: Getafe 2007
│   ├── Chapter card (2s)
│   ├── Narration (12s)
│   ├── Goal footage (15s)
│   └── Slow-mo replay (6s)
├── Goal 2: Bilbao 2015
│   ├── Chapter card (2s)
│   ├── Narration (14s)
│   ├── Goal footage (18s)
│   └── Slow-mo replay (7s)
├── Goal 3: Boateng 2015
│   ├── Chapter card (2s)
│   ├── Narration (13s)
│   ├── Goal footage (12s)
│   └── Slow-mo replay (5s)
└── End Card (3s)
Total: ~2min 30s
```

### Full Compilation (5-7 goals)
- Same structure, more goals
- Total duration: 4-6 minutes
- Perfect for YouTube full videos

---

## 🎨 Customization Options

### Trimming Clips
Remove unnecessary intro/outro from YouTube videos:

```bash
# Start at 30 seconds, take 15 seconds
python backend/compile_goals.py --download URL clip_name --start 0:30 --duration 15
```

### Adding Slow-Motion
```json
{
  "clip_path": "...",
  "add_slowmo": true  // Replays last 3 seconds in 50% speed
}
```

### Custom Narration
Write dramatic, emotional narration for each goal:

```json
{
  "narration": "Your custom dramatic narration here. Keep it engaging, emotional, and concise. Tell the story behind the goal, the context, the moment."
}
```

---

## ⚖️ Legal Considerations

### Fair Use Guidelines

When using YouTube footage:

1. **Keep clips short** (10-20 seconds per goal)
2. **Add transformative content:**
   - AI narration explaining the goal
   - Historical context
   - Technical analysis
3. **Credit sources** in video description
4. **Educational purpose** - teaching about football history
5. **Non-commercial** - for personal/educational use

### Attribution Example
```
Sources:
- Goal footage courtesy of [Original Channel Name]
- Player statistics from TheSportsDB
- Narration by FootballVerse AI
- Music: [if you add music, credit it here]

This video is created for educational purposes under fair use.
```

### Alternative to YouTube Downloads

If you prefer to avoid copyright issues entirely:

1. **Use Creative Commons** football footage
2. **Record FIFA/eFootball** gameplay
3. **Create animations** of the goals
4. **License official footage** from leagues
5. **Partner with content creators** who have rights

---

## 🚀 Quick Start Commands

```bash
# 1. Check what clips you have
python backend/compile_goals.py --list

# 2. Download a goal (example)
python backend/compile_goals.py --download \
  "https://youtube.com/watch?v=NweFRP7kYyU" \
  messi_getafe_2007 \
  --start 0:15 \
  --duration 20

# 3. Start backend server (if not running)
cd backend
.\.venv\Scripts\uvicorn app.main:app --reload

# 4. Login and get token
# Use Swagger UI: http://127.0.0.1:8000/docs
# Or frontend: http://localhost:5173

# 5. Create compilation via API
# Use the /videos/compile endpoint in Swagger UI
# Or send POST request as shown above
```

---

## 📁 File Locations

- **Downloaded clips:** `backend/static/videos/clips/*.mp4`
- **Final compilations:** `backend/static/videos/compilation_*.mp4`
- **Temp files:** `backend/temp/` (auto-cleaned)

---

## 🎯 Tips for Best Results

1. **Download in 1080p** - Higher quality clips look better
2. **Trim tightly** - Remove commentary/replays, keep just the goal action
3. **Write dramatic narration** - Make it emotional and engaging
4. **Use slow-motion sparingly** - Only for the best moments
5. **3-5 goals ideal** - Not too short, not too long
6. **Test clips first** - Play them to verify quality before compiling

---

## 🔧 Troubleshooting

**Problem:** yt-dlp says "Video unavailable"
- **Solution:** Video may be region-locked or private. Try a different video.

**Problem:** Download is very slow
- **Solution:** YouTube throttles downloads. Be patient or try at different times.

**Problem:** Clip won't play in compilation
- **Solution:** Re-encode with: `ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4`

**Problem:** Compilation endpoint returns 404
- **Solution:** Ensure clips exist in `backend/static/videos/clips/` directory

---

## 📞 Support

For issues or questions:
1. Check the download script output for errors
2. Verify clips are in correct directory
3. Test clips play normally in a video player
4. Check API logs: `backend/app/main.py` logs

---

**Happy compiling! Create amazing Messi highlight reels! ⚽🎬**
