# ghostbuster-submodules  
**Detect and eliminate dead Git submodules.**  
*Who you gonna call? → ghostbuster-submodules*

       .----------.
      /  GO AWAY   \
     |  SUBMODULE   |
      \    GHOST    /
       '----------'
           ( •_•)
          <)   )╯   ghostbuster-submodules.py
           /   \

---

## What is this?

Large Git repositories often collect *ghost submodules*: entries in `.gitmodules` or `.submodules` that nobody uses anymore, were left behind after a migration, or refer to directories that no longer exist.

These “submodule ghosts” slow down your workflow, increase cognitive load, confuse new developers, and clutter your build process.

`ghostbuster-submodules.py` scans your repository and tells you:

- Which submodules are actually referenced in your repo  
- Which submodules are **unused** (ghosts)  
- Which files reference which submodules  
- Highlights unused submodules in red  
- Helps you clean up safely

It works by parsing `.gitmodules` (or `.submodules`) and checking for textual references to each submodule path anywhere in your project.

---

## Features

- 🟢 Detect active submodules  
- 🔴 Detect dead/unused submodules  
- 📁 Scans any directory recursively  
- 🎨 Color output for easy readability  
- 🧪 Zero dependencies — pure Python  
- ⚡ Fast, simple, safe  
- 🧰 Works with `.gitmodules` **and** `.submodules`  
- 🛡 Ignores `.git/`, README, `.gitmodules`, `.submodules` by default  ( configurable :P )

---

## Installation

Clone the repo and run the script directly:

git clone https://github.com/mkleinman64/ghostbuster-submodules.git
cd ghostbuster-submodules
python3 ghostbuster-submodules.py <directory>

Or create an alias for easier access and use!

alias ghostbuster="python3 /path/to/ghostbuster-submodules.py"

Or just make it an executable.
chmod +x ghostbuster-submodules.py

## Basic scan
python3 ghostbuster-submodules.py [path-to-gitrepo]

## Example output

Scanning directory: /my/project

Found submodules:
  - Shared/Schema_SomeProject
  - Shared/AndAnotherModule

Submodule: Shared/Schema_SomeProject    <-- USED :)
  -> src/somefile.java
  -> config/something.xml

Submodule: Shared/AndAnotherModule (no references found!)   <-- GHOST 👻

Unused submodules are shown in red.

## Color Output

The script uses ANSI colors to highlight results:

🟢 Green → referenced submodules

🔴 Red → unused / ghost submodules


## How it works

This is a very simple and nifty Python project. Basically it does this:

1. Reads .gitmodules or .submodules
2. Extracts each path = ... entry
3. Normalizes values (strips optional quotes)
4. Recursively scans your repository while excluding specific files and directories ( configurable )
5. Searches for literal occurrences of each submodule path in file contents
6. Prints a report of:
    referenced submodules
    files where they appear
    unused (ghost) submodules

Zero ambiguity. Zero guesswork.

## Who you gonna call!

ghostbuster-submodules
Because haunted repos are nobody’s friend.

---

(  •_•) 
<(    )╯  "No more ghosts."
 /    \

---

If your Git repo is haunted...
You know exactly who to call.

