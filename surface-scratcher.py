from bs4 import BeautifulSoup as bs
import urllib.request
import argparse
import requests
import os


def get_args():
    parser = argparse.ArgumentParser(description = "Download images and labels from scratchthesurface.tumblr.com")
    parser.add_argument("-n", "--no_context", help = "(optional) - disables the download of context images", action = "store_true")
    parser.add_argument("-u", "--update", help = "(optional) - updates the local dataset with newly added surfaces", action = "store_true")
    return parser.parse_args()
    
    
def process_post(post_url, no_context):
    html_text = requests.get(post_url).text
    soup = bs(html_text, features = "html.parser")
    image_scratcher(soup, no_context)
    next = soup.find("span", {"class": "next_cell"})
    if next:
        post_url = next.previous_element["href"]
        return post_url
        
        
def image_scratcher(soup, no_context):
    if "counter" not in image_scratcher.__dict__:
        image_scratcher.counter = 0
    image_scratcher.counter += 1
    
    img = soup.find("img", {"class": "notPhotoset"})
    img_url = img["src"]
    name = img_url.split("/")[-1]
    urllib.request.urlretrieve(img_url, "surfaces/{}.jpg".format(image_scratcher.counter))
    if not no_context:
        context = soup.find("figure", {"class": "tmblr-full"}).find("img")
        context_url = context["src"]
        urllib.request.urlretrieve(context_url, "contexts/{}.jpg".format(image_scratcher.counter))
        
        
def init_directories():
    if not os.path.isdir("surfaces"):
        os.mkdir("surfaces")
    if not os.path.isdir("contexts"):
        os.mkdir("contexts")
        
        
def scratch(no_context):
    post_url = "https://scratchthesurface.tumblr.com/post/635159455418466304/scratch-the-surface-1-18nov2020-coarse"
    next = process_post(post_url, no_context)
    while next:
        next = process_post(next, no_context)
        
def update():
    pass
    


if __name__ == "__main__":
    args = get_args()
    no_context, update = args.no_context, args.update
    
    init_directories()
    if update:
        update(no_context)
    else:
        scratch(no_context)

    
