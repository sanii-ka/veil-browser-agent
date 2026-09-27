
from pii_detector import detect_pii
from pii_handler import redact_pii

test_text = "My phone number is 9876543210"

pii = detect_pii(test_text)
safe_text = redact_pii(test_text, pii)

print("PII detected:", bool(pii))
print("Masking successful:", safe_text != test_text)