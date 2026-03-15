#!/usr/bin/env python3
"""
Google Drive Video Uploader
Uploads generated videos to Google Drive language folders based on file prefix
Run this after generate_videos_with_bg.py to upload videos to Google Drive
"""

import os
import sys
import subprocess
from pathlib import Path
import logging
import re

# Check if gdrive CLI tool is available (for uploads)
try:
    result = subprocess.run(['gdrive', 'version'], 
                          capture_output=True, 
                          text=True,
                          check=False)
    if result.returncode != 0:
        raise FileNotFoundError
    HAS_GDRIVE_CLI = True
except FileNotFoundError:
    HAS_GDRIVE_CLI = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class GoogleDriveUploader:
    """Upload generated videos to Google Drive language folders"""
    
    # Base paths
    BASE_PATH = "/Users/vkuma153/video_generator/image_audio_video_maker"
    OUTPUT_VIDEOS_FOLDER = f"{BASE_PATH}/output"
    
    # ======================================================================
    # 🔧 CONFIGURATION - Language Output Folder IDs
    # ======================================================================
    
    # For each language, specify the Google Drive folder where videos should be uploaded
    # Navigate to: Srisatupasi > GG ENGLISH > Generated Videos (or create this folder)
    # Right-click → Share → Get link → Extract folder ID
    
    LANGUAGE_CONFIG = {
        'ENGLISH': {
            'code': 'GGENG',              # File prefix to detect language
            'output_folder_id': '',       # ID of folder in Google Drive where videos go
        },
        'KANNADA': {
            'code': 'GGKND',
            'output_folder_id': '',
        },
        'TELUGU': {
            'code': 'GGTLG',
            'output_folder_id': '',
        },
        'HINDI': {
            'code': 'GGHND',
            'output_folder_id': '',
        },
        'MARATHI': {
            'code': 'GGMRT',
            'output_folder_id': '',
        },
        'TAMIL': {
            'code': 'GGTML',
            'output_folder_id': '',
        },
    }
    
    # ======================================================================
    
    def __init__(self):
        """Initialize the uploader"""
        if not HAS_GDRIVE_CLI:
            logger.error("❌ 'gdrive' CLI tool not found")
            logger.error("📦 Install it with: brew install gdrive")
            logger.error("   Or visit: https://github.com/prasmussen/gdrive")
            logger.error("\n💡 First time setup:")
            logger.error("   1. Run: gdrive about")
            logger.error("   2. Follow the OAuth authentication flow")
            logger.error("   3. Run this script again")
            sys.exit(1)
    
    def _detect_language(self, filename):
        """
        Detect language from filename prefix
        
        Args:
            filename: Video filename (e.g., GGENG001.mp4)
            
        Returns:
            Language name or None
        """
        for lang, config in self.LANGUAGE_CONFIG.items():
            if filename.startswith(config['code']):
                return lang
        return None
    
    def _get_videos_by_language(self):
        """
        Group videos in output folder by language
        
        Returns:
            Dictionary: {language: [list of file paths]}
        """
        videos_by_lang = {}
        output_path = Path(self.OUTPUT_VIDEOS_FOLDER)
        
        if not output_path.exists():
            logger.error(f"❌ Output folder not found: {self.OUTPUT_VIDEOS_FOLDER}")
            return {}
        
        # Find all mp4 files
        video_files = list(output_path.glob('*.mp4'))
        
        if not video_files:
            logger.warning("⚠️  No video files found in output folder")
            return {}
        
        # Group by language
        for video_file in video_files:
            lang = self._detect_language(video_file.name)
            if lang:
                if lang not in videos_by_lang:
                    videos_by_lang[lang] = []
                videos_by_lang[lang].append(video_file)
            else:
                logger.warning(f"⚠️  Could not detect language for: {video_file.name}")
        
        return videos_by_lang
    
    def _upload_file(self, file_path, folder_id):
        """
        Upload a single file to Google Drive folder
        
        Args:
            file_path: Path to local file
            folder_id: Google Drive folder ID
            
        Returns:
            True if successful
        """
        try:
            # Upload using gdrive CLI
            cmd = ['gdrive', 'upload', '--parent', folder_id, str(file_path)]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                return True
            else:
                logger.error(f"   Upload failed: {result.stderr.strip()}")
                return False
                
        except Exception as e:
            logger.error(f"   Error: {e}")
            return False
    
    def upload_videos(self, language=None, delete_after_upload=False):
        """
        Upload videos to Google Drive
        
        Args:
            language: Specific language to upload (None = all)
            delete_after_upload: Delete local files after successful upload
            
        Returns:
            Dictionary with upload statistics
        """
        logger.info("="*60)
        logger.info("📤 Google Drive Video Uploader")
        logger.info("="*60)
        
        # Get videos grouped by language
        videos_by_lang = self._get_videos_by_language()
        
        if not videos_by_lang:
            logger.error("❌ No videos to upload")
            return {'total': 0, 'success': 0, 'failed': 0}
        
        # Filter by specific language if requested
        if language:
            language = language.upper()
            if language in videos_by_lang:
                videos_by_lang = {language: videos_by_lang[language]}
            else:
                logger.error(f"❌ No videos found for language: {language}")
                return {'total': 0, 'success': 0, 'failed': 0}
        
        # Upload statistics
        stats = {'total': 0, 'success': 0, 'failed': 0, 'by_language': {}}
        
        # Upload each language
        for lang, video_files in videos_by_lang.items():
            config = self.LANGUAGE_CONFIG[lang]
            folder_id = config.get('output_folder_id', '')
            
            if not folder_id:
                logger.warning(f"\n⚠️  {lang}: No output_folder_id configured - skipping")
                continue
            
            logger.info(f"\n📤 Uploading {lang} videos ({len(video_files)} files)...")
            
            lang_stats = {'success': 0, 'failed': 0}
            
            for video_file in video_files:
                stats['total'] += 1
                logger.info(f"   Uploading: {video_file.name}...")
                
                if self._upload_file(video_file, folder_id):
                    logger.info(f"   ✓ Uploaded: {video_file.name}")
                    stats['success'] += 1
                    lang_stats['success'] += 1
                    
                    # Delete local file if requested
                    if delete_after_upload:
                        video_file.unlink()
                        logger.info(f"   🗑️  Deleted local file")
                else:
                    logger.error(f"   ✗ Failed: {video_file.name}")
                    stats['failed'] += 1
                    lang_stats['failed'] += 1
            
            stats['by_language'][lang] = lang_stats
        
        # Print summary
        logger.info("\n" + "="*60)
        logger.info("📊 UPLOAD SUMMARY")
        logger.info("="*60)
        logger.info(f"Total videos:  {stats['total']}")
        logger.info(f"✓ Successful:  {stats['success']}")
        logger.info(f"✗ Failed:      {stats['failed']}")
        
        if stats['by_language']:
            logger.info("\nBy Language:")
            for lang, lang_stats in stats['by_language'].items():
                logger.info(f"  {lang}: {lang_stats['success']} uploaded, {lang_stats['failed']} failed")
        
        logger.info("="*60)
        
        return stats


def print_instructions():
    """Print setup and usage instructions"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║            Google Drive Video Uploader - Setup Guide              ║
╚════════════════════════════════════════════════════════════════════╝

📋 SETUP INSTRUCTIONS:

1️⃣  Install gdrive CLI tool:
   brew install gdrive
   
   Or download from: https://github.com/prasmussen/gdrive

2️⃣  First-time authentication:
   gdrive about
   
   This will:
   - Open your browser for Google authentication
   - Create a token file for future use
   - Show your Google Drive info

3️⃣  Create upload folders in Google Drive:
   
   For each language, create a folder for videos:
   Srisatupasi/
   └── GG ENGLISH/
       └── Generated Videos/  ← Create this folder
   
   Do the same for: GG KANNADA, GG HINDI, etc.

4️⃣  Get folder IDs and configure:
   
   - Right-click "Generated Videos" folder → Share → Get link
   - Extract ID from: https://drive.google.com/drive/folders/FOLDER_ID
   - Paste into upload_to_gdrive.py → LANGUAGE_CONFIG → output_folder_id

═══════════════════════════════════════════════════════════════════

📤 USAGE EXAMPLES:

1. Upload all videos (auto-detects language from filename):
   python3 upload_to_gdrive.py

2. Upload only specific language:
   python3 upload_to_gdrive.py --language ENGLISH

3. Upload and delete local files after success:
   python3 upload_to_gdrive.py --delete

4. Upload specific language and delete:
   python3 upload_to_gdrive.py --language KANNADA --delete

═══════════════════════════════════════════════════════════════════

📂 HOW IT WORKS:

- Scans: /output folder for .mp4 files
- Detects language from prefix: GGENG001.mp4 → ENGLISH
- Uploads to corresponding Google Drive folder
- Optional: Deletes local files after successful upload

    """)


def main():
    """Main entry point"""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Upload generated videos to Google Drive',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload all videos
  python3 upload_to_gdrive.py
  
  # Upload specific language
  python3 upload_to_gdrive.py --language ENGLISH
  
  # Upload and delete local copies
  python3 upload_to_gdrive.py --delete
        """
    )
    
    parser.add_argument('--language', '-l', type=str,
                       help='Upload only this language (e.g., KANNADA, ENGLISH)')
    parser.add_argument('--delete', '-d', action='store_true',
                       help='Delete local files after successful upload')
    
    args = parser.parse_args()
    
    # Print instructions
    print_instructions()
    
    # Create uploader and run
    uploader = GoogleDriveUploader()
    stats = uploader.upload_videos(
        language=args.language,
        delete_after_upload=args.delete
    )
    
    # Exit with appropriate code
    sys.exit(0 if stats['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
