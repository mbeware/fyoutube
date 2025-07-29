import os
import sys
import subprocess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import Config
from typing import Any
from pathlib import Path
from core.Config import Request_type

import yt_dlp




from core.Config import messagelog



def get_from_youtube(request_type: Request_type, yt_dlp_parameters: dict[str,str],fyoutube_parameters:dict[str,str] ):

    pass


def download_all_video_from_channel(channel_url:str,
                                    video_destination:str,
                                    downloaded_video_archive_file:str):
    if not os.path.exists(downloaded_video_archive_file): #New channel - Don't download all old videos
        return InfoFromPlaylist(channel_url,downloaded_video_archive_file)
    cname = Config.get_channel_name(channel_url)
    messagelog.info(f"Processing channel: {cname}")
    
    # cmd:list[str] = [
    #         'yt-dlp',
    #         '--sleep-subtitles',Config.SLEEP_SUBTITLES,           #sleep_interval_subtitles.download_value = 1
    #         '--sleep-interval',Config.SLEEP_INTERVAL,             #sleep_interval.download_value = 10
    #         '--sleep-requests',Config.SLEEP_REQUESTS,             #sleep_interval_requests.download_value = 1
    #         '--max-sleep-interval',Config.MAX_SLEEP_INTERVAL,     #max_sleep_interval.download_value = 20
    #         '--force-write-archive',                              #force_write_download_archive.download_value = True
    #         '-P',video_destination,
    #         '-P','temp:tmp',
    #         '-P','subtitle:subs',
    #         '-o','[%(upload_date)s]-[%(uploader)s]_[%(title)s].%(ext)s',            
    #          '--download-archive',downloaded_video_archive_file,
    #         '-f','bestvideo+bestaudio/best',
    #         '--sub-langs','all,-live_chat',
    #         '--embed-subs',
    #         '--yes-playlist',
    #         '--remux-video', 'mkv',            
    #         '--progress',
    #         '--xattrs',    
    #         '--match-filters', "live_status!~=?'post_live|is_live|is_upcoming'&availability~=?'unlisted|public'",     
    #         '--no-abort-on-error',
    #         '--check-formats',
    #         '--no-abort-on-error',
    #         '--restrict-filenames', 
    #         '-q',
    #         '--verbose',
    #         channel_url,
    # ]





# skip_download.download_value = False
# subtitleslangs.download_value= 'all,-live_chat'
# embedsubtitles.download_value=True
# noplaylist.download_value=False
# remuxvideo.download_value='mkv'
# noprogress.download_value=False
# xattrs.download_value=True
# match_filter.download_value= "live_status!~=?'post_live|is_live|is_upcoming'&availability~=?'unlisted|public'"
# ignoreerrors.download_value='only_download'
# check_formats.download_value= 'selected'
# quiet.download_value=True
# paths.download_value={'default':VIDEO_DIR,
#                        'home':VIDEO_DIR,
#                       'temp':'tmp',
#                       'subtitle':'subs',
#                       'pl_video':VIDEO_DIR,
#                       }
# outtmpl.download_value={'default':'[%(upload_date)s]-[%(uploader)s]_[%(title)s].%(ext)s'}
# download_archive.download_value="************************"

    ytdlp_params:dict[str,Any]=Config.build_options(Request_type.DOWNLOAD_ALL_CHANNEL)
    ytdlp_params['download_archive']=downloaded_video_archive_file
    for option_name,option_value in ytdlp_params.items():
            messagelog.debug(f'{option_name=}-{option_value=}-{type(option_value)=}')    
    downloader=yt_dlp.YoutubeDL(ytdlp_params)
    listurl:list[str]=[]
    listurl.append(channel_url)
    r=downloader.download(listurl)

    return r

    # try:


    #     with open(f"{Config.LOGS_DIR}/yt_dlp_{cname}_verbose.log", 'a') as error_file:
    #         r=subprocess.run(cmd, check=True, stdout=None, text=True, stderr=error_file )
    #         return r.returncode



#     except subprocess.CalledProcessError:
#         messagelog.error(f"Error occurred during download for [{cname}] ")
# #        moreinfo(url)
#         return 22
  

#     except FileNotFoundError:
#         messagelog.error("Error: yt-dlp not found. Please install it first:")
#         messagelog.error("pip install yt-dlp")
#         sys.exit(1)
        

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
        messagelog.error(f"Error occurred during Info: {e}")
        messagelog.error("Make sure yt-dlp is installed and the playlist URL is valid.")
        sys.exit(1)
    except FileNotFoundError:
        messagelog.error("Error: yt-dlp not found. Please install it first:")
        messagelog.error("pip install yt-dlp")
        sys.exit(1)

def moreinfo(url:str):
    cname = Config.get_channel_name(url)
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



    

