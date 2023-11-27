import sys
import os

# Append the repo path to the PYTHONPATH so that the display import works
repo_path = os.path.dirname(__file__)
sys.path.append(repo_path)

print(f"Repo directory: {repo_path}.")

from config import LIBDIR, PICDIR

libdir = os.path.join(repo_path, LIBDIR)
picdir = os.path.join(repo_path, PICDIR)

sys.path.append(libdir)
sys.path.append(picdir)