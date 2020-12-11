from bs4 import BeautifulSoup as bs
import pandas as pd
import argparse
import requests
import os


def get_args():
    parser = argparse.ArgumentParser(description = "Download images and labels from scratchthesurface.tumblr.com")
    parser.add_argument("-n", "--no_context", help = "(optional) - disables the download of context images", action = "store_true")
    parser.add_argument("-u", "--update", help = "(optional) - updates the local dataset with newly added surfaces", action = "store_true")
    return parser.parse_args()
    
    
def parse_labels(soup):
    '''
    Argument:
        soup: bs4.BeautifulSoup with a scratchthesurface post
    Output:
        tuple with 6 elements:
            integer - post index
            string - post date
            string - surface coarse taxonomy
            string - surface fine taxonomy
            string - surface color
            string - object description
    '''
    label_soup = soup.find("span", {"class": "notes_headline_inner"})
    index_date, labels = list(label_soup)[1:3]
    index, date = index_date.find(text=True).split(" - ")
    _, coarse, _, fine, _, color, _, object = labels.findAll(text=True)
    coarse, fine, color, object = coarse[2:], fine[2:], color[2:], object[2:]
    return int(index),date,coarse,fine,color,object
    
    
def image_scratcher(soup, index, no_context):
    '''
    Behaviour:
        Downloads the post images and saves in the respective folder (surfaces or contexts)
    Argument:
        soup: bs4.BeautifulSoup with a scratchthesurface post
        index: integer with the post index
        no_context: boolean, when 0 download the context image, else don't
    Output:
        None
    '''
    img_url = soup.find("img", {"class": "notPhotoset"})["src"]
    urllib.request.urlretrieve(img_url, "surfaces/{}.jpg".format(index))
    if not no_context:
        context_url = soup.find("figure", {"class": "tmblr-full"}).find("img")["src"]
        urllib.request.urlretrieve(context_url, "contexts/{}.jpg".format(index))
        
        
def get_last_post():
    '''
    Argument:
        None
    Output:
        string - the url of the most recent scratchthesurface post 
    '''
    tumblr_url = "https://scratchthesurface.tumblr.com"
    html_text = requests.get(tumblr_url).text
    soup = bs(html_text, features = "html.parser")
    posts = soup.find("div", {"id": "posts"})
    last_post = posts.find("div", {"class": ["post","not_audio","photopost","loaded"]})
    id = last_post["id"][5:]
    return tumblr_url + "/" + id
    
    
def process_post(post_url, no_context):
    '''
    Behaviour:
        Downloads the post images, saves in the respective folder (surfaces or contexts)
        and returns the post labels 
    Argument:
        post_url: string with the url of the scratchthesurface post to be processed
        no_context: boolean, when 0 download the context image, else don't
    Output:
        tuple with 6 elements:
            string or None - string with the url of the previous post or None if post_url is 
                the first post
            integer - post index
            string - post date
            string - surface coarse taxonomy
            string - surface fine taxonomy
            string - surface color
            string - object description
    '''
    html_text = requests.get(post_url).text
    soup = bs(html_text, features = "html.parser")

    index,date,coarse,fine,color,object = parse_labels(soup)
    print(" downloading post", index)
    image_scratcher(soup, index, no_context)
    prev = soup.find("span", {"class": "prev_cell"})
    if prev:
        return prev.previous_element["href"],index,date,coarse,fine,color,object
    return None,index,date,coarse,fine,color,object
        
        
def init_directories():
    if not os.path.isdir("surfaces"):
        os.mkdir("surfaces")
    if not os.path.isdir("contexts"):
        os.mkdir("contexts")
        
        
def append_dataframe(labels,row_data):
    row = pd.DataFrame([row_data], columns=labels.columns)
    return pd.concat([labels,row])
        
        
def scratch_surfaces(no_context):
    '''
    Behaviour:
        Downloads post images and labels from the new to old
    Argument:
        no_context: boolean, when 0 download the context image, else don't
    Output:
        None
    '''
    print("Scratching surfaces...")
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
        labels["index"] = labels["index"].astype(int)
        labels = labels.sort_values("index", ascending = False)
        labels.to_csv("labels.csv", index = False)
    print("done!")
        

def update_surfaces(no_context):
    '''
    Behaviour:
        Downloads post images and labels from the new to old until the last downloaded post.
        Usefull when your local dataset doesn't contain newly added surfaces to scratchthesurface.tumblr.com
    Argument:
        no_context: boolean, when 0 download the context image, else don't
    Output:
        None
    '''
    assert os.path.isfile("labels.csv"), "update: no labels.csv file found. Download the dataset before upading, like so: python3 surface-scratcher.py"
    print("Updating surfaces...")
    labels = pd.read_csv("labels.csv")
    max_index = labels["index"].max()
    post_url = get_last_post()
    try:
        data = process_post(post_url, no_context)
        next,row_data = data[0],data[1:]
        index = row_data[0]
        if index > max_index:
            labels = append_dataframe(labels,row_data)
            while index > max_index+1:
                data = process_post(next, no_context)
                next,row_data = data[0],data[1:]
                labels = append_dataframe(labels,row_data)
                index = row_data[0]
    finally:
        labels["index"] = labels["index"].astype(int)
        labels = labels.sort_values("index", ascending = False)
        labels.to_csv("labels.csv", index = False)
    print("done!")        
        

if __name__ == "__main__":
    args = get_args()
    no_context, update = args.no_context, args.update
    
    init_directories()
    if update:
        update_surfaces(no_context)
    else:
        scratch_surfaces(no_context)

    
