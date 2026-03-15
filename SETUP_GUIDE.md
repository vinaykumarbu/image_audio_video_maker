# 🎬 Video Generator - Setup Guide

## 📋 Overview

This guide will help you set up the automated video generation system using GitHub Actions with **manual triggering** from the GitHub website.

## ⚙️ Prerequisites

- ✅ GitHub account (vinaykumarbu)
- ✅ GitHub repository (image_audio_video_maker)
- ✅ Terminal access
- ⏳ Google Drive credentials (optional - can add later)

---

## 🚀 Quick Setup (2 Steps)

### Step 1: Push Your Code to GitHub

```bash
cd /Users/vkuma153/video_generator/image_audio_video_maker

# Add all changes
git add .

# Commit changes
git commit -m "Setup automated video generation with GitHub Actions"

# Push to GitHub
git push origin main
```

### Step 2: Bookmark the Workflow URL

Save this link in your browser bookmarks:

```
https://github.com/vinaykumarbu/image_audio_video_maker/actions/workflows/generate-videos.yml
```

**That's it!** You're ready to use it.

---

## 🎯 How to Generate Videos

### Quick Steps:

1. **Open your bookmark** (the link above)
2. **Click "Run workflow"** button (top right)
3. **Fill in the form:**
   - Language: Select from dropdown (ENGLISH, KANNADA, HINDI, etc.)
   - Start: First file number (e.g., 1)
   - End: Last file number (e.g., 3)
4. **Click the green "Run workflow"** button
5. **Done!** Videos will be generated and downloaded in ~15-20 minutes

---

## 📂 Where to Find Output

After the workflow completes:

1. **Check the workflow run:**
   - Go to: https://github.com/vinaykumarbu/image_audio_video_maker/actions
   - Click on the latest run
   - Scroll down to "Artifacts" section
   - Download the `generated-videos` zip file

2. **Videos will be in:** `output/` folder in the downloaded zip

---

## ⚙️ Optional: Setup Google Drive Upload

If you want videos automatically uploaded back to Google Drive, follow these steps:

### Step A: Setup gdrive Authentication

```bash
# Install gdrive (if not already done)
brew install gdrive

# Authenticate
gdrive about
```

This will give you instructions to set up Google API credentials (takes ~30 minutes).

### Step B: Add GDRIVE_TOKEN to GitHub Secrets

1. After authentication completes, copy your token:

   ```bash
   cat ~/.gdrive/token_v2.json
   ```

2. Go to: https://github.com/vinaykumarbu/image_audio_video_maker/settings/secrets/actions

3. Click "New repository secret"

4. Add secret:
   - Name: `GDRIVE_TOKEN`
   - Value: Paste the entire content from `token_v2.json`

5. Click "Add secret"

Now uploads will work automatically!

---

## ✅ Testing

### Test the Workflow

1. Go to: https://vinaykumarbu.github.io/image_audio_video_maker/
2. Fill the form:
   - Language: ENGLISH
   - Start: 1
   - End: 1
3. Click "Generate Videos"
4. Should see success message
5. Check workflow at: https://github.com/vinaykumarbu/image_audio_video_maker/actions

### Verify Setup

```bash
# Check folder structure
ls -la .github/workflows/
# Should see: generate-videos.yml

ls -la docs/
# Should see: index.html
```

---

## 📱 Share with Your Team

Send this link to your team:

```
https://vinaykumarbu.github.io/image_audio_video_maker/
```

They can bookmark it and use it anytime!

---

## 🔧 Troubleshooting

### Workflow fails with "Authentication error"

- Check if `GDRIVE_TOKEN` secret is set correctly
- Token may have expired, regenerate: `gdrive about`

### Web interface says "Failed to start"

- Check if GitHub token in `index.html` is correct
- Token needs `repo` and `workflow` scopes

### No videos generated

- Check if Google Drive folder IDs are configured in:
  - `download_from_gdrive.py`
  - `upload_to_gdrive.py`

---

## 📊 Monitoring

View all workflow runs:
https://github.com/vinaykumarbu/image_audio_video_maker/actions

Each run shows:

- ✅ Success/Failure status
- ⏱️ Duration
- 📋 Detailed logs
- 🔄 Ability to re-run

---

## 💡 Next Steps

1. Test with 1 video first
2. Train your team on how to use the web form
3. Monitor first few runs to ensure everything works
4. Adjust batch sizes based on processing time

---

## 📞 Support

If issues arise:

1. Check workflow logs on GitHub
2. Verify Google Drive has the files
3. Ensure folder IDs are correct
4. Check secrets are configured
