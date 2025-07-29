
from typing import Any
import logging 
from enum import Enum


import tomli
import tomli_w
from platformdirs import user_config_path
import platformdirs


class DotDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for thekey, thevalue in self.items():
            if isinstance(thevalue, dict):
                self[thekey] = DotDict(thevalue)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __setattr__(self, key, value):
        self[key] = value

    def to_dict(self):
        result = {}
        for thekey, thevalue in self.items():
            if isinstance(thevalue, DotDict):
                result[thekey] = thevalue.to_dict()
            else:
                result[thekey] = thevalue
        return result


class UserConfig:
    def __init__(
        self,
        app_name="fyoutube",
        org_name="mbeware",
        filename="baseconfig.toml",
        default_config=None,
    ):
        from pathlib import Path
        if isinstance(filename, (str, Path)):
            if str(filename).endswith('.toml') and ('/' in str(filename) or '\\' in str(filename)):
                self.config_path = Path(filename)
            else:
                self.config_path = user_config_path(app_name, org_name) / filename
        else:
            self.config_path = user_config_path(app_name, org_name) / filename
        self.default_config = default_config or {"Config": {"Empty":"True"},}
        self._ensure_config_file()
        self.data = self._load()

    def _ensure_config_file(self):
        if not self.config_path.exists():
            print(f"Creating default config at: {self.config_path}")
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with self.config_path.open("wb") as f:
                tomli_w.dump(self.default_config, f)

    def _load(self):
        with self.config_path.open("rb") as f:
            return DotDict(tomli.load(f))

    def save(self):
        """Write current config back to the file."""
        with self.config_path.open("wb") as f:
            tomli_w.dump(self.data.to_dict(), f)

    def reload(self):
        """Reload the config from file."""
        self.data = self._load()

    def __getattr__(self, name):
        return getattr(self.data, name)

    def _resolve(self,value):
        t={}
        lv = value
        while "%-" in lv:
            tplv1=lv.partition("%-")
            tplv2=tplv1[2].partition("-%")
            p1=tplv1[0]
            kw=tplv2[0]
            p2=tplv2[2]
            print(p1,kw,p2)
            lv2=f'{p1}{t[kw]}{p2}'
            print(lv2)
            lv=lv2
        return lv

Config_app_name="fyoutube"
Config_org_name="mbeware"
Config_filename="baseconfig.toml"

#     SelectedFeatures={'KeepDownloadedVideoList':True,'DownloadVideo':True,'AddSubtitles':True,'FilterSponsor':True,'ShowProgress':True, 'stdouttofile':False, "stderrortofile":True, 'verboseToFile': True}

# from dataclasses import dataclass
# @dataclass
# class ParameterConfig:
#     Optional:bool=False
#     DefaultValue:Any|None=None
#     Configurable:bool=True
# @dataclass
# class ParameterValue:
#     current:Any
#     previous:Any
#     changed:bool
#     valid:bool

# @dataclass
# class FeatureParameter:
#     parameter:str
#     config:ParameterConfig
#     value:ParameterValue


# @dataclass
# class FeatureParameterList:
#     feature:str
#     parameters:list[FeatureParameter]
    
#     ParametersValues={}
#     FeatureParameterValues={}
#     AllFeatureParameterValues={}
# 'KeepDownloadedVideoList':{'ParamName':{Optional:False,DefaultValue:3,Configurable:True}','DownloadVideo':True,'AddSubtitles':True,'FilterSponsor':True,'ShowProgress':True, 'stdouttofile':False, "stderrortofile":True, 'verboseToFile': True}


BaseConfig={        
            "Paths": {
                "VIDEO_DIR": f"{platformdirs.user_downloads_path()}", #/mnt/AllVideo/0082-youtube",
                "ARCHIVE_DIR": '%Paths.VIDEO_DIR%/archive',
                "LOGS_DIR": '%Paths.ARCHIVE_DIR%/logs',
                "BASE_DOWNLOAD_LIST" : f'{platformdirs.user_data_path(Config_app_name,Config_org_name)}', #/home/mbeware/Documents/dev/fyoutube',
                "SUBSCRIPTIONS_FILE": '%BASE_DOWNLOAD_LIST%/subscriptions.list',
                "LASTDOWNLOADEDCHANNEL_FILE" : '%BASE_DOWNLOAD_LIST%/lastdownloadedchannel.info',
                
            },
            "Sleep": {
                "SUBTITLES":"1",
                "INTERVAL":"2",
                "REQUESTS":"1",
                "MAX_INTERVAL":"20",
            },
            "Download": {
                "format": "best",
                "quiet": True,
                "force_write_download_archive": True,
                "skip_download": False,
                "subtitleslangs": "all,-live_chat",
                "embedsubtitles": True,
                "noplaylist": False,
                "remuxvideo": "mkv",
                "noprogress": False,
                "xattrs": True,
                "match_filter": "live_status!~=?'post_live|is_live|is_upcoming'&availability~=?'unlisted|public'",
                "ignoreerrors": "only_download",
                "check_formats": "selected",
                "sleep_interval_subtitles": 1,
                "sleep_interval": 10,
                "sleep_interval_requests": 1,
                "max_sleep_interval": 20,
                "download_archive": "************************"
            },
            "Info": {
                "quiet": True,
                "force_write_download_archive": True,
                "skip_download": True,
                "noplaylist": False,
                "forceprint": "%(id)s",
                "extract_flat": "in_playlist",
                "noprogress": False,
                "concurrent_fragment_downloads": 4
            },
            "Debug": {
                "verbose": False,
                "print_to_file": False,
                "restrictfilenames": False,
                "break_on_existing": False,
                "break_per_url": False,
                "force_keyframes_at_cuts": False,
                "ffmpeg_location": ""
            },
            "General": {
                "no_warnings": False,
                "forcejson": False,
                "dump_single_json": False,
                "simulate": False,
                "overwrites": False,
                "writedescription": False,
                "writeinfojson": False,
                "clean_infojson": False,
                "allow_playlist_files": False,
                "writelink": False,
                "writeurllink": False,
                "writewebloclink": False,
                "writedesktoplink": False,
                "writesubtitles": False,
                "writeautomaticsub": False,
                "progress_template": "download"
            }
        }
 


USER = UserConfig(app_name="fyoutube",org_name="mbeware",filename="baseconfig.toml",default_config=BaseConfig)




#@dataclass
class OptionDescriptor:
    name:str|None = None
    description:str|None = None
    active:bool = False
    info:bool = False
    download:bool = False
    debug:bool = False
    info_required:bool = False
    download_required:bool = False
    debug_required:bool = False
    allowed_values:list[str] = []
    download_value:Any|None = None
    info_value:Any|None = None
    debug_value:Any|None = None
    def __init__(self,  
                name:str|None=None,
                description:str|None = None,
                active:bool = False,
                info:bool = False,
                download:bool = False,
                debug:bool = False,
                info_required:bool = False,
                download_required:bool = False,
                debug_required:bool = False,
                allowed_values:list[str] = [],
                download_value:Any|None = None,
                info_value:Any|None = None,
                debug_value:Any|None = None,
                ) -> None:
        self.name:str|None = name
        self.description:str|None = description
        self.active:bool = active
        self.info:bool = info
        self.download:bool = download
        self.debug:bool = debug
        self.info_required:bool = info_required
        self.download_required:bool = download_required
        self.debug_required:bool = debug_required
        self.allowed_values:list[str] = allowed_values
        self.download_value:Any|None = download_value
        self.info_value:Any|None = info_value
        self.debug_value:Any|None = debug_value




verbose=OptionDescriptor(active=True,debug=True)           
quiet=OptionDescriptor(active=True,info=True,download=True)             
no_warnings=OptionDescriptor(active=True)       
forceprint=OptionDescriptor(active=True,info=True)
print_to_file=OptionDescriptor(active=True,info=True,debug=True)     
forcejson=OptionDescriptor(active=True)         
dump_single_json=OptionDescriptor(active=True)  
force_write_download_archive=OptionDescriptor(active=True,info=True,download=True)
simulate=OptionDescriptor(active=True)          
format=OptionDescriptor(active=True,download_required=True)            
check_formats =OptionDescriptor(active=True,download=True)    
paths=OptionDescriptor(active=True,info=True,download=True,allowed_values=['home','temp','chapter','subtitle','thumbnail','description','annotation','infojson','link','pl_video','pl_thumbnail','pl_description','pl_infojson' ])
outtmpl=OptionDescriptor(active=True,download=True,allowed_values=['default','chapter','subtitle','thumbnail','description','annotation','infojson','link','pl_video','pl_thumbnail','pl_description','pl_infojson' ])           
restrictfilenames=OptionDescriptor(active=True,info=True,debug=True,download=True) 
ignoreerrors=OptionDescriptor(active=True,download_required=True)                             
overwrites=OptionDescriptor(active=True)        
writedescription=OptionDescriptor(active=True)  
writeinfojson=OptionDescriptor(active=True)     
clean_infojson=OptionDescriptor(active=True)    
allow_playlist_files=OptionDescriptor(active=True) 
writelink=OptionDescriptor(active=True)         
writeurllink=OptionDescriptor(active=True)      
writewebloclink=OptionDescriptor(active=True)   
writedesktoplink=OptionDescriptor(active=True)  
writesubtitles=OptionDescriptor(active=True)    
writeautomaticsub=OptionDescriptor(active=True) 
subtitleslangs=OptionDescriptor(active=True,download=True)    
skip_download=OptionDescriptor(active=True,info_required=True,download_required=True)     
noplaylist=OptionDescriptor(active=True,download=True,info=True)        
download_archive=OptionDescriptor(active=True,download_required=True)  
break_on_existing=OptionDescriptor(active=True,info=True,debug=True,download=True) 
break_per_url=OptionDescriptor(active=True,info=True,debug=True,download=True)     
extract_flat=OptionDescriptor(active=True,info_required=True)         
sleep_interval_requests=OptionDescriptor(active=True,download_required=True)
sleep_interval=OptionDescriptor(active=True,download_required=True)    
max_sleep_interval=OptionDescriptor(active=True,download_required=True)
sleep_interval_subtitles=OptionDescriptor(active=True,download_required=True) 
match_filter=OptionDescriptor(active=True,download=True)      
progress_template=OptionDescriptor(active=True,allowed_values=['download', 'postprocess','download-title','postprocess-title']) 
force_keyframes_at_cuts=OptionDescriptor(active=True,info=True,debug=True,download=True) 
noprogress=OptionDescriptor(active=True,info=True,download=True)        
ffmpeg_location=OptionDescriptor(active=True,info=True,debug=True,download=True)   
concurrent_fragment_downloads=OptionDescriptor(active=True,info=True)
embedsubtitles=OptionDescriptor(active=True,download=True)
remuxvideo=OptionDescriptor(active=True,download_required=True)
xattrs=OptionDescriptor(active=True,download=True)    

all_options:dict[str,OptionDescriptor] = {
    name: obj for name, obj in globals().items()
    if isinstance(obj, OptionDescriptor)
}

for option_name, option_instance in all_options.items():
    option_instance.name = option_name if None else option_instance.name



SLEEP_SUBTITLES:str ='1'
SLEEP_INTERVAL: str = '10'
SLEEP_REQUESTS: str = '1'
MAX_SLEEP_INTERVAL: str = '20'
VIDEO_DIR: str = '/mnt/AllVideo/0082-youtube'
ARCHIVE_DIR: str = f'{VIDEO_DIR}/archive'
LOGS_DIR: str = f'{ARCHIVE_DIR}/logs'
BASE_DOWNLOAD_LIST : str = '/home/ubuntu/repos/fyoutube'
SUBSCRIPTIONS_FILE: str = f'{BASE_DOWNLOAD_LIST}/subscriptions.list'
LASTDOWNLOADEDCHANNEL_FILE:str = f'{BASE_DOWNLOAD_LIST}/lastdownloadedchannel.info'
GLOBAL_CONFIGDIR:str = str(platformdirs.user_data_path(Config_app_name,Config_org_name) )




### How to read a value : 
## aaa = sleep_interval.info_value if (sleep_interval.info_value is not None and sleep_interval.active and (sleep_interval.info_required or sleep_interval.info)) else None
### Info
concurrent_fragment_downloads.info_value = 4
force_write_download_archive.info_value = True
skip_download.info_value = True
noplaylist.info_value=False
forceprint.info_value='%(id)s'
extract_flat.info_value='in_playlist'
noprogress.info_value=False
quiet.info_value=True
### Download 
sleep_interval_subtitles.download_value = 1
sleep_interval.download_value = 10
sleep_interval_requests.download_value = 1
max_sleep_interval.download_value = 20
force_write_download_archive.download_value = True
skip_download.download_value = False
subtitleslangs.download_value= 'all,-live_chat'
embedsubtitles.download_value=True
noplaylist.download_value=False
remuxvideo.download_value='mkv'
noprogress.download_value=False
xattrs.download_value=True
match_filter.download_value= "live_status!~=?'post_live|is_live|is_upcoming'&availability~=?'unlisted|public'"
ignoreerrors.download_value='only_download'
check_formats.download_value= 'selected'
quiet.download_value=True
paths.download_value={'home':VIDEO_DIR,
                      'temp':'tmp',
                      'subtitle':'subs',
                      'pl_video':VIDEO_DIR,
                      }
outtmpl.download_value={'default':'[%(upload_date)s]-[%(uploader)s]_[%(title)s].%(ext)s'}
download_archive.download_value="************************"





i_PIRATEMESSAGE = "\033[1m\033[93m\033[41mUsing this tool means that the video creators are not getting paid for their work, so please consider supporting them directly.\033[0m"
i_EPILOG:str ="This is a tool using yt-dlp to download videos from YouTube and store them locally to watch them offline, without ads, and without relying on YouTube's servers."
i_EPILOG += "\n" + i_PIRATEMESSAGE



i_BASENAME = 'fyoutube'
i_VERSIONS: dict[str, str] = {
 # Version   :   ModuleName without the .py extension
    'dev'   :  f'{i_BASENAME}_main',
    'V0.9'    :   f'{i_BASENAME}_V09',
    'Current':   f'{i_BASENAME}_V09',     
        }



def run_config():
    try:
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from gui.config_editor import ConfigEditor
        import tkinter as tk
        root = tk.Tk()
        app = ConfigEditor(root)
        root.mainloop()
    except ImportError as e:
        messagelog.error(f"GUI dependencies not available: {e}")
        print("GUI configuration not available. Please install required dependencies.")
    except Exception as e:
        messagelog.error(f"Error launching GUI: {e}")
        print(f"Error launching GUI configuration: {e}")

def run_install():
    print("Running installation process...")

def run_status():
    print("Checking installation status...")

global messagelog
global channel_info_log_handler
global channel_debug_log_handler
global messagelog_formatter 

channel_info_log_handler:logging.Handler|None=None
channel_debug_log_handler:logging.Handler|None=None

messagelog_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

messagelog = logging.getLogger("fyoutube")
messagelog.setLevel(logging.DEBUG)

general_handler = logging.FileHandler(f"{LOGS_DIR}/fyoutube.info.log")
general_handler.setLevel(logging.INFO)
general_handler.setFormatter(messagelog_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(messagelog_formatter)

messagelog.addHandler(general_handler)
messagelog.addHandler(console_handler)


def log_channel(channel_name:str):
    global messagelog
    global channel_info_log_handler
    global channel_debug_log_handler
    if channel_info_log_handler:
        messagelog.removeHandler(channel_info_log_handler)
        channel_info_log_handler=None
    if channel_debug_log_handler:
        messagelog.removeHandler(channel_debug_log_handler)
        channel_debug_log_handler=None
    
    channel_info_log_handler = logging.FileHandler(f"{LOGS_DIR}/{channel_name}_info.log")
    channel_debug_log_handler = logging.FileHandler(f"{LOGS_DIR}/{channel_name}_debug.log")
    channel_info_log_handler.setLevel(logging.INFO)
    channel_info_log_handler.setFormatter(messagelog_formatter)
    channel_debug_log_handler.setLevel(logging.DEBUG)
    channel_debug_log_handler.setFormatter(messagelog_formatter)
    messagelog.addHandler(channel_info_log_handler)
    messagelog.addHandler(channel_debug_log_handler)

class Request_type(Enum):
    DOWNLOAD_ALL_CHANNEL = 'DOWNLOAD_CHANNEL'
    DOWNLOAD_ALL_LIST = 'DOWNLOAD_LIST'
    LIST_VIDEO_CHANNEL = 'LIST_VIDEO_CHANNEL'
    LIST_VIDEO_PLAYLIST ='LIST_VIDEO_PLAYLIST'
    LIST_VIDEO_RSS ='LIST_VIDEO_RSS'
    LIST_RSS_CHANNEL ='LIST_RSS_CHANNEL'
    LIST_RSS_PLAYLIST ='LIST_RSS_PLAYLIST'
    


def build_options(request_type:Request_type|None)->dict[str,Any]:
    selected_options:dict[str,Any]={}

    for option_name,option in all_options.items():
        if (option.download_value is not None and option.active and (option.download_required or option.download)):
            selected_options[option_name]=option.download_value
            messagelog.debug(f'{option_name=}-{option.download_value=}-{type(option.download_value)=}')
    return selected_options
    

def get_channel_name(channel_url:str)->str:
    sep=None
    if '@' in channel_url:
        sep = '@'
    elif '?' in channel_url:
        sep = '?'
    cname = channel_url.split(sep)[1] if sep else channel_url
    return cname


def buildtemplate(nuggetlist:list, bannednuggetlist:list=[], separator:str|None=None,prefix:str|None=None,postfix:str|None=None):
    template = ""
    for nugget in nuggetlist:
        if nugget not in bannednuggetlist:
            if prefix:
                template += prefix
            template += f'%({nugget})s'    
            if postfix:
                template += postfix
            if separator:
                template += separator
    return template

def load_config_to_options(config_file_path=None):
    """Load configuration from TOML file into OptionDescriptor instances"""
    try:
        if config_file_path:
            from pathlib import Path
            USER.config_path = Path(config_file_path)
            USER.reload()
        
        for section_name in ["Download", "Info", "Debug", "General"]:
            if hasattr(USER, section_name):
                section_config = getattr(USER, section_name)
                
                for option_name, option in all_options.items():
                    if option_name in section_config:
                        value = section_config[option_name]
                        
                        if section_name == "Download" and (option.download or option.download_required):
                            option.download_value = value
                        elif section_name == "Info" and (option.info or option.info_required):
                            option.info_value = value
                        elif section_name == "Debug" and option.debug:
                            option.debug_value = value
                            
        messagelog.info("Configuration loaded successfully into OptionDescriptor instances")
            
    except Exception as e:
        messagelog.error(f"Failed to load config: {e}")
        raise

def save_options_to_config():
    """Save OptionDescriptor values back to TOML configuration"""
    try:
        for section_name in ["Download", "Info", "Debug", "General"]:
            if not hasattr(USER, section_name):
                setattr(USER, section_name, {})
            
            section_config = getattr(USER, section_name)
            
            for option_name, option in all_options.items():
                if section_name == "Download" and option.download_value is not None:
                    section_config[option_name] = option.download_value
                elif section_name == "Info" and option.info_value is not None:
                    section_config[option_name] = option.info_value
                elif section_name == "Debug" and option.debug_value is not None:
                    section_config[option_name] = option.debug_value
        
        USER.save()
        messagelog.info("OptionDescriptor values saved to configuration")
            
    except Exception as e:
        messagelog.error(f"Failed to save config: {e}")
        raise
