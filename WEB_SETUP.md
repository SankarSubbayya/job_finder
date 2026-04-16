# 🌐 Job Finder Agent - Web UI Guide

A beautiful, Claude-style web interface for the Job Finder Agent!

---

## ⚡ Quick Start (2 minutes)

### 1. Install Dependencies
```bash
cd /Users/sankar/projects/job_finder
source .venv/bin/activate  # or: uv venv && source .venv/bin/activate
uv sync
```

### 2. Run the Web Server
```bash
python app.py
```

### 3. Open in Browser
Visit: **http://localhost:5000**

That's it! 🎉

---

## 🎨 Features

### Upload Resume
- Clean, modern UI similar to Claude
- Drag & drop support
- PDF file validation
- File size display

### Real-time Processing
- Live progress bar
- Status updates during job search
- Animated loading spinner

### Beautiful Results
- Summary card with profile info
- Job cards with match scores
- Color-coded match percentages
- Direct apply links
- Company information

### Export Results
- Download as JSON
- Structured data format
- Easy to process further

---

## 🏗️ Project Structure

```
job_finder/
├── app.py                      # Flask web server (NEW)
├── templates/
│   └── index.html              # Main HTML page (NEW)
├── static/
│   ├── css/
│   │   └── style.css           # Claude-style CSS (NEW)
│   └── js/
│       └── app.js              # Frontend JavaScript (NEW)
├── uploads/                    # Temporary resume storage
├── requirements.txt            # Updated with Flask
└── [other files...]
```

---

## 📋 Setup Steps

### Step 1: Create Virtual Environment (if not done)
```bash
uv venv
source .venv/bin/activate
```

### Step 2: Update Dependencies
```bash
uv sync
```

This will install:
- ✅ pdfplumber (PDF parsing)
- ✅ apify-client (Job scraping)
- ✅ requests (HTTP)
- ✅ python-dotenv (Config)
- ✅ **flask** (Web server)
- ✅ **werkzeug** (Flask utilities)

### Step 3: Verify Setup
```bash
python check.py
```

Should show all ✓ checks passed.

### Step 4: Run Web Server
```bash
python app.py
```

Output should show:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://localhost:5000
 * Press CTRL+C to quit
```

### Step 5: Open Browser
Click or visit: **http://localhost:5000**

---

## 🚀 Using the Web UI

### 1. Upload Resume
- Click "Choose File" or drag-drop a PDF
- Supported: PDF files only
- Max size: 16MB

### 2. Search Jobs
- Click "Search Jobs" button
- Watch progress bar
- Takes 45-75 seconds

### 3. View Results
- Summary card shows your profile
- Job cards display matches
- Color-coded match scores:
  - 🟢 Green (80%+): Excellent match
  - 🟡 Yellow (60-79%): Good match
  - 🔴 Red (<60%): Fair match

### 4. Apply
- Click "Apply Now" on any job
- Opens job link in new tab

### 5. Export
- Click "Export JSON" to download results
- Saves as `job_matches.json`

---

## 🎯 Features Details

### Upload Section
```
📄 Upload Your Resume
├── Drag & drop support
├── File picker button
└── File validation (PDF only)
```

### Loading Section
```
⏳ Searching for jobs...
├── Spinner animation
├── Status text updates
└── Progress bar
```

### Results Section
```
📋 Summary Card
├── Job title
├── Experience level
├── Location
├── Total matches
├── Average match score
└── Key skills

🎯 Job Cards
├── Job title & company
├── Match percentage with color bar
├── Location & source (LinkedIn/Indeed/HackerNews)
├── Salary (if available)
├── Job description (truncated)
├── Company info (from You.com)
└── Apply link
```

### Error Section
```
⚠️ Error Display
├── Error message
└── Retry button
```

---

## 🔧 Configuration

### Flask Settings
Edit `app.py` to customize:

```python
# Change port
app.run(debug=True, port=8080)

# Disable debug mode for production
app.run(debug=False)

# Set host for network access
app.run(host='0.0.0.0', port=5000)
```

### File Upload Limits
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

---

## 🐛 Troubleshooting

### "Port 5000 is already in use"
```bash
# Use a different port
# Edit app.py, change: app.run(debug=True, port=5000)
# To: app.run(debug=True, port=8080)
```

### "Module not found: flask"
```bash
# Make sure dependencies are installed
uv sync

# Or manually:
pip install flask werkzeug
```

### "Connection refused at localhost:5000"
```bash
# Make sure server is running
# Check terminal where you ran: python app.py

# Server should show:
# * Running on http://localhost:5000
```

### Resume upload fails
- Make sure PDF is readable (not scanned image)
- Check file size is < 16MB
- Try with a different PDF

### Jobs not found / low matches
- Check resume has clear job title
- Add more technical skills
- Try less specific job titles

---

## 📊 API Endpoints

### POST /api/search
Upload resume and search for jobs

**Request:**
```bash
curl -X POST -F "resume=@resume.pdf" http://localhost:5000/api/search
```

**Response:**
```json
{
  "success": true,
  "summary": "...",
  "results": "...",
  "total_matches": 18,
  "matched_jobs": [...],
  "resume_info": {...}
}
```

### POST /api/export
Export results as JSON

### GET /api/health
Health check endpoint

---

## 🌍 Access from Other Devices

### Local Network Access
```bash
# Get your IP address
ifconfig | grep inet

# Run Flask on all interfaces
# Edit app.py:
app.run(host='0.0.0.0', port=5000)

# Then access from other device:
# http://YOUR_IP:5000
```

---

## 📱 Responsive Design

The UI is fully responsive:
- ✅ Desktop (wide screens)
- ✅ Tablet (medium screens)
- ✅ Mobile (narrow screens)

---

## 🔒 Security Notes

### Production Deployment
For production, use:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### File Upload Security
- ✅ File validation (PDF only)
- ✅ Secure filename handling
- ✅ Files deleted after processing
- ✅ Max file size limit

---

## 🎨 UI Customization

### Change Colors
Edit `static/css/style.css`:

```css
:root {
    --accent-color: #10a37f;      /* Main color */
    --accent-hover: #0d9970;      /* Hover color */
    --text-primary: #0d0d0d;      /* Text color */
    /* ... more colors */
}
```

### Change Branding
Edit `templates/index.html`:

```html
<div class="logo">
    <span class="logo-icon">🎯</span>  <!-- Change icon -->
    <h1>Job Finder</h1>              <!-- Change title -->
</div>
```

---

## 📈 Performance

| Metric | Time |
|--------|------|
| Page load | < 500ms |
| Resume upload | < 1 second |
| Job search | 45-75 seconds |
| Results render | < 1 second |
| JSON export | < 500ms |

---

## 🧪 Testing the Web UI

### Manual Test
```bash
# 1. Start server
python app.py

# 2. Open browser
open http://localhost:5000

# 3. Upload a test resume
# 4. Check results display

# 5. Export JSON and verify
```

### API Test
```bash
# Test with curl
curl -X POST -F "resume=@test_resume.pdf" http://localhost:5000/api/search

# Pretty print response
curl -X POST -F "resume=@test_resume.pdf" http://localhost:5000/api/search | python -m json.tool
```

---

## 🚀 Deployment

### Heroku Deployment
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create requirements.txt (already done)
# Commit and push to Heroku
git push heroku main
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

---

## 📚 Next Steps

1. **Run the server:** `python app.py`
2. **Open browser:** `http://localhost:5000`
3. **Upload resume:** Use the UI
4. **View results:** Beautiful job matches!
5. **Export:** Download as JSON

---

## 📞 Support

- **Flask Docs:** https://flask.palletsprojects.com/
- **Bootstrap Docs:** https://getbootstrap.com/
- **API Examples:** See `app.py` for endpoint details

---

**Enjoy finding your perfect job with style!** 🎉

Built with ❤️ Claude-style UI
