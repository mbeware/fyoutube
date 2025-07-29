#!/usr/bin/env python3
from importlib import import_module
from inspect import getmembers
from engines.fyoutube_download import download_video
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.Config import get_channel_name
import os
from datetime import datetime

def main():
    MODULE_NAME = 'fyoutube_select'
    testing_module = import_module(MODULE_NAME)

    testing_feature = "InfoFromPlaylist"

    ListMFDFolder="/tmp/fyoutube"
    ListMFDFile="ArchiveMarkedForDownload"
    ListMFDExtension=".list"

    DOWNLOADEDVIDEOLIST="/tmp/fyoutube/Archivedownloadedvideo.list"


    all = getmembers(testing_module)
    
    all_dict = dict(all)

    ChannelURL = "https://www.youtube.com/@LinusTechTips"
    cname = get_channel_name(ChannelURL)
    ArchiveListMFDFileForChannel = f'{ListMFDFolder}/{ListMFDFile}_{cname}{ListMFDExtension}'
    urls=all_dict[testing_feature](ChannelURL,cname,ArchiveListMFDFileForChannel)
    downloadfolder = f'{ListMFDFolder}/vid/{cname}' #downloaded_video_folder 
    verboselog = f'{ListMFDFolder}/verbose.{cname}.log'
    stroutlog = f'{ListMFDFolder}/stdout.{cname}.log'
    print(f"{datetime.now().strftime('%H:%M:%S')} - Processing channel: {cname}\n" )

    for url in urls:  
        url = url.strip()
        if url and url != "": 
            print(f"{datetime.now().strftime('%H:%M:%S')} - Processing video : {url}" )
            os.makedirs(downloadfolder, exist_ok=True)
            download_video( url,
                            cname, #cname
                            DOWNLOADEDVIDEOLIST, #downloaded_video_archive_file
                            downloadfolder, #downloaded_video_folder
                            verboselog, #verboselog
                            stroutlog #stdoutlog
            )
               
    

if __name__ == "__main__":
    main()

