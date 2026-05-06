# Setup, Config & Remotes

> Part of the Git CLI Reference.

---

## Setup & Config

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor vim
git config --list
git config --global alias.st status
```

---

## Repository

```bash
# Init and clone
git init
git clone <url>
git clone <url> <directory>
git clone --depth 1 <url>       # Shallow clone

# Remotes
git remote -v
git remote add origin <url>
git remote remove <name>
git remote set-url origin <new_url>
```
