#!/usr/bin/env python3
from importlib import import_module
from inspect import getmembers
from engines.fyoutube_download import download_video
from core.Config import get_channel_name
import os
from datetime import datetime
import sys
import subprocess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import Config
from pathlib import Path
import os





def InfoFromPlaylist(url:str,cname:str,MFD_video_archive_file:str,verboselog:str|None=None,stdoutlog:str|None=None):    
    print(f"New channel: {cname}" )

    MFD_videoUrls_temp = f'/tmp/fyoutube/MFD_videoUrls_temp_{cname}.list'
    DEBUG_videoUrls_temp = f'/tmp/fyoutube/DEBUG_videoUrls_temp_{cname}.list'
    open(MFD_videoUrls_temp,'w').close()

    
    infoprefix='['
    infopostfix=']'
    infoseparator='-'
    
    MFD_videoUrlslist=['original_url']
    MFD_videoUrlsTemplate=Config.buildtemplate(MFD_videoUrlslist)
    
    DEBUG_videoUrlslistTemplate="[id->%(id)s]-[title->%(title)s]-[playlist_channel->%(playlist_channel)s]-[timestamp->%(timestamp)s]-[upload_date->%(upload_date)s]-[release_timestamp->%(release_timestamp)s]-[release_date->%(release_date)s]-[release_year->%(release_year)s]-[modified_timestamp->%(modified_timestamp)s]-[modified_date->%(modified_date)s]-[webpage_url->%(webpage_url)s]-[webpage_url_basename->%(webpage_url_basename)s]-[webpage_url_domain->%(webpage_url_domain)s]-[original_url->%(original_url)s]-[extractor->%(extractor)s]-[extractor_key->%(extractor_key)s]-[live_status->%(live_status)s]-[is_live->%(is_live)s]-[was_live->%(was_live)s]-[playable_in_embed->%(playable_in_embed)s]-[availability->%(availability)s]-[media_type->%(media_type)s]"
    
    progresslist=['info.title','progress.elapsed', 'progress.eta', 'progress.speed']
    progresstemplate=Config.buildtemplate(progresslist,[],infoseparator,infoprefix,infopostfix)    
    cmd = [

            'yt-dlp',
            ### Downloaded video
            '--concurrent-fragments','4',            
            '--use-extractors','all', 
##            '--flat-playlist', 
            '--yes-playlist',
#            '--no-simulate',
            '--skip-download', 
            
            ### Filters
            '--match-filters', "live_status!~=?'post_live|is_live|is_upcoming'&availability~=?'unlisted|public'",  
            #'--match-filters', "live_status!~=?'post_live|is_live|is_upcoming'&availability~=?'unlisted|public'&upload_date>?20250723",

            ## Download only videos uploaded <date>. 
            ## The date can be "YYYYMMDD" 
            ## or in the format [now|today|yesterday][-N[day|week|month|year]].
            ## E.g. "--date today-2weeks" downloads only videos uploaded on the same day two weeks ago

            #'--date','DATE',
            #'--datebefore','DATE'  ,
            '--dateafter',  'now-3day' , 

            ### Keep downloaded list
            '--force-write-archive',
            '--download-archive',MFD_video_archive_file,

            ### working dir and other mandatory values
            '-P','temp:/tmp/fyoutube/tmp',

            ### logs and feedback
            '--progress',
            ## progress templace can use info about the video with info prefix and progress prefix for progress info
            ## info attributes : <look for fields in doc>
            ## progress attributes : elapsed|speed|eta|total
#            '--progress-template','download:'+progresstemplate, 
            ##'--progress-template','download-title:TEMPLATE', progresstemplate
#            '--progress-template','postprocess:'+progresstemplate,
            ##'--progress-template','postprocess-title:TEMPLATE',

#            '--print',stdouttemplate, # Need --no-simulate to download
#            '--no-simulate',

            '--quiet',
#            '--verbose',
#            '--cookies-from-browser', 'brave',

            '--print-to-file',MFD_videoUrlsTemplate, MFD_videoUrls_temp,           
#            '--print-to-file',DEBUG_videoUrlslistTemplate, DEBUG_videoUrls_temp,           

            url,
    ]       


    try:
        MFD_videoUrls = []
        result = subprocess.run(cmd, check=True, capture_output=False) # Keep capture_output=False if you want to see yt-dlp's progress
        if result.returncode == 0:
            print("Info retrieval completed successfully.")
            with open(MFD_videoUrls_temp,'r') as f:
                MFD_videoUrls = f.readlines()

        Path(MFD_video_archive_file).touch() # just in case there were no video on that channel
        return MFD_videoUrls
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during Info: {e}")
        print("Make sure yt-dlp is installed and the playlist URL is valid.")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install it first:")
        print("pip install yt-dlp")
        sys.exit(1)


def main():

    ListMFDFolder="/tmp/fyoutube"
    ListMFDFile="ArchiveMarkedForDownload"
    ListMFDExtension=".list"

    ChannelURL = "https://www.youtube.com/watch?v=HZgQp-WDebU"
    ChannelURL = "https://www.youtube.com/@LinusTechTips"

    cname = 'LinusTechTips'
    ArchiveListMFDFileForChannel = f'{ListMFDFolder}/{ListMFDFile}_{cname}{ListMFDExtension}'
        
    urls=InfoFromPlaylist(ChannelURL,cname,ArchiveListMFDFileForChannel)

    for url in urls:  
        url = url.strip()
              
    

if __name__ == "__main__":
    main()

