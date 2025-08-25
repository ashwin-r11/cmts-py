#!/usr/bin/env python3
# --- Debug Snippet (add at the very top of cmd.py) ---
import os, sys

print("\n[DEBUG] Running:", os.path.abspath(__file__))
print("[DEBUG] Python version:", sys.version, "\n")

ascii_art = r"""
# ============================================================
#  ⚡ Commands-Directory ⚡ by ashwin-r11
#  A modern interactive command cheatsheet with fzf & man pages
# ============================================================

"""

print(ascii_art)
# -----------------------------------------------------
import os
import sys
import shutil
import subprocess
from pathlib import Path

# ------------- Helpers -------------
def which(cmd: str) -> str | None:
    return shutil.which(cmd)

def have(cmd: str) -> bool:
    return which(cmd) is not None

def get_all_commands() -> list[str]:
    """
    Enumerate commands available in the user's shell PATH, similar to `compgen -c`.
    Prefer bash's compgen (fast, deduped), else fall back to scanning $PATH.
    """
    # Try bash compgen (handles aliases/functions too if you source bashrc)
    if have("bash"):
        try:
            out = subprocess.check_output(
                ["bash", "-lc", "compgen -c | sort -u"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            cmds = [c.strip() for c in out.splitlines() if c.strip()]
            return sorted(set(cmds))
        except Exception:
            pass

    # Fallback: scan PATH
    cmds = set()
    for p in os.environ.get("PATH", "").split(os.pathsep):
        try:
            for name in os.listdir(p):
                full = os.path.join(p, name)
                if os.path.isfile(full) and os.access(full, os.X_OK):
                    cmds.add(name)
        except Exception:
            continue
    return sorted(cmds)

def open_man_full(command: str) -> int:
    """
    Open the full man page in a proper pager (best user experience).
    Returns man exit code; falls back to tldr / cheat.sh if missing.
    """
    env = os.environ.copy()
    # Force a nice pager if not set
    if "MANPAGER" not in env and "PAGER" not in env:
        env["MANPAGER"] = "less -R"
    try:
        return subprocess.call(["man", command], env=env)
    except FileNotFoundError:
        # No man installed (rare), fallback
        return 1

def print_tldr_or_cheat(command: str) -> int:
    """
    If man fails/missing, try TLDR. If TLDR missing, try cheat.sh.
    """
    if have("tldr"):
        try:
            return subprocess.call(["tldr", command])
        except Exception:
            pass
    # cheat.sh as last resort (no install needed)
    if have("curl"):
        try:
            return subprocess.call(["bash", "-lc", f"curl -s https://cheat.sh/{command}?T"])
        except Exception:
            pass
    print(f"\033[31mNo docs found for '{command}'.\033[0m")
    return 1

def man_preview_cmd() -> str:
    """
    Build an fzf --preview command that shows a clean man page snippet.
    - Use 'man -P cat' to dump without pager
    - 'col -bx' to strip backspaces/formatting
    - 'sed' to show first N lines
    """
    if have("man"):
        # Safe pipeline; fzf runs this per selection
        return "man -P cat {} 2>/dev/null | col -bx | sed -n '1,200p'"
    # As a fallback, try tldr/cheat.sh preview
    if have("tldr"):
        return "tldr {} 2>/dev/null | sed -n '1,200p'"
    if have("curl"):
        return "curl -s https://cheat.sh/{}?T | sed -n '1,200p'"
    # Nothing available
    return "echo 'No preview available'"

# ------------- Modes -------------
def interactive_fzf():
    """
    fzf-powered interactive picker with live man preview.
    Enter = open full man page for selection.
    """
    if not have("fzf"):
        return None  # signal to fallback

    cmds = get_all_commands()
    if not cmds:
        print("\033[31mNo commands found in PATH.\033[0m")
        return 1

    preview = man_preview_cmd()
    fzf_cmd = [
        "fzf",
        "--prompt", "cmd> ",
        "--border",
        "--height", "90%",
        "--layout=reverse",
        "--ansi",
        "--preview", preview,
        "--preview-window", "right,70%,wrap",
        "--bind", "ctrl-d:preview-half-page-down,ctrl-u:preview-half-page-up",
        "--color", "header:italic,fg+:bold",
        "--header", "Type to search • Enter to open full man page • Ctrl-U/D to scroll preview",
    ]

    try:
        sel = subprocess.check_output(fzf_cmd, input="\n".join(cmds), text=True)
        command = sel.strip()
        if not command:
            return 0
        # Open full man page
        rc = open_man_full(command)
        if rc != 0:
            print_tldr_or_cheat(command)
        return 0
    except subprocess.CalledProcessError:
        # user likely Escaped out
        return 0

def interactive_fallback():
    """
    Minimal built-in fuzzy finder if fzf is not installed.
    Keeps it simple: prompt user, filter list in a loop.
    """
    cmds = get_all_commands()
    if not cmds:
        print("\033[31mNo commands found in PATH.\033[0m")
        return 1

    print("\033[36mSimple fuzzy search (install fzf for better UI).\033[0m")
    query = ""
    while True:
        os.system("clear")
        
        print(f"\033[33mcmd> {query}\033[0m   (Enter to open man, ESC/Ctrl-C to quit)")
        # filter
        q = query.lower()
        matches = [c for c in cmds if q in c.lower()]
        for c in matches[:30]:
            print("  " + c)
        # read a line (simple, not per-keystroke)
        try:
            new = input("\nType to refine, or exact command to open man: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not new and matches:
            command = matches[0]
            rc = open_man_full(command)
            if rc != 0:
                print_tldr_or_cheat(command)
            return 0
        elif new in cmds:
            rc = open_man_full(new)
            if rc != 0:
                print_tldr_or_cheat(new)
            return 0
        else:
            query = new

def direct_mode(command: str):
    """
    Direct: cmd.py <command> -> open man for that command (with fallbacks).
    """
    rc = open_man_full(command)
    if rc != 0:
        print_tldr_or_cheat(command)
    return 0

# ------------- Entry -------------
def main():
    # No args -> interactive
    if len(sys.argv) == 1:
        rc = interactive_fzf()
        if rc is None:  # no fzf available
            return interactive_fallback()
        return rc
    # One arg -> open that man page
    if len(sys.argv) == 2:
        return direct_mode(sys.argv[1])

    # Multiple words -> treat as a single command token (e.g., 'git commit')
    # Try 'man git-commit' first; many man pages are namespaced that way.
    joined = "-".join(sys.argv[1:])
    rc = open_man_full(joined)
    if rc != 0:
        # fallback to the first token
        direct_mode(sys.argv[1])
    return 0

if __name__ == "__main__":
    sys.exit(main())
