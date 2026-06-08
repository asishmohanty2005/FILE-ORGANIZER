"""Main file organization engine"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from config import get_category, IGNORE_FOLDERS, SKIP_FILES

class FileOrganizer:
    """Organize files by moving them into category folders"""
    
    def __init__(self, folder_path, dry_run=False):
        self.folder_path = Path(folder_path)
        self.dry_run = dry_run  # If True, only simulate (don't actually move)
        self.moved_files = []
        self.errors = []
        self.created_folders = set()
    
    def organize(self):
        """Main orchestration method"""
        print(f"\n{'🔍 DRY RUN MODE' if self.dry_run else '🚀 STARTING ORGANIZATION'}")
        print("="*50)
        
        if not self.folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {self.folder_path}")
        
        # Get all items in folder
        items = list(self.folder_path.iterdir())
        files = [item for item in items if item.is_file() and item.name.lower() not in SKIP_FILES]
        folders_to_skip = set(IGNORE_FOLDERS)
        
        print(f"📁 Found {len(files)} files to organize\n")
        
        # Organize each file
        for file_path in files:
            self._organize_file(file_path, folders_to_skip)
        
        # Print summary
        self._print_summary()
        
        return self.moved_files, self.errors
    
    def _organize_file(self, file_path, folders_to_skip):
        """Move a single file to its appropriate category folder"""
        try:
            # Get file extension and category
            extension = file_path.suffix.lower()
            category = get_category(extension)
            
            # Create category folder path
            category_folder = self.folder_path / category
            
            # Create folder if it doesn't exist (only in real mode)
            if not self.dry_run:
                if category_folder not in self.created_folders:
                    category_folder.mkdir(exist_ok=True)
                    self.created_folders.add(category_folder)
                    print(f"📁 Created folder: {category}")
            
            # Handle duplicate filenames
            destination = category_folder / file_path.name
            if not self.dry_run:
                destination = self._get_unique_filename(destination)
            
            # Move the file
            if self.dry_run:
                print(f"[DRY RUN] Would move: {file_path.name} → {category}/")
                self.moved_files.append((file_path.name, category))
            else:
                shutil.move(str(file_path), str(destination))
                print(f"✅ Moved: {file_path.name} → {category}/")
                self.moved_files.append((file_path.name, category))
                
        except Exception as e:
            error_msg = f"❌ Error moving {file_path.name}: {str(e)}"
            print(error_msg)
            self.errors.append(error_msg)
    
    def _get_unique_filename(self, file_path):
        """Generate unique filename if file already exists"""
        if not file_path.exists():
            return file_path
        
        counter = 1
        stem = file_path.stem
        suffix = file_path.suffix
        parent = file_path.parent
        
        while True:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1
    
    def _print_summary(self):
        """Print organization summary"""
        print("\n" + "="*50)
        print("📊 ORGANIZATION SUMMARY")
        print("="*50)
        
        if self.dry_run:
            print(f"🔍 DRY RUN - No files were actually moved")
        
        print(f"✅ Successfully moved: {len(self.moved_files)} files")
        
        if self.errors:
            print(f"❌ Errors: {len(self.errors)}")
        
        # Group by category
        if self.moved_files:
            print("\n📂 Files organized by category:")
            category_count = {}
            for filename, category in self.moved_files:
                category_count[category] = category_count.get(category, 0) + 1
            
            for category, count in sorted(category_count.items()):
                print(f"   • {category}: {count} file(s)")
    
    def undo(self):
        """Undo the last organization (move files back)"""
        if not self.moved_files:
            print("❌ No files to undo")
            return
        
        print("\n🔄 UNDOING LAST ORGANIZATION")
        print("="*50)
        
        for filename, original_category in self.moved_files:
            source = self.folder_path / original_category / filename
            destination = self.folder_path / filename
            
            if source.exists():
                shutil.move(str(source), str(destination))
                print(f"↩️  Restored: {filename}")
            else:
                print(f"⚠️  Could not find: {filename}")
        
        print(f"\n✅ Undo complete. Restored {len(self.moved_files)} files")
        self.moved_files = []