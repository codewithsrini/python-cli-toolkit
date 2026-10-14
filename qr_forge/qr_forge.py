import qrcode
import argparse
import getpass

def build_text(args):
  return args.value


def build_url(args):
  url = args.value
  if not url.startswith(("http://", "https://")):
      url = "https://" + url
  return url


def build_email(args):
  return f"mailto:{args.value}"


def build_phone(args):
  return f"tel:{args.value}"


def escape_wifi(value):
  """Wi-Fi QR format treats these characters as special, so escape them."""
  for ch in ["\\", ";", ",", ":", '"']:
    value = value.replace(ch, "\\" + ch)
  return value


def build_wifi(args):
  ssid = escape_wifi(args.ssid)
  if args.security == "nopass":
      return f"WIFI:T:nopass;S:{ssid};;"
  if not args.password:
      args.password = getpass.getpass("Wi-Fi password: ")
  return f"WIFI:T:{args.security};S:{ssid};P:{escape_wifi(args.password)};;"

def make_qr(data):
  qr = qrcode.QRCode(border=2)
  qr.add_data(data)
  qr.make(fit=True)
  return qr

def build_parser():
  parser = argparse.ArgumentParser(
      prog="qr_forge",
      description="Generate QR codes for text, URLs, emails, phones and Wi-Fi.",
  )

  # options shared by every subcommand
  common = argparse.ArgumentParser(add_help=False)
  common.add_argument("-o", "--output", help="also save as a PNG file")

  sub = parser.add_subparsers(dest="command", required=True)

  p = sub.add_parser("text", parents=[common], help="plain text, e.g. a name")
  p.add_argument("value")
  p.set_defaults(build=build_text)

  p = sub.add_parser("url", parents=[common], help="website address")
  p.add_argument("value")
  p.set_defaults(build=build_url)

  p = sub.add_parser("email", parents=[common], help="email address")
  p.add_argument("value")
  p.set_defaults(build=build_email)

  p = sub.add_parser("phone", parents=[common], help="phone number")
  p.add_argument("value")
  p.set_defaults(build=build_phone)

  p = sub.add_parser("wifi", parents=[common], help="Wi-Fi network login")
  p.add_argument("--ssid", required=True, help="network name")
  p.add_argument("--password", help="omit to be prompted securely")
  p.add_argument("--security", choices=["WPA", "WEP", "nopass"], default="WPA")
  p.set_defaults(build=build_wifi)

  return parser

def main():
  args = build_parser().parse_args()
  data = args.build(args)
  qr = make_qr(data)

  print(f"Encoding: {data}\n")
  qr.print_ascii(invert=True)

  if args.output:
    qr.make_image().save(args.output)
    print(f"\nSaved {args.output}")

if __name__ == "__main__":
  main()

