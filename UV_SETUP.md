# 🚀 Job Finder Agent - UV Setup Guide

**`uv` is a blazingly fast Python package manager written in Rust.** It's 10-100x faster than pip!

---

## ⚡ Quick Setup with UV (2 minutes)

### 1️⃣ Install UV (if not already installed)
```bash
# On macOS with Homebrew
brew install uv

# Or with pip
pip install uv

# Or with pipx
pipx install uv
```

Verify installation:
```bash
uv --version
```

### 2️⃣ Create Virtual Environment
```bash
cd /Users/sankar/projects/job_finder
uv venv
```

Activate it:
```bash
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
uv sync
```

That's it! ⚡ (Much faster than `pip install -r requirements.txt`)

---

## 📦 What `uv` Does

### Install from `pyproject.toml`
```bash
uv sync
```
- Reads `pyproject.toml` (modern Python packaging)
- Creates `uv.lock` (deterministic, reproducible)
- Installs all dependencies
- **10-100x faster than pip**

### Install from `requirements.txt`
```bash
uv pip install -r requirements.txt
```
- Alternative if you prefer requirements.txt
- Still faster than pip

### Add a New Dependency
```bash
uv add pydantic
```

### Remove a Dependency
```bash
uv remove pydantic
```

### Update Dependencies
```bash
uv sync --upgrade
```

---

## 🔧 Project Structure with UV

```
job_finder/
├── pyproject.toml          # Modern Python packaging (NEW)
├── uv.lock                 # Lockfile (auto-generated)
├── requirements.txt        # For pip compatibility
├── .venv/                  # Virtual environment
├── impl.py
├── pdf_parser.py
├── matcher.py
├── enricher.py
├── formatter.py
├── config.py
└── scrapers/
    ├── apify_client.py
    ├── linkedin.py
    ├── indeed.py
    └── hackernews.py
```

---

## 📋 Quick Reference

| Task | UV Command | Pip Command |
|------|-----------|-----------|
| Create venv | `uv venv` | `python3 -m venv venv` |
| Activate | `source .venv/bin/activate` | `source venv/bin/activate` |
| Install deps | `uv sync` | `pip install -r requirements.txt` |
| Add package | `uv add package` | `pip install package` |
| Remove package | `uv remove package` | `pip uninstall package` |
| List packages | `uv pip list` | `pip list` |
| Update all | `uv sync --upgrade` | `pip install --upgrade -r requirements.txt` |

---

## 🚀 Full Setup from Scratch

```bash
# 1. Navigate to project
cd /Users/sankar/projects/job_finder

# 2. Create virtual environment with UV
uv venv

# 3. Activate it
source .venv/bin/activate

# 4. Install all dependencies
uv sync

# 5. Verify setup
python check.py

# 6. Run the application
python impl.py --resume resume.pdf
```

---

## 🔄 Working with UV

### Daily Development

```bash
# Start work
source .venv/bin/activate

# Install/update dependencies
uv sync

# Run app
python impl.py --resume resume.pdf
```

### Adding Dependencies

```bash
# Add a new package
uv add requests

# Add dev dependency
uv add --group dev pytest

# Sync to install
uv sync
```

### Sharing with Others

1. Commit both `pyproject.toml` and `uv.lock`
2. Others run: `uv sync` (guaranteed identical environment)

---

## ✨ Why UV is Better

| Feature | UV | Pip |
|---------|-----|-----|
| **Speed** | 10-100x faster ⚡ | Baseline |
| **Dependency Resolution** | Instant ⚡ | Slow |
| **Lock File** | `uv.lock` (deterministic) | ❌ None |
| **Installation** | Parallel ⚡ | Sequential |
| **Resolver** | Robust | Sometimes fails |
| **Memory Usage** | Low ⚡ | High |

**Example:**
```bash
# Pip (slow)
$ pip install -r requirements.txt
Collecting pdfplumber...
Collecting apify-client...
[... 30+ seconds ...]

# UV (fast)
$ uv sync
Resolved 42 packages in 0.24ms
Installed 8 packages in 0.45s
```

---

## 🔒 Security

With `uv.lock`, your entire dependency tree is locked and reproducible:

```bash
# Anyone can recreate exact same environment
uv sync

# No version surprises, no security vulnerabilities from version drift
```

---

## 📚 UV Documentation

- Official Docs: https://docs.astral.sh/uv/
- GitHub: https://github.com/astral-sh/uv
- Quick Start: https://docs.astral.sh/uv/getting-started/

---

## ✅ Verification

After setup, run:

```bash
# Check Python version
python --version

# Check UV environment
which python

# Verify dependencies
uv pip list

# Run verification script
python check.py

# Run the app
python impl.py --resume test_resume.pdf
```

All commands should work without errors! ✅

---

## 🎯 Next Steps

1. **Install UV:** `brew install uv` (or your system's package manager)
2. **Create venv:** `uv venv`
3. **Activate:** `source .venv/bin/activate`
4. **Sync:** `uv sync`
5. **Test:** `python check.py`
6. **Run:** `python impl.py --resume your_resume.pdf`

---

**You're all set!** 🚀 Your Job Finder Agent is ready with UV!
