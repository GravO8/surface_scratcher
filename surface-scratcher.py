from bs4 import BeautifulSoup as bs
import urllib.request
import argparse
import requests
import os

def get_args():
    def to_download(arg):
        if arg == "all" or arg.isnumeric():
            return arg
        raise argparse.ArgumentTypeError("invalid expression for download flag. Please specify an integer or write 'all'")
    parser = argparse.ArgumentParser(description = "Download images and labels from scratchthesurface.tumblr.com")
    parser.add_argument("-n", "--no_context", help = "(optional) - disables the download of context images", action = "store_true")
    parser.add_argument("-u", "--update", help = "(optional) - updates the local dataset with newly added surfaces", action = "store_true")
    parser.add_argument("-f", "--full_update", help = "(optional) - checks and updates any difference of local dataset with the remote dataset", action = "store_true")
    parser.add_argument("-d", "--download", help = "(optional) - downloads the surface information of the specified surface index", type = to_download)
    parser.add_argument("-v", "--verbose", help = "(optional) - details what the program is doing", action = "store_true")
    return parser.parse_args()


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
    # img = soup.find("img", {"class": "notPhotoset"})
    # img_url = img["src"]
    # name = img_url.split("/")[-1]
    # urllib.request.urlretrieve(img_url, name)
    if scratch_context:
        context = soup.find("figure", {"class": "tmblr-full"}).find("img")
        print(context["src"])


if __name__ == "__main__":
    args = get_args()
    print(args)
    # if not os.path.isdir("surfaces"):
    #     os.mkdir("surfaces")
    # if not os.path.isdir("context"):
    #     os.mkdir("context")
    # post_url = "https://scratchthesurface.tumblr.com/post/635159455418466304/scratch-the-surface-1-18nov2020-coarse"
    # iter_posts(post_url, image_scratcher)

    
