import os
import re

def sanitize_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r"192\.168\.\d+\.\d+", "192.168.x.x", content)
    content = re.sub(r"glsa_[\w\d]+", "glsa_your_token_here", content)
    content = re.sub(r"root@[\w\-]+", "root@host", content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def walk_and_sanitize(root):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith((".py", ".sh", ".md", ".txt")):
                sanitize_file(os.path.join(dirpath, filename))

if __name__ == "__main__":
    walk_and_sanitize("./")
    print("✅ Files sanitized for public visibility.")
