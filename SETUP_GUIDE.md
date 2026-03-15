# 🎬 Video Generator - Setup Guide

## 📋 Overview
This guide will help you set up the automated video generation system using GitHub Actions.

## ⚙️ Prerequisites
- GitHub account (already have: vinaykumarbu)
- GitHub repository (already exists: image_audio_video_maker)
- Terminal access
- Google Drive credentials configured

---

## 🚀 Setup Instructions

### Step 1: Update Your GitHub Repository

```bash
cd /Users/vkuma153/video_generator/image_audio_video_maker

# Add all latest changes
git add .

# Commit changes
git commit -m "Add GitHub Actions workflow and web interface"

# Push to GitHub
git push origin main
```

### Step 2: Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: `Video Generator Workflow`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **COPY THE TOKEN** (you'll need it in Step 5)
   - `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 3: Configure Google Drive Token

```bash
# Authenticate with gdrive (if not already done)
gdrive about

# Copy the token
cat ~/.gdrive/token_v2.json
```

Copy the entire output (it's a JSON object).

### Step 4: Add Secrets to GitHub

1. Go to: https://github.com/vinaykumarbu/image_audio_video_maker/settings/secrets/actions
2. Click "New repository secret"
3. Add secret:
   - Name: `GDRIVE_TOKEN`
   - Value: Paste the content from `token_v2.json`
4. Click "Add secret"

### Step 5: Configure Web Interface

Edit the file: `docs/index.html`

Find this line (around line 195):
```javascript
const GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN_HERE';
```

Replace with your token from Step 2:
```javascript
const GITHUB_TOKEN = 'ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
```

Save the file and push:
```bash
git add docs/index.html
git commit -m "Configure GitHub token in web interface"
git push origin main
```

### Step 6: Enable GitHub Pages

1. Go to: https://github.com/vinaykumarbu/image_audio_video_maker/settings/pages
2. Under "Source", select:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
3. Click "Save"
4. Wait 1-2 minutes
5. Your page will be live at: https://vinaykumarbu.github.io/image_audio_video_maker/

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

