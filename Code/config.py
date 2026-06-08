"""File categories and extension mappings"""

# Map file extensions to folder names
CATEGORIES = {
    # Images
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".ico", ".webp"],
    
    # Documents
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".tex", ".wpd", ".md"],
    
    # Spreadsheets
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods", ".numbers"],
    
    # Presentations
    "Presentations": [".ppt", ".pptx", ".key", ".odp"],
    
    # Videos
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg"],
    
    # Music
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
    
    # Archives
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso"],
    
    # Code & Scripts
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".rb", ".go", ".json", ".xml", ".sql"],
    
    # Executables
    "Executables": [".exe", ".msi", ".app", ".deb", ".rpm", ".sh", ".bat", ".cmd"],
    
    # Fonts
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".fnt"],
    
    # Others (will go to "Misc" folder)
}

# Special folders to ignore (don't organize these)
IGNORE_FOLDERS = [
    "Images", "Documents", "Spreadsheets", "Presentations", 
    "Videos", "Music", "Archives", "Code", "Executables", 
    "Fonts", "Misc", "Organized_Logs"
]

# Files to skip (don't move these)
SKIP_FILES = [".ds_store", "thumbs.db", "desktop.ini"]

# Get category for a file extension
def get_category(file_extension):
    """Return category name for given file extension"""
    file_extension = file_extension.lower()
    
    for category, extensions in CATEGORIES.items():
        if file_extension in extensions:
            return category
    
    return "Misc"  # Default folder for unknown file types

# Get all registered extensions
def get_all_extensions():
    """Return list of all tracked extensions"""
    all_extensions = []
    for extensions in CATEGORIES.values():
        all_extensions.extend(extensions)
    return all_extensions