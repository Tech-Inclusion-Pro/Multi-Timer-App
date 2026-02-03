# Multi-Timer App

<p align="center">
  <img src="Multi-Timer App.png" alt="Multi-Timer App Logo" width="200"/>
</p>

<p align="center">
  <strong>Track time for many projects at once!</strong>
</p>

---

## What is Multi-Timer?

Multi-Timer is a free app that helps you keep track of time. You can use it to see how long you work on different things. It's like having many stopwatches on your screen at the same time!

### What Can You Do With It?

- **Start and stop timers** - Just click on a timer to start it. Click again to stop it.
- **Name your timers** - Give each timer a name like "Homework" or "Reading" or "Art Project"
- **Add more timers** - Need more than 3 timers? Just click the "Add Timer" button!
- **Save your timers** - Click "Save Timers for Next Session" and your timers will be there when you open the app again
- **Export to a file** - Save all your time data to a file you can open in Excel or Google Sheets

---

## How to Download and Install (Mac Computer)

Follow these easy steps to get Multi-Timer on your Mac computer!

### Step 1: Download the App

1. Look at the top of this page
2. Find the green button that says **"Code"**
3. Click on it
4. Click on **"Download ZIP"**
5. Wait for the download to finish

### Step 2: Find the Downloaded File

1. Open **Finder** (the blue and white smiley face icon in your dock)
2. Click on **Downloads** on the left side
3. Look for a file called **"Multi-Timer-App-main.zip"**

### Step 3: Unzip the File

1. Double-click on **"Multi-Timer-App-main.zip"**
2. A new folder will appear called **"Multi-Timer-App-main"**
3. Double-click on that folder to open it

### Step 4: Move the App to Your Applications Folder

1. Inside the folder, find **"Multi-Timer.app"**
2. Open a new Finder window (press Command + N)
3. Click on **Applications** on the left side
4. Drag **"Multi-Timer.app"** into the Applications folder

### Step 5: Open the App for the First Time

**Important!** The first time you open the app, you need to do something special because Mac wants to keep you safe from unknown apps.

1. Go to your **Applications** folder
2. Find **Multi-Timer.app**
3. **Right-click** on it (or hold Control and click)
4. Click **"Open"** from the menu that appears
5. A box will pop up asking if you want to open it
6. Click **"Open"** again

That's it! The app will open and you can start using it!

**Good news:** You only need to do the right-click thing once. After that, you can just double-click to open it like any other app.

---

## How to Use Multi-Timer

### Starting a Timer

1. Look at one of the red timer boxes
2. Click on it!
3. The box will turn **green** and start counting

### Stopping a Timer

1. Click on the green timer box
2. It will turn **red** and stop counting
3. Your time is saved!

### Naming Your Timers

1. Look above each timer - there's a text box
2. Click on it and type a new name
3. Press Enter or click somewhere else

### Adding More Timers

1. Find the **"+ Add Timer"** button
2. Click on it
3. A new timer will appear!

### Saving Your Timers

Want your timers to still be there when you close and open the app again?

1. Click the **"Save Timers for Next Session"** button
2. You'll see a message that says your timers are saved
3. Close the app
4. Open it again - your timers are still there!

### Exporting Your Time Data

Want to see all your times in a spreadsheet?

1. Make sure you've started and stopped at least one timer
2. Click the **"Export to CSV"** button
3. A file will be saved to your Desktop
4. Open it with Excel, Google Sheets, or Numbers

---

## Troubleshooting

### The app won't open!

If you see a message that says the app "can't be opened" or is from an "unidentified developer":

1. Go to **System Preferences** (or System Settings)
2. Click on **Security & Privacy** (or Privacy & Security)
3. Look for a message about Multi-Timer being blocked
4. Click **"Open Anyway"**

### The timers disappeared!

Did you forget to save? Next time, click **"Save Timers for Next Session"** before closing the app.

### I need help!

Ask a teacher, parent, or grown-up for help if something isn't working.

---

## For Developers

If you want to run this app from the source code:

### Requirements

- Python 3.10 or newer
- Pillow (PIL) library

### Installation

```bash
# Install required library
pip install Pillow

# Run the app
python timer_app.py
```

### Building the App

To create a standalone Mac app:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the app
pyinstaller --onefile --windowed --name "Multi-Timer" --icon="MultiTimer.icns" --add-data "Multi-Timer App.png:." timer_app.py
```

---

## License

This app is free to use for everyone!

---

<p align="center">
  Made with love by Rocco Catrone at <a href="https://github.com/Tech-Inclusion-Pro">Tech Inclusion Pro</a>
</p>
