from requests_html import HTMLSession
import pandas as pd
import time
import instaloader

session = HTMLSession()

insta_links = []
usernames = []
fcount = []


# reading data from sorted dataframe our jupyter notebook
df = pd.read_excel('sorted_scraped_data.xlsx', na_values='None')
links = df['url'].to_list()
links = [str(x) for x in links]
links = [x for x in links if x != 'nan']


def get_insta_username(links):
    def link_ext(urls):
        for link in urls:
            if 'instagram' in link:
                return(link)

    for link in links[1:30]:
        try:
            print(link)
            r = session.get(link)
            x = r.html.absolute_links
            urls = list(x)
            instaurl = link_ext(urls)
            print(instaurl)
            insta_links.append(instaurl)
            time.sleep(1)
        except:
            insta_links.append(None)
    print(insta_links)


def insta_usernames(insta_links):
    prefix = 'https://www.instagram.com/'
    for link in insta_links:
        if link != None:
            username = link[len(prefix):].rstrip('/')
            usernames.append(username)
        else:
            usernames.append(None)


def follower_count():
    L = instaloader.Instaloader()
    # Use a throwaway Id as it might get blocked,Dont use our main instagram account
    USER = 'your username'
    PASSWORD = 'your password'
    L.login(USER, PASSWORD)
    for name in usernames:
        time.sleep(1)
        if name != None:
            profile = instaloader.Profile.from_username(L.context, name)
            f = profile.followers
            fcount.append(f)
        else:
            fcount.append('None')


def save_res():
    df = pd.DataFrame({
        'insta_links': insta_links,
        'username': usernames,
        'FollowCount': fcount
    })
    df.to_excel('sorted_insta_data.xlsx', index=False)  # Saving to excel sheet


get_insta_username(links)
insta_usernames(insta_links)
follower_count()
save_res()
