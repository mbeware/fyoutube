#!/usr/bin/env python3
from . import Config
from . import manage_arguments
from .manage_arguments import parse_arguments, load_fyoutube_version

from .Config import messagelog



def main():

  

    args = parse_arguments()
    
    if hasattr(args, 'config_file') and args.config_file:
        try:
            from pathlib import Path
            Config.USER.config_path = Path(args.config_file)
            Config.USER.reload()
            if messagelog:
                messagelog.info(f"Loaded config from: {args.config_file}")
        except Exception as e:
            if messagelog:
                messagelog.error(f"Failed to load config file {args.config_file}: {e}")
            print(f"Failed to load config file {args.config_file}: {e}")
    
    if not args.IAmAPirateAndIWillStarveTheCreators:
        if messagelog :
            messagelog.critical(Config.i_PIRATEMESSAGE)
        print(Config.i_PIRATEMESSAGE)   

    if args.version:
        if messagelog :
            messagelog.info(f"Version = {args.compatibilitymode}")
        else:
            print(f"Version = {args.compatibilitymode}")
    elif args.command == "guiconfig":
        Config.run_config()
    elif args.command == "install":
        Config.run_install()
    elif args.command == "status":
        Config.run_status()
    elif args.command == "set":
        if messagelog :
            messagelog.info("Set mode activated:")
            messagelog.info(args)            
        else:
            print("Set mode activated:")
            print(args)
    elif args.command == "go":
        main_module = load_fyoutube_version(args.compatibilitymode)
        main_module.get_videos()
    else:
        if messagelog :
            messagelog.warning("No command specified. Use -h for help.")
        else:
            print("No command specified. Use -h for help.")
        return


if __name__ == "__main__":
    main()



####
# Todo : Create a RSS feed of magnets to share with others with torrent clients
# Todo : Embed a torrent client.
# Todo : Download from the torrent client before downloading from YouTube
# Todo : Offer to the creator to upload the video directly to the torrent rss feed
