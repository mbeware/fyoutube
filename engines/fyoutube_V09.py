import os
import sys
import subprocess
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import Config
from datetime import datetime
from pathlib import Path
from typing import Any
from core.Config import messagelog

from core import manage_arguments



#09S

def InfoFromPlaylist(url:str, downloaded_video_archive_file:str):    
    cname = Config.get_channel_name(url)
    messagelog.info(f"New channel: {cname}" )
    cmd = [
            'yt-dlp',
            '--concurrent-fragments','4', # This might still be useful for processing multiple playlists/channels
            '--force-write-archive',
            '--skip-download', 
            '-P','/mnt/AllVideo/0082-youtube',
            '-P','temp:tmp',
            '--download-archive',downloaded_video_archive_file,
            '--yes-playlist',
#            '-O','%(id)s', # Output only the video ID
            '--flat-playlist', 
            '--progress',
            '-q',
            url,
    ]       
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False) # Keep capture_output=False if you want to see yt-dlp's progress
        if result.returncode == 0:
            messagelog.info("Info retrieval completed successfully.")
        Path(downloaded_video_archive_file).touch() # just in case there were no video on that channel
        return result.returncode
    
    except subprocess.CalledProcessError as e:
        messagelog.critical(f"Error occurred during Info: {e}")
        messagelog.critical("Make sure yt-dlp is installed and the playlist URL is valid.")
        sys.exit(1)
    except FileNotFoundError:
        messagelog.critical("Error: yt-dlp not found. Please install it first:")
        messagelog.critical("pip install yt-dlp")
        sys.exit(1)

def moreinfo(url:str):
    cname =Config.get_channel_name(url)
    messagelog.info(f"Getting more info: {cname}" )
    moreinfofile = f'{Config.LOGS_DIR}/archive_{cname}_moreinfo_debug.txt'
          
    cmd2 = [
    'yt-dlp',
    '--skip-download', 
    '-P','/mnt/AllVideo/0082-youtube',
    '-P','temp:tmp',
    '--yes-playlist',
    #'-O','%(id)s', # Output only the video ID
    '--flat-playlist', 
    '--progress',
    '--ignore-errors',
    '--print-to-file', '[%(id)s]-[%(title)s]-[release date : %(release_date)s]-[live_status:%(live_status)s]-[is_live:%(is_live)s]-[was_live:%(was_live)s]-[url:%(webpage_url)s]-[%(original_url)s]', moreinfofile,        
    url,
    ]       
    subprocess.run(cmd2, check=True, capture_output=False) # Keep capture_output=False if you want to see yt-dlp's progress


def download_playlist(url:str):    
    
    cname = Config.get_channel_name(url)
    downloaded_video_archive_file = f'{Config.ARCHIVE_DIR}/archive_global.list'
    channel_config_file = f'{Config.GLOBAL_CONFIGDIR}/{cname}.config'
    if True or not os.path.exists(channel_config_file): #New channel - Don't download all old videos
        r = InfoFromPlaylist(url,downloaded_video_archive_file)
        if r == 0 :
            with open(channel_config_file,'a') as f:
                pass
    return 0
    
    messagelog.info(f"{datetime.now().strftime('%H:%M:%S')} - Processing channel: {cname}" )
    moreinfofile = f'{Config.LOGS_DIR}/archive_{cname}_debug.log'
    cmd:list[str] = [
            'yt-dlp',
            '--use-extractors','all', 
            '--sleep-subtitles',Config.SLEEP_SUBTITLES,
            '--sleep-interval',Config.SLEEP_INTERVAL,
            '--sleep-requests',Config.SLEEP_REQUESTS,
            '--max-sleep-interval',Config.MAX_SLEEP_INTERVAL,
#            '--concurrent-fragments','4',
            '--force-write-archive',
#            '--skip-download',  # Skip downloading videos
            '-P',Config.VIDEO_DIR,
            '-P','temp:tmp',
            '-P','subtitle:subs',
            '-o','[%(upload_date)s]-[%(uploader)s]_[%(title)s].%(ext)s',            
             '--download-archive',downloaded_video_archive_file,
            '-f','bestvideo+bestaudio/best',
#            '--sub-langs','all,-live_chat',
#            '--embed-subs',
            '--yes-playlist',
            '--remux-video', 'mkv',            
            '--progress',
            '--xattrs',    
            '--match-filters', "live_status!~=?'post_live|is_live|is_upcoming'",     
            '--no-abort-on-error',
            '--check-formats',
            '--no-abort-on-error',
            '--restrict-filenames', 
            '--print-to-file', '['+datetime.now().strftime('%Y-%m-%d% %H:%M:%S')+']-[%(id)s]-[%(title)s]-[release date : %(release_date)s]-[live_status:%(live_status)s]-[is_live:%(is_live)s]-[was_live:%(was_live)s]-[url:%(webpage_url)s]-[%(original_url)s]', moreinfofile,        
            '--force-keyframes-at-cuts',
            '--sponsorblock-remove',"sponsor,selfpromo",
            '-q',
            '--verbose',
            url,
    ]
    #ytdlp_params:dict[str,Any]=Config.build_options(None)
    #ytdlp_params['download_archive']=downloaded_video_archive_file
    #for option_name,option_value in ytdlp_params.items():
    #    print(f'{option_name=}-{option_value=}-{type(option_value)=}')    
    #for optionitem in cmd:
    #    print(f'{optionitem=}')
    
    try:
        with open(f"{Config.LOGS_DIR}/archive_{cname}_stderr.log", 'w') as error_file:
            r=subprocess.run(cmd, check=True, stdout=None, text=True, stderr=error_file )
            return r.returncode



    except subprocess.CalledProcessError:
        messagelog.error(f"Error occurred during download for [{cname}] ")
#        moreinfo(url)
        return 22
  

    except FileNotFoundError:
        messagelog.critical("Error: yt-dlp not found. Please install it first:")
        messagelog.critical("pip install yt-dlp")
        sys.exit(1)
    
    

def is_next_channel(url:str,last_url:str)-> bool:
    cname = Config.get_channel_name(url)   
    lasturlcname = Config.get_channel_name(last_url)         
    if last_url == url:
        messagelog.info(f'found {cname}! - downloading will start with next channel')
        return True
    
    messagelog.info(f'Looking for {lasturlcname} - skipping {cname} for now')
    return False

def save_lastchannel(url:str):
    with open(Config.LASTDOWNLOADEDCHANNEL_FILE, 'w') as lastdownloadedchannel:
        lastdownloadedchannel.write(url)

def get_lastchannel()->str:
    with open(Config.LASTDOWNLOADEDCHANNEL_FILE, 'r+') as lastdownloadedchannel:
        return lastdownloadedchannel.readline()    

def get_videos():
    
    last_url = get_lastchannel()
    
    loop_count = 0 
    downloaded_count = 0
    while True:
        messagelog.info(f"* V09 *{loop_count=}*{downloaded_count=}***********************************************************************************************************")
        if not manage_arguments.g_args.IAmAPirateAndIWillStarveTheCreators:
            messagelog.critical(Config.i_PIRATEMESSAGE)
        urls = []
        with open(Config.SUBSCRIPTIONS_FILE, 'r') as f:
            urls = f.readlines()    
        messagelog.info("Here we go for an other round...")
        for url in urls:  
            url = url.strip()
            if url and is_next_channel(url,last_url) if last_url else True: 
                if last_url:
                    last_url=None 
                else:                
                    if download_playlist(url) == 0:
                        downloaded_count +=1
                        save_lastchannel(url)
        if loop_count > 0 or downloaded_count > 0:
            messagelog.info("Waiting for a bit...")
            time.sleep(600)  # Sleep for a while before checking again
        loop_count += 1
