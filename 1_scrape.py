import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile
import csv

# class GetInstagramProfile():
#     def __init__(self) -> None:
#         self.L = instaloader.Instaloader(download_comments=True)

#     def download_users_profile_picture(self,username):
#         self.L.download_profile(username, profile_pic_only=True)

#     def get_posts(self, shortcode):
#         post = instaloader.Post.from_shortcode(self.L.context,shortcode).get_comments()
#         # post.PostComment
#         self.L.download_post(post, target='#')
#         # self.L.download_comments(post)

# if __name__=="__main__":
#     cls = GetInstagramProfile()
#     cls.get_posts('CCLdtg8JeZN')
#     #cls.download_users_profile_picture("best_gadgets_2030")
#     #cls.download_users_posts_with_periods("best_gadgets_2030")
#     #cls.download_hastag_posts("gadgets")
#     #cls.get_users_followers("best_gadgets_2030")
#     #cls.get_users_followings("best_gadgets_2030")
#     #cls.get_post_comments("laydline")
#     # cls.get_post_info_csv("coolest.gadget")

# post = instaloader.Post.from_shortcode(L.context, 'CCLdtg8JeZN')

# username = input('Username  : ')
# password = input('Password  : ')
# searchuser = input('Search Username : ')

# L = instaloader.Instaloader()

# L.load_session_from_file('gralam27', filename='session-gralam27')
# posts = instaloader.Profile.from_username(L.context, searchuser).get_posts()

# SINCE = datetime(2015, 7, 27)
# UNTIL = datetime(2023, 7, 27)

# for post in takewhile(lambda p:p.date>UNTIL, dropwhile(lambda p:p.date>SINCE, posts)):
#     L.download_post(post, searchuser)


def insta():
    username = 'gralam27'
    loader = instaloader.Instaloader(download_comments=True, download_pictures=False, download_videos=False,
                                     download_video_thumbnails=False, compress_json=False, save_metadata=False)
    loader.load_session_from_file(username)

    profile = instaloader.Profile.from_username(loader.context, 'mnaufalr27')

    # since = datetime(2021, 1, 1)
    # until = datetime(2021, 12, 31)
    # k = 0

    post_list = []
    try:
        for idx, save_post in enumerate(profile.get_posts()):
            # postdate = save_post.date

            # if postdate > until:
            #     continue
            # elif postdate <= since:
            #     k += 1
            #     if k == 50:
            #         break
            #     else:
            #         continue
            # else:
            post_list.append(save_post)
            loader.download_post(post_list[idx], 'uinsgd.official_comments')

    except IndexError:
        print('tidak tersimpan')

    # insta()
# insta()


loader = instaloader.Instaloader(download_comments=True, download_pictures=True, download_videos=False,
                                 download_video_thumbnails=False, compress_json=False, save_metadata=False)
loader.load_session_from_file('gralam27')

profile = instaloader.Profile.from_username(
    loader.context, 'uinsgd.official').get_posts()

since = datetime(2023, 1, 1)  # datetime(2022, 9, 1)
until = datetime(2023, 2, 28)

k = 0

# for post in takewhile(lambda p: p.date < until, dropwhile(lambda p: p.date < since, profile)):
#     print(post.date)

for post in profile:
    postdate = post.date

    if postdate > until:
        continue
    elif postdate <= since:
        k += 1
        if k == 50:
            break
        else:
            continue
    else:
        print(postdate)
        loader.download_post(post, 'uinsgd.official_comments_test')


# scrape -> text/document
# preprocessing -> case folding,
# pembobotan
# worldcloud
# TF-IDF
