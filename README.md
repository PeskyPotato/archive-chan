# 4chan-archiver
> Downloads threads on 4chan and saves the images/videos

This program has the ability to download entire threads saving the format of the discussion as well as preserving any video, gifs or images that may have been posted. Each thread is downloaded in an html file in a similar layout to 4chan albeit simplified.

## Requirments
* Python3
* BeautifulSoup

## Usage

### Archive 4chan threads or catalogs

To archive one or multiple threads of your choosing pass in the thread url or a text file of thread urls each on a new line to `archiver.py`. A number of flags can be set in addition to this.

This is the help output
```
pepe@boysclub:~/4chan-archiver$ python3 archiver.py -h
usage: archiver.py [-h] [-p] [-r RETRIES] [--posts POSTS] [-v] Thread


positional arguments:
  Thread                Enter the link or txt file of links to the 4chan thread

optional arguments:
  -h, --help            show this help message and exit
  -p, --preserve_files  Save images and video files locally
  -r RETRIES, --retries RETRIES
                        Set total number of retries if a download fails
  --posts POSTS         Number of posts to download
  -v, --verbose         Print more information on each post
```

Here is an example that downloads every post in a thread and saves all the media uploaded.
```
pepe@boysclub ~/4chan-archiver$ python3 archiver.py http://boards.4channel.org/p/thread/3434289/ect-edit-challenge-thread -p
```

To archive all the threads pass in the board as a positional argument. A number of flags can be set in addition to this.

Here is an example that downloads every active post in a /g/.
```
pepe@boysclub ~/4chan-archiver$ python3 catalog.py g -v
Downloading thread: 51971506
Downloading post: p51971506 posted on 12/20/15(Sun)20:03:52
Downloading reply: p67501950 replied on 09/07/18(Fri)19:58:36
Downloading thread: 70621338
Downloading post: p70621338 posted on 04/19/19(Fri)23:03:23
Downloading reply: p70621345 replied on 04/19/19(Fri)23:04:13
Downloading reply: p70621391 replied on 04/19/19(Fri)23:10:35
Downloading reply: p70621407 replied on 04/19/19(Fri)23:12:27
```