# Create Your Messi Compilation Video NOW

## Quick Start (5 Minutes)

### Step 1: Open Swagger UI in Browser
```
http://127.0.0.1:8000/docs
```

### Step 2: Login to Get Token

1. Find **POST /auth/login** endpoint
2. Click "Try it out"
3. Use this:
```json
{
  "email": "admin@footballverse.com",
  "password": "admin123"
}
```
4. Click "Execute"
5. **Copy the access_token** from the response

### Step 3: Create Compilation

1. Find **POST /videos/compile** endpoint
2. Click "Try it out"
3. Click the 🔒 Authorize button at top
4. Paste your token: `Bearer YOUR_TOKEN_HERE`
5. Click "Authorize", then "Close"

6. In the "story_id" field, enter: `100`

7. In the Request body, paste this:
```json
{
  "title": "Messi's Greatest Moments",
  "goals": [
    {
      "clip_path": "static/videos/clips/messi_demo_goal1.mp4",
      "title": "The Impossible Dribble",
      "narration": "Five defenders beaten with pure magic. This is the moment that announced a legend to the world.",
      "add_slowmo": false
    },
    {
      "clip_path": "static/videos/clips/messi_demo_goal2.mp4",
      "title": "The Trophy Winner",
      "narration": "Seventy meters of determination. From his own half to glory. The Copa del Rey is won.",
      "add_slowmo": false
    },
    {
      "clip_path": "static/videos/clips/messi_demo_goal3.mp4",
      "title": "Champions League Magic",
      "narration": "Boateng collapses. Neuer is helpless. This is why he's called the greatest of all time.",
      "add_slowmo": false
    }
  ]
}
```

8. Click **Execute**
9. Wait 2-3 minutes (making the video...)
10. You'll get a response with `output_path`

### Step 4: Watch Your Video

The video is saved at:
```
C:\dev\FootballVerse\backend\static\videos\compilation_100_XXXXX.mp4
```

**OR** watch in browser:
```
http://127.0.0.1:8000/videos/compilation_100_XXXXX.mp4
```
(Replace XXXXX with the timestamp from the response)

---

## What You'll Get

A professional compilation video with:
- ✅ Cinematic title card: "Messi's Greatest Moments"
- ✅ Legal disclaimer
- ✅ Chapter 1: Title card + AI narration + Goal video
- ✅ Chapter 2: Title card + AI narration + Goal video  
- ✅ Chapter 3: Title card + AI narration + Goal video
- ✅ End card with branding

**Total Duration:** ~2-3 minutes
**Quality:** 1080p Full HD

---

## Next: Use REAL YouTube Videos

Once this works, download real Messi goals:

### Download Real Clips:
```bash
python backend/compile_goals.py --download "YOUTUBE_URL" messi_real_goal1 --start 0:30 --duration 15
```

Then change the `clip_path` in the JSON to your downloaded clips!

---

## Troubleshooting

**Problem:** Swagger UI not loading
- **Fix:** Make sure backend is running: `cd backend && .\.venv\Scripts\uvicorn app.main:app --reload`

**Problem:** "Unauthorized" error
- **Fix:** Click 🔒 Authorize button and add `Bearer YOUR_TOKEN`

**Problem:** "Clip not found"
- **Fix:** Check clips exist: `dir backend\static\videos\clips`

**Problem:** Video taking too long
- **Fix:** Be patient, it takes 2-3 minutes to render

---

## That's It!

You now have a professional football compilation system! 🎬⚽
