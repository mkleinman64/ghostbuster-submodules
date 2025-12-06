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

Large Git repositories often collect *ghost submodules*: entries in `.gitmodules` or `.submodules` that nobody uses anymore, were left behind after a migration, went obsolete after a code upgrade or refer to directories that no longer exist.

These “submodule ghosts” slow down your workflow, increase cognitive load, confuse new developers, and clutter your build process.

They also increase your repository’s attack surface.  
Even unused submodules are still *declared dependencies* inside your Git metadata.

This means they can:

- introduce unnoticed supply-chain risk  
- reference outdated or vulnerable code  
- trigger dependency-confusion scenarios  
- mislead security scanners  
- create false trust in code that is no longer maintained  

In short:  
**a ghost submodule is not just technical debt — it’s a potential security liability.**

`ghostbuster-submodules.py` scans your repository and tells you:

- Which submodules are actually referenced in your repo  
- Which submodules are **unused** (ghosts)  
- Which files reference which submodules  
- Highlights unused submodules in red 
- Optional != 0 exit_code for use in CI/CD pipelines or any other script you want to use ( --fail-on-ghosts ) 
- Helps you clean up safely

It works by parsing `.gitmodules` (or `.submodules`) and checking for textual references to each submodule path anywhere in your project.

And you can configure which files are not to be processed. E.g. parsing a README.md file inside your project might contain a reference to a specific submodule which would cause a false positive. 

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
- --fail-on-ghosts for != 0 exit_code

---

## Installation

Clone the repo and run the script directly:

<pre>
git clone https://github.com/mkleinman64/ghostbuster-submodules.git
cd ghostbuster-submodules
python3 ghostbuster-submodules.py <directory> [--fail-on-ghosts]
</pre>

Or create an alias for easier access and use!

<pre>
alias ghostbuster="python3 /path/to/ghostbuster-submodules.py"
</pre>

Or just make it an executable.

<pre>
chmod +x ghostbuster-submodules.py
</pre>

## Basic scan
<pre>
python3 ghostbuster-submodules.py [path-to-gitrepo]
</pre>

## --fail-on-ghosts 
<pre>
python3 ghostbuster-submodules.py [path-to-gitrepo] --fail-on-ghosts
</pre>

When this flag is enabled, the scanner will exit with exit code 1 if any ghost submodules are detected.

This makes it ideal for:
- CI/CD pipelines
- pre-commit hooks
- quality gates
- automated cleanup workflows

### Example (bash)
<pre>
ghostbuster-submodules.py [some_dir] --fail-on-ghosts
if [ $? -ne 0 ]; then
    echo "Ghost submodules detected!"
    exit 1
fi
</pre>

Use this flag inside your CI/CD pipeline to prevent dead submodules from silently accumulating in your repository.

## Example output
<pre>
python3 ghostbuster-submodules.py ~/temp_mk/scannertest/ --fail-on-ghosts
Ghostbuster-submodules: 1.1.0
-----------------------------------------
Parameters :
--fail-on-ghosts: True
-----------------------------------------
Scanning directory: /home/repository
.Valid submodules file found: /home/repository/.submodules

 submodules:
  - Shared/Schema_SomeProject
  - Shared/AndAnotherModule

References found:

Submodule path: Shared/Schema_SomeProject (no references found!)    <-- GHOST 👻

Submodule path: Shared/AndAnotherModule
  -> ProxyServices/test.proxy

Ghosts detected → exiting with code 1 as requested (--fail-on-ghosts).

</pre>

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
<pre>
(  •_•) 
<(    )╯  "No more ghosts."
 /    \
</pre>
---

If your Git repo is haunted... You know exactly who to call.

Brain 2025!

