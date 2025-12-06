from .profile import Profile
from .database import Database

profile_handler = Profile()
database_handler = Database()
profile_handler.load_from_file('./psociety_server/Coco.nofil')
database_handler.load()


