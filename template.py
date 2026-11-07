
from pathlib import Path

# Project root folder (where template.py is located)
BASE_DIR = Path(__file__).resolve().parent

# All folders and files to create
project_files = [
    "app.py",
    "backend.py",
    "tools/__init__.py",
    "tools/age_tool.py",
    "tools/bmi_tool.py",
    "tools/date_difference_tool.py",
    "tools/calculator_tool.py",
    "templates/index.html",
    ".env.example",
    "requirements.txt",
]

# Create folders and files
for file_name in project_files:
    file_path = BASE_DIR / file_name

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)

    print(f"Created: {file_name}")

print("Project structure(all folders and files) created successfully!")
