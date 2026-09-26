import re


def detect_pii(text):
    findings = []

    # Email detection
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    for email in emails:
        findings.append({
            "type": "EMAIL",
            "value": email
        })

    # Phone number detection
    phones = re.findall(
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
        text
    )

    for phone in phones:
        findings.append({
            "type": "PHONE",
            "value": phone
        })

    return findings