#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.Config import USER, all_options, messagelog

def load_config_to_options(config_file_path=None):
    """Load configuration from TOML file into OptionDescriptor instances"""
    try:
        if config_file_path:
            USER.config_path = config_file_path
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
                            
        if messagelog:
            messagelog.info("Configuration loaded successfully into OptionDescriptor instances")
            
    except Exception as e:
        if messagelog:
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
        
        if messagelog:
            messagelog.info("OptionDescriptor values saved to configuration")
            
    except Exception as e:
        if messagelog:
            messagelog.error(f"Failed to save config: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) > 1:
        load_config_to_options(sys.argv[1])
    else:
        load_config_to_options()
    
    print("Configuration integration test completed successfully")
