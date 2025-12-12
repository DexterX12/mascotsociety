from .profile import Profile
from .database import Database
import os
from pathlib import Path

profile_handler = Profile()
database_handler = Database()
database_handler.load()
save_path = os.path.dirname(__file__)

for _file in os.listdir(save_path):
    if _file.startswith("profile"):
        profile_handler.load_from_file(os.path.join(save_path, Path(f"./{_file}")))


