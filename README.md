# 4chan-archiver
> Downloads threads on 4chan and saves the images/videos

This program has the ability to download entire threads saving the format of the discussion as well as preserving any video, gifs or images that may have been posted. Each thread is downloaded in an html file in a similar layout to 4chan albeit simplified.

## Requirments
* Python3
* BeautifulSoup

## Usage
The url to a thread passed in as a positional argument as well as a number of flags.

This is the help output
```
pepe@boysclub:~/4chan-archiver$ python3 archiver.py -h
usage: archiver.py [-h] [-p] [-r RETRIES] [--posts POSTS] Thread

Archives 4chan threads

positional arguments:
  Thread                Enter the link to the 4chan thread

optional arguments:
  -h, --help            show this help message and exit
  -p, --preserve_files  Save images and video files locally
  -r RETRIES, --retries RETRIES
                        Set total number of retries if a download fails
  --posts POSTS         Number of posts to download
```

Here is an example that downloads every post in a thread and saves all the media uploaded.
```
pepe@boysclub ~/4chan-archiver$ python3 archiver.py http://boards.4channel.org/p/thread/3434289/ect-edit-challenge-thread -p
```

