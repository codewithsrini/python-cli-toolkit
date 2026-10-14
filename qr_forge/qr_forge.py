import qrcode
import argparse

def build_data(args):
  """Turn the chosen input into the string the QR will generate"""
  if args.url:
    url = args.url
    if not url.startswith("http://", "https://"):
      url = "https://" + url
      return url
  if args.email:
    return f"mailto:{args.email}"
  if args.phone:
    return f"tel:{args.phone}"
  return args.text

def make_qr(data):
  qr = qrcode.QRCode(border=2)
  qr.add_data(data)
  qr.make(fit=True)
  return qr

def main():
  parser = argparse.ArgumentParser(
    prog="qr_forge",
    description="Generate QR code from text, URL, email and phone numbers."
  )

  source = parser.add_mutually_exclusive_group(required=True)
  source.add_argument("-t", "--text", help="Plain text, e.g. a name")
  source.add_argument("-u", "--url", help="Website address")
  source.add_argument("-e", "--email", help="Email address")
  source.add_argument("-p", "--phone", help="Phone number")

  parser.add_argument("-o", "--output", help="also save as a PNG file")

  args = parser.parse_args()
  data = build_data(args=args)
  qr = make_qr(data)

  print(f"Encoding: {data}\n")
  qr.print_ascii(invert=True)

  if args.output:
    qr.make_image().save(args.output)
    print(f"\nSaved {args.output}")

if __name__ == "__main__":
  main()

