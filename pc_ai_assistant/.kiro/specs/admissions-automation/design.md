# PC AI Assistant - Admissions Automation System
## Design Document

**Feature Name**: admissions-automation  
**Version**: 3.0  
**Date**: February 11, 2026  
**Status**: ✅ Implemented

---

## 1. Architecture Overview

### 1.1 System Architecture

The system follows a client-server architecture with the following components:

```
┌─────────────────────────────────────────────────────────┐
│                    Browser (Client)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   HTML/CSS   │  │  JavaScript  │  │  Chat UI     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │ HTTP/REST
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Flask Web Server                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Routes     │  │  Job Queue   │  │  File Serve  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Policy     │  │   Document   │  │   Browser    │
│  Validator   │  │  Generator   │  │  Automation  │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ YAML Config  │  │  Documents/  │  │   Selenium   │
│    Files     │  │   Folder     │  │   WebDriver  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 1.2 Component Responsibilities

**Frontend (Browser)**:
- Render modern UI with dark theme
- Handle user interactions
- Display chat messages and validation results
- Poll for job status updates
- Provide download links

**Backend (Flask Server)**:
- Handle HTTP requests
- Manage job queue
- Coordinate automation tasks
- Serve generated files
- Validate application data

**Policy Validator**:
- Validate personal information
- Validate contact information
- Validate academic information
- Generate validation reports

**Document Generator**:
- Generate Word documents
- Generate PDF documents
- Generate Markdown documents
- Generate HTML documents
- Generate PowerPoint presentations

**Browser Automation**:
- Control Chrome browser via Selenium
- Navigate to admissions portal
- Fill forms automatically
- Handle authentication

---

## 2. Data Models

### 2.1 Application Data Model

```yaml
# data/application.yaml
personal_info:
  first_name: string (required, min 2 chars)
  last_name: string (optional, recommended)
  cnic: string (required, 13 digits)
  date_of_birth: date (required, YYYY-MM-DD)
  gender: string (required, "Male" | "Female" | "Other")
  nationality: string (required)

contact_info:
  email: string (required, valid email format)
  mobile: string (required, format: 03XXXXXXXXX)
  address: string (required, min 10 chars)
  city: string (optional)
  province: string (optional)

academic_info:
  program: string (required)
  campus: string (required)
  level: string (required)
  last_institute: string (optional, recommended)
  last_degree: string (optional)
  last_marks: number (optional)

credentials:
  username: string (required for automation)
  password: string (required for automation)
```

### 2.2 Validation Result Model

```python
{
    "is_valid": boolean,
    "errors": [string],      # Critical errors that block submission
    "warnings": [string],    # Recommendations that don't block
    "info": [string],        # Informational messages
    "report": string         # Formatted text report
}
```

### 2.3 Job Model

```python
{
    "job_id": string,        # Unique identifier (8 chars hex)
    "action": string,        # "apply", "create_doc", "create_ppt"
    "status": string,        # "running", "completed", "failed"
    "result": any,           # Result data or error message
    "created_at": datetime,  # Job creation timestamp
    "completed_at": datetime # Job completion timestamp (optional)
}
```

### 2.4 Document Request Model

```python
{
    "title": string,         # Document title
    "format": string,        # "word", "pdf", "markdown", "html"
    "content": string        # Document content (paragraphs)
}
```

### 2.5 Presentation Request Model

```python
{
    "title": string,         # Presentation title
    "slides": string         # Slides content (separated by blank lines)
}
```

---

## 3. API Design

### 3.1 REST Endpoints

#### GET /
**Purpose**: Serve main application interface  
**Response**: HTML page  
**Status Codes**: 200 OK

#### POST /command
**Purpose**: Execute automation command  
**Request Body**:
```json
{
    "action": "apply" | "create_doc" | "create_ppt",
    "payload": {
        // Action-specific data
    }
}
```
**Response**:
```json
{
    "job_id": "abc12345",
    "status": "running"
}
```
**Status Codes**: 200 OK, 400 Bad Request, 500 Internal Server Error

#### GET /jobs
**Purpose**: Get status of all jobs  
**Response**:
```json
{
    "job_id_1": {
        "status": "completed",
        "result": "..."
    },
    "job_id_2": {
        "status": "running",
        "result": null
    }
}
```
**Status Codes**: 200 OK

#### GET /policies
**Purpose**: Fetch university policies  
**Response**:
```json
{
    "policies": [
        {
            "title": "Admission Policy",
            "content": "..."
        }
    ]
}
```
**Status Codes**: 200 OK

#### POST /validate/application
**Purpose**: Validate complete application data  
**Request Body**: Application data object  
**Response**: Validation result object  
**Status Codes**: 200 OK, 400 Bad Request

#### GET /application/data
**Purpose**: Get application data from YAML file  
**Response**: Application data object  
**Status Codes**: 200 OK, 500 Internal Server Error

#### GET /download/<job_id>
**Purpose**: Download generated file  
**Response**: File download  
**Status Codes**: 200 OK, 404 Not Found

---

## 4. Module Design

### 4.1 Policy Validator Module

**File**: `agent/policy_validator.py`

**Class**: `PolicyValidator`

**Methods**:

```python
def __init__(self):
    """Initialize validator with empty error/warning/info lists"""

def validate_personal_info(self, data: Dict) -> None:
    """Validate personal information fields"""
    # Validates: first_name, last_name, cnic, age, gender, nationality

def validate_contact_info(self, data: Dict) -> None:
    """Validate contact information fields"""
    # Validates: email, mobile, address

def validate_academic_info(self, data: Dict) -> None:
    """Validate academic information fields"""
    # Validates: program, campus, level, last_institute

def validate_eligibility(self, data: Dict) -> None:
    """Check eligibility criteria"""
    # Checks: age requirements, document requirements

def validate_all(self, data: Dict) -> Tuple[bool, List[str], List[str], List[str]]:
    """Validate all application data"""
    # Returns: (is_valid, errors, warnings, info)

def generate_report(self) -> str:
    """Generate formatted validation report"""
    # Returns: Multi-line text report with indicators
```

**Validation Logic**:

1. **CNIC Validation**: Must be exactly 13 digits
2. **Age Validation**: Calculate from DOB, must be 16-35 years
3. **Email Validation**: Use regex pattern for valid email
4. **Mobile Validation**: Must match Pakistan format (03XXXXXXXXX)
5. **Required Fields**: Check presence and minimum length
6. **Recommended Fields**: Warn if missing but don't block

---

### 4.2 Document Generator Module

**File**: `agent/document_generator.py`

**Functions**:

```python
def create_word_document(title: str, content: str) -> str:
    """
    Create Word document using python-docx
    
    Args:
        title: Document title
        content: Document content (paragraphs separated by newlines)
    
    Returns:
        Filepath of generated document
    """
    # 1. Create Document object
    # 2. Add title as heading
    # 3. Add timestamp
    # 4. Parse content into paragraphs
    # 5. Add each paragraph
    # 6. Save to documents/ folder
    # 7. Return filepath

def create_pdf_document(title: str, content: str) -> str:
    """
    Create PDF document using reportlab
    
    Args:
        title: Document title
        content: Document content
    
    Returns:
        Filepath of generated PDF
    """
    # 1. Create Canvas object
    # 2. Set font and size
    # 3. Add title
    # 4. Add timestamp
    # 5. Add content with word wrapping
    # 6. Save PDF
    # 7. Return filepath

def create_markdown_document(title: str, content: str) -> str:
    """
    Create Markdown document
    
    Args:
        title: Document title
        content: Document content
    
    Returns:
        Filepath of generated markdown file
    """
    # 1. Format title as # heading
    # 2. Add timestamp
    # 3. Add content
    # 4. Write to .md file
    # 5. Return filepath

def create_html_document(title: str, content: str) -> str:
    """
    Create HTML document
    
    Args:
        title: Document title
        content: Document content
    
    Returns:
        Filepath of generated HTML file
    """
    # 1. Create HTML structure
    # 2. Add CSS styling
    # 3. Add title in <h1>
    # 4. Add timestamp
    # 5. Add content in <p> tags
    # 6. Write to .html file
    # 7. Return filepath

def create_powerpoint(title: str, slides_content: str) -> str:
    """
    Create PowerPoint presentation using python-pptx
    
    Args:
        title: Presentation title
        slides_content: Slides content (separated by blank lines)
    
    Returns:
        Filepath of generated presentation
    """
    # 1. Create Presentation object
    # 2. Add title slide
    # 3. Parse slides_content into individual slides
    # 4. For each slide:
    #    - Add new slide
    #    - Set title
    #    - Add bullet points
    # 5. Save presentation
    # 6. Return filepath
```

**File Naming Convention**:
```
{title}_{YYYYMMDD}_{HHMMSS}.{ext}
Example: Project_Report_20260211_143052.docx
```

---

### 4.3 Browser Automation Module

**File**: `agent/apply_riphah.py`

**Main Function**:

```python
def apply_riphah(config: Dict, submit: bool = False) -> None:
    """
    Automate Riphah admissions application
    
    Args:
        config: Configuration with credentials and data
        submit: Whether to submit or just fill
    
    Process:
        1. Load application data from YAML
        2. Validate data using PolicyValidator
        3. Show validation report
        4. If errors, ask user to proceed or cancel
        5. Initialize browser with persistent profile
        6. Navigate to admissions portal
        7. Login with credentials
        8. Navigate to application form
        9. Fill all form fields
        10. Take screenshots
        11. Submit if requested
        12. Close browser
    """
```

**Helper Functions**:

```python
def validate_before_apply(data: Dict) -> Dict:
    """Run validation and return result"""

def init_browser(headless: bool = False) -> webdriver.Chrome:
    """Initialize Chrome browser with profile"""

def login_to_portal(driver, username: str, password: str) -> bool:
    """Login to admissions portal"""

def fill_application_form(driver, data: Dict) -> bool:
    """Fill application form fields"""

def take_screenshot(driver, name: str) -> None:
    """Take screenshot for debugging"""
```

---

### 4.4 Web Frontend Module

**File**: `web_frontend.py`

**Flask Application**:

```python
app = Flask(__name__)

# Global job storage
jobs = {}

@app.route('/')
def index():
    """Serve main interface"""

@app.route('/command', methods=['POST'])
def execute_command():
    """
    Execute automation command in background thread
    
    Process:
        1. Parse request JSON
        2. Generate unique job_id
        3. Create job entry
        4. Start background thread
        5. Return job_id to client
    """

@app.route('/jobs')
def get_jobs():
    """Return status of all jobs"""

@app.route('/download/<job_id>')
def download_file(job_id):
    """
    Serve generated file for download
    
    Process:
        1. Validate job_id
        2. Check if job completed
        3. Get filepath from job result
        4. Send file to client
    """

def _run_job(job_id: str, action: str, payload: Dict):
    """
    Background job runner
    
    Process:
        1. Update job status to "running"
        2. Execute action (apply, create_doc, create_ppt)
        3. Catch exceptions
        4. Update job status to "completed" or "failed"
        5. Store result or error message
    """
```

---

## 5. User Interface Design

### 5.1 Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│                      Header Bar                          │
│              PC AI Assistant - Admissions                │
└─────────────────────────────────────────────────────────┘
┌──────────┬──────────────────────────────────────────────┐
│          │                                               │
│ Sidebar  │           Chat Interface                      │
│          │                                               │
│ 🏠 Home  │  ┌─────────────────────────────────────┐    │
│ 👤 Login │  │ Assistant: Welcome! How can I help? │    │
│ 📝 Reg   │  └─────────────────────────────────────┘    │
│ 🎯 Apply │                                               │
│ 📋 Pol   │  ┌─────────────────────────────────────┐    │
│ 📄 Doc   │  │ You: Create a document              │    │
│ 📊 PPT   │  └─────────────────────────────────────┘    │
│          │                                               │
│          │  ┌─────────────────────────────────────┐    │
│          │  │ Assistant: Document created!        │    │
│          │  │ 📥 Download: report.docx            │    │
│          │  └─────────────────────────────────────┘    │
│          │                                               │
│          │  ┌───────────────────────────────────┐      │
│          │  │ Type a message...          [Send] │      │
│          │  └───────────────────────────────────┘      │
└──────────┴──────────────────────────────────────────────┘
```

### 5.2 Color Scheme

**Primary Colors**:
- Background: `#1a1a2e` (dark blue-gray)
- Sidebar: `#16213e` (darker blue)
- Accent: `#0f3460` (medium blue)
- Highlight: `#e94560` (red-pink)

**Text Colors**:
- Primary: `#ffffff` (white)
- Secondary: `#cccccc` (light gray)
- Muted: `#888888` (gray)

**Status Colors**:
- Success: `#4caf50` (green)
- Warning: `#ff9800` (orange)
- Error: `#f44336` (red)
- Info: `#2196f3` (blue)

### 5.3 Modal Designs

**Apply Modal**:
```
┌─────────────────────────────────────┐
│  Apply for Admission            [X] │
├─────────────────────────────────────┤
│                                     │
│  Username: [________________]       │
│  Password: [________________]       │
│                                     │
│  ☑ Validate against policies        │
│                                     │
│  [Cancel]          [Apply Now]      │
└─────────────────────────────────────┘
```

**Create Document Modal**:
```
┌─────────────────────────────────────┐
│  Create Document                [X] │
├─────────────────────────────────────┤
│                                     │
│  Title: [________________]          │
│                                     │
│  Format: [Word ▼]                   │
│          Word (.docx)               │
│          PDF (.pdf)                 │
│          Markdown (.md)             │
│          HTML (.html)               │
│                                     │
│  Content:                           │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │                             │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Cancel]      [Create Document]    │
└─────────────────────────────────────┘
```

**Create Presentation Modal**:
```
┌─────────────────────────────────────┐
│  Create Presentation            [X] │
├─────────────────────────────────────┤
│                                     │
│  Title: [________________]          │
│                                     │
│  Slides Content:                    │
│  ┌─────────────────────────────┐   │
│  │ Slide 1 Title               │   │
│  │ Bullet point 1              │   │
│  │ Bullet point 2              │   │
│  │                             │   │
│  │ Slide 2 Title               │   │
│  │ Bullet point 1              │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Cancel]   [Create Presentation]   │
└─────────────────────────────────────┘
```

---

## 6. Algorithms and Logic

### 6.1 Validation Algorithm

```
FUNCTION validate_application(data):
    errors = []
    warnings = []
    info = []
    
    // Personal Info Validation
    IF data.first_name is empty OR length < 2:
        errors.append("First name required (min 2 chars)")
    
    IF data.last_name is empty:
        warnings.append("Last name recommended")
    
    IF data.cnic is empty OR length != 13 OR not all digits:
        errors.append("CNIC must be 13 digits")
    ELSE:
        info.append("✅ CNIC format valid")
    
    age = calculate_age(data.date_of_birth)
    IF age < 16 OR age > 35:
        errors.append("Age must be 16-35 years")
    ELSE:
        info.append(f"✅ Age: {age} years - Eligible")
    
    // Contact Info Validation
    IF NOT is_valid_email(data.email):
        errors.append("Valid email required")
    ELSE:
        info.append("✅ Email format valid")
    
    IF NOT matches_pattern(data.mobile, "03[0-9]{9}"):
        errors.append("Mobile must be 03XXXXXXXXX")
    ELSE:
        info.append("✅ Mobile format valid")
    
    // Academic Info Validation
    IF data.program is empty:
        errors.append("Program required")
    ELSE:
        info.append(f"✅ Selected program: {data.program}")
    
    IF data.last_institute is empty:
        warnings.append("Last institute recommended")
    
    // Generate Report
    is_valid = (length of errors == 0)
    report = format_validation_report(errors, warnings, info)
    
    RETURN {
        is_valid: is_valid,
        errors: errors,
        warnings: warnings,
        info: info,
        report: report
    }
```

### 6.2 Document Generation Algorithm

```
FUNCTION create_document(title, format, content):
    timestamp = current_datetime()
    filename = f"{title}_{timestamp}.{format}"
    filepath = f"documents/{filename}"
    
    SWITCH format:
        CASE "word":
            doc = create_word_doc()
            doc.add_heading(title, level=1)
            doc.add_paragraph(f"Created: {timestamp}")
            FOR paragraph IN split_content(content):
                doc.add_paragraph(paragraph)
            doc.save(filepath)
        
        CASE "pdf":
            pdf = create_pdf()
            pdf.add_title(title)
            pdf.add_text(f"Created: {timestamp}")
            pdf.add_content(content)
            pdf.save(filepath)
        
        CASE "markdown":
            md_content = f"# {title}\n\n"
            md_content += f"*Created: {timestamp}*\n\n"
            md_content += content
            write_file(filepath, md_content)
        
        CASE "html":
            html = create_html_template()
            html.set_title(title)
            html.add_timestamp(timestamp)
            html.add_content(content)
            write_file(filepath, html.render())
    
    RETURN filepath
```

### 6.3 Job Queue Algorithm

```
FUNCTION execute_command(action, payload):
    job_id = generate_unique_id()
    
    jobs[job_id] = {
        status: "running",
        result: null,
        created_at: now()
    }
    
    START_THREAD:
        TRY:
            SWITCH action:
                CASE "apply":
                    result = apply_riphah(payload)
                CASE "create_doc":
                    result = create_document(payload)
                CASE "create_ppt":
                    result = create_presentation(payload)
            
            jobs[job_id].status = "completed"
            jobs[job_id].result = result
            jobs[job_id].completed_at = now()
        
        CATCH exception:
            jobs[job_id].status = "failed"
            jobs[job_id].result = str(exception)
            jobs[job_id].completed_at = now()
    
    RETURN job_id
```

---

## 7. Security Design

### 7.1 Credential Management

**Storage**: Credentials stored in `data/credentials.json` (gitignored)

**Access**: Only backend has access to credentials

**Transmission**: Credentials sent over HTTPS only

**Validation**: Credentials validated before use

### 7.2 Input Validation

**All user inputs validated**:
- Length checks
- Format checks
- Type checks
- Sanitization

### 7.3 File Access Control

**Generated files**:
- Stored in dedicated `documents/` folder
- Accessed only via job_id
- Served with proper MIME types
- Cleaned up after download (optional)

### 7.4 Error Handling

**Sensitive information**:
- Never logged
- Never displayed to user
- Masked in error messages

---

## 8. Performance Optimization

### 8.1 Caching Strategy

**Browser Profile**: Persistent profile caches:
- Login sessions
- Cookies
- Local storage

**Static Assets**: Cached by browser

### 8.2 Async Operations

**Background Jobs**: All long-running tasks run in threads

**Non-blocking**: Server remains responsive during automation

### 8.3 Resource Management

**Browser Instances**: Closed after use

**File Cleanup**: Old documents cleaned periodically

**Memory**: Job results cleared after retrieval

---

## 9. Testing Strategy

### 9.1 Unit Tests

**Test Files**:
- `test_policy_validator.py`
- `test_document_generator.py`
- `test_api_endpoints.py`

**Coverage**: Aim for 80%+ code coverage

### 9.2 Integration Tests

**Test Scenarios**:
- End-to-end validation flow
- Document creation and download
- Application automation flow

### 9.3 Manual Testing

**Test Cases**:
- UI functionality
- Browser automation
- Error handling
- Edge cases

---

## 10. Deployment Architecture

### 10.1 Development Environment

```
Local Machine
├── Python 3.13+
├── Chrome Browser
├── Virtual Environment
└── Flask Development Server (port 5000)
```

### 10.2 Production Environment (Future)

```
Server
├── Python 3.13+
├── Chrome Headless
├── Gunicorn WSGI Server
├── Nginx Reverse Proxy
└── SSL Certificate
```

---

## 11. Correctness Properties

### 11.1 Validation Properties

**Property 1.1**: All required fields must be validated before submission  
**Validates**: Requirements 2.1.1, 2.1.2, 2.1.3

**Property 1.2**: Invalid data must not proceed to automation  
**Validates**: Requirements 2.1.5

**Property 1.3**: Validation results must be displayed to user  
**Validates**: Requirements 2.1.4, 2.1.6

### 11.2 Document Generation Properties

**Property 2.1**: Generated documents must contain user-specified content  
**Validates**: Requirements 2.2.2

**Property 2.2**: Document generation must complete within time limit  
**Validates**: Requirements 2.2.7

**Property 2.3**: Generated files must be downloadable  
**Validates**: Requirements 2.2.4

### 11.3 Security Properties

**Property 3.1**: Credentials must never be logged or displayed  
**Validates**: Requirements 5.5

**Property 3.2**: All inputs must be validated before processing  
**Validates**: Requirements 5.3

---

## 12. Maintenance and Support

### 12.1 Logging

**Log Levels**:
- INFO: Normal operations
- WARNING: Validation warnings
- ERROR: Failures and exceptions
- DEBUG: Detailed debugging info

**Log Files**:
- `server.out.log`: Standard output
- `server.err.log`: Error output

### 12.2 Monitoring

**Metrics to Track**:
- Job success/failure rates
- Response times
- Error frequencies
- Resource usage

### 12.3 Updates

**Regular Maintenance**:
- Update dependencies quarterly
- Test automation monthly
- Review logs weekly
- Backup data daily

---

**Last Updated**: February 11, 2026  
**Version**: 3.0  
**Status**: Implemented ✅
