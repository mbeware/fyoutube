import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import Config
from core.Config import log_channel

from .fyoutube_yt_dlp import download_all_video_from_channel
from core.Config import messagelog



def is_next_channel(url:str,last_url:str)-> bool:
    cname = Config.get_channel_name(url)           
    lasturlcname = Config.get_channel_name(last_url)            
    if last_url == url:
        messagelog.info(f'found {cname}! - downloading will start with next channel')
        return True
    
    print(f'Looking for {lasturlcname} - skipping {cname} for now')
    return False

def save_lastchannel(url:str):
    with open(Config.LASTDOWNLOADEDCHANNEL_FILE, 'w') as lastdownloadedchannel:
        lastdownloadedchannel.write(url)

def get_lastchannel()->str:
    with open(Config.LASTDOWNLOADEDCHANNEL_FILE, 'r+') as lastdownloadedchannel:
        return lastdownloadedchannel.readline()    

def get_videos():
    last_url = get_lastchannel()
    while True:
        print("* main ************************************************************************************************************")
        
        urls = []
        with open(Config.SUBSCRIPTIONS_FILE, 'r') as f:
            urls = f.readlines()    
        messagelog.info("Here we go for an other round...")
        for url in urls:  
            url = url.strip()
            
            if url and url != "" and (is_next_channel(url,last_url) if last_url else True): 
                if last_url:
                    last_url=None 
                else:                
                    if download_all_video_from_channel(url,Config.VIDEO_DIR,f'{Config.ARCHIVE_DIR}/archive_global.list') == 0:
                        save_lastchannel(url)
                
        messagelog.info("Waiting for a bit...")
        time.sleep(600)  # Sleep for a while before checking again



    