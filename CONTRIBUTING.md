# Contributing

Thanks for your interest in improving LogTracer! This guide helps you get set up and submit contributions smoothly.

## Quick start
- Python 3.10+ recommended
- No pip dependencies (see `requirements.txt`)
- Optional system tools: `fzf`, `man` (man-db), `tldr`, `curl`, `col`, `sed`

## Setup
1. Fork and clone the repo.
2. Create a virtual environment (optional but recommended):
   - python -m venv .venv
   - source .venv/bin/activate
3. Install Python requirements:
   - pip install -r requirements.txt

## Running
- Interactive mode: `python cmts.py`
- Direct mode: `python cmts.py <command>` (opens that command's man page)

## Coding style
- Follow PEP 8.
- Keep functions small and focused.
- Prefer clear, defensive error handling over silent failures.
- Update README or docs if behavior changes.

## Commit style
- Use concise, imperative subject lines: "Add …", "Fix …", "Refactor …"
- Reference issues when relevant: `Fixes #123`.

## Pull requests
- Describe the change and rationale.
- Include screenshots or terminal output for UX changes.
- Ensure no stray debug prints remain unless gated behind a flag.

## Reporting issues
- Include OS, Python version, and steps to reproduce.
- Paste any error output and describe what you expected to happen.
