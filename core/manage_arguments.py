from . import Config
import argparse
from argparse import  Action
from types import ModuleType
from importlib import import_module
from .Config import all_options, messagelog

global g_args


global configurables
configurables:dict[str,str] = {}

configurables_V09:dict[str,str] = {}
for name,val in Config.__dict__.items():
    if not name.startswith('__') and not name.startswith('i_')  and not callable(val):
        configurables_V09[name] = val




configurables_new :dict[str,str] = {
    name: name for name, obj in all_options.items()
    if obj.active
}



def load_fyoutube_version(version:str)->ModuleType:
    global configurables
    compatibility_mode = version if version in Config.i_VERSIONS else "Current"
    if compatibility_mode == "V0.9":
        configurables = configurables_V09
    else:
        configurables = configurables_new

    module_name = Config.i_VERSIONS[compatibility_mode]
    message=f"* using module {module_name} *"
    if messagelog:
        messagelog.info(message)
    else:
        print(message)
    
    if module_name.startswith('fyoutube_'):
        module_name = f"engines.{module_name}"
    
    return import_module(module_name)



def define_arguments(parser:argparse.ArgumentParser)->argparse.ArgumentParser:

    # Hidden optional arguments
    global configurables
    parser.add_argument(
        "--compatibilitymode", "-cm", type=str,
        choices=list(Config.i_VERSIONS.keys()),
        default="Current",
        help=argparse.SUPPRESS
    )
    parser.add_argument("--IAmAPirateAndIWillStarveTheCreators",
        action='store_true',
        default=False,
        help=argparse.SUPPRESS
    )
    parser.add_argument("-V",
        "--version",
        action='store_true',
        default=False
        
    )
    parser.add_argument(
        "--config-file", "-c", type=str,
        help="Specify custom configuration file path"
    )
    helpconfig = "Set configuration options for fyoutube:\n"
    for key in configurables.keys():
        helpconfig += f"--{key} (default: {configurables[key]})\n"
    subparsers = parser.add_subparsers(dest="command", title="Available commands")
    sparser = subparsers.add_parser("set",formatter_class=argparse.RawTextHelpFormatter, add_help=False, help=helpconfig)
    allConfigParams: list[Action|None]=[]
    for configoption in configurables.keys():
        allConfigParams.append(sparser.add_argument(f"--{configoption}", type=str, default=configurables[configoption], help=f"Set {configoption}"))

    sparser = subparsers.add_parser("guiconfig", help="Show GUI configuration dialog")
    sparser = subparsers.add_parser("install",  help="Install fyoutube in the system's scheduler")
    sparser = subparsers.add_parser("status",  help="Display it fyoutube is currently running, and if it is installed in the system's scheduler")
    sparser = subparsers.add_parser("go",  help="Download videos from the configured channels")
    return parser

def parse_arguments():
    global g_args
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="local youtube library",
                                     epilog=Config.i_EPILOG)

    parser = define_arguments(parser)
    g_args = parser.parse_args()
    return  parser.parse_args()

