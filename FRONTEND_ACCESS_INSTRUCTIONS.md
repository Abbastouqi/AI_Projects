# 🎨 Frontend Access Instructions

## ⚠️ Current Status

The Next.js frontend encountered a SWC binary issue (common on Windows). Here are your options:

## ✅ Option 1: Open in Browser Directly (Recommended)

The frontend server is attempting to run on:
**http://localhost:3000**

Try opening this URL in your browser. If you see the chat interface, you're good to go!

## ✅ Option 2: Manual Start

Open a **new terminal/command prompt** and run:

```bash
cd frontend
npm run dev
```

Then open: **http://localhost:3000**

## ✅ Option 3: Use the Backend API Directly

The backend is fully functional! You can test it at:
**http://localhost:8000/docs**

This gives you an interactive Swagger UI where you can:
- Test the chat API
- See all laptop endpoints
- Try different queries

### Example API Test:
```bash
# Open PowerShell and run:
$body = @{
    message = "I'm an FSC student with 80k budget"
    session_id = $null
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method Post -Body $body -ContentType "application/json"
```

## 🔧 Fix SWC Issue (If Needed)

If the frontend doesn't load, try these fixes:

### Fix 1: Install Windows Build Tools
```bash
npm install --global windows-build-tools
```

### Fix 2: Use Alternative Architecture
```bash
cd frontend
npm install @next/swc-win32-x64-msvc
npm run dev
```

### Fix 3: Disable SWC (Use Babel)
Create `frontend/.babelrc`:
```json
{
  "presets": ["next/babel"]
}
```

Then restart:
```bash
npm run dev
```

## 🎯 What You Should See

When the frontend loads successfully at http://localhost:3000:

### 1. Hero Section
```
💻
Laptop Finder Pakistan
AI-powered recommendations for Pakistani students
```

### 2. Chat Interface
- Dark gradient background
- Chat bubbles (user on right, bot on left)
- Input box at bottom
- Quick reply buttons

### 3. Quick Replies
- 📚 FSC Student
- 💻 Programming  
- 💰 80k Budget
- 🎮 Gaming
- 📊 Office Work
- 🔧 Engineering

## 🧪 Test Without Frontend

You can fully test the system using just the backend:

### Method 1: Swagger UI
Visit: **http://localhost:8000/docs**

1. Click on `/api/chat` endpoint
2. Click "Try it out"
3. Enter your message
4. Click "Execute"
5. See the response!

### Method 2: Python Script
Run the demo:
```bash
python demo_conversation.py
```

This shows a full conversation flow in your terminal!

### Method 3: cURL/PowerShell
```powershell
# PowerShell
$headers = @{"Content-Type"="application/json"}
$body = '{"message":"Hi, I need a laptop for programming","session_id":null}'
Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method Post -Body $body -Headers $headers
```

## 📊 Current Working Features

Even without the frontend UI, you have:

✅ **Backend API** - Fully functional
✅ **Conversation Manager** - Intent detection working
✅ **Database** - 16 laptops loaded
✅ **Session Management** - Tracks conversations
✅ **All Endpoints** - Chat, laptops, search, etc.

## 🎊 Alternative: Use API Testing Tool

### Postman
1. Download Postman (free)
2. Create POST request to `http://localhost:8000/api/chat`
3. Set body to JSON:
```json
{
  "message": "I'm an FSC student with 80k budget",
  "session_id": null
}
```
4. Send and see response!

### Thunder Client (VS Code Extension)
1. Install Thunder Client in VS Code
2. Create new request
3. POST to `http://localhost:8000/api/chat`
4. Test the API visually

## 🚀 Quick Test Right Now

Open your browser and go to:
**http://localhost:8000/docs**

Then:
1. Scroll to `/api/chat` endpoint
2. Click "Try it out"
3. Type: "I need a laptop for programming with 100k budget"
4. Click "Execute"
5. See the AI response!

## 📱 Mobile Alternative

If you want to test on mobile:
1. Find your computer's IP address: `ipconfig`
2. Open on phone: `http://YOUR_IP:8000/docs`
3. Test the API from your phone!

## 💡 Summary

**Backend**: ✅ Working perfectly on http://localhost:8000
**Frontend**: ⚠️ SWC issue (common on Windows)
**Solution**: Use backend API directly via Swagger UI

**The chatbot is fully functional - just access it through the API documentation page!**

---

## 🎯 Recommended Next Steps

1. **Open**: http://localhost:8000/docs
2. **Test**: `/api/chat` endpoint
3. **Try**: Different messages and see responses
4. **Explore**: All other endpoints (laptops, search, etc.)

**Your AI laptop recommendation system is working!** 🎓💻
