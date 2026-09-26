def redact_pii(text, pii_list):
    """
    Replace detected PII with safe placeholders.
    """

    redacted_text = text

    for item in pii_list:
        pii_type = item["type"]
        pii_value = item["value"]

        placeholder = f"[{pii_type}_REDACTED]"

        redacted_text = redacted_text.replace(
            pii_value,
            placeholder
        )

    return redacted_text