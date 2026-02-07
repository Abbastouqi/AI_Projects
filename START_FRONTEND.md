# 🚀 START FRONTEND - EXACT COMMANDS

## 📝 Step-by-Step Commands

### Step 1: Open a New Terminal/Command Prompt

**Windows:**
- Press `Windows Key + R`
- Type: `cmd` or `powershell`
- Press Enter

**Or:**
- Right-click in your project folder
- Select "Open in Terminal" or "Open PowerShell window here"

---

### Step 2: Navigate to Frontend Folder

```bash
cd D:\Fetch_laptop\frontend
```

**Or if you're already in the project root:**
```bash
cd frontend
```

---

### Step 3: Start the Development Server

```bash
npm run dev
```

---

### Step 4: Wait for Server to Start

You'll see output like:
```
> laptop-chatbot-frontend@0.1.0 dev
> next dev

  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000

✓ Ready in 3.2s
```

---

### Step 5: Open in Browser

Open your browser and go to:
```
http://localhost:3000
```

---

## 🎯 Complete Command Sequence

**Copy and paste these commands one by one:**

```bash
# 1. Go to frontend folder
cd D:\Fetch_laptop\frontend

# 2. Start the server
npm run dev
```

**That's it!** The server will start and show you the URL.

---

## ⚠️ If You See Errors

### Error: "Cannot find module"
**Solution:**
```bash
cd D:\Fetch_laptop\frontend
npm install
npm run dev
```

### Error: "Port 3000 already in use"
**Solution:** Next.js will automatically use port 3001
- Open: http://localhost:3001

### Error: "SWC binary failed"
**Solution:** This is a Windows issue, but the app should still work
- Just open http://localhost:3000 anyway
- Or use the backend API at http://localhost:8000/docs

---

## 🎨 Alternative: Use VS Code Terminal

If you're using VS Code:

1. Press `` Ctrl + ` `` (backtick) to open terminal
2. Type: `cd frontend`
3. Type: `npm run dev`
4. Click the link that appears: http://localhost:3000

---

## 📊 What You'll See

When it works, you'll see in terminal:
```
✓ Ready in 3.2s
○ Local:   http://localhost:3000
```

Then in your browser at http://localhost:3000:
- 💻 Animated laptop hero section
- 🎨 Dark gradient background
- 💬 Chat interface
- 📱 Quick reply buttons
- 🤖 Bot avatar

---

## 🔥 FASTEST WAY (Copy-Paste)

**Open PowerShell/CMD and paste this:**

```powershell
cd D:\Fetch_laptop\frontend ; npm run dev
```

**Then open browser:** http://localhost:3000

---

## ✅ Verify It's Working

**In terminal, you should see:**
```
✓ Ready in 3.2s
○ Local:   http://localhost:3000
```

**In browser at http://localhost:3000, you should see:**
- Title: "Laptop Finder Pakistan"
- Subtitle: "AI-powered recommendations for Pakistani students"
- Chat interface with input box
- Quick reply buttons

---

## 🎊 You're Done!

Once you see the chat interface, you can:
1. Click quick reply buttons (FSC Student, Programming, etc.)
2. Type messages in the input box
3. See AI responses
4. Get laptop recommendations
5. Compare laptops side-by-side

**Enjoy your AI chatbot!** 🚀
