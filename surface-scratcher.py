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
    
    
def parse_labels(soup, labels_file):
    label_soup = soup.find("span", {"class": "notes_headline_inner"})
    index_date, labels = list(label_soup)[1:3]
    index, date = index_date.find(text=True).split(" - ")
    _, coarse, _, fine, _, color, _, object = labels.findAll(text=True)
    coarse, fine, color, object = coarse[2:], fine[2:], color[2:], object[2:]
    labels_file.write("{},{},".format(index,date))
    labels_file.write("{},{},{},{}\n".format(coarse, fine, color, object))
    return index
    
    
def process_post(post_url, labels_file, no_context):
    html_text = requests.get(post_url).text
    soup = bs(html_text, features = "html.parser")

    image_scratcher(soup, labels_file, no_context)
    next = soup.find("span", {"class": "next_cell"})
    if next:
        post_url = next.previous_element["href"]
        return post_url
        
        
def image_scratcher(soup, labels_file, no_context):
    index = parse_labels(soup, labels_file)
    img_url = soup.find("img", {"class": "notPhotoset"})["src"]
    urllib.request.urlretrieve(img_url, "surfaces/{}.jpg".format(index))
    if not no_context:
        context_url = soup.find("figure", {"class": "tmblr-full"}).find("img")["src"]
        urllib.request.urlretrieve(context_url, "contexts/{}.jpg".format(index))
        
        
def init_directories():
    if not os.path.isdir("surfaces"):
        os.mkdir("surfaces")
    if not os.path.isdir("contexts"):
        os.mkdir("contexts")
        
        
def scratch(no_context):
    post_url = "https://scratchthesurface.tumblr.com/post/635159455418466304/scratch-the-surface-1-18nov2020-coarse"
    labels_file = open("labels.csv", "w")
    labels_file.write("index,date,coarse taxonomy,fine taxonomy,color,object\n")
    next = process_post(post_url, labels_file, no_context)
    while next:
        next = process_post(next, labels_file, no_context)
    labels_file.close()
        

def update(no_context):
    pass
    


if __name__ == "__main__":
    args = get_args()
    no_context, update = args.no_context, args.update
    
    init_directories()
    if update:
        update(no_context)
    else:
        scratch(no_context)

    
