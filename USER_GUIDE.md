# 📖 Quick Reference: Manual Workflow Trigger

---

## 🎯 How to Generate Videos (30 seconds)

### **Step 1:** Open the Workflow Page

Bookmark and open this link:

```
https://github.com/vinaykumarbu/image_audio_video_maker/actions/workflows/generate-videos.yml
```

---

### **Step 2:** Click "Run workflow"

Look for the **"Run workflow"** button on the right side (green button).

---

### **Step 3:** Fill in the Details

A form will appear with these fields:

| Field        | Example   | Description                                                |
| ------------ | --------- | ---------------------------------------------------------- |
| **Language** | `ENGLISH` | Select: ENGLISH, KANNADA, HINDI, TAMIL, TELUGU, or MARATHI |
| **Start**    | `1`       | First file number (e.g., 1 for GGENG001)                   |
| **End**      | `3`       | Last file number (e.g., 3 for GGENG003)                    |

---

### **Step 4:** Click the Green "Run workflow" Button

The workflow will start immediately!

---

## ⏱️ What Happens Next?

1. **Download** (~2 min): Downloads images and audio from Google Drive
2. **Generate** (~10-15 min): Creates videos using ffmpeg
3. **Upload** (~2 min): Uploads videos back to Google Drive (optional)

**Total Time:** ~15-20 minutes

---

## 📊 Check Progress

1. Go to: https://github.com/vinaykumarbu/image_audio_video_maker/actions
2. Click on the latest workflow run (at the top)
3. Watch the progress in real-time

**Status indicators:**

- 🟡 Yellow spinning = Running
- ✅ Green checkmark = Success
- ❌ Red X = Failed (check logs)

---

## 📂 Get Your Videos

### Option 1: From GitHub (if upload disabled)

1. Go to the completed workflow run
2. Scroll down to **"Artifacts"** section
3. Download the `generated-videos` zip file
4. Unzip and find videos in `output/` folder

### Option 2: From Google Drive (if upload enabled)

Videos will automatically appear in:

```
Srisatupasi > GG LANGUAGE > video files > MP4 files
```

Example: For English videos, check:

```
Srisatupasi > GG ENGLISH > video files > MP4 files
```

---

## 💬 Communication with Team

When your team says: _"We uploaded GGENG001-003 images and audio"_

You:

1. Open the bookmark
2. Click "Run workflow"
3. Select: Language=ENGLISH, Start=1, End=3
4. Click green button
5. Reply: _"Started! Videos will be ready in ~20 minutes"_

**That's it!** No need to download/upload manually anymore.

- English
- Kannada
- Hindi
- Tamil
- Telugu
- Marathi

**Example:** If you uploaded English files, select "English"

---

### Step 3: Enter File Numbers

#### Start Number

This is the **first** file number you want to convert to video.

**Example:**

- If your first file is `GGENG001.jpg`, enter: **1**
- If your first file is `GGENG010.jpg`, enter: **10**

#### End Number

This is the **last** file number you want to convert to video.

**Example:**

- If your last file is `GGENG003.jpg`, enter: **3**
- If your last file is `GGENG015.jpg`, enter: **15**

---

### Step 4: Click "Generate Videos"

Click the big purple button that says **"Generate Videos"**

---

### Step 5: Wait for Confirmation

You'll see a green success message:

```
✅ Success! Video generation started for English (1-3).

⏱️ This will take approximately 15-20 minutes.

📁 Videos will appear in Google Drive when complete.
```

**That's it! You're done!**

The videos will automatically appear in Google Drive in 15-20 minutes.

---

## 📋 Complete Example

**Scenario:** You uploaded these files to Google Drive:

- Images: `GGENG001.jpg`, `GGENG002.jpg`, `GGENG003.jpg`
- Audio: `GGENG001.mp3`, `GGENG002.mp3`, `GGENG003.mp3`

**What to do:**

1. Open: https://vinaykumarbu.github.io/image_audio_video_maker/
2. Select Language: **English**
3. Start Number: **1**
4. End Number: **3**
5. Click **"Generate Videos"**
6. Wait 15-20 minutes
7. Check Google Drive folder for videos!

---

## ❓ Common Questions

### Q: How long does it take?

**A:** Usually 15-20 minutes for 1-3 videos. Larger batches may take longer.

### Q: Where do the videos appear?

**A:** In the same Google Drive folder structure, in a "Generated Videos" folder.

### Q: Can I generate videos for multiple languages at once?

**A:** Yes! Open the page in different browser tabs and submit one for each language.

### Q: What if I make a mistake?

**A:** Just fill the form again with the correct numbers and click generate.

### Q: How do I know if it's working?

**A:** You'll see a green success message. After 15-20 minutes, check Google Drive.

### Q: What if I don't see the success message?

**A:** Try again or contact the administrator.

---

## 🚨 Important Notes

### ✅ DO:

- Make sure image AND audio files are uploaded before generating
- Use the correct file numbers
- Wait for the success message before closing the page

### ❌ DON'T:

- Don't click "Generate Videos" multiple times (wait for the message)
- Don't close your browser immediately after clicking
- Don't use file names, only use numbers (1, 2, 3, not GGENG001)

---

## 🎯 Quick Reference Card

**Print this and keep it handy:**

```
┌─────────────────────────────────────┐
│  VIDEO GENERATOR - QUICK GUIDE      │
├─────────────────────────────────────┤
│                                     │
│ 1. Open Browser                     │
│    vinaykumarbu.github.io/          │
│    image_audio_video_maker          │
│                                     │
│ 2. Fill Form:                       │
│    ✓ Language (English, Hindi...)   │
│    ✓ Start Number (e.g., 1)         │
│    ✓ End Number (e.g., 3)           │
│                                     │
│ 3. Click "Generate Videos"          │
│                                     │
│ 4. Wait 15-20 minutes              │
│                                     │
│ 5. Check Google Drive               │
│                                     │
│ Need Help? Contact: [Your Contact] │
│                                     │
└─────────────────────────────────────┘
```

---

## 📞 Support

If you have any issues:

1. Take a screenshot of the error message
2. Note down what numbers you entered
3. Contact: **[Add your contact info here]**

---

**Remember:** You're just 3 clicks away from automated video generation! 🎬
