import os
import sys

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

IGNORE_FILENAMES = {
    ".gitignore",
    ".gitmodules",
    ".submodules",
    "README.md",
    "readme.md",
    "reader.md",
    "Reader.md",
}

IGNORE_DIRS = {
    ".git"
}

#
# Find .gitmodules or .submodules file and return it as a reference for further processing.
#
def find_gitmodules_file(base_dir: str) -> str:
    gm = os.path.join(base_dir, ".gitmodules")
    sm = os.path.join(base_dir, ".submodules")

    if os.path.exists(gm):
        return gm
    if os.path.exists(sm):
        return sm

    raise FileNotFoundError(
        f"No .gitmodules or .submodules was found in: {base_dir}"
    )

#
# Parse .gitmodules/.submodules file to extract submodule paths.
#
def parse_submodule_paths(gitmodules_path: str) -> list[str]:
    submodule_paths: list[str] = []

    with open(gitmodules_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Check all lines starting with "path"
            if line.startswith("path"):
                if "=" not in line:
                    continue

                _, value = line.split("=", 1)
                path = value.strip()

                # Important: remove surrounding quotes if present
                # Else this script will not finfd references correctly.
                # annoying :)
                if (path.startswith('"') and path.endswith('"')) or (
                    path.startswith("'") and path.endswith("'")
                ):
                    path = path[1:-1].strip()

                if path:
                    submodule_paths.append(path)

    return submodule_paths


#
# Check if a file should be ignored based on its name or directory.
#
def is_ignored_file(root: str, filename: str, base_dir: str) -> bool:
    if filename in IGNORE_FILENAMES:
        return True

    rel = os.path.relpath(os.path.join(root, filename), base_dir)
    parts = rel.split(os.sep)

    if any(part in IGNORE_DIRS for part in parts):
        return True

    return False


#
# Scan all files in base_dir for submodule paths in their content.
# Returns dict: {submodule_path: [files_that_mention_it]}.
#
def scan_repo_for_submodule_references(base_dir: str, submodule_paths: list[str]) -> dict[str, list[str]]:
    references: dict[str, list[str]] = {p: [] for p in submodule_paths}

    for root, dirs, files in os.walk(base_dir):
        # Remove ignored directories from traversal
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        # Remove ignored files from traversal
        for filename in files:
            if is_ignored_file(root, filename, base_dir):
                continue

            full_path = os.path.join(root, filename)

            # Read the file content
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except (OSError, UnicodeDecodeError):
                continue

            for sub_path in submodule_paths:
                if sub_path in content:
                    rel_file = os.path.relpath(full_path, base_dir)
                    references[sub_path].append(rel_file)

    return references


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scanner.py <directory>")
        sys.exit(1)

    base_dir = os.path.abspath(sys.argv[1])

    if not os.path.isdir(base_dir):
        print(f"Error: {base_dir} is not a valid directory.")
        sys.exit(1)

    print(f"Scanning directory: {base_dir}")

    gitmodules_path = find_gitmodules_file(base_dir)
    print(f".Valid submodules file found: {gitmodules_path}")

    submodule_paths = parse_submodule_paths(gitmodules_path)

    print("\n submodules:")
    for p in submodule_paths:
        print(f"  - {p}")

    refs = scan_repo_for_submodule_references(base_dir, submodule_paths)

    print("\nReferences found:\n")
    for sub_path, files in refs.items():
        if files:
            print(f"{GREEN}Submodule path: {sub_path}{RESET}")
            for f in files:
                print(f"  -> {f}")
        else:
            print(f"{RED}Submodule path: {sub_path} (no references found!){RESET}")
        print()


if __name__ == "__main__":
    main()
