import sys
import subprocess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import Config

def InfoFromPlaylist(url):    
    cname = Config.get_channel_name(url)
    print(f"Processing channel: {cname}" )
    cmd = [
            'yt-dlp',
            # Removed sleep options as they are not needed for just IDs
            '--concurrent-fragments','4', # This might still be useful for processing multiple playlists/channels
            '--force-write-archive',
            '--skip-download',  # Still skip downloading videos
            '-P','/mnt/AllVideo/0082-youtube', # These paths are still relevant if you use them for other purposes
            '-P','temp:tmp',
            '--download-archive',f'/mnt/AllVideo/0082-youtube/archive_{cname}.md',
            '--yes-playlist',
            '-O','%(id)s', # Output only the video ID
            '--flat-playlist', # This is crucial for faster ID extraction from playlists
            '--print-to-file', '%(id)s', f'/home/mbeware/Documents/dev/fyoutube/ids/ids_for_{cname}', 
            url,
    ]       
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False) # Keep capture_output=False if you want to see yt-dlp's progress
        if result.returncode == 0:
            print("Info retrieval completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during Info: {e}")
        print("Make sure yt-dlp is installed and the playlist URL is valid.")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: yt-dlp not found. Please install it first:")
        print("pip install yt-dlp")
        sys.exit(1)

def main():
    urls = []
    with open('/home/mbeware/Documents/dev/fyoutube/subscriptions.md', 'r') as f:
        urls = f.readlines()    
    for url in urls:   
        url = url.strip()
        if url: # Check if the line is not empty
            InfoFromPlaylist(url)
    

if __name__ == "__main__":
    main()
