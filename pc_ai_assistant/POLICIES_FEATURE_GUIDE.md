# University Policies Feature Guide

## 🎓 Overview

The PC AI Assistant now includes a comprehensive University Policies feature that scrapes and displays policies from the Riphah Sahiwal website in real-time.

---

## ✨ Features

### 1. **Policy Categories**
- HEC's Sexual Harassment Policy
- University Standing Committee on Harassment
- Disability Policy HEC
- QEC Policy

### 2. **Detailed Policy Information**
- General Academic Rules and Regulations
- Admission Process
- Transfer of Credits/Margins
- Medium of Instructions and Examinations
- Attendance Policy
- Add/Drop of Courses

### 3. **Search Functionality**
- Search policies by keyword
- Find specific rules quickly
- Get relevant policy excerpts

---

## 🚀 How to Use

### From the Web Interface

**1. Access Policies Section:**
- Click the "Policies" card on the homepage
- Or click "📋 Policies" in the sidebar menu

**2. View All Policies:**
```
The system will automatically fetch and display:
- Policy categories with links
- Detailed policy descriptions
- Source URL for full information
```

**3. Search for Specific Policies:**
```javascript
// In the chat input, type:
"search policies: admission"
"search policies: attendance"
"search policies: harassment"
```

### From API Endpoints

**Get All Policies:**
```
GET http://127.0.0.1:5000/policies
```

**Get Policy Summary:**
```
GET http://127.0.0.1:5000/policies/summary
```

**Search Policies:**
```
GET http://127.0.0.1:5000/policies/search?q=admission
```

**Get Specific Policies:**
```
GET http://127.0.0.1:5000/policies/specific
```

---

## 📋 Available Policies

### Academic Policies
1. **General Academic Rules**
   - Semester system guidelines
   - Credit hour requirements
   - Grade point system

2. **Admission Process**
   - Merit-based selection
   - Application procedures
   - Provisional admission rules

3. **Attendance Policy**
   - Minimum attendance requirements
   - Absence procedures
   - Make-up work policies

4. **Transfer of Credits**
   - Credit transfer criteria
   - Minimum grade requirements
   - Migration procedures

### Student Policies
5. **Medium of Instructions**
   - English as primary language
   - Examination language

6. **Add/Drop Courses**
   - Course registration deadlines
   - Drop procedures
   - Academic calendar

### Institutional Policies
7. **Harassment Policy**
   - HEC guidelines
   - Reporting procedures
   - Committee structure

8. **Disability Policy**
   - Equal opportunities
   - Support services
   - Accommodations

9. **QEC Policy**
   - Quality standards
   - Assessment procedures
   - Continuous improvement

---

## 🔧 Technical Implementation

### Backend (Python)

**File:** `agent/policy_checker.py`

```python
# Main functions:
fetch_policies()        # Scrapes policies from website
get_policy_summary()    # Returns formatted summary
search_policy(keyword)  # Searches by keyword
get_specific_policies() # Returns important policies
```

### Frontend (JavaScript)

**File:** `static/app.js`

```javascript
// Main functions:
showPolicies()           # Displays all policies
searchPolicies(keyword)  # Searches policies
```

### API Routes

**File:** `web_frontend.py`

```python
/policies          # GET all policies
/policies/summary  # GET formatted summary
/policies/search   # GET search results
/policies/specific # GET specific policies
```

---

## 📊 Data Structure

### Policy Object
```json
{
  "url": "https://riphahsahiwal.edu.pk/rules-and-policies/",
  "title": "Rules and Policies",
  "categories": [
    {
      "name": "HEC's Sexual Harassment Policy",
      "url": "https://..."
    }
  ],
  "details": [
    {
      "title": "General Academic Rules and Regulations",
      "content": "Note: The Academic Rules..."
    }
  ]
}
```

### Search Result
```json
{
  "keyword": "admission",
  "results": [
    {
      "type": "detail",
      "title": "Admission Process",
      "content": "Applications for..."
    }
  ]
}
```

---

## 🎨 UI Components

### Sidebar Menu Item
```html
<div class="menu-item" onclick="showPolicies()">
    <span>📋</span>
    <span>Policies</span>
</div>
```

### Quick Action Card
```html
<div class="action-card" onclick="showPolicies()">
    <div class="action-icon">📋</div>
    <div class="action-title">Policies</div>
    <div class="action-desc">View university rules & policies</div>
</div>
```

### Chat Messages
- Policy categories displayed as numbered list
- Each policy detail shown in separate message
- Links provided for full information

---

## 🔍 Search Examples

**Search for admission policies:**
```
Input: "search policies: admission"
Output: Admission Process details
```

**Search for attendance rules:**
```
Input: "search policies: attendance"
Output: Attendance Policy information
```

**Search for harassment policy:**
```
Input: "search policies: harassment"
Output: HEC Harassment Policy details
```

---

## 🌐 Source Website

**URL:** https://riphahsahiwal.edu.pk/rules-and-policies/

The system scrapes data from this official Riphah Sahiwal website in real-time, ensuring you always get the latest policy information.

---

## 🛠️ Dependencies

```
beautifulsoup4>=4.12.0  # HTML parsing
requests>=2.31.0        # HTTP requests
```

Install with:
```bash
pip install beautifulsoup4 requests
```

---

## 📱 User Experience

### Flow
1. User clicks "Policies" button
2. System shows loading message
3. Fetches policies from website
4. Displays categories and details
5. Provides search functionality
6. Shows source URL for reference

### Messages
- ✅ Success: "Policies loaded successfully"
- ⏳ Loading: "Loading university policies..."
- ❌ Error: "Failed to load policies"
- 🔍 Search: "Searching for 'keyword'..."

---

## 🎯 Use Cases

### For Students
- Check admission requirements
- Understand attendance rules
- Learn about credit transfers
- Know harassment reporting procedures

### For Applicants
- Review admission process
- Understand eligibility criteria
- Check required documents
- Learn about scholarships

### For Faculty
- Reference academic policies
- Check grading guidelines
- Understand QEC standards
- Review institutional policies

---

## 🔐 Security & Privacy

- No personal data collected
- Read-only access to public website
- No authentication required
- Respects website robots.txt
- Implements request timeouts

---

## 🚦 Error Handling

### Network Errors
```python
try:
    response = requests.get(POLICIES_URL, timeout=10)
except requests.exceptions.Timeout:
    return {"error": "Request timeout"}
```

### Parsing Errors
```python
try:
    soup = BeautifulSoup(response.content, 'html.parser')
except Exception as e:
    return {"error": "Failed to parse content"}
```

### Display Errors
```javascript
if (data.error) {
    addMessage('assistant', `❌ Error: ${data.error}`);
}
```

---

## 📈 Future Enhancements

### Planned Features
- [ ] Policy change notifications
- [ ] Bookmark favorite policies
- [ ] Download policies as PDF
- [ ] Multi-language support
- [ ] Policy comparison tool
- [ ] Historical policy versions
- [ ] Email policy updates
- [ ] Mobile app integration

### Improvements
- [ ] Cache policies for faster loading
- [ ] Offline policy access
- [ ] Advanced search filters
- [ ] Policy recommendations
- [ ] Related policies suggestions

---

## 🧪 Testing

### Test Policy Fetching
```bash
cd pc_ai_assistant
python agent/policy_checker.py
```

### Test API Endpoints
```bash
# Start server
python launcher.py

# Test in another terminal
curl http://127.0.0.1:5000/policies
curl http://127.0.0.1:5000/policies/summary
curl "http://127.0.0.1:5000/policies/search?q=admission"
```

### Test UI
1. Open http://127.0.0.1:5000
2. Click "Policies" card
3. Verify policies display
4. Test search functionality

---

## 📞 Support

**Issues?**
- Check internet connection
- Verify website is accessible
- Check browser console for errors
- Review server logs

**Questions?**
- Read this guide
- Check API documentation
- Review source code
- Contact support

---

## 🎉 Summary

The University Policies feature provides:
- ✅ Real-time policy information
- ✅ Easy search functionality
- ✅ Clean, modern interface
- ✅ Mobile-friendly design
- ✅ Fast and reliable
- ✅ Always up-to-date

**Start using it now:** http://127.0.0.1:5000

Click "Policies" and explore! 📋✨
