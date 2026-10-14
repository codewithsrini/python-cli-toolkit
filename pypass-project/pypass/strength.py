import string

def check_strength(password: str) -> tuple[str, int]:
  score = 0

  if len(password) >= 12:
    score += 1
  if len(password) >= 16:
    score += 1
  if any(c.islower() for c in password):
    score += 1
  if any(c.isupper() for c in password):
    score += 1
  if any(c.isdigit() for c in password):
    score += 1
  if any(c in string.punctuation for c in password):
    score += 1

  if score <= 2:
    label = "Weak"
  elif score <= 4:
    label = "Okay"
  else:
    label = "Strong"

  return score, label  
