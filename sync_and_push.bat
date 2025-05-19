@echo off
cd /d %~dp0

set /p NOTE=📝 Enter changelog note: 
echo Creating changelog entry...
echo ## [%DATE% %TIME%] - %NOTE% >> CHANGELOG.md

set /p TAG=🏷️ Enter version tag (leave blank to skip): 

echo Running sanitizer...
python sanitize_for_public.py

echo Staging and committing changes...
git add .
git commit -m "🤖 Manual sync: %NOTE%"
git push

if not "%TAG%"=="" (
    echo Creating Git tag: %TAG%
    git tag %TAG%
    git push origin %TAG%
)

echo Logging sync...
echo [%DATE% %TIME%] NOTE: %NOTE% >> sync_log.txt
if not "%TAG%"=="" (
    echo [%DATE% %TIME%] TAG: %TAG% >> sync_log.txt
)

echo 🔄 Updating Grafana changelog panel...
python grafana_sync_changelog.py

echo ✅ Sync complete.
pause
