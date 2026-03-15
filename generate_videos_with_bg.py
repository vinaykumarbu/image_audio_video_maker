#!/usr/bin/env python3
"""
Video Generator Script with Background Music Support
Combines matching images and audio files into high-resolution videos with background music
Optimized for YouTube with parallel processing support
"""

import os
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Optional
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class VideoGenerator:
    """Generate high-resolution videos from matching image and audio files with background music"""
    
    # Paths - automatically detect script location (works on any machine)
    BASE_PATH = Path(__file__).parent.resolve()
    INPUT_IMAGES_FOLDER = BASE_PATH / "input" / "images"
    INPUT_AUDIO_FOLDER = BASE_PATH / "input" / "audio"
    INPUT_BACKGROUND_FOLDER = BASE_PATH / "input" / "background" / "background.mp3"
    OUTPUT_VIDEOS_FOLDER = BASE_PATH / "output"
    
    # Supported formats
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}
    AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.aac', '.flac'}
    
    # Video settings (YouTube optimized)
    VIDEO_RESOLUTION = "1920x1080"  # 1080p
    VIDEO_CODEC = "libx264"
    AUDIO_CODEC = "aac"
    AUDIO_BITRATE = "192k"
    PIXEL_FORMAT = "yuv420p"
    CRF = "23"  # Constant Rate Factor (lower = better quality, 23 is good balance)
    PRESET = "medium"  # Encoding speed vs compression (medium is good balance)
    
    # Background music settings
    BACKGROUND_MUSIC_VOLUME = "0.01"  # 10% volume (adjust as needed: 0.05 = 5%, 0.15 = 15%, 0.2 = 20%, etc.)
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize the video generator
        
        Args:
            max_workers: Maximum number of parallel video generation processes
            background_music_path: Optional path to background music file (if None, no background music)
        """
        self.max_workers = max_workers
        self.INPUT_BACKGROUND_FOLDER = Path(self.INPUT_BACKGROUND_FOLDER) if self.INPUT_BACKGROUND_FOLDER else None
        
        if self.INPUT_BACKGROUND_FOLDER and not self.INPUT_BACKGROUND_FOLDER.exists():
            logger.warning(f"Background music file not found: {self.INPUT_BACKGROUND_FOLDER}")
            logger.warning("Continuing without background music...")
            self.INPUT_BACKGROUND_FOLDER = None
        
        if self.INPUT_BACKGROUND_FOLDER:
            logger.info(f"Background music enabled: {self.INPUT_BACKGROUND_FOLDER}")
            logger.info(f"Background music volume: {float(self.BACKGROUND_MUSIC_VOLUME) * 100:.0f}%")
        
        self._validate_ffmpeg()
        self._create_output_directory()
    
    def _validate_ffmpeg(self):
        """Check if FFMPEG is installed and accessible"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("FFMPEG is available")
            logger.debug(f"FFMPEG version: {result.stdout.split()[2]}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("FFMPEG is not installed or not in PATH")
            sys.exit(1)
    
    def _create_output_directory(self):
        """Create output directory if it doesn't exist"""
        Path(self.OUTPUT_VIDEOS_FOLDER).mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory ready: {self.OUTPUT_VIDEOS_FOLDER}")
    
    def _get_file_pairs(self) -> List[Tuple[Path, Path, str]]:
        """
        Find matching image and audio files
        
        Returns:
            List of tuples (image_path, audio_path, base_name)
        """
        # Get all image files
        image_files: Dict[str, Path] = {}
        image_folder = Path(self.INPUT_IMAGES_FOLDER)
        
        if not image_folder.exists():
            logger.error(f"Image folder not found: {self.INPUT_IMAGES_FOLDER}")
            return []
        
        for img_file in image_folder.iterdir():
            if img_file.suffix.lower() in self.IMAGE_EXTENSIONS:
                base_name = img_file.stem
                image_files[base_name] = img_file
        
        logger.info(f"Found {len(image_files)} image files")
        
        # Get all audio files and match with images
        audio_folder = Path(self.INPUT_AUDIO_FOLDER)
        
        if not audio_folder.exists():
            logger.error(f"Audio folder not found: {self.INPUT_AUDIO_FOLDER}")
            return []
        
        matched_pairs: List[Tuple[Path, Path, str]] = []
        
        for audio_file in audio_folder.iterdir():
            if audio_file.suffix.lower() in self.AUDIO_EXTENSIONS:
                base_name = audio_file.stem
                
                if base_name in image_files:
                    matched_pairs.append((
                        image_files[base_name],
                        audio_file,
                        base_name
                    ))
                    logger.info(f"Matched pair: {base_name}")
                else:
                    logger.warning(f"No matching image for audio: {audio_file.name}")
        
        logger.info(f"Found {len(matched_pairs)} matching pairs")
        return matched_pairs
    
    def _generate_single_video(
        self,
        image_path: Path,
        audio_path: Path,
        output_name: str
    ) -> Tuple[str, bool, str]:
        """
        Generate a single video from image and audio (with optional background music)
        
        Args:
            image_path: Path to the image file
            audio_path: Path to the audio file
            output_name: Base name for the output file
            
        Returns:
            Tuple of (output_name, success, message)
        """
        output_path = Path(self.OUTPUT_VIDEOS_FOLDER) / f"{output_name}.mp4"
        
        try:
            logger.info(f"Starting video generation: {output_name}")
            
            # Parse resolution for pad filter (needs width:height format)
            width, height = self.VIDEO_RESOLUTION.split('x')
            pad_resolution = f"{width}:{height}"
            
            # Build FFMPEG command
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output file if exists
                '-loop', '1',  # Loop the image
                '-i', str(image_path),  # Input 0: Image
                '-i', str(audio_path),  # Input 1: Main audio
            ]
            
            # Add background music input if enabled
            if self.INPUT_BACKGROUND_FOLDER:
                cmd.extend([
                    '-stream_loop', '-1',  # Loop background music indefinitely
                    '-i', str(self.INPUT_BACKGROUND_FOLDER),  # Input 2: Background music
                ])
            
            # Add video encoding options
            cmd.extend([
                '-c:v', self.VIDEO_CODEC,  # Video codec
                '-tune', 'stillimage',  # Optimize for still image
                '-pix_fmt', self.PIXEL_FORMAT,  # Pixel format for compatibility
                '-crf', self.CRF,  # Quality setting
                '-preset', self.PRESET,  # Encoding preset
                '-vf', f'scale={self.VIDEO_RESOLUTION}:force_original_aspect_ratio=decrease,pad={pad_resolution}:(ow-iw)/2:(oh-ih)/2',  # Scale and pad to 1080p
            ])
            
            # Add audio mixing filter if background music is enabled
            if self.INPUT_BACKGROUND_FOLDER:
                # Filter: [2:a]volume=0.2[bg] - Lower background music volume
                #         [1:a][bg]amix=inputs=2:duration=first[aout] - Mix main audio + background
                filter_complex = f"[2:a]volume={self.BACKGROUND_MUSIC_VOLUME}[bg];[1:a][bg]amix=inputs=2:duration=first[aout]"
                cmd.extend([
                    '-filter_complex', filter_complex,
                    '-map', '0:v',  # Map video from input 0 (image)
                    '-map', '[aout]',  # Map mixed audio output
                ])
            else:
                # No background music - just map video and main audio
                cmd.extend([
                    '-map', '0:v',  # Map video from input 0 (image)
                    '-map', '1:a',  # Map audio from input 1 (main audio)
                ])
            
            # Add audio encoding and final options
            cmd.extend([
                '-c:a', self.AUDIO_CODEC,  # Audio codec
                '-b:a', self.AUDIO_BITRATE,  # Audio bitrate
                '-shortest',  # End video when audio ends
                '-movflags', '+faststart',  # Optimize for web streaming
                str(output_path)
            ])
            
            # Run FFMPEG
            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Check if output file was created
            if output_path.exists():
                file_size = output_path.stat().st_size / (1024 * 1024)  # Size in MB
                logger.info(f"✓ Successfully generated: {output_name}.mp4 ({file_size:.2f} MB)")
                return (output_name, True, f"Success - {file_size:.2f} MB")
            else:
                logger.error(f"✗ Output file not created: {output_name}")
                return (output_name, False, "Output file not created")
                
        except subprocess.CalledProcessError as e:
            error_msg = f"FFMPEG error: {e.stderr[-200:]}"  # Last 200 chars of error
            logger.error(f"✗ Failed to generate {output_name}: {error_msg}")
            return (output_name, False, error_msg)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"✗ Unexpected error for {output_name}: {error_msg}")
            return (output_name, False, error_msg)
    
    def generate_videos(self) -> Dict[str, any]:
        """
        Generate all videos from matched pairs in parallel
        
        Returns:
            Dictionary with generation statistics
        """
        start_time = datetime.now()
        logger.info("="*60)
        logger.info("Starting video generation process")
        if self.INPUT_BACKGROUND_FOLDER:
            logger.info("Background music: ENABLED")
        else:
            logger.info("Background music: DISABLED")
        logger.info("="*60)
        
        # Get matched pairs
        file_pairs = self._get_file_pairs()
        
        if not file_pairs:
            logger.error("No matching image/audio pairs found!")
            return {
                'total': 0,
                'success': 0,
                'failed': 0,
                'duration': 0
            }
        
        logger.info(f"Processing {len(file_pairs)} videos with {self.max_workers} workers")
        
        # Process videos in parallel
        results = {
            'total': len(file_pairs),
            'success': 0,
            'failed': 0,
            'details': []
        }
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_name = {
                executor.submit(
                    self._generate_single_video,
                    img_path,
                    audio_path,
                    base_name
                ): base_name
                for img_path, audio_path, base_name in file_pairs
            }
            
            # Process completed tasks
            for future in as_completed(future_to_name):
                name, success, message = future.result()
                results['details'].append({
                    'name': name,
                    'success': success,
                    'message': message
                })
                
                if success:
                    results['success'] += 1
                else:
                    results['failed'] += 1
        
        # Calculate duration
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        results['duration'] = duration
        
        # Print summary
        logger.info("="*60)
        logger.info("Video Generation Complete!")
        logger.info("="*60)
        logger.info(f"Total videos processed: {results['total']}")
        logger.info(f"✓ Successful: {results['success']}")
        logger.info(f"✗ Failed: {results['failed']}")
        logger.info(f"⏱ Total time: {duration:.2f} seconds")
        logger.info(f"📁 Output folder: {self.OUTPUT_VIDEOS_FOLDER}")
        logger.info("="*60)
        
        return results


def main():
    """Main entry point"""
    print("🎬 Video Generator with Background Music - High Resolution Video Creation")
    print("="*60)
    
    
    # If you want to use background music, uncomment and set the path:
    # background_music = "/Users/vinaykumarbu/Workspace/srisatupasi/image_audio_video_maker-main/input/audio/background_music.mp3"
    
    # Create generator instance
    # Adjust max_workers based on your system (4 is a good default)
    generator = VideoGenerator(
        max_workers=5,
    )
    
    # Generate videos
    results = generator.generate_videos()
    
    # Exit with appropriate code
    sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()