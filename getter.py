from bs4 import BeautifulSoup as soup
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import URLError
from os import sys
from time import time
import os

'''
Donwload file to `path` with `name`. If fails
wait and retry, until total retries reached.
'''
def download(path, name, verbose, path_to_download, total_retries, retries = 0):
    try:
        if verbose: print("Downloading image:", path, name)
        urlretrieve('{}'.format(path), '{}/{}'.format(path_to_download, name))
    except URLError:
        if(total_retries > retries):
            print("Failed, retrying", retries)
            retries += 1
            download(path, name, path_to_download, total_retries, retries)


def getOP(page_soup, verbose, preserve, path_to_download, total_retries):
    # Get op details
    op_post = page_soup.find_all("div", {"class":"postContainer opContainer"})
    op_message = op_post[0].find_all("blockquote", {"class":"postMessage"})[0]
    op_img_src = op_post[0].find_all("div", {"class":"fileText"})[0].find_all("a")[0]['href']
    op_img_text = op_post[0].find_all("div", {"class":"fileText"})[0].find_all("a")[0].text
    op_subject = op_post[0].find_all("span", {"class":"subject"})[0].text
    op_name = op_post[0].find_all("span", {"class":"name"})[0].text
    op_date = op_post[0].find_all("span", {"class":"dateTime"})[0].text
    op_pid = op_post[0].find_all("div", {"class":"post op"})[0]['id']
    op_img_src = 'https:{}'.format(op_img_src)

    if verbose:
        print("Downloading post:", op_pid, "posted on", op_date)

    if preserve:
        download(op_img_src, op_img_text, verbose, path_to_download, total_retries)
        op_img_src = '{}/{}'.format(path_to_download,op_img_text)

    return (op_message, op_img_src, op_img_text, op_subject, op_name, op_date, op_pid)
