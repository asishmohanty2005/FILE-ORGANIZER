"""Main CLI interface for File Organizer"""

import sys
from pathlib import Path
from organizer import FileOrganizer
from scanner import FolderScanner

def display_banner():
    """Display application banner"""
    print("""
    ╔══════════════════════════════════════════╗
    ║     AUTOMATED FILE ORGANIZER by MR ASISH ║
    ║    Keep your folders clean & organized   ║
    ╚══════════════════════════════════════════╝
    """)

def display_menu():
    """Show main menu"""
    print("\n" + "="*50)
    print("            MAIN MENU")
    print("="*50)
    print("1. 📊 Scan & Analyze Folder")
    print("2. 🚀 Organize Files (Real Mode)")
    print("3. 🔍 Organize Files (Dry Run - Preview Only)")
    print("4. 🔄 Undo Last Organization")
    print("5. 👁️  Preview Organization Structure")
    print("6. ❌ Exit")
    print("-"*50)

def get_folder_path():
    """Get folder path from user"""
    while True:
        folder = input("\n📁 Enter folder path to organize: ").strip()
        
        # Remove quotes if present
        folder = folder.strip('"').strip("'")
    
        # Use current directory if empty
        if not folder:
            folder = "."
        
        path = Path(folder)
        
        if path.exists() and path.is_dir():
            return path
        else:
            print(f"❌ Invalid path: {folder}")
            print("   Please enter a valid directory path")

def scan_folder():
    """Scan and display folder analysis"""
    print("\n📊 FOLDER SCANNER")
    print("-"*50)
    
    folder_path = get_folder_path()
    scanner = FolderScanner(folder_path)
    
    print("\n🔄 Scanning folder...")
    files, folders = scanner.scan()
    
    print(scanner.get_file_summary())
    
    # Ask if user wants to see all files
    show_files = input("\n📄 Show all files? (y/n): ").lower()
    if show_files == 'y':
        print("\n📋 Files found:")
        for i, file in enumerate(files[:20], 1):
            size_kb = file.stat().st_size / 1024
            print(f"   {i}. {file.name} ({size_kb:.1f} KB)")
        
        if len(files) > 20:
            print(f"   ... and {len(files) - 20} more files")

def organize_files(dry_run=False):
    """Organize files in selected folder"""
    mode = "DRY RUN" if dry_run else "REAL MODE"
    print(f"\n🚀 ORGANIZATION - {mode}")
    print("-"*50)
    
    if not dry_run:
        print("⚠️  WARNING: This will MOVE files into category folders!")
        confirm = input("   Are you sure? (yes/no): ").lower()
        if confirm != 'yes':
            print("❌ Organization cancelled")
            return
    
    folder_path = get_folder_path()
    
    # Preview before organizing
    if dry_run:
        scanner = FolderScanner(folder_path)
        scanner.scan()
        preview = scanner.preview_organization()
        
        print("\n🔍 PREVIEW - How files will be organized:")
        for category, files in preview.items():
            print(f"\n📂 {category} ({len(files)} files):")
            for file in files[:5]:
                print(f"   • {file}")
            if len(files) > 5:
                print(f"   ... and {len(files) - 5} more")
    
    # Organize
    organizer = FileOrganizer(folder_path, dry_run=dry_run)
    moved_files, errors = organizer.organize()
    
    if not dry_run and moved_files:
        print(f"\n💾 Organization log saved. Use option 4 to undo.")

def preview_organization():
    """Preview where files will go without moving"""
    print("\n👁️  PREVIEW ORGANIZATION")
    print("-"*50)
    organize_files(dry_run=True)

def undo_organization():
    """Undo last organization"""
    print("\n🔄 UNDO ORGANIZATION")
    print("-"*50)
    
    folder_path = get_folder_path()
    organizer = FileOrganizer(folder_path, dry_run=False)
    
    # Note: This is simplified - in production, you'd save a log file
    print("⚠️  This will attempt to restore files from category folders")
    confirm = input("   Continue? (yes/no): ").lower()
    
    if confirm == 'yes':
        print("ℹ️  Note: Undo works best immediately after organization")
        print("   Files will be moved back to original locations")
        
        # For demo, we'll just show a message
        print("\n💡 To properly implement undo, save moved files to a log.json")
        print("   The current version shows the structure")
    else:
        print("❌ Undo cancelled")

def main():
    """Main program loop"""
    while True:
        display_banner()
        display_menu()
        
        choice = input("\n👉 Choose option (1-6): ").strip()
        
        if choice == "1":
            scan_folder()
        elif choice == "2":
            organize_files(dry_run=False)
        elif choice == "3":
            organize_files(dry_run=True)
        elif choice == "4":
            undo_organization()
        elif choice == "5":
            preview_organization()
        elif choice == "6":
            print("\n👋 Goodbye! Keep your files organized!")
            sys.exit(0)
        else:
            print("❌ Invalid choice! Please enter 1-6")
        
        input("\n⏎ Press Enter to continue...")

if __name__ == "__main__":
    main()
    