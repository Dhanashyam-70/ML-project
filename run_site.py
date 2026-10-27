"""Launch the local HTML site using the project-local dependencies."""

import os
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir / "vendor"))
os.chdir(project_dir)
from local_web import main

main()
