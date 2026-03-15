#!/usr/bin/env python3
"""
Google Drive Media Downloader for Nested Language Folders
Downloads specific language images and audio files with file range support
Run this before generate_videos_with_bg.py to automatically fetch media
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import logging
import re

# Check if gdown command-line tool is available
try:
    result = subprocess.run(['gdown', '--version'], 
                          capture_output=True, 
                          text=True,
                          check=False)
    if result.returncode != 0:
        raise FileNotFoundError
except FileNotFoundError:
    print("❌ Error: 'gdown' command-line tool is not found")
    print("📦 Install it with: brew install gdown")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class GoogleDriveDownloader:
    """Download media files from Google Drive nested language folders"""
    
    # Base paths - automatically detect script location (works on any machine)
    BASE_PATH = Path(__file__).parent.resolve()
    INPUT_IMAGES_FOLDER = BASE_PATH / "input" / "images"
    INPUT_AUDIO_FOLDER = BASE_PATH / "input" / "audio"
    INPUT_BACKGROUND_FOLDER = BASE_PATH / "input" / "background"
    TEMP_DOWNLOAD_FOLDER = BASE_PATH / "temp_download"
    
    # ======================================================================
    # 🔧 CONFIGURATION - Language Folder IDs
    # ======================================================================
    
    # HOW TO GET FOLDER IDs:
    # 1. Navigate in Google Drive: Srisatupasi > GG KANNADA
    # 2. Right-click on "KANNADA jpg files" folder → Share → Get link
    #    Example link: https://drive.google.com/drive/folders/1AbC2dEf3GhI4jKl5MnO
    #    Extract ID: 1AbC2dEf3GhI4jKl5MnO ← Paste this below in images_folder_id
    # 3. Right-click on "Final KANNADA audio files" folder → Share → Get link
    #    Extract ID and paste in audio_folder_id
    # 4. Make sure both folders are shared with "Anyone with the link can view"
    
    # Language configurations: Each language maps to its deepest-level folder IDs
    
    LANGUAGE_CONFIG = {
        'ENGLISH': {
            'code': 'GGENG',           # File prefix (e.g., GGENG001.jpg)
            'images_folder_id': '1WM3BmU46pRya1ZloxZJ---HbU_phALlZ',    # ID of "ENGLISH jpg files" folder (inside GG ENGLISH folder)
            'audio_folder_id': '1luI0MuvI5NnRh8Oh-0b6NWAJ8SAaWU2R',     # ID of "Final ENGLISH audio files" folder (inside GG ENGLISH folder)
            'digits': 3                # Number of digits in filename (GGENG001 = 3 digits)
        },
        'KANNADA': {
            'code': 'GGKND',           # File prefix (e.g., GGKND001.jpg)
            'images_folder_id': '',    # ID of "KANNADA jpg files" folder (inside GG KANNADA folder)
            'audio_folder_id': '',     # ID of "Final KANNADA audio files" folder (inside GG KANNADA folder)
            'digits': 3                # Number of digits in filename (GGKND001 = 3 digits)
        },
        'TELUGU': {
            'code': 'GGTLG',           # File prefix (e.g., GGTLG001.jpg)
            'images_folder_id': '',    # ID of "TELUGU jpg files" folder (inside GG TELUGU folder)
            'audio_folder_id': '',     # ID of "Final TELUGU audio files" folder (inside GG TELUGU folder)
            'digits': 3
        },
        'HINDI': {
            'code': 'GGHND',           # File prefix (e.g., GGHND001.jpg)
            'images_folder_id': '',    # ID of "HINDI jpg files" folder (inside GG HINDI folder)
            'audio_folder_id': '',     # ID of "Final HINDI audio files" folder (inside GG HINDI folder)
            'digits': 3
        },
        'MARATHI': {
            'code': 'GGMRT',           # File prefix (e.g., GGMRT001.jpg)
            'images_folder_id': '',    # ID of "MARATHI jpg files" folder (inside GG MARATHI folder)
            'audio_folder_id': '',     # ID of "Final MARATHI audio files" folder (inside GG MARATHI folder)
            'digits': 3
        },
        'TAMIL': {
            'code': 'GGTML',           # File prefix (e.g., GGTML001.jpg)
            'images_folder_id': '',    # ID of "TAMIL jpg files" folder (inside GG TAMIL folder)
            'audio_folder_id': '',     # ID of "Final TAMIL audio files" folder (inside GG TAMIL folder)
            'digits': 3
        },
        # Add more languages as needed following the same pattern
    }
    
    # Optional: Background music file ID (single file)
    BACKGROUND_FILE_ID = ""  # Example: "1u2v3w4x5y6z7a8b9c0d"
    BACKGROUND_FILENAME = "background.mp3"
    
    # ======================================================================
    
    def __init__(self, language: str = None, start_num: int = None, end_num: int = None):
        """
        Initialize the downloader
        
        Args:
            language: Language to download (e.g., 'KANNADA', 'ENGLISH')
            start_num: Starting file number (e.g., 5 for GGKND005)
            end_num: Ending file number (e.g., 10 for GGKND010)
        """
        self.language = language.upper() if language else None
        self.start_num = start_num
        self.end_num = end_num
        self._create_directories()
        
    def _create_directories(self):
        """Create necessary directories"""
        for folder in [self.INPUT_IMAGES_FOLDER, self.INPUT_AUDIO_FOLDER, 
                       self.INPUT_BACKGROUND_FOLDER, self.TEMP_DOWNLOAD_FOLDER]:
            Path(folder).mkdir(parents=True, exist_ok=True)
    
    def _get_language_config(self):
        """Get configuration for the selected language"""
        if not self.language:
            logger.error("❌ No language specified")
            return None
            
        if self.language not in self.LANGUAGE_CONFIG:
            logger.error(f"❌ Language '{self.language}' not found in configuration")
            logger.error(f"   Available languages: {', '.join(self.LANGUAGE_CONFIG.keys())}")
            return None
            
        config = self.LANGUAGE_CONFIG[self.language]
        
        if not config['images_folder_id'] or not config['audio_folder_id']:
            logger.error(f"❌ {self.language} folder IDs not configured")
            logger.error(f"   Please set 'images_folder_id' and 'audio_folder_id' for {self.language}")
            return None
            
        return config
    
    def _get_file_pattern(self, config, num):
        """
        Generate filename pattern for a given number
        
        Args:
            config: Language configuration
            num: File number
            
        Returns:
            Filename without extension (e.g., 'GGKND005')
        """
        digits = config['digits']
        code = config['code']
        return f"{code}{str(num).zfill(digits)}"
    
    def _clear_input_folders(self):
        """Clear existing files in input folders (auto-delete in non-interactive mode)"""
        for folder_path, description in [(self.INPUT_IMAGES_FOLDER, "images"), 
                                         (self.INPUT_AUDIO_FOLDER, "audio")]:
            folder = Path(folder_path)
            if folder.exists():
                files = [f for f in folder.iterdir() if f.is_file()]
                if files:
                    # Auto-delete without prompting (for GitHub Actions compatibility)
                    logger.info(f"✓ Clearing {len(files)} existing {description} file(s)...")
                    for file in files:
                        file.unlink()
                    logger.info(f"✓ Cleared {description} folder")
    
    def _download_folder_to_temp(self, folder_id, folder_type):
        """
        Download entire folder to temp directory
        
        Args:
            folder_id: Google Drive folder ID
            folder_type: Type of folder ('images' or 'audio')
            
        Returns:
            Path to downloaded folder
        """
        temp_path = Path(self.TEMP_DOWNLOAD_FOLDER) / folder_type
        
        # Clean temp folder
        if temp_path.exists():
            shutil.rmtree(temp_path)
        temp_path.mkdir(parents=True, exist_ok=True)
        
        try:
            url = f"https://drive.google.com/drive/folders/{folder_id}"
            
            # Use command-line gdown tool
            cmd = ['gdown', '--folder', url, '-O', str(temp_path)]
            result = subprocess.run(
                cmd,
                capture_output=False,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                return temp_path
            else:
                logger.error(f"❌ gdown command failed with exit code {result.returncode}")
                return None
            
        except Exception as e:
            logger.error(f"❌ Error downloading {folder_type}: {e}")
            return None
    
    def _filter_and_copy_files(self, source_folder, dest_folder, config, file_extension):
        """
        Filter files by range and copy to destination
        
        Args:
            source_folder: Source folder path
            dest_folder: Destination folder path
            config: Language configuration
            file_extension: File extension to filter (.jpg or .mp3)
            
        Returns:
            Number of files copied
        """
        copied_count = 0
        source_path = Path(source_folder)
        dest_path = Path(dest_folder)
        
        if not source_path.exists():
            logger.error(f"Source folder not found: {source_folder}")
            return 0
        
        # Get all files matching the pattern
        code = config['code']
        all_files = list(source_path.glob(f"{code}*{file_extension}"))
        
        # Filter by range if specified
        for file in all_files:
            # Extract number from filename (e.g., GGKND005.jpg -> 5)
            match = re.search(rf"{code}(\d+){re.escape(file_extension)}$", file.name)
            if match:
                file_num = int(match.group(1))
                
                # Check if within range
                if self.start_num is not None and self.end_num is not None:
                    if self.start_num <= file_num <= self.end_num:
                        # Copy file
                        dest_file = dest_path / file.name
                        shutil.copy2(file, dest_file)
                        copied_count += 1
                else:
                    # No range specified, copy all
                    dest_file = dest_path / file.name
                    shutil.copy2(file, dest_file)
                    copied_count += 1
        
        return copied_count
    
    def download_language_media(self):
        """Download images and audio for specified language and range"""
        
        # Get language configuration
        config = self._get_language_config()
        if not config:
            return False
        
        logger.info("="*60)
        logger.info(f"📥 Downloading {self.language} Media")
        logger.info("="*60)
        logger.info(f"File prefix: {config['code']}")
        
        if self.start_num and self.end_num:
            logger.info(f"Range: {self._get_file_pattern(config, self.start_num)} to {self._get_file_pattern(config, self.end_num)}")
        else:
            logger.info("Range: ALL FILES")
        
        logger.info("="*60)
        
        # Clear existing input folders
        self._clear_input_folders()
        
        # Download images to temp
        logger.info("\n📸 Step 1/2: Downloading images...")
        temp_images = self._download_folder_to_temp(config['images_folder_id'], 'images')
        if not temp_images:
            return False
        
        # Filter and copy images
        images_copied = self._filter_and_copy_files(
            temp_images, 
            self.INPUT_IMAGES_FOLDER, 
            config, 
            '.jpg'
        )
        
        # Download audio to temp
        logger.info("\n🎵 Step 2/2: Downloading audio files...")
        temp_audio = self._download_folder_to_temp(config['audio_folder_id'], 'audio')
        if not temp_audio:
            return False
        
        # Filter and copy audio
        audio_copied = self._filter_and_copy_files(
            temp_audio,
            self.INPUT_AUDIO_FOLDER,
            config,
            '.mp3'
        )
        
        # Clean up temp folder
        shutil.rmtree(self.TEMP_DOWNLOAD_FOLDER)
        
        # Summary
        logger.info("="*60)
        logger.info("📊 DOWNLOAD SUMMARY")
        logger.info("="*60)
        logger.info(f"Language:      {self.language}")
        logger.info(f"Images copied: {images_copied}")
        logger.info(f"Audio copied:  {audio_copied}")
        
        if images_copied == audio_copied and images_copied > 0:
            logger.info("✅ Success! All files downloaded and matched")
            return True
        elif images_copied != audio_copied:
            logger.warning(f"⚠️  Mismatch: {images_copied} images vs {audio_copied} audio files")
            logger.warning("   Some files may not match - check your Google Drive folders")
            return True
        else:
            logger.error("❌ No files were copied")
            return False
    
    def download_background_music(self):
        """Download background music file from Google Drive"""
        if not self.BACKGROUND_FILE_ID:
            logger.info("⏭️  No background music configured (optional)")
            return True
            
        logger.info("="*60)
        logger.info("🎼 Downloading BACKGROUND MUSIC from Google Drive...")
        logger.info("="*60)
        
        try:
            # Download file
            url = f"https://drive.google.com/uc?id={self.BACKGROUND_FILE_ID}"
            output_path = os.path.join(self.INPUT_BACKGROUND_FOLDER, self.BACKGROUND_FILENAME)
            
            # Delete existing file if present
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # Use command-line gdown tool
            cmd = ['gdown', url, '-O', output_path]
            result = subprocess.run(
                cmd,
                capture_output=False,
                text=True,
                check=False
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                logger.info(f"✓ Downloaded background music ({file_size:.2f} MB)")
                return True
            else:
                logger.error("❌ Background music file not downloaded")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error downloading background music: {e}")
            logger.error("   Make sure the file is shared with 'Anyone with the link can view'")
            return False


def print_instructions():
    """Print setup and usage instructions"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         Google Drive Media Downloader - Language & Range          ║
╚════════════════════════════════════════════════════════════════════╝

📋 SETUP INSTRUCTIONS:

1️⃣  Navigate to your Google Drive folder structure:
   
   Srisatupasi/
   └── GG KANNADA/                      ← Navigate here in Google Drive
       ├── KANNADA jpg files/          ← RIGHT-CLICK THIS → Share → Get link
       │   └── GGKND001.jpg, etc.
       └── Final KANNADA audio files/  ← RIGHT-CLICK THIS → Share → Get link
           └── GGKND001.mp3, etc.

2️⃣  For EACH language, get TWO folder IDs:
   
   Step A: Right-click "KANNADA jpg files" folder
           → Share → "Anyone with the link can view" → Copy link
           
   Step B: Right-click "Final KANNADA audio files" folder
           → Share → "Anyone with the link can view" → Copy link

3️⃣  Extract Folder IDs from the share links:
   
   Link: https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j
   ID:   1a2b3c4d5e6f7g8h9i0j  ← Copy just this part

4️⃣  Edit this script (download_from_gdrive.py):
   - Find LANGUAGE_CONFIG section (around line 45)
   - For KANNADA:
     • Paste first ID into:  images_folder_id
     • Paste second ID into: audio_folder_id
   - Repeat for other languages (ENGLISH, etc.)

═══════════════════════════════════════════════════════════════════

📥 USAGE EXAMPLES:

1. Interactive mode (will prompt for inputs):
   python3 download_from_gdrive.py

2. Download specific language and range:
   python3 download_from_gdrive.py --language KANNADA --start 5 --end 10
   
   This downloads: GGKND005 to GGKND010

3. Download all files for a language:
   python3 download_from_gdrive.py --language ENGLISH
   
   This downloads all ENGLISH files

═══════════════════════════════════════════════════════════════════

📂 FOLDER STRUCTURE EXPECTED:

Google Drive:
  Srisatupasi/
    └── GG KANNADA/
        ├── KANNADA jpg files/
        │   ├── GGKND001.jpg
        │   ├── GGKND002.jpg
        │   └── ...
        └── Final KANNADA audio files/
            ├── GGKND001.mp3
            ├── GGKND002.mp3
            └── ...

Downloads to:
  input/
    ├── images/     ← GGKND005.jpg to GGKND010.jpg
    └── audio/      ← GGKND005.mp3 to GGKND010.mp3

    """)


def get_user_input():
    """Get language and range from user interactively"""
    print("\n" + "="*60)
    print("  INTERACTIVE MODE")
    print("="*60)
    
    # Show available languages
    downloader_temp = GoogleDriveDownloader()
    available_languages = [lang for lang, config in downloader_temp.LANGUAGE_CONFIG.items() 
                          if config['images_folder_id'] and config['audio_folder_id']]
    
    if not available_languages:
        print("❌ No languages configured yet!")
        print("   Please edit the script and add your Google Drive folder IDs")
        return None, None, None
    
    print(f"\n📚 Available Languages: {', '.join(available_languages)}")
    
    # Get language
    while True:
        language = input("\nEnter language (e.g., KANNADA, ENGLISH): ").strip().upper()
        if language in available_languages:
            break
        print(f"❌ Invalid language. Choose from: {', '.join(available_languages)}")
    
    # Get config
    config = downloader_temp.LANGUAGE_CONFIG[language]
    
    # Ask about range
    print(f"\n📁 File pattern: {config['code']}XXX (e.g., {config['code']}001)")
    use_range = input("\nDownload specific range? (y/n, default=n): ").strip().lower()
    
    start_num = None
    end_num = None
    
    if use_range == 'y':
        while True:
            try:
                start_num = int(input(f"Start number (e.g., 5 for {config['code']}005): ").strip())
                end_num = int(input(f"End number (e.g., 10 for {config['code']}010): ").strip())
                
                if start_num > end_num:
                    print("❌ Start number must be <= end number")
                    continue
                    
                pattern_start = config['code'] + str(start_num).zfill(config['digits'])
                pattern_end = config['code'] + str(end_num).zfill(config['digits'])
                print(f"\n✓ Will download: {pattern_start} to {pattern_end}")
                confirm = input("Proceed? (y/n): ").strip().lower()
                if confirm == 'y':
                    break
                    
            except ValueError:
                print("❌ Please enter valid numbers")
    else:
        print(f"\n✓ Will download ALL {language} files")
    
    return language, start_num, end_num


def main():
    """Main entry point"""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Download media files from Google Drive for video generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python3 download_from_gdrive.py
  
  # Download specific range
  python3 download_from_gdrive.py --language KANNADA --start 5 --end 10
  
  # Download all files for a language
  python3 download_from_gdrive.py --language ENGLISH
        """
    )
    
    parser.add_argument('--language', '-l', type=str, 
                       help='Language to download (e.g., KANNADA, ENGLISH)')
    parser.add_argument('--start', '-s', type=int,
                       help='Starting file number (e.g., 5)')
    parser.add_argument('--end', '-e', type=int,
                       help='Ending file number (e.g., 10)')
    parser.add_argument('--background', '-b', action='store_true',
                       help='Also download background music')
    
    args = parser.parse_args()
    
    # Print instructions
    print_instructions()
    
    # Get parameters
    language = args.language
    start_num = args.start
    end_num = args.end
    
    # If no arguments provided, use interactive mode
    if not language:
        language, start_num, end_num = get_user_input()
        if not language:
            sys.exit(1)
    else:
        # Command line mode - validate
        language = language.upper()
        if start_num is not None and end_num is None:
            print("❌ Error: --start requires --end")
            sys.exit(1)
        if end_num is not None and start_num is None:
            print("❌ Error: --end requires --start")
            sys.exit(1)
    
    # Create downloader and run
    print("\n🚀 Starting download process...")
    downloader = GoogleDriveDownloader(language, start_num, end_num)
    
    # Download language-specific media
    success = downloader.download_language_media()
    
    # Optionally download background music
    if args.background:
        print()
        downloader.download_background_music()
    
    # Final message
    if success:
        print("\n" + "="*60)
        print("✅ READY TO GENERATE VIDEOS!")
        print("="*60)
        print("Run: python3 generate_videos_with_bg.py")
        print("="*60)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
