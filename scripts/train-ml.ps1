Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location ml
try {
  ..\backend\.venv\Scripts\python.exe training_scripts\train_all.py
}
finally {
  Pop-Location
}
