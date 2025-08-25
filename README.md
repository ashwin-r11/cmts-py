
---

# 📖 cmts.py – Interactive Linux Command Cheatsheet

`cmd.py` is your go-to interactive terminal assistant, designed to quickly show you the **most useful Linux commands** or let you explore any command’s **man page** in a clean, colorful way.

It works like a lightweight `fzf` for man pages — making it easier to refresh your memory without searching online every time.

---

## 🚀 Features

* ✅ Displays a **colorful cheatsheet** of the most commonly used Linux commands when run without arguments.
* ✅ Query any command (`ls`, `grep`, `ssh`, etc.) to view its **man page** directly inside your terminal.
* ✅ Shows a **preview snippet** first (first 3000 chars) for quick reference.
* ✅ Option to pipe into `less` for **scrollable full view**.
* ✅ Works entirely **offline** (relies on installed man pages).

---

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/cmd-cheatsheet.git
   cd cmd-cheatsheet
   ```

2. Make it executable:

   ```bash
   chmod +x cmd.py
   ```

3. (Optional) Add it to your `$PATH` for global usage:

   ```bash
   sudo cp cmd.py /usr/local/bin/cmd
   ```

---

## ⚡ Usage

### Show  cheatsheet:

```bash
python3 cmts.py
```

Output → list of most useful Linux commands with syntax & description.


---

## 🎨 Demo

![demo.gif](/images/demo.gif)


---

## 🔮 Future Enhancements

* [ ] Add syntax-highlighted examples for each command.
* [ ] Cache most viewed man pages for instant lookup.
* [ ] Option to show **cheatsheet + man page examples** side by side.

---

## 🛠 Requirements


* Python 3.x
* Linux/Unix environment with `man` installed

---

## 📄 License

MIT License © 2025 Ashwin

---
