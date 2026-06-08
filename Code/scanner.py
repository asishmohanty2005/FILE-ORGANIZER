"""Folder scanning and file analysis utilities"""

import os
from pathlib import Path
from datetime import datetime
from config import IGNORE_FOLDERS, SKIP_FILES

class FolderScanner:
    """Scan and analyze folder contents"""
    
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)
        self.files = []
        self.folders = []
        self.stats = {
            "total_files": 0,
            "total_folders": 0,
            "files_by_type": {},
            "total_size_bytes": 0
        }
    
    def scan(self):
        """Scan folder and collect all files and subfolders"""
        if not self.folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {self.folder_path}")
        
        for item in self.folder_path.iterdir():
            if item.is_file():
                # Skip system files
                if item.name.lower() not in SKIP_FILES:
                    self.files.append(item)
                    self.stats["total_files"] += 1
                    self.stats["total_size_bytes"] += item.stat().st_size
                    
                    # Track by extension
                    ext = item.suffix.lower()
                    if ext:
                        self.stats["files_by_type"][ext] = self.stats["files_by_type"].get(ext, 0) + 1
                    
            elif item.is_dir() and item.name not in IGNORE_FOLDERS:
                self.folders.append(item)
                self.stats["total_folders"] += 1
        
        return self.files, self.folders
    
    def get_file_summary(self):
        """Return formatted summary of scan results"""
        summary = f"""
📊 SCAN SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Folder: {self.folder_path}
📁 Total folders: {self.stats['total_folders']}
📄 Total files: {self.stats['total_files']}
💾 Total size: {self._format_size(self.stats['total_size_bytes'])}
        """
        
        if self.stats['files_by_type']:
            summary += "\n📂 File types found:\n"
            for ext, count in sorted(self.stats['files_by_type'].items(), key=lambda x: x[1], reverse=True)[:10]:
                summary += f"   • {ext or 'NO EXTENSION'}: {count} file(s)\n"
        
        return summary
    
    def _format_size(self, size_bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def preview_organization(self):
        """Preview where files would be organized"""
        from config import get_category
        
        preview = {}
        for file_path in self.files:
            ext = file_path.suffix.lower()
            category = get_category(ext)
            
            if category not in preview:
                preview[category] = []
            preview[category].append(file_path.name)
        
        return preview