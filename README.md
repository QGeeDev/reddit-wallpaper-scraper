# Python Wallpaper Scraper
## Introduction

This is a simple Python program written in Python 3.8.10 that scans subreddits for image posts that are suitable to use as wallpapers, and downloads them to your local machine. Having this run on start up of your machine will provide you with an ever changing selection of wallpapers, all taken from your favourite subreddits.

---
## Requirements
This project is built in Python 3.8.10. Additional Python modules used can be found in the file _requirements.txt_.

---
## Usage
To run this project, run _app.py_. 

Settings for the project can be adjusted in _config.ini_.
- ```subreddits```
  - ```sub_list```: comma separated list of subreddits to take pictures from
- ```requestData```
  - ```max_images_per_sub```: This is the number of posts that will be queried against in the request. This does not mean that you will receive this number of images per sub, but rather the number of posts to sample from.
  - ```timeframe```: As is on Reddit, how recent posts should be.
    - One of (```hour, day, week, month, year, all```)
  - ```listing```: How the posts fetched should be sorted
    - One of (```relevance, hot, top, new, comments```)
  - ```image_formats```
    - Comma separated list of suitable filetypes that can be downloaded to the folder.
- ```UserSettings```
  - ```PathToSaveLocation```
    - Full file path to where the downloaded photos should be saved. This path does not need to exist, and will be created if not found
  - ```MinHeight``` and ```MinWidth```
    - Minimum height and width of the images to keep in pixels. All images will be downloaded, however will then be checked to see if they should be kept based on these criteria. To keep all images, set these values to 1.

When run, the program will download all images found from the criteria defined above. 

Set Windows to have Desktop Background as a Slideshow, select the destination folder as the album to use. This will give you new backgrounds whenever you want.