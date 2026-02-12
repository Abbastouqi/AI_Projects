# 🧪 Testing Instructions - Policy Validation

**Date**: February 12, 2026  
**Status**: ✅ Ready for Testing  
**Server**: Running on http://127.0.0.1:5000

---

## ✅ What's Been Done

The policy validation system has been enhanced to show detailed output in the terminal:

1. **Enhanced `policy_validator.py`**
   - Added detailed print statements for each policy check
   - Shows policy names and requirements
   - Displays pass/fail status with emojis (✅/❌/⚠️/ℹ️)
   - Provides comprehensive validation summary

2. **Server Running**
   - Flask server is active on port 5000
   - All endpoints registered successfully
   - Debug mode enabled for testing

3. **Documentation Created**
   - `POLICY_VALIDATION_OUTPUT.md` - Shows sample output
   - `BUG_FIX_DUPLICATE_EMAIL.md` - Documents previous fix
   - This file - Testing instructions

---

## 🧪 How to Test

### Step 1: Access the Application
1. Open your browser
2. Go to: **http://127.0.0.1:5000**
3. You should see the modern UI

### Step 2: Navigate to Apply Section
1. Click **"Apply"** in the sidebar
2. You'll see the application form interface

### Step 3: Trigger Validation
1. **Keep the validation checkbox checked** (should be checked by default)
2. Enter your credentials:
   - Email: `tabbas@cs.qau.edu.pk`
   - Password: (your password)
3. Click **"Apply Now"** button

### Step 4: Watch the Terminal
1. **Switch to your terminal/command prompt** where the server is running
2. You should see detailed output like this:

```
======================================================================
🔍 POLICY VALIDATION STARTED
======================================================================

📋 Checking Personal Information Policies...
   → Policy: Personal Information - Name Requirements
      ✅ PASSED: First name valid (tuqir)
   → Policy: Identification - CNIC Requirements
      ✅ PASSED: CNIC format valid (3520212345678)
   → Policy: Admission - Age Requirements (16-35 years)
      ✅ PASSED: Age 25 within eligible range
   → Policy: Personal Information - Gender
      ✅ PASSED: Gender specified (Male)

📋 Checking Contact Information Policies...
   → Policy: Communication - Email Requirements
      ✅ PASSED: Email format valid (tabbas@cs.qau.edu.pk)
   → Policy: Communication - Mobile Number Requirements
      ✅ PASSED: Mobile format valid (03146002855)
   → Policy: Contact Information - Address Requirements
      ✅ PASSED: Address provided (32 chars)

📋 Checking Academic Information Policies...
   → Policy: Academic History - Last Institute
      ✅ PASSED: Last institute provided (Punjab College)
   → Policy: Admission - Program Selection
      ✅ PASSED: Program selected (BS Computer Science)
   → Policy: Admission - Campus Selection
      ✅ PASSED: Campus selected (Islamabad/Rawalpindi)
   → Policy: Admission - Program Level
      ✅ PASSED: Program level selected (Undergraduate)

📋 Checking Eligibility Policies...
   → Policy: Eligibility - Nationality Requirements
      ✅ PASSED: Nationality specified (Pakistan)

   → Policy: Documentation Requirements
      ℹ️  Required: CNIC/B-Form copy
      ℹ️  Required: Educational certificates
      ℹ️  Required: Passport size photographs

   → University Policies - Important Reminders
      ℹ️  Attendance Policy: Minimum 75% required
      ℹ️  Medium of Instruction: English proficiency needed
      ℹ️  Selection Policy: Purely merit-based

======================================================================
📊 VALIDATION SUMMARY
======================================================================
✅ ALL POLICIES PASSED
   • Errors: 0
   • Warnings: 0
   • Info: 13

✅ APPLICATION IS READY FOR SUBMISSION
======================================================================
```

### Step 5: Verify Behavior
- **If all policies pass**: Browser automation should start automatically
- **If any policy fails**: You'll see ❌ FAILED messages with details
- **Warnings**: Shown with ⚠️ but don't block submission

---

## 📋 What You Should See

### In Terminal
- **Policy category headers**: 📋 Checking Personal Information Policies...
- **Individual policy checks**: → Policy: [Policy Name]
- **Status for each check**: ✅ PASSED / ❌ FAILED / ⚠️ WARNING / ℹ️ INFO
- **Validation summary**: Shows counts of errors, warnings, info
- **Final decision**: ✅ READY or ❌ NOT READY

### In Browser
- Application form interface
- Credentials input fields
- "Apply Now" button
- Status updates as automation proceeds

---

## 🔍 Policies Being Validated

### 1. Personal Information
- ✅ First name (required, min 2 chars)
- ⚠️ Last name (recommended)
- ✅ CNIC (required, 13 digits)
- ✅ Date of birth (age 16-35)
- ✅ Gender (required)

### 2. Contact Information
- ✅ Email (valid format)
- ✅ Mobile (Pakistan format: 03XXXXXXXXX)
- ✅ Address (min 10 chars)

### 3. Academic Information
- ⚠️ Last institute (recommended)
- ✅ Program selection (required)
- ✅ Campus selection (required)
- ✅ Program level (required)

### 4. Eligibility
- ✅ Nationality (required)
- ℹ️ Documentation requirements (informational)
- ℹ️ University policies (informational)

---

## 🐛 Troubleshooting

### Issue: No output in terminal
**Solution**: Make sure you're looking at the terminal where `python web_frontend.py` is running

### Issue: Validation fails
**Solution**: Check the error messages - they tell you exactly what's wrong
- Fix the data in `data/application.yaml`
- Try again

### Issue: Server not responding
**Solution**: 
```bash
# Check if server is running
# If not, restart it:
cd pc_ai_assistant
python web_frontend.py
```

### Issue: Browser automation doesn't start
**Solution**: 
- Check if validation passed (look for "✅ ALL POLICIES PASSED")
- If validation failed, fix errors first
- Make sure credentials are correct

---

## 📊 Current Application Data

Your current data in `data/application.yaml`:

```yaml
first_name: tuqir
last_name: ''
cnic: '3520212345678'
dob: '2000-05-15'
gender: Male
email: tabbas@cs.qau.edu.pk
mobile: 03146002855
address: House 12 Street 5 Islamabad
nationality: Pakistan
last_institute: Punjab College
program1: BS Computer Science
campus: Islamabad/Rawalpindi
level: Undergraduate
```

**Note**: Last name is empty - you'll see a ⚠️ WARNING but it won't block submission.

---

## ✅ Expected Results

### Success Case
1. Click "Apply Now"
2. Terminal shows all policy checks
3. All checks show ✅ PASSED
4. Summary shows "✅ ALL POLICIES PASSED"
5. Browser automation starts
6. Application is submitted

### Failure Case
1. Click "Apply Now"
2. Terminal shows policy checks
3. Some checks show ❌ FAILED
4. Summary shows "❌ VALIDATION FAILED"
5. Automation stops
6. Fix errors and try again

---

## 🎯 What to Look For

### Good Signs ✅
- Detailed policy names displayed
- Clear pass/fail status for each check
- Comprehensive summary at the end
- Easy to understand what passed/failed

### Red Flags ❌
- No output in terminal
- Validation passes but shouldn't
- Validation fails but should pass
- Missing policy checks

---

## 📝 Testing Checklist

- [ ] Server is running on port 5000
- [ ] Can access http://127.0.0.1:5000
- [ ] Can see the Apply interface
- [ ] Can enter credentials
- [ ] Click "Apply Now" triggers validation
- [ ] Terminal shows detailed policy checks
- [ ] Each policy shows pass/fail status
- [ ] Summary shows total counts
- [ ] Clear indication if ready to submit
- [ ] Browser automation starts if all pass

---

## 🚀 Next Steps After Testing

1. **If everything works**:
   - Test with invalid data to see error messages
   - Verify all policy checks are working
   - Confirm automation proceeds after validation

2. **If issues found**:
   - Note which policy check is failing
   - Check if the error message is clear
   - Report any bugs or unclear messages

3. **Ready for production**:
   - All policies validated correctly
   - Clear output for users
   - Automation works smoothly

---

## 📞 Support

If you encounter any issues:
1. Check the terminal output for error messages
2. Review `POLICY_VALIDATION_OUTPUT.md` for expected output
3. Verify data in `data/application.yaml` is correct
4. Check server logs for any errors

---

**Server Status**: ✅ Running  
**Port**: 5000  
**URL**: http://127.0.0.1:5000  
**Ready for Testing**: ✅ Yes

---

**Last Updated**: February 12, 2026  
**Version**: 3.1  
**Status**: Ready for User Testing
