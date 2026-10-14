# 🔐 PyPass
 
A small command-line tool to **generate secure passwords** and **check password strength**, with styled terminal output.

## Features
 
- Cryptographically secure passwords using Python's `secrets` module
- Custom length, with optional symbols
- Strength meter (Weak / Okay / Strong) with a visual bar
- Copies the generated password to your clipboard automatically
- Check your own password's strength with hidden input (never stored in shell history)
- Colorful terminal UI built with [Rich](https://github.com/Textualize/rich)
## Requirements
 
- Python 3.10+
## Installation
 
```bash
git clone https://github.com/<your-username>/pypass-project.git
cd pypass-project
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
 
## Usage
 
Generate a 16-character password (default):
 
```bash
python -m pypass
```
 
Generate a 24-character password with symbols:
 
```bash
python -m pypass --length 24 --symbols
```
 
Generate without copying to the clipboard:
 
```bash
python -m pypass -l 32 -s --no-copy
```
 
Check the strength of your own password:
 
```bash
python -m pypass --check
```
 
See all options:
 
```bash
python -m pypass --help
```
 
### Options
 
| Option | Short | Description |
|---|---|---|
| `--length N` | `-l` | Password length (default: 16, minimum: 8) |
| `--symbols` | `-s` | Include symbols like `!@#$` |
| `--no-copy` | | Don't copy the password to the clipboard |
| `--check` | `-c` | Check the strength of a password you enter |
 
## How strength is scored
 
Each password gets one point for each of the following, for a score out of 6:
 
- At least 12 characters
- At least 16 characters
- Contains a lowercase letter
- Contains an uppercase letter
- Contains a digit
- Contains a symbol
A score of 0–2 is **Weak**, 3–4 is **Okay**, and 5–6 is **Strong**.
 
## Project structure
 
```
pypass-project/
├── pypass/
│   ├── __init__.py
│   ├── __main__.py     # CLI entry point and terminal UI
│   ├── generator.py    # password generation
│   └── strength.py     # strength scoring
├── requirements.txt
└── README.md
```
 
## Built with
 
- [Rich](https://github.com/Textualize/rich): terminal styling
- [pyperclip](https://github.com/asweigart/pyperclip): clipboard support
- `argparse`, `secrets`, `getpass` from the Python standard library
## License
 
MIT