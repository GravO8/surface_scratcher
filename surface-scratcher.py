from bs4 import BeautifulSoup as bs
import requests
import urllib.request


def do_nothing(soup):
    pass 
    
def iter_posts(post_url, post_processor = do_nothing):
    # print(post_url)
    html_text = requests.get(post_url).text
    soup = bs(html_text, features = "html.parser")
    post_processor(soup)
    next = soup.find("span", {"class": "next_cell"})
    if next:
        post_url = next.previous_element["href"]
        iter_posts(post_url, post_processor)
        
def image_scratcher(soup, scratch_context = True):
    img = soup.find("img", {"class": "notPhotoset"})
    img_url = img["src"]
    name = img_url.split("/")[-1]
    urllib.request.urlretrieve(img_url, name)


if __name__ == "__main__":
    post_url = "https://scratchthesurface.tumblr.com/post/635159455418466304/scratch-the-surface-1-18nov2020-coarse"
    iter_posts(post_url, image_scratcher)

    
