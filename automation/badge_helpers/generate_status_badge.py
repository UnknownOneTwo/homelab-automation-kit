import os
from datetime import datetime

def generate_svg(status, timestamp, output_file):
    color = "brightgreen" if status.lower() == "success" else "red"
    label = f"System Sync: {status.capitalize()} – {timestamp}"
    footer = f"Last run: {timestamp}"

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="500" height="40">
  <style>
    .title {{ font: bold 12px Verdana, sans-serif; fill: #fff; }}
    .footer {{ font: 10px Verdana, sans-serif; fill: #eee; }}
  </style>
  <rect width="500" height="20" fill="{color}" />
  <text x="10" y="14" class="title">{label}</text>
  <text x="10" y="35" class="footer">{footer}</text>
</svg>"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg_content)

def main():
    status = os.getenv("SYNC_STATUS", "unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    output_path = os.path.join("badges", "system_sync_status.svg")
    generate_svg(status, timestamp, output_path)
    print(f"✅ Badge generated: {output_path}")

if __name__ == "__main__":
    main()
