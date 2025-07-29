#!/usr/bin/env python3
"""
Setup script to create the required directory structure for fyoutube.
This script creates all necessary folders for video downloads, archives, logs, etc.
"""

import os
import sys
from pathlib import Path


def create_directory_structure():
    """Create the complete directory structure needed for fyoutube."""
    
    # Base directory structure
    base_dirs = [
        "/mnt/AllVideo/0082-youtube",
        "/mnt/AllVideo/0082-youtube/archive",
        "/mnt/AllVideo/0082-youtube/archive/logs", 
        "/mnt/AllVideo/0082-youtube/config",
        "/mnt/AllVideo/0082-youtube/subs",
        "/mnt/AllVideo/0082-youtube/tmp"
    ]
    
    print("🚀 Setting up fyoutube directory structure...")
    
    created_dirs = []
    existing_dirs = []
    
    for dir_path in base_dirs:
        path = Path(dir_path)
        
        if path.exists():
            existing_dirs.append(dir_path)
            print(f"✅ Already exists: {dir_path}")
        else:
            try:
                # Create directory with parents, set appropriate permissions
                path.mkdir(parents=True, exist_ok=True)
                
                # Set permissions to be writable by the user
                os.chmod(path, 0o755)
                
                created_dirs.append(dir_path)
                print(f"📁 Created: {dir_path}")
                
            except PermissionError:
                print(f"❌ Permission denied creating: {dir_path}")
                print(f"   Try running with sudo: sudo python3 {sys.argv[0]}")
                return False
            except Exception as e:
                print(f"❌ Error creating {dir_path}: {e}")
                return False
    
    # Summary
    print("\n📊 Setup Summary:")
    print(f"   📁 Created directories: {len(created_dirs)}")
    print(f"   ✅ Existing directories: {len(existing_dirs)}")
    
    if created_dirs:
        print("\n🆕 Newly created directories:")
        for dir_path in created_dirs:
            print(f"   • {dir_path}")
    
    if existing_dirs:
        print("\n♻️  Already existing directories:")
        for dir_path in existing_dirs:
            print(f"   • {dir_path}")
    
    print("\n🎉 Directory setup completed successfully!")
    print("\n💡 Directory structure:")
    print("   /mnt/AllVideo/0082-youtube/")
    print("   ├── archive/")
    print("   │   └── logs/")
    print("   ├── config/")
    print("   ├── subs/")
    print("   └── tmp/")
    
    return True


def verify_structure():
    """Verify that all required directories exist and are writable."""
    
    required_dirs = [
        "/mnt/AllVideo/0082-youtube",
        "/mnt/AllVideo/0082-youtube/archive",
        "/mnt/AllVideo/0082-youtube/archive/logs",
        "/mnt/AllVideo/0082-youtube/config", 
        "/mnt/AllVideo/0082-youtube/subs",
        "/mnt/AllVideo/0082-youtube/tmp"
    ]
    
    print("\n🔍 Verifying directory structure...")
    
    all_good = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        
        if not path.exists():
            print(f"❌ Missing: {dir_path}")
            all_good = False
        elif not path.is_dir():
            print(f"❌ Not a directory: {dir_path}")
            all_good = False
        elif not os.access(path, os.W_OK):
            print(f"⚠️  Not writable: {dir_path}")
            all_good = False
        else:
            print(f"✅ OK: {dir_path}")
    
    return all_good


def main():
    """Main function to set up and verify the directory structure."""
    
    print("🎯 fyoutube Directory Setup Script")
    print("=" * 50)
    
    # Create directories
    if not create_directory_structure():
        print("\n❌ Setup failed!")
        sys.exit(1)
    
    # Verify setup
    if verify_structure():
        print("\n✅ All directories verified successfully!")
        print("\n🚀 fyoutube is ready to use!")
    else:
        print("\n⚠️  Some directories have issues. Please check permissions.")
        sys.exit(1)


if __name__ == "__main__":
    main()