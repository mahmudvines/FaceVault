#!/usr/bin/env python3
"""
FaceVault External Devices - Quick Start Guide
================================================

This script provides quick commands for external device operations.
Run from the FaceVault directory.
"""

import subprocess
import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def main():
    print_header("FaceVault External Devices Quick Start")
    
    print(f"{BOLD}Welcome!{RESET} This guide will help you get started with external device support.\n")
    
    print("What would you like to do?\n")
    print("1. Run FaceVault with external device support enabled")
    print("2. Scan for connected devices")
    print("3. View external devices documentation")
    print("4. Check Python environment")
    print("5. Exit")
    
    choice = input(f"\n{BOLD}Select an option (1-5): {RESET}").strip()
    
    if choice == "1":
        run_facevault()
    elif choice == "2":
        scan_devices()
    elif choice == "3":
        show_documentation()
    elif choice == "4":
        check_environment()
    elif choice == "5":
        print_info("Goodbye!")
        sys.exit(0)
    else:
        print_error("Invalid option")

def run_facevault():
    print_header("Starting FaceVault")
    
    # Check if Flask is installed
    try:
        import flask
        print_success(f"Flask {flask.__version__} found")
    except ImportError:
        print_error("Flask not installed")
        print("Run: pip install -r requirements.txt")
        return
    
    # Check if external_devices module exists
    if not os.path.exists("external_devices.py"):
        print_error("external_devices.py not found in current directory")
        return
    
    print_success("external_devices.py module found")
    
    print_info("Starting FaceVault server...")
    print_info("Browser will open at http://localhost:5050\n")
    
    try:
        # Run the app
        if sys.platform == "win32":
            os.system("python app.py")
        else:
            os.system("python3 app.py")
    except KeyboardInterrupt:
        print_info("\nFaceVault stopped.")

def scan_devices():
    print_header("Scanning for External Devices")
    
    try:
        from external_devices import get_device_manager
        
        manager = get_device_manager()
        devices = manager.get_all_devices()
        
        if not devices:
            print_warning("No external devices detected")
            print_info("Try:")
            print("  - Plugging in a USB drive")
            print("  - Inserting an SD card")
            print("  - Connecting your phone via USB")
            return
        
        print_success(f"Found {len(devices)} device(s)\n")
        
        for dev in devices:
            icon = get_device_icon(dev['device_type'])
            status = "✓ Ready" if dev['accessible'] else "✗ Not accessible"
            
            print(f"{icon} {dev['label']}")
            print(f"   Type: {dev['device_type'].replace('_', ' ').title()}")
            print(f"   Path: {dev['mount_point']}")
            print(f"   Status: {status}")
            print(f"   Space: {format_bytes(dev['free_space'])} free / {format_bytes(dev['total_space'])} total")
            print()
    
    except ImportError as e:
        print_error(f"Import error: {e}")
    except Exception as e:
        print_error(f"Failed to scan: {e}")

def show_documentation():
    print_header("External Devices Documentation")
    
    doc_path = Path("EXTERNAL_DEVICES_GUIDE.md")
    
    if not doc_path.exists():
        print_error("Documentation not found at EXTERNAL_DEVICES_GUIDE.md")
        return
    
    print_info("Opening documentation...\n")
    
    # Try to open with default viewer
    if sys.platform == "win32":
        os.system(f"start {doc_path}")
    elif sys.platform == "darwin":
        os.system(f"open {doc_path}")
    else:
        print_info(f"View documentation at: {doc_path.absolute()}")
        print("\nOr read it with: cat EXTERNAL_DEVICES_GUIDE.md")

def check_environment():
    print_header("Checking Python Environment")
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}\n")
    
    # Check required modules
    required = [
        ('flask', 'Flask'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
        ('face_recognition', 'face_recognition'),
    ]
    
    optional = [
        ('cv2', 'OpenCV'),
    ]
    
    print_info("Required modules:")
    for module_name, display_name in required:
        try:
            mod = __import__(module_name)
            version = getattr(mod, '__version__', 'unknown')
            print_success(f"{display_name} ({version})")
        except ImportError:
            print_error(f"{display_name} - NOT INSTALLED")
    
    print_info("\nOptional modules:")
    for module_name, display_name in optional:
        try:
            mod = __import__(module_name)
            version = getattr(mod, '__version__', 'unknown')
            print_success(f"{display_name} ({version})")
        except ImportError:
            print_warning(f"{display_name} - not installed (optional)")
    
    print_info("\nDevice detection support:")
    print_info(f"Platform: {sys.platform}")
    
    if sys.platform == "win32":
        try:
            import ctypes
            print_success("Windows API available (for drive detection)")
        except:
            print_warning("Windows API not available")
    else:
        print_success(f"Unix-like system ({sys.platform})")

def get_device_icon(device_type):
    icons = {
        'usb': '💾',
        'sd_card': '💿',
        'mobile': '📱',
        'external_hdd': '🖥',
        'unknown': '💾',
    }
    return icons.get(device_type, icons['unknown'])

def format_bytes(bytes_val):
    if bytes_val == 0:
        return "0 B"
    
    k = 1024
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    
    while bytes_val >= k and i < len(sizes) - 1:
        bytes_val /= k
        i += 1
    
    return f"{bytes_val:.1f} {sizes[i]}"

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_info("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)
