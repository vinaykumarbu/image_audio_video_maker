# Generated Videos

Your generated videos will appear in this folder.

## Video Specifications

- **Resolution**: 1920x1080 (1080p Full HD)
- **Format**: MP4 (H.264 video + AAC audio)
- **Video Codec**: H.264 (x264)
- **Audio Codec**: AAC at 192kbps
- **Compatibility**: YouTube, Vimeo, social media platforms

## File Naming

Generated videos will use the same name as your input files:
- Input: `1_shloka.jpg` + `1_shloka.mp3`
- Output: `1_shloka.mp4`

## Video Duration

The video duration matches the audio duration:
- 3-minute audio → 3-minute video
- 10-minute audio → 10-minute video

## Logs

A log file `video_generation.log` is also created here with detailed processing information.

## Tips

- Videos are optimized for web streaming (faststart flag enabled)
- Ready to upload directly to YouTube or other platforms
- High quality encoding with CRF 23 (good balance of quality and file size)
- Letterboxing automatically applied to maintain 16:9 aspect ratio
