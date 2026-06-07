"""
External Device Detection and Management for FaceVault
Supports: USB drives, SD cards, mobile devices, external hard drives
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional


class ExternalDevice:
    """Represents an external device (USB, SD card, mobile, etc.)"""
    
    def __init__(self, mount_point: str, label: str = "", device_type: str = "unknown"):
        self.mount_point = mount_point
        self.label = label or os.path.basename(mount_point)
        self.device_type = device_type  # usb, sd_card, mobile, external_hdd, etc.
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        try:
            total, used, free = self.get_space()
        except:
            total = used = free = 0
        
        return {
            "mount_point": self.mount_point,
            "label": self.label,
            "device_type": self.device_type,
            "total_space": total,
            "used_space": used,
            "free_space": free,
            "accessible": self.is_accessible()
        }
    
    def is_accessible(self) -> bool:
        """Check if device is accessible"""
        return os.path.exists(self.mount_point) and os.access(self.mount_point, os.R_OK)
    
    def get_space(self) -> tuple:
        """Get space info in bytes (total, used, free)"""
        try:
            if not self.is_accessible():
                return 0, 0, 0
            
            if sys.platform == "win32":
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                total_bytes = ctypes.c_ulonglong(0)
                used_bytes = ctypes.c_ulonglong(0)
                
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(self.mount_point),
                    None,
                    ctypes.pointer(total_bytes),
                    ctypes.pointer(free_bytes)
                )
                
                total = total_bytes.value
                free = free_bytes.value
                used = total - free
                return total, used, free
            else:
                import shutil
                stat = shutil.disk_usage(self.mount_point)
                return stat.total, stat.used, stat.free
        except:
            return 0, 0, 0
    
    def find_images(self, extensions: set = None) -> List[str]:
        """Find all image files on device"""
        if extensions is None:
            extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
        
        if not self.is_accessible():
            return []
        
        images = []
        try:
            for root, dirs, files in os.walk(self.mount_point):
                # Skip hidden and system directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if Path(file).suffix.lower() in extensions:
                        images.append(os.path.join(root, file))
        except PermissionError:
            pass
        
        return images


class DeviceManager:
    """Manages detection and tracking of external devices"""
    
    def __init__(self):
        self.devices: Dict[str, ExternalDevice] = {}
        self._config_file = "external_devices_config.json"
    
    def scan_devices(self) -> List[ExternalDevice]:
        """Scan for connected external devices"""
        devices = []
        
        if sys.platform == "win32":
            devices.extend(self._scan_windows())
        elif sys.platform == "darwin":
            devices.extend(self._scan_macos())
        else:
            devices.extend(self._scan_linux())
        
        # Store devices
        self.devices = {dev.mount_point: dev for dev in devices}
        return devices
    
    def _scan_windows(self) -> List[ExternalDevice]:
        """Scan for devices on Windows"""
        import ctypes
        from ctypes import wintypes
        
        devices = []
        
        # Get drive letters
        drive_letters = []
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            if bitmask & 1:
                drive_letters.append(f"{letter}:\\")
            bitmask >>= 1
        
        print(f"[DeviceManager] Found drive letters: {drive_letters}")
        
        for drive in drive_letters:
            try:
                # Skip C: (system drive)
                if drive.upper() == "C:\\":
                    continue
                
                # Check if drive exists and is accessible
                if not os.path.exists(drive):
                    continue
                
                try:
                    # Check if we can read it
                    os.listdir(drive)
                except (PermissionError, OSError):
                    print(f"[DeviceManager] Skipping {drive} - not accessible")
                    continue
                
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
                label = self._get_volume_label(drive)
                
                print(f"[DeviceManager] Drive {drive}: type={drive_type}, label={label}")
                
                # Include removable drives (2), fixed drives (3), and network drives (4)
                # Type: 2=removable, 3=fixed, 4=remote, 5=optical, 6=ramdisk
                if drive_type in [2, 3, 4]:  # Include fixed drives (likely external HDDs)
                    device_type = self._detect_device_type(drive)
                    devices.append(ExternalDevice(drive, label, device_type))
                    print(f"[DeviceManager] Added device: {drive} ({device_type})")
            except Exception as e:
                print(f"[DeviceManager] Error scanning {drive}: {e}")
        
        print(f"[DeviceManager] Windows scan complete. Found {len(devices)} devices")
        return devices
    
    def _scan_linux(self) -> List[ExternalDevice]:
        """Scan for devices on Linux"""
        devices = []
        
        # Check /media and /mnt directories
        for base_path in ["/media", "/mnt"]:
            if os.path.exists(base_path):
                try:
                    for entry in os.listdir(base_path):
                        mount_point = os.path.join(base_path, entry)
                        if os.path.isdir(mount_point) and os.access(mount_point, os.R_OK):
                            device_type = "usb" if "/media" in mount_point else "external_hdd"
                            devices.append(ExternalDevice(mount_point, entry, device_type))
                except PermissionError:
                    pass
        
        return devices
    
    def _scan_macos(self) -> List[ExternalDevice]:
        """Scan for devices on macOS"""
        devices = []
        
        volumes_path = "/Volumes"
        try:
            for entry in os.listdir(volumes_path):
                if entry != "Macintosh HD":  # Skip system drive
                    mount_point = os.path.join(volumes_path, entry)
                    if os.path.isdir(mount_point) and os.access(mount_point, os.R_OK):
                        devices.append(ExternalDevice(mount_point, entry, "external_hdd"))
        except:
            pass
        
        return devices
    
    def _get_volume_label(self, drive: str) -> str:
        """Get the label of a Windows drive"""
        try:
            import ctypes
            from ctypes import wintypes
            
            volume_name_buffer = ctypes.create_unicode_buffer(1024)
            ctypes.windll.kernel32.GetVolumeInformationW(
                ctypes.c_wchar_p(drive),
                volume_name_buffer,
                ctypes.sizeof(volume_name_buffer),
                None, None, None, None, 0
            )
            return volume_name_buffer.value or drive.rstrip("\\")
        except:
            return drive.rstrip("\\")
    
    def _is_external_drive(self, drive: str) -> bool:
        """Check if a fixed drive is external (not system drive)"""
        try:
            import ctypes
            
            # Get volume serial number and other info
            volume_name = ctypes.create_unicode_buffer(1024)
            serial = ctypes.c_uint32()
            
            result = ctypes.windll.kernel32.GetVolumeInformationW(
                ctypes.c_wchar_p(drive),
                volume_name,
                ctypes.sizeof(volume_name),
                ctypes.pointer(serial),
                None, None, None, 0
            )
            
            # If it's not the C: drive, it's likely external
            return drive.upper() != "C:\\"
        except:
            return False
    
    def _detect_device_type(self, drive: str) -> str:
        """Detect the type of removable device"""
        label = self._get_volume_label(drive).upper()
        
        if "MOBILE" in label or "ANDROID" in label or "IPHONE" in label:
            return "mobile"
        elif "SD" in label or "MICROSD" in label:
            return "sd_card"
        elif "THUMB" in label or "STICK" in label:
            return "usb"
        else:
            return "usb"  # Default to USB
    
    def get_all_devices(self) -> List[Dict]:
        """Get all available external devices"""
        self.scan_devices()
        return [dev.to_dict() for dev in self.devices.values()]
    
    def get_device(self, mount_point: str) -> Optional[ExternalDevice]:
        """Get a specific device"""
        return self.devices.get(mount_point)
    
    def add_favorite(self, mount_point: str, label: str = "") -> None:
        """Add device to favorites"""
        config = self._load_config()
        if "favorites" not in config:
            config["favorites"] = []
        
        if mount_point not in config["favorites"]:
            config["favorites"].append({
                "mount_point": mount_point,
                "label": label or mount_point,
                "added_at": str(Path.ctime)
            })
        
        self._save_config(config)
    
    def get_favorites(self) -> List[Dict]:
        """Get favorite devices"""
        config = self._load_config()
        return config.get("favorites", [])
    
    def _load_config(self) -> Dict:
        """Load device configuration"""
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_config(self, config: Dict) -> None:
        """Save device configuration"""
        try:
            with open(self._config_file, "w") as f:
                json.dump(config, f, indent=2)
        except:
            pass


# Global instance
_device_manager = None

def get_device_manager() -> DeviceManager:
    """Get or create the global device manager"""
    global _device_manager
    if _device_manager is None:
        _device_manager = DeviceManager()
    return _device_manager
