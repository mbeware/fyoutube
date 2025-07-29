#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.Config import USER, all_options, load_config_to_options, save_options_to_config
import tempfile

def test_config_loading():
    """Test that config loading works correctly"""
    print("Testing config loading...")
    
    try:
        USER.reload()
        print("✓ Config loaded successfully")
        
        print(f"Available sections: {[attr for attr in dir(USER) if not attr.startswith('_')]}")
        
        if hasattr(USER, 'Paths'):
            print(f"✓ Paths section found: {USER.Paths}")
        
        if hasattr(USER, 'Download'):
            print(f"✓ Download section found with {len(USER.Download)} options")
            
        return True
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        return False

def test_option_descriptors():
    """Test that OptionDescriptor instances are working"""
    print("\nTesting OptionDescriptor instances...")
    
    try:
        print(f"Found {len(all_options)} OptionDescriptor instances")
        
        download_options = [name for name, opt in all_options.items() if opt.download or opt.download_required]
        info_options = [name for name, opt in all_options.items() if opt.info or opt.info_required]
        debug_options = [name for name, opt in all_options.items() if opt.debug]
        
        print(f"✓ Download options: {len(download_options)}")
        print(f"✓ Info options: {len(info_options)}")
        print(f"✓ Debug options: {len(debug_options)}")
        
        return True
    except Exception as e:
        print(f"✗ OptionDescriptor test failed: {e}")
        return False

def test_config_integration():
    """Test config integration functions"""
    print("\nTesting config integration...")
    
    try:
        load_config_to_options()
        print("✓ Config loaded to options successfully")
        
        save_options_to_config()
        print("✓ Options saved to config successfully")
        
        return True
    except Exception as e:
        print(f"✗ Config integration failed: {e}")
        return False

def test_custom_config_file():
    """Test custom config file loading"""
    print("\nTesting custom config file...")
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write("""
[Paths]
VIDEO_DIR = "/tmp/test_videos"

[Download]
quiet = false
format = "worst"
""")
            temp_config = f.name
        
        original_path = USER.config_path
        load_config_to_options(temp_config)
        USER.config_path = original_path
        
        print("✓ Custom config file loaded successfully")
        os.unlink(temp_config)
        return True
    except Exception as e:
        print(f"✗ Custom config file test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== fyoutube Configuration System Test ===\n")
    
    tests = [
        test_config_loading,
        test_option_descriptors,
        test_config_integration,
        test_custom_config_file
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results: {passed}/{len(tests)} passed ===")
    
    if passed == len(tests):
        print("✓ All tests passed! Configuration system is working correctly.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check the implementation.")
        sys.exit(1)
