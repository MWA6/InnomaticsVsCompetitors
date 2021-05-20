from requests_html import HTMLSession
import pandas as pd
import re
import time

session = HTMLSession()

nxt_pages = []
clean_res = []
num_of_reviews = []
clean_names = []
list_review = []
web_links = []


# Cleaned Gooogle Search url (Cleaned using urlclean.com)
url = 'https://www.google.com/search?q=data+science+course+hyderabad&tbm=lcl'
base_url = 'https://www.google.com/'
r = session.get(url)
r.html.render(sleep=2)  # Renders javascript(Not necessary)

links = r.html.find('a.fl', clean=True)  # ,first=True)
base_url = 'https://www.google.com'
for link in links:
    x = link.xpath('//a/@href')
    final_url = base_url+x[0]
    nxt_pages.append(final_url)

print(f'Total no. of pages {len(nxt_pages)+1}')


def clean_res_block(r):
    res_block = r.html.find('div.cXedhc', clean=True)
    for i in range(len(res_block)):
        y = res_block[i].full_text
        y = y.replace("\n", " ")
        clean_res.append(y)


def total_reviews():
    for text in clean_res:
        ts = re.findall(r'\(([^\)]+)\)', text)
        try:
            num_of_reviews.append(ts[0])
        except:
            num_of_reviews.append('None')
    clean_res.clear()
    #print('scraping reviews...')


def cleaned_names(r):
    names_res = r.html.find('div.dbg0pd', clean=True)
    for i in range(len(names_res)):
        y = names_res[i].text
        y = y.replace("\n", " ")
        clean_names.append(y)
    #print('Extracing Names...')


def web_links_reviews(r):
    w = r.html.find('div.uMdZh.tIxNaf.mnr-c')
    for x in range(len(w)):
        if w[x].find('span.BTtC6e') != []:
            y = w[x].find('span.BTtC6e')
            list_review.append(y[0].text)
        else:
            list_review.append('None')
    #print('scraping no. of stars...')

    for x in range(len(w)):
        if w[x].find('a.T8HSqd.yYlJEf.L48Cpd') != []:
            rlin = w[x].find('a.T8HSqd.yYlJEf.L48Cpd')
            web_links.append(list(rlin[0].absolute_links)[0])
        else:
            web_links.append('None')
    #print('scraping Website links...')


def save_to_dataframe():
    df = pd.DataFrame({
        'name': clean_names,
        'reviews': list_review,
        'url': web_links,
        'Number of reviews': num_of_reviews
    })

    df.to_excel('scraped_data.xlsx', index=False)


def initial_run():
    clean_res_block(r)
    total_reviews()
    cleaned_names(r)
    web_links_reviews(r)


def scrape_all():
    int1 = 1

    initial_run()
    print('scraping page 1...')

    for page in nxt_pages:
        r = session.get(page)
        clean_res_block(r)
        total_reviews()
        cleaned_names(r)
        web_links_reviews(r)
        int1 += 1
        print(f'scraping page {int1} ')

        time.sleep(5)

    save_to_dataframe()

if __name__ == "__main__":
    scrape_all()
