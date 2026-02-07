# 🎨 How to View the Frontend

## ✅ Frontend is Starting!

The Next.js development server is currently starting up. Here's how to access it:

## 📍 Access the Frontend

### Option 1: Wait for Server to Start (Recommended)
The server is starting now. In a few moments, you'll see a message like:
```
✓ Ready in 3.2s
○ Local:   http://localhost:3000
```

Then simply open your browser and go to:
**http://localhost:3000**

### Option 2: Check Server Status
Run this command to see if the server is ready:
```bash
curl http://localhost:3000
```

If you get a response, the server is ready!

### Option 3: Manual Start (If Needed)
If the server isn't running, start it manually:
```bash
cd frontend
npm run dev
```

## 🎯 What You'll See

When you open http://localhost:3000, you'll see:

### 1. **Hero Section**
- Animated laptop emoji 💻
- Dark gradient background (slate-900 to purple-900)
- Title: "Laptop Finder Pakistan"
- Subtitle: "AI-powered recommendations for Pakistani students"

### 2. **Chat Interface**
- Modern glassmorphism design
- Bot avatar (🤖) and user avatar (👤)
- Message bubbles with timestamps
- Typing indicator with animated dots

### 3. **Quick Reply Buttons**
Six preset options:
- 📚 FSC Student
- 💻 Programming
- 💰 80k Budget
- 🎮 Gaming
- 📊 Office Work
- 🔧 Engineering

### 4. **Laptop Cards**
When the bot recommends laptops, you'll see:
- Laptop name and brand
- Price in PKR (green badge)
- Specs with icons (⚡ CPU, 💾 RAM, 💿 Storage, 🖥️ Display)
- "View Details" button
- "Compare" button

### 5. **Comparison View**
Select 2-3 laptops to compare:
- Side-by-side spec comparison
- Winner badge for best value
- Full-screen modal overlay

## 🧪 Try These Interactions

### Test 1: Basic Conversation
1. Click "FSC Student" quick reply
2. Type "My budget is 80k"
3. See laptop recommendations

### Test 2: Programming Student
1. Type "I need a laptop for programming"
2. Type "Budget around 120k"
3. Get programming-focused recommendations

### Test 3: Comparison
1. Wait for laptop recommendations
2. Click "Compare" on 2-3 laptops
3. View side-by-side comparison

### Test 4: Purchase Help
1. Type "Where can I buy laptops in Pakistan?"
2. Get info about Czone, Paklap, Daraz

## 🎨 Design Features

### Dark Theme
- Background: Gradient from slate-900 via purple-900
- Animated pulsing orbs in background
- Glassmorphism effects on cards

### Responsive Design
- Mobile: Single column, full width
- Tablet: Optimized spacing
- Desktop: Max width 6xl (1280px)

### Animations
- Smooth message transitions
- Hover effects on buttons
- Scale transforms on cards
- Typing indicator animation

## 🔧 Troubleshooting

### Frontend Not Loading?

**Check if server is running:**
```bash
# In a new terminal
cd frontend
npm run dev
```

**Check for errors:**
Look at the terminal where you ran `npm run dev` for any error messages.

**Port already in use?**
If port 3000 is busy, Next.js will use 3001:
- Try http://localhost:3001

**Clear cache and restart:**
```bash
cd frontend
rm -rf .next
npm run dev
```

### Backend Not Responding?

Make sure the backend is running:
```bash
# Check backend status
curl http://localhost:8000/api/health
```

If not running:
```bash
cd backend
python main.py
```

## 📱 Mobile View

The interface is fully responsive. To test mobile view:
1. Open http://localhost:3000
2. Press F12 (Developer Tools)
3. Click the device toggle icon
4. Select a mobile device

## 🎊 Features to Explore

### 1. Session Persistence
- Your conversation is saved in localStorage
- Refresh the page - your chat history remains!

### 2. Quick Replies
- Click any quick reply button
- Message is sent automatically

### 3. Laptop Selection
- Click "Compare" on multiple laptops
- Select up to 3 laptops
- Click "Compare" button at bottom

### 4. Comparison View
- See specs side-by-side
- Winner badge shows best value
- Click X to close

### 5. Real-time Chat
- Type and press Enter
- Or click Send button
- See typing indicator while bot responds

## 🌟 Pro Tips

1. **Use Quick Replies** for faster interaction
2. **Compare laptops** to see differences clearly
3. **Check session persistence** by refreshing
4. **Try different budgets** to see varied recommendations
5. **Ask about brands** to get comparison info

## 📊 What's Connected

The frontend connects to:
- **Backend API**: http://localhost:8000/api/chat
- **Database**: 16 Pakistani laptops
- **Conversation Manager**: Intelligent intent detection
- **Session Storage**: localStorage for persistence

## 🎯 Next Steps

Once the frontend loads:
1. ✅ Try the quick reply buttons
2. ✅ Have a conversation about your needs
3. ✅ Compare recommended laptops
4. ✅ Ask about where to buy
5. ✅ Test session persistence (refresh page)

---

## 🚀 Quick Access

**Frontend**: http://localhost:3000
**Backend API**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

**Enjoy your AI-powered laptop recommendation chatbot!** 🎓💻🇵🇰
