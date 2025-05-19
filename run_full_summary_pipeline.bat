@echo off
SET MODE=%1
IF "%MODE%"=="" SET MODE=prod

echo Using mode: %MODE%
copy /Y .env.%MODE% .env > nul

echo 🧠 Summarizing system logs with Ollama...
python summarize_system_logs_with_ollama.py

echo 📚 Updating Obsidian vault...
python obsidian_update_from_logs.py

echo 📊 Pushing system summary to Grafana...
python grafana_summary_updater.py

echo ✅ All steps completed.
pause
