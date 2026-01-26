# Image Files

Place your image files in this folder.

## Supported Formats
- JPG, JPEG
- PNG
- BMP

## Important Notes

1. **Matching Names**: Image filenames must match your audio filenames
   - Example: `1_shloka.jpg` should pair with `1_shloka.mp3`
   - Example: `2_meditation.png` should pair with `2_meditation.wav`

2. **Recommended Resolution**: 1920x1080 (1080p) for best results
   - The generator will automatically scale and letterbox images to 1080p

3. **File Naming**: Use clear, descriptive names
   - ✅ Good: `1_shloka.jpg`, `2_meditation.png`
   - ❌ Avoid: `IMG_001.jpg`, `photo.jpg`

## Example Files

```
input/images/
├── 1_shloka.jpg
├── 2_meditation.png
├── 3_relaxation.jpg
└── 4_peace.png
```

These should match with audio files:
```
input/audio/
├── 1_shloka.mp3
├── 2_meditation.wav
├── 3_relaxation.mp3
└── 4_peace.m4a
```
