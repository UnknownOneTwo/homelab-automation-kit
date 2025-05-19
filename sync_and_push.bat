@echo off
cd /d %~dp0
echo Running sanitizer...
python sanitize_for_public.py

echo Committing changes...
git add .
git commit -m "🤖 Manual sync and sanitize"
git push
echo Done.
pause
