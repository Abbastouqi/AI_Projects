# 👤 User Guide - Riphah Auto-Apply

## 🚀 Quick Start

### Step 1: Open the Chatbot
Open your browser and go to:
```
http://localhost:5000
```

### Step 2: Click Auto Apply
Click the green button: **🎓 Auto Apply**

### Step 3: Watch the Magic
- Chrome browser opens automatically
- Navigates to Riphah portal
- Fills form fields
- Shows you results

---

## 🎯 What's Fixed

### ✅ No More Speaking
- Agent no longer speaks responses
- Only text output in chat
- Speaker button is muted by default (🔇)
- You can enable it by clicking the speaker button if needed

### ✅ Browser Opens Properly
- Chrome opens in visible mode
- You can see what's happening
- Browser starts maximized
- Better error handling

---

## 🎮 How to Use

### Method 1: Click Buttons (Easiest)
```
1. Click "🎓 Auto Apply" → Opens portal & fills form
2. Click "📝 Auto Fill" → Fills current form
3. Click "➕ New App" → Clicks New Application
4. Click "✅ Submit" → Submits form
```

### Method 2: Type Commands
```
"riphah auto apply"
"auto fill"
"click new application"
"fill name with John Doe"
"click submit"
```

### Method 3: Voice Commands
```
1. Click microphone button (🎤)
2. Say: "riphah auto apply"
3. Agent processes your command
```

---

## 📋 Complete Workflow

### Scenario 1: Full Automation
```
1. Click "🎓 Auto Apply"
   → Browser opens
   → Goes to Riphah portal
   → Attempts login
   → Fills form

2. Review filled data in browser

3. Click "✅ Submit"
   → Form submitted
```

### Scenario 2: Manual Login
```
1. Click "🎓 Auto Apply"
   → Browser opens
   → Shows login page

2. Type: "fill email with your@email.com"
3. Type: "fill password with YourPassword"
4. Type: "click login"

5. Click "➕ New App"
   → Opens application form

6. Click "📝 Auto Fill"
   → Fills all fields

7. Click "✅ Submit"
   → Form submitted
```

### Scenario 3: Manual Corrections
```
1. Click "🎓 Auto Apply"
   → Auto-fills form

2. Type: "fill program with Computer Science"
3. Type: "fill semester with Fall 2024"
4. Type: "fill cgpa with 3.5"

5. Click "✅ Submit"
```

---

## 🎨 Interface Guide

### Top Bar
```
┌─────────────────────────────────────┐
│   🎓 Riphah AI Assistant            │
│   Your intelligent admission guide   │
└─────────────────────────────────────┘
```

### Status Bar
```
┌─────────────────────────────────────┐
│ ● Online  ● Voice  ○ Speaker        │
└─────────────────────────────────────┘
```
- Green dot = Active
- Gray dot = Inactive

### Quick Actions
```
┌─────────────────────────────────────┐
│ [🎓 Auto Apply] [📝 Auto Fill]      │
│ [➕ New App] [✅ Submit]             │
└─────────────────────────────────────┘
```

### Input Area
```
┌─────────────────────────────────────┐
│ [🎤] [Type message...] [🔇] [➤]     │
└─────────────────────────────────────┘
```
- 🎤 = Voice input
- 🔇 = Speaker (muted)
- ➤ = Send message

---

## 💡 Tips & Tricks

### Tip 1: Enable Speaker (Optional)
If you want voice output:
1. Click the speaker button (🔇)
2. It changes to 🔊
3. Agent will speak responses

### Tip 2: Use Voice Input
1. Click microphone (🎤)
2. Button turns red (recording)
3. Speak your command
4. Agent processes it

### Tip 3: Clear Chat
Click the trash icon (🗑️) to clear conversation

### Tip 4: Watch the Browser
Keep the Chrome window visible to see what's happening

### Tip 5: Manual Override
You can always manually fill fields:
```
"fill [field] with [value]"
```

---

## 🔍 What to Expect

### When You Click "🎓 Auto Apply":

**Step 1: Browser Opens** (2-3 seconds)
- Chrome window appears
- Maximized view

**Step 2: Navigation** (3-4 seconds)
- Goes to Riphah portal
- Page loads

**Step 3: Login Attempt** (2-3 seconds)
- Fills email
- Fills password
- Clicks login

**Step 4: Form Filling** (3-5 seconds)
- Detects form fields
- Fills all fields
- Shows progress

**Step 5: Results** (instant)
- Chat shows what was filled
- You can review in browser

**Total Time**: ~10-15 seconds

---

## 📊 Understanding Results

### Success Message:
```
🤖 RIPHAH AUTO-APPLY IN PROGRESS!

📊 Auto-Fill Results:
   • Forms detected: 1
   • Fields found: 12
   • Fields filled: 10

📝 Filled Fields:
   ✓ name: Muhammad Ahmed Khan
   ✓ email: student@example.com
   ✓ phone: 03001234567
   ... more fields

✅ Application form auto-filled!
```

**What it means**:
- Found 1 form on page
- Detected 12 input fields
- Successfully filled 10 fields
- 2 fields might need manual filling

### Partial Success:
```
⚠️ Login attempted but may have failed.

Please check:
• Credentials are correct
• Account exists
• No CAPTCHA required
```

**What to do**:
- Use manual login commands
- Check your credentials
- Solve CAPTCHA if present

---

## 🐛 Troubleshooting

### Issue: Browser doesn't open
**Try**:
1. Check if Chrome is installed
2. Restart the server
3. Check terminal for errors

### Issue: Login fails
**Try**:
1. Use manual login:
   - "fill email with your@email.com"
   - "fill password with YourPassword"
   - "click login"
2. Check credentials
3. Solve CAPTCHA manually

### Issue: Form not filled
**Try**:
1. Click "➕ New App" first
2. Wait for page to load
3. Click "📝 Auto Fill" again
4. Use manual filling

### Issue: Can't submit
**Try**:
1. "press enter"
2. Manually click submit in browser
3. Check required fields

---

## 🎯 Common Commands

| Command | What It Does |
|---------|--------------|
| "riphah auto apply" | Full automation |
| "auto fill" | Fill current form |
| "click new application" | Click New App button |
| "fill name with John" | Fill name field |
| "fill email with john@email.com" | Fill email |
| "click submit" | Submit form |
| "press enter" | Press Enter key |
| "help" | Show help |

---

## 📞 Need Help?

### Check Server Status:
Look at the terminal running `web_server.py`

### Check Browser Console:
Press F12 in Chrome to see errors

### Restart Server:
```bash
# Stop: Ctrl+C
# Start: python AI_agent/web_server.py
```

### Test Manually:
Try commands one by one to isolate issues

---

## ✅ Checklist

Before using:
- [ ] Server running (http://localhost:5000)
- [ ] Chrome installed
- [ ] Internet connection active
- [ ] Riphah credentials ready

During use:
- [ ] Browser opens
- [ ] Portal loads
- [ ] Form appears
- [ ] Fields filled
- [ ] Data reviewed

After use:
- [ ] Form submitted
- [ ] Confirmation received
- [ ] Browser closed

---

## 🎉 You're Ready!

**Everything is set up and working!**

1. ✅ No speaking (text only)
2. ✅ Browser opens properly
3. ✅ Auto-fill working
4. ✅ Quick actions ready

**Open http://localhost:5000 and start applying!** 🚀
