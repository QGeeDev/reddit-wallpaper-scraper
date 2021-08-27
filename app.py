from genericpath import exists
import requests
from configparser import ConfigParser
import wget
from PIL import Image
import os
import pathlib

REDDIT_URL = "https://www.reddit.com"
SUBREDDIT_PREFIX = "/r/"

class ConfigManager():
    def __init__(self, configFileName: str) -> None:
        self.parser = ConfigParser()
        try:
            with open(configFileName) as c:
                self.parser.read(configFileName)
        except IOError:
            print("Config file not found. Looking for file: {}".format(configFileName))
            exit()

    def getConfigSetting(self, section: str, key: str):
        if section not in self.parser.sections():
            print("Section not in config")
            return
        if key not in self.parser[section]:
            print("Key not found in section")
            return
        return str(self.parser[section][key])

class RedditImageDownloader():
    def __init__(self, config: ConfigManager) -> None:
        self.config = config
        self.minWidth = int(self.config.getConfigSetting("UserSettings", "MinWidth"))
        self.minHeight = int(self.config.getConfigSetting("UserSettings", "MinHeight"))
        self.SaveFilePath = self.createSaveLocation(self.config.getConfigSetting("UserSettings", "PathToSaveLocation"))
        self.cleanOutWallpaperFolder()
    
    def createSaveLocation(self, pathString: str):
        path = pathlib.Path(pathString)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def cleanOutWallpaperFolder(self):
        files = [x for x in self.SaveFilePath.glob("**/*") if x.is_file()]
        for file in files:
            os.remove(self.SaveFilePath / file)

    def downloadImages(self):
        subredditList = self.config.getConfigSetting("subreddits", "sub_list").split(",")
        cleanlist = []
        for sub in subredditList:
            cleanlist.append(sub.strip())
        subredditList = cleanlist
        for item in subredditList:
            requestJson = self.fetchSubredditPosts(item)
            if('data' in requestJson and 'children' in requestJson['data']):
                for post in requestJson['data']['children']:
                    post = post['data']
                    if(('post_hint' in post and post['post_hint']=='image') or post['url'].endswith(tuple(self.config.getConfigSetting("requestData","image_formats").split(",")))):
                        self.getPhoto(post['url'])

    
    def getPhoto(self, photoURL : str):
        if(photoURL.endswith(tuple(self.config.getConfigSetting("requestData","image_formats").split(",")))):
            fileName = wget.download(photoURL, out=str(self.SaveFilePath.absolute()))
            img = Image.open(fileName)
            width, height = img.size
            img.close()
            if(width < self.minWidth or height < self.minHeight):
                os.remove(fileName)


    def fetchSubredditPosts(self, subredditName):
        try:
            redditURL = REDDIT_URL + SUBREDDIT_PREFIX + subredditName + f"/{self.config.getConfigSetting('requestData', 'listing')}.json?limit={self.config.getConfigSetting('requestData', 'max_images_per_sub')}&t={self.config.getConfigSetting('requestData', 'timeframe')}"
            request = requests.get(redditURL, headers = {'User-agent': 'QG-Wallpaper-Ripper'})
            return request.json()
        except:
            pass
        

def main():
    c1 = ConfigManager("config.ini")
    downloader = RedditImageDownloader(c1)
    downloader.downloadImages()


if __name__ == '__main__':
    main()

