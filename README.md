# 🎬 Image Audio Video Maker

Generate high-resolution 1080p videos by combining matching image and audio files with parallel processing for maximum efficiency!

## ✨ Features

- ✅ **Automatic Matching**: Pairs images and audio by filename
- ✅ **Parallel Processing**: Generate multiple videos simultaneously
- ✅ **1080p Quality**: Full HD output optimized for YouTube
- ✅ **Cross-Platform**: Works on Mac and Windows
- ✅ **No Installation Hassle**: Everything runs in Docker
- ✅ **Multiple Formats**: Support for various image and audio formats
- ✅ **One-Click Operation**: Simple scripts to run

## 🚀 Quick Start

### Prerequisites

1. **Install Docker Desktop**
   - Download from: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - Install and start Docker Desktop

### First Time Setup

#### 🍎 Mac Users

```bash
# Make scripts executable (one-time)
chmod +x mac/*.sh

# Run setup (builds Docker image)
./mac/SETUP.sh
```

#### 🪟 Windows Users

```batch
# Double-click to run setup
windows\SETUP.bat
```

### Regular Usage

#### 🍎 Mac

1. Add your files to `input/images/` and `input/audio/`
2. Run: `./mac/RUN_GENERATOR.sh`
3. Find videos in `output/` folder

#### 🪟 Windows

1. Add your files to `input\images\` and `input\audio\`
2. Double-click: `windows\RUN_GENERATOR.bat`
3. Find videos in `output\` folder

## 📁 File Requirements

### Image Files (input/images/)

**Supported Formats:**

- JPG, JPEG
- PNG
- BMP

**Requirements:**

- Any resolution (will be scaled to 1080p)
- Recommended: 1920x1080 for best quality
- Filenames must match audio files

### Audio Files (input/audio/)

**Supported Formats:**

- MP3
- WAV
- M4A
- AAC
- FLAC

**Requirements:**

- Any duration
- Recommended: 192kbps or higher quality
- Filenames must match image files

### 🔑 Critical: Filename Matching

**Images and audio must have matching base names:**

✅ **Correct Examples:**

```
input/images/1_shloka.jpg      → input/audio/1_shloka.mp3    → output/1_shloka.mp4
input/images/2_meditation.png  → input/audio/2_meditation.wav → output/2_meditation.mp4
input/images/3_peace.jpg       → input/audio/3_peace.m4a     → output/3_peace.mp4
```

❌ **Won't Work:**

```
input/images/video1.jpg + input/audio/audio1.mp3  (different names)
```

## 📹 Output Videos

### Specifications

- **Resolution:** 1920x1080 (1080p Full HD)
- **Format:** MP4 (H.264 + AAC)
- **Video Codec:** H.264 (x264) with CRF 23
- **Audio Codec:** AAC at 192kbps
- **Optimization:** Web streaming ready (faststart enabled)
- **Duration:** Matches audio file duration

### Output Location

Videos are saved in the `output/` folder with the same name as input files:

- `1_shloka.jpg` + `1_shloka.mp3` → `output/1_shloka.mp4`

## 🎯 Example Workflow

1. **Prepare Your Files:**

   ```
   input/images/
   ├── 1_morning_prayer.jpg
   ├── 2_evening_prayer.jpg
   └── 3_meditation.jpg

   input/audio/
   ├── 1_morning_prayer.mp3
   ├── 2_evening_prayer.mp3
   └── 3_meditation.mp3
   ```

2. **Run the Generator:**
   - Mac: `./mac/RUN_GENERATOR.sh`
   - Windows: Double-click `windows\RUN_GENERATOR.bat`

3. **Get Your Videos:**
   ```
   output/
   ├── 1_morning_prayer.mp4
   ├── 2_evening_prayer.mp4
   ├── 3_meditation.mp4
   └── video_generation.log
   ```

## ⚙️ Advanced Settings

### Adjust Parallel Processing

By default, 4 videos are generated simultaneously. To change this:

1. Open `generate_videos.py`
2. Find line: `generator = VideoGenerator(max_workers=4)`
3. Change the number (e.g., `max_workers=8` for 8 parallel jobs)
4. Rebuild: Run setup script again

**Note:** More workers = faster processing but higher CPU/memory usage.

### Video Quality Settings

Default settings provide excellent quality. To customize:

Edit these variables in `generate_videos.py`:

```python
VIDEO_RESOLUTION = "1920x1080"  # Resolution
CRF = "23"                       # Quality (lower = better, 18-28 range)
PRESET = "medium"                # Speed (ultrafast/fast/medium/slow/veryslow)
AUDIO_BITRATE = "192k"           # Audio quality
```

## 🛠️ Troubleshooting

### Docker Not Running

```
ERROR: Docker is not running!
```

**Solution:** Start Docker Desktop and wait for it to fully start.

### No Matching Files

```
WARNING: No matching image/audio pairs found!
```

**Solution:** Ensure image and audio filenames match exactly (excluding extension).

### Build Fails

```
ERROR: Docker build failed!
```

**Solution:**

- Check your internet connection
- Ensure Docker Desktop has enough resources (Settings → Resources)
- Try running setup again

### Permission Denied (Mac)

```
Permission denied: ./mac/RUN_GENERATOR.sh
```

**Solution:**

```bash
chmod +x mac/*.sh
```

## 📊 Performance

**Processing Speed:**

- Depends on video count, audio duration, and CPU
- Parallel processing significantly speeds up multiple videos
- Example: 10 videos (5 min each) ≈ 15-20 minutes on 4-core system

**Resource Usage:**

- CPU: Moderate to high during encoding
- RAM: ~500MB per parallel worker
- Disk: Output videos are ~5-20MB per minute

## 🔍 Logs

Detailed logs are saved to `output/video_generation.log`:

- Matched file pairs
- Processing status for each video
- Success/failure messages
- File sizes and durations
- Error details

## 📦 Distribution

To share this with others:

1. **Create a zip file** of the entire `gg_parayana` folder
2. **Share with these instructions:**
   - Extract the folder
   - Install Docker Desktop
   - Run setup script (one time)
   - Add files and run generator

**What's Included:**

- Docker configuration
- Python script
- Run scripts for Mac/Windows
- Setup scripts
- Documentation
- Input/output folder structure

## 🎓 Technical Details

### Docker Container

- Base: Python 3.11 slim
- Includes: FFMPEG, Python
- Volumes: input/output folders mounted
- Runs: Automatically on `docker-compose up`

### FFMPEG Command

The generator uses optimized FFMPEG settings:

- Still image optimization (`-tune stillimage`)
- Smart scaling with letterboxing
- Fast start for web streaming
- High compatibility (yuv420p pixel format)

### Python Script

- Automatic file discovery and matching
- ThreadPoolExecutor for parallel processing
- Comprehensive error handling
- Detailed logging
- Clean shutdown

## 📝 License

This tool is provided as-is for generating videos from your own content.

## 🙏 Support

For issues or questions:

1. Check the logs in `output/video_generation.log`
2. Verify Docker Desktop is running
3. Ensure files are named correctly
4. Check available disk space

---

**Made with ❤️ for easy video generation from images and audio**

# Download media for English videos 1-5

./download.sh --language ENGLISH --start 1 --end 5

# Generate the videos

python3 generate_videos_with_bg.py

# Upload generated videos and delete local copies

python3 upload_to_gdrive.py --language ENGLISH --delete

---

# Step 1: Download media from Google Drive

python3 download_from_gdrive.py --language ENGLISH --start 1 --end 10

# Step 2: Generate videos

python3 generate_videos_with_bg.py

# Step 3: Upload videos back to Google Drive

python3 upload_to_gdrive.py --language ENGLISH

---

# Upload all videos (auto-detects language from filename)

python3 upload_to_gdrive.py

# Upload only ENGLISH videos

python3 upload_to_gdrive.py --language ENGLISH

# Upload and delete local files after success

python3 upload_to_gdrive.py --delete

# Upload specific language and clean up

python3 upload_to_gdrive.py --language KANNADA --delete
