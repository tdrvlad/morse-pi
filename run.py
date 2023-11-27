import sys
import os

# Append the repo path to the PYTHONPATH so that the display import works
repo_path = os.path.dirname(__file__)
sys.path.append(repo_path)

print(f"Repo directory: {repo_path}.")

from config import LIBDIR, PICDIR
sys.path.append(os.path.join(repo_path, LIBDIR))
sys.path.append(os.path.join(repo_path, PICDIR))

from morse import run

run()