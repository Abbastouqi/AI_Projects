from flask import Flask, request, jsonify, render_template, send_file
import threading
import uuid
import yaml
import time
import os
from agent.command_router import route_command
from agent.policy_checker import fetch_policies, get_policy_summary, search_policy, get_specific_policies
from agent.policy_validator import validate_before_apply, check_policy_compliance

print("=" * 60)
print("LOADING WEB_FRONTEND.PY - VERSION 2.0 WITH VALIDATION")
print("=" * 60)

app = Flask(__name__)

# Load config once
with open("config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

# Simple in-memory job store
JOBS = {}
JOBS_LOCK = threading.Lock()

# HTML served from templates/index.html and styles in static/style.css


def _run_job(job_id, payload):
  """Run a job payload. Payload is a dict with keys: command, action, credentials, fields."""
  from agent.credentials import set_injected_credentials, clear_injected_credentials, save_credentials, load_saved_credentials
  from agent.apply_riphah import apply_riphah
  from agent.admissions_riphah import login_only, register_then_login
  from agent.document_generator import create_word_document, create_pdf_document, create_powerpoint, create_markdown_document, create_html_document

  with JOBS_LOCK:
    JOBS[job_id] = {"status": "running", "message": ""}

  # Inject credentials if provided so flows don't prompt on terminal
  creds = payload.get("credentials") or {}
  remember = bool(payload.get("remember", False))
  if (not creds.get("email") or not creds.get("password")):
    saved = load_saved_credentials()
    if saved.get("email") and saved.get("password"):
      creds = {**saved, **creds}

  if creds:
    set_injected_credentials(creds)
    if remember and creds.get("email") and creds.get("password"):
      save_credentials(creds)

  # Show output in terminal instead of capturing it
  print(f"\n{'='*60}")
  print(f"JOB {job_id[:8]} STARTED")
  print(f"{'='*60}\n")
  
  try:
    action = payload.get("action")
    cmd_text = payload.get("command", "")

    if action == "login":
      login_only(CONFIG)
    elif action == "register":
      register_then_login(CONFIG)
    elif action == "register_apply":
      register_then_login(CONFIG)
      run_cfg = dict(CONFIG)
      run_cfg["application_overrides"] = {}
      apply_riphah(run_cfg, submit=payload.get("submit", False))
    elif action == "apply":
      # Apply uses pre-filled data from data/application.yaml
      # Only login credentials (email/password) are passed from the UI
      run_cfg = dict(CONFIG)
      run_cfg["application_overrides"] = {}  # Don't override - use yaml file data
      apply_riphah(run_cfg, submit=payload.get("submit", False))
    elif action == "create_doc":
      # Create documents locally using Python libraries
      title = payload.get("title", "Untitled Document")
      content = payload.get("content", [])
      doc_format = payload.get("format", "word")  # word, pdf, markdown, html
      
      if doc_format == "word":
        filepath = create_word_document(title, content)
      elif doc_format == "pdf":
        filepath = create_pdf_document(title, content)
      elif doc_format == "markdown":
        filepath = create_markdown_document(title, content)
      elif doc_format == "html":
        filepath = create_html_document(title, content)
      else:
        filepath = create_word_document(title, content)
      
      # Store filepath in job result
      with JOBS_LOCK:
        JOBS[job_id]["filepath"] = filepath
        JOBS[job_id]["filename"] = os.path.basename(filepath)
      
      print(f"✅ Document created: {filepath}")
      
    elif action == "create_ppt":
      # Create PowerPoint presentation
      title = payload.get("title", "Untitled Presentation")
      slides = payload.get("slides", [])
      filepath = create_powerpoint(title, slides)
      
      # Store filepath in job result
      with JOBS_LOCK:
        JOBS[job_id]["filepath"] = filepath
        JOBS[job_id]["filename"] = os.path.basename(filepath)
      
      print(f"✅ Presentation created: {filepath}")
    else:
      # fallback to routing by text
      route_command(cmd_text, CONFIG)

    # Success
    print(f"\n{'='*60}")
    print(f"JOB {job_id[:8]} COMPLETED SUCCESSFULLY")
    print(f"{'='*60}\n")
    with JOBS_LOCK:
      JOBS[job_id]["status"] = "done"
      JOBS[job_id]["message"] = "Completed"
  except Exception as e:
    # Show error in terminal
    print(f"\n{'='*60}")
    print(f"JOB {job_id[:8]} FAILED")
    print(f"ERROR: {str(e)}")
    print(f"{'='*60}\n")
    import traceback
    traceback.print_exc()
    
    with JOBS_LOCK:
      JOBS[job_id]["status"] = "failed"
      JOBS[job_id]["message"] = str(e)
  finally:
    clear_injected_credentials()


@app.route('/')
def index():
  return render_template('index_modern.html')

@app.route('/classic')
def classic():
  return render_template('index.html')


@app.route('/command', methods=['POST'])
def command():
  data = request.get_json(force=True)
  # data should be a payload dict; minimal validation
  job_id = str(uuid.uuid4())
  with JOBS_LOCK:
    JOBS[job_id] = {"status": "queued", "message": ""}
  payload = data
  t = threading.Thread(target=_run_job, args=(job_id, payload), daemon=True)
  t.start()
  return jsonify({"job_id": job_id})


@app.route('/jobs')
def jobs():
    with JOBS_LOCK:
        return jsonify(JOBS)


@app.route('/status/<job_id>')
def status(job_id):
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job:
            return jsonify({"error": "not found"}), 404
        return jsonify(job)


@app.route('/policies')
def policies():
    """Get university policies"""
    try:
        policies_data = fetch_policies()
        return jsonify(policies_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/policies/summary')
def policies_summary():
    """Get formatted policy summary"""
    try:
        summary = get_policy_summary()
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/policies/search')
def policies_search():
    """Search policies by keyword"""
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({"error": "No search keyword provided"}), 400
    
    try:
        results = search_policy(keyword)
        return jsonify({"keyword": keyword, "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/policies/specific')
def policies_specific():
    """Get specific important policies"""
    try:
        policies_data = get_specific_policies()
        return jsonify(policies_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test')
def test():
    return jsonify({"message": "Test endpoint works!", "timestamp": time.time()})

print("Registered /test endpoint")

@app.route('/application/data')
def get_application_data():
    """Get application data from YAML file"""
    try:
        with open("data/application.yaml", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

print("Registered /application/data endpoint")


@app.route('/validate/application', methods=['POST'])
def validate_application():
    """Validate application data against policies"""
    try:
        data = request.get_json(force=True)
        validation_result = validate_before_apply(data)
        return jsonify(validation_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/validate/field', methods=['POST'])
def validate_field():
    """Validate a specific field against policies"""
    try:
        data = request.get_json(force=True)
        field_name = data.get('field_name', '')
        field_value = data.get('field_value', '')
        
        if not field_name or not field_value:
            return jsonify({"error": "field_name and field_value required"}), 400
        
        compliance = check_policy_compliance(field_name, field_value)
        return jsonify(compliance)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



@app.route('/download/<job_id>')
def download_file(job_id):
    """Download a generated document"""
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        
        filepath = job.get("filepath")
        if not filepath or not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404
        
        return send_file(filepath, as_attachment=True, download_name=job.get("filename"))
