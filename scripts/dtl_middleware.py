#!/usr/bin/env python3
"""DTL middleware for OpenAI/Anthropic pipelines (e.g. signal parsers).
Wraps messages: codebook in system (cacheable), compress user payloads, log usage to CSV.
o200k counts are EXACT for OpenAI models. Usage:

    from dtl_middleware import dtl_messages, log_usage
    msgs = dtl_messages(raw_signal_text, codebook=MY_CODEBOOK, macro="P+R")
    resp = client.chat.completions.create(model=..., messages=msgs)
    log_usage(resp.usage, "dtl_usage.csv", baseline_prompt_tokens=55)
"""
import csv, os, datetime
from dtl_engine import compress_text, compress_json

def dtl_messages(payload: str, codebook: str, macro: str = "P+R", compress_payload=False):
    body = compress_text(payload) if compress_payload else payload
    return [
        {"role": "system", "content": codebook},   # stable prefix -> provider cache
        {"role": "user", "content": f"{macro}: {body}"},
    ]

def log_usage(usage, path="dtl_usage.csv", baseline_prompt_tokens=None):
    """usage = response.usage (openai) or response.usage (anthropic). Appends one row."""
    new = not os.path.exists(path)
    pt = getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", 0)
    ct = getattr(usage, "completion_tokens", None) or getattr(usage, "output_tokens", 0)
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(["ts","prompt_tokens","completion_tokens","baseline_prompt","saved_pct"])
        saved = round(100-100*pt/baseline_prompt_tokens,1) if baseline_prompt_tokens else ""
        w.writerow([datetime.datetime.now().isoformat(timespec="seconds"), pt, ct, baseline_prompt_tokens or "", saved])

if __name__ == "__main__":
    print(__doc__)
