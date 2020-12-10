from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib.request
import argparse
import requests
import os


def get_args():
    parser = argparse.ArgumentParser(description = "Download images and labels from scratchthesurface.tumblr.com")
    parser.add_argument("-n", "--no_context", help = "(optional) - disables the download of context images", action = "store_true")
    parser.add_argument("-u", "--update", help = "(optional) - updates the local dataset with newly added surfaces", action = "store_true")
    return parser.parse_args()
    
    
def parse_labels(soup):
    label_soup = soup.find("span", {"class": "notes_headline_inner"})
    index_date, labels = list(label_soup)[1:3]
    index, date = index_date.find(text=True).split(" - ")
    _, coarse, _, fine, _, color, _, object = labels.findAll(text=True)
    coarse, fine, color, object = coarse[2:], fine[2:], color[2:], object[2:]
    return index,date,coarse,fine,color,object
    
    
def image_scratcher(soup, index, no_context):
    img_url = soup.find("img", {"class": "notPhotoset"})["src"]
    urllib.request.urlretrieve(img_url, "surfaces/{}.jpg".format(index))
    if not no_context:
        context_url = soup.find("figure", {"class": "tmblr-full"}).find("img")["src"]
        urllib.request.urlretrieve(context_url, "contexts/{}.jpg".format(index))
        
        
def get_last_post():
    tumblr_url = "https://scratchthesurface.tumblr.com"
    html_text = requests.get(tumblr_url).text
    soup = bs(html_text, features = "html.parser")
    posts = soup.find("div", {"id": "posts"})
    last_post = posts.find("div", {"class": ["post","not_audio","photopost","loaded"]})
    id = last_post["id"][5:]
    return tumblr_url + "/" + id
    
    
def process_post(post_url, no_context):
    html_text = requests.get(post_url).text
    soup = bs(html_text, features = "html.parser")

    index,date,coarse,fine,color,object = parse_labels(soup)
    image_scratcher(soup, index, no_context)
    next = soup.find("span", {"class": "prev_cell"})
    if next:
        post_url = next.previous_element["href"]
        return post_url,index,date,coarse,fine,color,object
    return None,index,date,coarse,fine,color,object
        
        
def init_directories():
    if not os.path.isdir("surfaces"):
        os.mkdir("surfaces")
    if not os.path.isdir("contexts"):
        os.mkdir("contexts")
        
def append_dataframe(labels,row_data):
    row = pd.DataFrame([row_data], columns=labels.columns)
    return pd.concat([labels,row])
        
        
def scratch(no_context):
    post_url = get_last_post()
    labels = pd.DataFrame({"index":[],"date":[],"coarse taxonomy":[],"fine taxonomy":[],"color":[],"object":[]})
    try:
        data = process_post(post_url, no_context)
        next,row_data = data[0],data[1:]
        labels = append_dataframe(labels,row_data)
        while next:
            data = process_post(next, no_context)
            next,row_data = data[0],data[1:]
            labels = append_dataframe(labels,row_data)
    finally:
        labels.to_csv("labels.csv", index=False)
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

    
