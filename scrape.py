import instaloader

from datetime import datetime
from itertools import dropwhile, takewhile

L = instaloader.Instaloader(download_pictures=False, download_videos=False,
                            download_video_thumbnails=False, download_comments=True, compress_json=False, save_metadata=False)
L.load_session_from_file(username="mwafa89k", filename="session-mwafa89k")
profile = "uinsgd.official"
posts = instaloader.Profile.from_username(
    L.context, profile).get_posts()

SINCE = datetime(2023, 5, 31)
UNTIL = datetime(2022, 9, 1)

for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
    L.download_post(post, "test")
