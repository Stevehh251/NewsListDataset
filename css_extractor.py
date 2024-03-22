'''
    This script will extract records from html page using folder with css selectors
'''
import json
import os
import sys

from glob import glob
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def xpath_soup(element):
    '''
        This function generate xpath from BeautifulSoup4 element.
        This was adapted from a gist from Felipe A. Hernandez to a GitHub:
        https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf
    '''
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
            )
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def generate_xpaths(html: str, block_selector: str) -> list:
    '''
        This function generate list of xpaths for first node with text into each block
    '''

    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.select(block_selector)

    xpaths = []

    for entity in blocks:
        text_node = entity.find(text=True)
        if text_node:
            xpaths += [xpath_soup(text_node)]

    return xpaths


def load_selectors(selectors_folder: str) -> dict:
    '''
        This function returns dict of css_selectors
        netloc:str -> selector:str
    '''
    if not os.path.exists(selectors_folder):
        raise Exception("Invalid css selectors directory")

    selectors_folder = os.path.abspath(selectors_folder)

    files_path = glob(os.path.join(selectors_folder, "*.json"))

    selectors = dict()

    for file_path in files_path:
        with open(file_path) as file:
            record = json.load(file) 
        
        # print(record)

        url = urlparse(record["startUrls"][0]).netloc
        if url.startswith("www."):
            url = url[4:]

        for selector in record["selectors"]:
            if selector["id"] == "block":
                block_selector = selector["selector"]
                selectors[url] = block_selector
                break

        
    return selectors



if __name__ == "__main__":

    if not os.path.exists(sys.argv[1]):
        raise Exception("Invalid input directory")

    if not os.path.exists(sys.argv[3]):
        print("Make new directory")
        os.mkdir(sys.argv[3])
    else:
        print("Directory already exists")
        
    
    in_path = os.path.abspath(sys.argv[1])
    selectors_folder = os.path.abspath(sys.argv[2])
    out_path = os.path.abspath(sys.argv[3])

    selectors = load_selectors(selectors_folder)

    files_path = glob(os.path.join(in_path, "*.json"))

    for file_path in files_path:
        with open(file_path) as file:
            info = json.load(file)

        netloc = urlparse(info["url"]).netloc
        if netloc.startswith("www."):
            netloc = netloc[4:]

        xpaths = generate_xpaths(info["html"], selectors[netloc])
        info["xpaths"] = xpaths

        filename = os.path.basename(file_path)

        with open(os.path.join(out_path, filename), "w", encoding="utf-8") as file:
            json.dump(info, file, ensure_ascii=False, indent=4)
