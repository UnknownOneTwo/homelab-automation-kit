import os
from datetime import datetime
import subprocess
import re

LOG_FILE = "system_updates.log"
SUMMARY_FILE = "latest_summary.txt"
ARCHIVE_FOLDER = "summaries"

def strip_ansi(text):
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:    # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |      # or [ for CSI, followed by a control sequence
            \[ [0-?]* [ -/]* [@-~]
        )
    ''', re.VERBOSE)
    return ansi_escape.sub('', text)

def summarize_with_ollama(text):
    prompt = f"""Summarize the following system log data and highlight key updates, errors, or noteworthy events:

{text}

Return the summary in clear markdown format."""
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )
    clean_output = strip_ansi(result.stdout.strip())
    return clean_output

def main():
    if not os.path.exists(LOG_FILE):
        print(f"❌ Log file not found: {LOG_FILE}")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = f.read()

    if not data.strip():
        print("⚠️ Log file is empty. Skipping summary.")
        return

    print("🧠 Sending logs to Ollama for summarization...")
    summary = summarize_with_ollama(data)

    os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    archive_file = os.path.join(ARCHIVE_FOLDER, f"System Summary - {timestamp}.md")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write(summary)

    with open(archive_file, "w", encoding="utf-8") as f:
        f.write(summary)

    rotated_log = f"system_updates_{timestamp}.log"
    os.rename(LOG_FILE, rotated_log)

    print(f"✅ Summary written to {SUMMARY_FILE} and archived.")
    print(f"🧹 Log file rotated to {rotated_log}")

if __name__ == "__main__":
    main()
