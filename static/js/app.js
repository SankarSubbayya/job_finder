/**
 * Job Finder Agent - Frontend Application
 */

let selectedFile = null;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const searchBtn = document.getElementById('searchBtn');
const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const loadingText = document.getElementById('loadingText');
const progressFill = document.getElementById('progressFill');

// File upload handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

/**
 * Handle file selection
 */
function handleFileSelect(file) {
    if (!file.name.endsWith('.pdf')) {
        showError('Please select a PDF file');
        return;
    }

    selectedFile = file;
    fileName.textContent = `✓ ${file.name} (${formatFileSize(file.size)})`;
    fileName.classList.add('show');
    searchBtn.disabled = false;
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Start job search
 */
async function startSearch() {
    if (!selectedFile) {
        showError('Please select a resume file');
        return;
    }

    showLoading();

    const formData = new FormData();
    formData.append('resume', selectedFile);

    try {
        // Simulate progress
        simulateProgress();

        const response = await fetch('/api/search', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to search jobs');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        showError(error.message);
    }
}

/**
 * Simulate progress bar
 */
function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 90) progress = 90;

        progressFill.style.width = progress + '%';

        if (progress > 85) {
            clearInterval(interval);
        }
    }, 500);

    // Complete on timeout
    setTimeout(() => {
        progressFill.style.width = '100%';
        clearInterval(interval);
    }, 8000);
}

/**
 * Display results
 */
function displayResults(data) {
    progressFill.style.width = '100%';

    setTimeout(() => {
        loadingSection.style.display = 'none';
        resultsSection.style.display = 'block';

        // Display summary
        displaySummary(data);

        // Display jobs
        displayJobs(data.matched_jobs);

        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }, 500);
}

/**
 * Display summary card
 */
function displaySummary(data) {
    const resumeInfo = data.resume_info || {};
    const skills = (resumeInfo.skills || []).slice(0, 5).join(', ');
    const moreSkills = (resumeInfo.skills || []).length > 5
        ? ` +${resumeInfo.skills.length - 5} more`
        : '';

    const avgScore = data.matched_jobs.length > 0
        ? Math.round(
            data.matched_jobs.reduce((sum, job) => sum + (job.match_score || 0), 0) /
            data.matched_jobs.length * 100
          )
        : 0;

    const summaryHtml = `
        <h3>📋 Your Job Search Profile</h3>
        <div class="summary-info">
            <div class="info-item">
                <div class="info-label">Job Title</div>
                <div class="info-value">${resumeInfo.title || 'N/A'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Experience Level</div>
                <div class="info-value">${(resumeInfo.level || 'mid').charAt(0).toUpperCase() + (resumeInfo.level || 'mid').slice(1)}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Location</div>
                <div class="info-value">${resumeInfo.location || 'Remote'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Matches Found</div>
                <div class="info-value">${data.total_matches}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Average Match</div>
                <div class="info-value">${avgScore}%</div>
            </div>
            <div class="info-item">
                <div class="info-label">Key Skills</div>
                <div class="info-value" style="font-size: 0.9rem;">${skills}${moreSkills}</div>
            </div>
        </div>
    `;

    document.getElementById('summaryCard').innerHTML = summaryHtml;
}

/**
 * Display jobs list
 */
function displayJobs(jobs) {
    const jobsList = document.getElementById('jobsList');

    if (!jobs || jobs.length === 0) {
        jobsList.innerHTML = `
            <div style="padding: 2rem; text-align: center; color: var(--text-secondary);">
                No matching jobs found. Try adjusting your location or skills preferences.
            </div>
        `;
        return;
    }

    let html = '';
    jobs.forEach((job, index) => {
        const score = (job.match_score || 0) * 100;
        const scoreColor = score >= 80 ? '#10a37f' : score >= 60 ? '#f59e0b' : '#ef4444';

        html += `
            <div class="job-card">
                <div class="job-header">
                    <div>
                        <div class="job-title">${job.title || 'Position'}</div>
                        <div class="job-company">${job.company || 'Company'}</div>
                    </div>
                    <div class="job-score">
                        <div class="score-percentage" style="color: ${scoreColor};">${score.toFixed(0)}%</div>
                        <div class="score-bar">
                            <div class="score-fill" style="width: ${score}%; background-color: ${scoreColor};"></div>
                        </div>
                    </div>
                </div>

                <div class="job-meta">
                    <div class="meta-item">
                        📍 ${job.location || 'Unknown Location'}
                    </div>
                    <div class="meta-item">
                        🏢 ${job.source ? job.source.charAt(0).toUpperCase() + job.source.slice(1) : 'Unknown'}
                    </div>
                    ${job.salary ? `<div class="meta-item">💰 ${job.salary}</div>` : ''}
                </div>

                ${job.description ? `
                    <div class="job-description">
                        ${job.description.substring(0, 200)}${job.description.length > 200 ? '...' : ''}
                    </div>
                ` : ''}

                ${job.company_summary ? `
                    <div class="job-company-info">
                        <strong>About ${job.company}:</strong> ${job.company_summary.substring(0, 150)}...
                    </div>
                ` : ''}

                <div class="job-footer">
                    ${job.url ? `
                        <a href="${job.url}" target="_blank" rel="noopener noreferrer" class="btn btn-small btn-apply">
                            Apply Now →
                        </a>
                    ` : ''}
                </div>
            </div>
        `;
    });

    jobsList.innerHTML = html;
}

/**
 * Show loading state
 */
function showLoading() {
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    loadingSection.style.display = 'flex';
    progressFill.style.width = '10%';
}

/**
 * Show error
 */
function showError(message) {
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    errorSection.style.display = 'flex';

    document.getElementById('errorMessage').textContent = message;

    // Scroll to error
    setTimeout(() => {
        errorSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

/**
 * Reset search
 */
function resetSearch() {
    selectedFile = null;
    fileInput.value = '';
    fileName.classList.remove('show');
    fileName.textContent = '';
    searchBtn.disabled = true;

    uploadSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    loadingSection.style.display = 'none';

    setTimeout(() => {
        uploadSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

/**
 * Export results as JSON
 */
async function exportResults() {
    try {
        // Collect results data
        const jobs = Array.from(document.querySelectorAll('.job-card')).map(card => ({
            title: card.querySelector('.job-title').textContent,
            company: card.querySelector('.job-company').textContent,
            score: card.querySelector('.score-percentage').textContent
        }));

        // Create blob
        const blob = new Blob([JSON.stringify(jobs, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        // Download
        const a = document.createElement('a');
        a.href = url;
        a.download = 'job_matches.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

    } catch (error) {
        showError('Failed to export results: ' + error.message);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Job Finder Agent loaded');
});
