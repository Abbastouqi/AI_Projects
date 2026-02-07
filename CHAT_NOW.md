# 🚀 HOW TO RUN AND CHAT - SUPER SIMPLE!

## ✅ STEP 1: Start the Backend (30 seconds)

### Option A: Double-click this file
```
START_CHATBOT.bat
```

### Option B: Run these commands
Open Command Prompt and run:
```bash
cd D:\Fetch_laptop\backend
pip install fastapi uvicorn python-dotenv sqlalchemy pydantic pydantic-settings
python main.py
```

**Wait until you see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## ✅ STEP 2: Open the Chat Interface

### Option A: HTML File (Easiest!)
**Double-click this file:**
```
simple-chat.html
```

### Option B: API Documentation
**Open in browser:**
```
http://localhost:8000/docs
```

---

## 💬 HOW TO CHAT

### Using simple-chat.html:

1. **Open** `simple-chat.html` in your browser
2. **You'll see:**
   - 💻 Laptop Finder Pakistan
   - Chat interface with bot greeting
   - Quick reply buttons at bottom
   - Message input box

3. **Start chatting:**
   - **Click** any quick reply button (📚 FSC Student, 💻 Programming, etc.)
   - **OR type** your message in the input box
   - **Press Enter** or click 📤 button

4. **Example conversations:**
   ```
   You: "I'm an FSC student"
   Bot: [Explains FSC student needs]
   
   You: "My budget is 80k"
   Bot: [Shows budget recommendations]
   
   You: "I need it for programming"
   Bot: [Recommends programming laptops]
   ```

### Using API Docs (http://localhost:8000/docs):

1. **Open** http://localhost:8000/docs in browser
2. **Scroll** to "POST /api/chat"
3. **Click** "Try it out"
4. **Type** your message in the JSON:
   ```json
   {
     "message": "I'm an FSC student with 80k budget",
     "session_id": null
   }
   ```
5. **Click** "Execute"
6. **See** the AI response below!

---

## 🎯 QUICK TEST

### Test 1: Quick Reply
1. Open `simple-chat.html`
2. Click "📚 FSC Student" button
3. See bot response!

### Test 2: Type Message
1. Type: "I need a laptop for programming"
2. Press Enter
3. See recommendations!

### Test 3: Budget Query
1. Type: "My budget is 100k PKR"
2. See budget analysis!

---

## 🎨 What You'll See

### In simple-chat.html:
```
┌─────────────────────────────────────┐
│         💻                          │
│   Laptop Finder Pakistan            │
│   AI-powered recommendations        │
├─────────────────────────────────────┤
│                                     │
│  🤖 Bot: السلام علیکم! Welcome...  │
│                                     │
│  👤 You: I'm an FSC student         │
│                                     │
│  🤖 Bot: Great! What's your budget? │
│                                     │
├─────────────────────────────────────┤
│  Quick Replies:                     │
│  [📚 FSC] [💻 Programming] [💰 80k] │
├─────────────────────────────────────┤
│  Type your message... [📤]          │
└─────────────────────────────────────┘
```

---

## 🧪 Try These Messages

**Greeting:**
- "Hi"
- "Hello"
- "Salam"

**Student Type:**
- "I'm an FSC student"
- "I'm a university student"
- "I'm studying engineering"

**Budget:**
- "My budget is 80k"
- "I have 100,000 PKR"
- "Budget around 120k"

**Use Case:**
- "I need it for programming"
- "I want to play games"
- "For office work"

**Comparison:**
- "Compare HP vs Dell"
- "Which is better, Lenovo or ASUS?"

**Purchase:**
- "Where can I buy laptops?"
- "Tell me about Czone"

---

## ✅ Checklist

- [ ] Backend running (see "Application startup complete")
- [ ] Open `simple-chat.html` in browser
- [ ] See chat interface with bot greeting
- [ ] Click a quick reply button OR type a message
- [ ] See bot response!

---

## 🎊 YOU'RE READY!

**Just follow these 2 steps:**

1. **Run:** `START_CHATBOT.bat` (or the commands above)
2. **Open:** `simple-chat.html`

**Then start chatting!** 🚀

---

## 📱 Features You Can Use

✅ **Quick Replies** - Click buttons for instant responses
✅ **Type Messages** - Ask anything about laptops
✅ **Get Recommendations** - See laptop suggestions with specs
✅ **Budget Analysis** - Get advice for your price range
✅ **Brand Comparison** - Compare HP, Dell, Lenovo, etc.
✅ **Purchase Guidance** - Learn where to buy in Pakistan
✅ **Session Memory** - Bot remembers your conversation

---

## 🎯 Summary

**To run:** Double-click `START_CHATBOT.bat`
**To chat:** Open `simple-chat.html`
**To test:** Click quick reply buttons or type messages

**Your AI laptop recommendation chatbot is ready!** 🎓💻🇵🇰
