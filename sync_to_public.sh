#!/bin/bash
# sync_to_public.sh - Sync from private repo to public sanitized version

PRIVATE_REPO_DIR="../proxmox-homelab"
PUBLIC_REPO_DIR="../homelab-automation-kit"

rsync -av --delete \
  --exclude-from="$PRIVATE_REPO_DIR/.publicignore" \
  "$PRIVATE_REPO_DIR/" "$PUBLIC_REPO_DIR/"

cd "$PUBLIC_REPO_DIR"
git add .
git commit -m "🚀 Sync sanitized files from private repo"
git push
