# Just one line to find Chrome cookie DBs
Get-ChildItem "$env:LOCALAPPDATA\Google\Chrome\User Data\" -Recurse -Filter Cookies -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName | Tee-Object -FilePath "cookie_file_paths.txt"

# This will:
# - Search recursively for all Cookies DBs in Chrome profiles.
# - Output full paths on the console.
# - Save results in cookie_file_paths.txt.
