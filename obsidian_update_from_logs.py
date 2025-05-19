import os
from datetime import datetime

SUMMARY_FILE = "latest_summary.txt"
VAULT_DIR = "C:/Users/Steve/Documents/ObsidianVaults/MainVault/System Summaries"

def main():
    if not os.path.exists(SUMMARY_FILE):
        print(f"❌ No summary found to export.")
        return

    os.makedirs(VAULT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M")
    md_file = os.path.join(VAULT_DIR, f"System Summary - {timestamp}.md")

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# 🧠 System Summary - {timestamp}\n\n{content}")

    print("✅ Summary saved to Obsidian vault:", md_file)

if __name__ == "__main__":
    main()
