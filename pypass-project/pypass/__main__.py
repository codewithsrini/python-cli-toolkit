
# python -m pypass
# python -m pypass --length 24 --symbols
# python -m pypass -l 32 -s --no-copy
# python -m pypass --length 4
# python -m pypass --help

import argparse
import pyperclip
from rich.console import Console
from rich.panel import Panel

from pypass.generator import generate_password
from pypass.strength import check_strength

console = Console()

def parse_args():
  parser = argparse.ArgumentParser(
    prog="PyPass",
    description="Generate secure passwords from your terminal."
  )

  parser.add_argument(
    "-l", "--length",
    type=int,
    default=16,
    help="Password length (defalt: 16)"
  )

  parser.add_argument(
    "-s", "--symbols",
    action="store_true",
    help="include symbols like !@#$",
  )

  parser.add_argument(
    "--no-copy",
    action="store_true",
    help="don't copy the password to the clipboard",
  )

  return parser.parse_args()

def main():

  args = parse_args()

  if args.length < 8:
    console.print("[bold red]✘ Length must be at least 8.[/bold red]")
    raise SystemExit(1)
  
  password = generate_password(args.length, args.symbols)

  score, label = check_strength(password)
  color = {"Weak": "red", "Okay": "yellow", "Strong": "green"}[label]
  bar = "█" * score + "░" * (6 - score)

  console.print(
    Panel(
      f"[bold green]{password}[/bold green]\n\n"
      f"Strength: [{color}]{bar} {label}[/{color}] ({score}/6)",
      title="🔐 [bold cyan]PyPass[/bold cyan]",
      subtitle=f"[dim]{args.length} chars · symbols {'on' if args.symbols else 'off'}[/dim]",
      border_style="cyan",
      expand=False,
      padding=(1, 4),
    )
  )

  if not args.no_copy:  
    pyperclip.copy(password)
    console.print("[yellow]✔ Copied to clipboard[/yellow]")

if __name__ == "__main__":
  main()
