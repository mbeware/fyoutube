import sys
import subprocess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import Config

from datetime import datetime



def download_video(url:str,cname:str,downloaded_video_archive_file:str,downloaded_video_folder:str,verboselog:str,stdoutlog:str):    

    debuglist=['id','title','playlist_channel_id','playlist_channel''extractor_key','playlist_id','playlist_title','original_url','live_status','is_live','was_live','availability']
    infoprefix='['
    infopostfix=']'
    infoseparator='-'

    stdoutlist=['id','title','playlist_channel']
    debugtemplate=Config.buildtemplate(debuglist,[],infoseparator,infoprefix,infopostfix)
    stdouttemplate=Config.buildtemplate(stdoutlist,[],infoseparator,infoprefix,infopostfix)



    progresslist=['info.title','progress.elapsed', 'progress.eta', 'progress.speed']
    progresstemplate=Config.buildtemplate(progresslist,[],infoseparator,infoprefix,infopostfix)


    cmd:list[str] = [
            'yt-dlp',
            ### Downloaded video
            '--concurrent-fragments','4',            
            '-P',downloaded_video_folder, # videodownloadfolder
            '-o','%(upload_date)s-%(title)s_[%(id)s].%(ext)s',    #filename format        
            '--format','bestvideo*+bestaudio/best',
            '--remux-video', 'mkv',            
            '--xattrs',    
            '--no-check-formats',
            '--no-abort-on-error',
            '--restrict-filenames', 
            '--use-extractors','all', 

            ### Filters
            '--match-filters', "live_status!~=?'post_live|is_live|is_upcoming'",  
            '--match-filters', "availability~=?'unlisted|public'",
            ## Download only videos uploaded <date>. 
            ## The date can be "YYYYMMDD" 
            # or in the format [now|today|yesterday][-N[day|week|month|year]].
            ## E.g. "--date today-2weeks" downloads only videos uploaded on the same day two weeks ago

            #'--date','DATE',
            #'--datebefore','DATE'  ,
            '--dateafter',  'now-3day' , 
            
            ### subtitle
            '-P','subtitle:/tmp/fyoutube/subs',
            '--sub-langs','all,-live_chat',
            '--embed-subs',

            ### sponsor
            '--force-keyframes-at-cuts',
            '--sponsorblock-remove',"sponsor,selfpromo",


            ### Limiter
            '--sleep-subtitles',Config.SLEEP_SUBTITLES,
            '--sleep-interval',Config.SLEEP_INTERVAL,
            '--sleep-requests',Config.SLEEP_REQUESTS,
            '--max-sleep-interval',Config.MAX_SLEEP_INTERVAL,

            ### Keep downloaded list
            '--force-write-archive',
            '--download-archive',downloaded_video_archive_file,

            ### working dir and other mandatory values
            '-P','temp:/tmp/fyoutube/tmp',

            ### logs and feedback
            '--progress',
            ## progress templace can use info about the video with info prefix and progress prefix for progress info
            ## info attributes : <look for fields in doc>
            ## progress attributes : elapsed|speed|eta|total
            '--progress-template','download:'+progresstemplate, 
            ##'--progress-template','download-title:TEMPLATE', progresstemplate
            '--progress-template','postprocess:'+progresstemplate,
            ##'--progress-template','postprocess-title:TEMPLATE',

            '--print',stdouttemplate, # Need --no-simulate to download
            '--no-simulate',
            '--print-to-file',debugtemplate, verboselog,            
            '--quiet',
            '--verbose',
            '--cookies-from-browser', 'brave',

            url,
    ]

 
    try:
        with open(stdoutlog, 'a') as error_file:
            error_file.write("*"*(8*12))
            error_file.write("\n")
            error_file.write(f"{datetime.now().strftime('%H:%M:%S')} - Processing channel: {cname}" )
            error_file.write("\n")
            error_file.flush()

            r=subprocess.run(cmd, check=True, stdout=None, text=True, stderr=error_file )
            error_file.write("\n")
            error_file.flush()
            error_file.write("\n")
            error_file.write(f"{datetime.now().strftime('%H:%M:%S')}" )
            error_file.write("\n")
            error_file.write("🭶🭷🭸🭹🭺🭻🭻🭺🭹🭸🭷🭶"*8)
            error_file.write("\n")
            error_file.flush()
        return r.returncode


    except subprocess.CalledProcessError:
        print(f"Error occurred during download for [{cname}] ")
#        moreinfo(url)
        return 22
  

    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install it first:")
        print("pip install yt-dlp")
        sys.exit(1)
    
    