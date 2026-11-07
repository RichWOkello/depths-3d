"""Rebuild Depths 3D v6.0.0 from editable sources."""
from pathlib import Path
import runpy
import os
os.chdir(Path(__file__).resolve().parent)
runpy.run_path(str(Path(__file__).resolve().parent / 'build_bestiary.py'),run_name='__main__')
