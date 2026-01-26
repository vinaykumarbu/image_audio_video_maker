# Audio Files

Place your audio files in this folder.

## Supported Formats
- MP3
- WAV
- M4A
- AAC
- FLAC

## Important Notes

1. **Matching Names**: Audio filenames must match your image filenames
   - Example: `1_shloka.mp3` should pair with `1_shloka.jpg`
   - Example: `2_meditation.wav` should pair with `2_meditation.png`

2. **Audio Quality**: Higher quality audio produces better final videos
   - Recommended: 192kbps or higher for MP3
   - The generator will encode audio at 192kbps AAC in the final video

3. **Video Duration**: The video duration will match the audio duration
   - A 5-minute audio file will create a 5-minute video

4. **File Naming**: Use clear, descriptive names matching your images
   - ✅ Good: `1_shloka.mp3`, `2_meditation.wav`
   - ❌ Avoid: `track01.mp3`, `audio.mp3`

## Example Files

```
input/audio/
├── 1_shloka.mp3
├── 2_meditation.wav
├── 3_relaxation.mp3
└── 4_peace.m4a
```

These should match with image files:
```
input/images/
├── 1_shloka.jpg
├── 2_meditation.png
├── 3_relaxation.jpg
└── 4_peace.png
```
