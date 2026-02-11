// Global state
let lastJobId = null;
let jobCompleted = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    addMessage('assistant', 'Welcome! I can help you with university admissions. Choose an action from the sidebar or ask me anything.');
    refreshJobs();
    setInterval(refreshJobs, 3000);
});

// Message handling
function addMessage(type, text) {
    const container = document.getElementById('chatContainer');
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    container.appendChild(message);
    container.scrollTop = container.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    
    if (!text) return;
    
    addMessage('user', text);
    input.value = '';
    
    // Process the message
    addMessage('assistant', 'I understand. Let me help you with that...');
    
    // You can add AI processing here
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Modal functions
function showLoginModal() {
    document.getElementById('loginModal').classList.add('active');
}

function showRegisterModal() {
    document.getElementById('registerModal').classList.add('active');
}

function showApplyModal() {
    console.log('showApplyModal called');
    const modal = document.getElementById('applyModal');
    console.log('Modal element:', modal);
    if (modal) {
        modal.classList.add('active');
        console.log('Modal should now be visible');
    } else {
        console.error('Apply modal not found!');
    }
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function showWelcome() {
    const container = document.getElementById('chatContainer');
    container.innerHTML = '';
    addMessage('assistant', 'Welcome back! What would you like to do today?');
}

// Submit functions
async function submitLogin() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const remember = document.getElementById('loginRemember').checked;
    
    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }
    
    closeModal('loginModal');
    addMessage('user', 'Login to admissions portal');
    addMessage('assistant', '🔄 Logging in...');
    
    const payload = {
        action: 'login',
        command: 'login',
        credentials: { email, password },
        fields: {},
        submit: false,
        remember: remember
    };
    
    try {
        const response = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        lastJobId = result.job_id;
        updateStatus('Processing...');
        addMessage('assistant', `✅ Job created: ${result.job_id.substring(0, 8)}...`);
    } catch (error) {
        addMessage('assistant', `❌ Error: ${error.message}`);
    }
}

async function submitRegister() {
    const name = document.getElementById('regName').value;
    const mobile = document.getElementById('regMobile').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const remember = document.getElementById('regRemember').checked;
    
    if (!name || !mobile || !email || !password) {
        alert('Please fill in all fields');
        return;
    }
    
    closeModal('registerModal');
    addMessage('user', 'Register new account');
    addMessage('assistant', '🔄 Creating account...');
    
    const payload = {
        action: 'register',
        command: 'register',
        credentials: { email, password, name, mobile },
        fields: {},
        submit: false,
        remember: remember
    };
    
    try {
        const response = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        lastJobId = result.job_id;
        updateStatus('Processing...');
        addMessage('assistant', `✅ Job created: ${result.job_id.substring(0, 8)}...`);
    } catch (error) {
        addMessage('assistant', `❌ Error: ${error.message}`);
    }
}

async function submitApply() {
    const email = document.getElementById('applyEmail').value;
    const password = document.getElementById('applyPassword').value;
    const submit = document.getElementById('applySubmit').checked;
    const remember = document.getElementById('applyRemember').checked;
    const validate = document.getElementById('applyValidate').checked;
    
    if (!email || !password) {
        alert('Please fill in all fields');
        return;
    }
    
    closeModal('applyModal');
    addMessage('user', 'Apply for admission');
    
    // Validate application data if checkbox is checked
    if (validate) {
        addMessage('assistant', '🔍 Validating application against university policies...');
        
        try {
            // First, fetch the application data from YAML file
            const dataResponse = await fetch('/application/data');
            const applicationData = await dataResponse.json();
            
            if (applicationData.error) {
                throw new Error(applicationData.error);
            }
            
            // Now validate the complete application data
            const validateResponse = await fetch('/validate/application', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(applicationData)
            });
            
            const validationResult = await validateResponse.json();
            
            if (validationResult.errors && validationResult.errors.length > 0) {
                addMessage('assistant', '❌ Validation Errors Found:');
                validationResult.errors.forEach(error => {
                    addMessage('assistant', error);
                });
                
                const proceed = confirm('Validation errors found. Do you want to proceed anyway?');
                if (!proceed) {
                    addMessage('assistant', '❌ Application cancelled by user');
                    return;
                }
            }
            
            if (validationResult.warnings && validationResult.warnings.length > 0) {
                addMessage('assistant', '⚠️ Warnings:');
                validationResult.warnings.forEach(warning => {
                    addMessage('assistant', warning);
                });
            }
            
            if (validationResult.is_valid) {
                addMessage('assistant', '✅ Validation passed! Proceeding with application...');
            }
            
        } catch (error) {
            addMessage('assistant', `⚠️ Validation check failed: ${error.message}`);
            addMessage('assistant', 'Proceeding with application anyway...');
        }
    }
    
    addMessage('assistant', '🔄 Starting application process...');
    
    const payload = {
        action: 'apply',
        command: 'apply',
        credentials: { email, password },
        fields: {},
        submit: submit,
        remember: remember
    };
    
    try {
        const response = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        lastJobId = result.job_id;
        updateStatus('Processing...');
        addMessage('assistant', `✅ Job created: ${result.job_id.substring(0, 8)}...`);
    } catch (error) {
        addMessage('assistant', `❌ Error: ${error.message}`);
    }
}

// Jobs management
async function refreshJobs() {
    try {
        const response = await fetch('/jobs');
        const jobs = await response.json();
        
        const jobsList = document.getElementById('jobsList');
        jobsList.innerHTML = '';
        
        const jobIds = Object.keys(jobs).reverse().slice(0, 5);
        
        if (jobIds.length === 0) {
            jobsList.innerHTML = '<div style="color: #71717a; font-size: 13px;">No active jobs</div>';
            return;
        }
        
        jobIds.forEach(id => {
            const job = jobs[id];
            const jobItem = document.createElement('div');
            jobItem.className = 'job-item';
            
            const statusBadge = document.createElement('span');
            statusBadge.className = `status-badge ${job.status}`;
            statusBadge.textContent = job.status;
            
            const jobId = document.createElement('div');
            jobId.className = 'job-id';
            jobId.textContent = id.substring(0, 8) + '...';
            
            jobItem.appendChild(statusBadge);
            jobItem.appendChild(jobId);
            
            if (job.message) {
                const message = document.createElement('div');
                message.style.marginTop = '8px';
                message.style.fontSize = '12px';
                message.style.color = '#71717a';
                message.textContent = job.message.substring(0, 50) + '...';
                jobItem.appendChild(message);
            }
            
            jobsList.appendChild(jobItem);
            
            // Update status for last job
            if (id === lastJobId) {
                if (job.status === 'done') {
                    updateStatus('✅ Completed');
                    if (!jobCompleted) {
                        addMessage('assistant', '✅ Task completed successfully!');
                        
                        // If there's a file to download, show download link
                        if (job.filepath) {
                            const filename = job.filename || 'document';
                            addMessage('assistant', `📥 <a href="/download/${id}" download style="color: #667eea; text-decoration: underline;">Download ${filename}</a>`);
                        }
                        
                        jobCompleted = true;
                        speak('Task completed successfully!');
                    }
                } else if (job.status === 'failed') {
                    updateStatus('❌ Failed');
                    if (!jobCompleted) {
                        addMessage('assistant', `❌ Task failed: ${job.message || 'Unknown error'}`);
                        jobCompleted = true;
                    }
                } else if (job.status === 'running') {
                    updateStatus('⚡ Running...');
                }
            }
        });
    } catch (error) {
        console.error('Error refreshing jobs:', error);
    }
}

function updateStatus(text) {
    document.getElementById('statusText').textContent = text;
}

// Voice functions
function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        alert('Speech recognition not supported in this browser');
        return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    
    recognition.onstart = () => {
        addMessage('assistant', '🎤 Listening...');
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('messageInput').value = transcript;
        addMessage('assistant', 'Got it! Press Send or Enter to continue.');
    };
    
    recognition.onerror = (event) => {
        addMessage('assistant', `❌ Speech error: ${event.error}`);
    };
    
    recognition.start();
}

function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    }
}

function attachFile() {
    addMessage('assistant', 'File attachment feature coming soon!');
}

// Policies functions
async function showPolicies() {
    const container = document.getElementById('chatContainer');
    container.innerHTML = '';
    
    addMessage('assistant', '📋 Loading university policies...');
    updateStatus('Loading policies...');
    
    try {
        const response = await fetch('/policies');
        const data = await response.json();
        
        if (data.error) {
            addMessage('assistant', `❌ Error loading policies: ${data.message || data.error}`);
            return;
        }
        
        // Display policy categories
        if (data.categories && data.categories.length > 0) {
            let message = '📑 Policy Categories:\n\n';
            data.categories.forEach((cat, index) => {
                message += `${index + 1}. ${cat.name}\n`;
            });
            addMessage('assistant', message);
        }
        
        // Display policy details
        if (data.details && data.details.length > 0) {
            addMessage('assistant', '📖 Policy Details:');
            data.details.forEach((detail, index) => {
                const shortContent = detail.content.substring(0, 150) + '...';
                addMessage('assistant', `${index + 1}. ${detail.title}\n${shortContent}`);
            });
        }
        
        addMessage('assistant', `\n🔗 Full policies: ${data.url}`);
        updateStatus('✅ Policies loaded');
        
    } catch (error) {
        addMessage('assistant', `❌ Failed to load policies: ${error.message}`);
        updateStatus('❌ Error');
    }
}

async function searchPolicies(keyword) {
    addMessage('user', `Search policies: ${keyword}`);
    addMessage('assistant', `🔍 Searching for "${keyword}"...`);
    
    try {
        const response = await fetch(`/policies/search?q=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        
        if (data.error) {
            addMessage('assistant', `❌ Error: ${data.error}`);
            return;
        }
        
        if (data.results.length === 0) {
            addMessage('assistant', `No policies found for "${keyword}"`);
            return;
        }
        
        addMessage('assistant', `Found ${data.results.length} result(s):`);
        data.results.forEach((result, index) => {
            if (result.type === 'category') {
                addMessage('assistant', `${index + 1}. ${result.name}\n🔗 ${result.url}`);
            } else {
                addMessage('assistant', `${index + 1}. ${result.title}\n${result.content.substring(0, 150)}...`);
            }
        });
        
    } catch (error) {
        addMessage('assistant', `❌ Search failed: ${error.message}`);
    }
}

// Close modal on outside click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});


// Document automation functions
function showCreateDocModal() {
    document.getElementById('createDocModal').classList.add('active');
}

function showCreatePPTModal() {
    document.getElementById('createPPTModal').classList.add('active');
}

async function createDocument() {
    const title = document.getElementById('docTitle').value;
    const content = document.getElementById('docContent').value;
    const format = document.getElementById('docFormat').value;
    
    if (!title || !content) {
        alert('Please fill in all fields');
        return;
    }
    
    closeModal('createDocModal');
    addMessage('user', `Create ${format.toUpperCase()} document: ${title}`);
    addMessage('assistant', `📄 Creating ${format.toUpperCase()} document...`);
    
    const payload = {
        action: 'create_doc',
        title: title,
        content: content.split('\n'),
        format: format
    };
    
    try {
        const response = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        lastJobId = result.job_id;
        jobCompleted = false;  // Reset flag
        updateStatus('Creating document...');
        addMessage('assistant', `✅ Job created: ${result.job_id.substring(0, 8)}...`);
    } catch (error) {
        addMessage('assistant', `❌ Error: ${error.message}`);
    }
}

async function createPresentation() {
    const title = document.getElementById('pptTitle').value;
    const slides = document.getElementById('pptSlides').value;
    
    if (!title || !slides) {
        alert('Please fill in all fields');
        return;
    }
    
    closeModal('createPPTModal');
    addMessage('user', `Create presentation: ${title}`);
    addMessage('assistant', '📊 Creating PowerPoint presentation...');
    
    // Parse slides (format: Title|Content1,Content2)
    const slidesArray = slides.split('\n\n').map(slide => {
        const lines = slide.split('\n');
        return {
            title: lines[0],
            content: lines.slice(1)
        };
    });
    
    const payload = {
        action: 'create_ppt',
        title: title,
        slides: slidesArray
    };
    
    try {
        const response = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        lastJobId = result.job_id;
        jobCompleted = false;  // Reset flag
        updateStatus('Creating presentation...');
        addMessage('assistant', `✅ Job created: ${result.job_id.substring(0, 8)}...`);
    } catch (error) {
        addMessage('assistant', `❌ Error: ${error.message}`);
    }
}
