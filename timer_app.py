#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
import csv
import os
import json
from pathlib import Path
from PIL import Image, ImageTk


class TimerWidget:
    def __init__(self, parent, row, timer_number, label_text=None, elapsed_time=0):
        self.running = False
        self.start_time = None
        self.elapsed = elapsed_time
        self.sessions = []  # List of (start_time, stop_time, duration)
        self.row = row
        self.timer_number = timer_number

        # Frame for this timer
        self.frame = tk.Frame(parent, bg='#2b2b2b', padx=20, pady=15)
        self.frame.grid(row=row, column=0, pady=10, padx=20)

        # Label entry
        default_label = label_text if label_text else f"Timer {timer_number}"
        self.label_var = tk.StringVar(value=default_label)
        self.label_entry = tk.Entry(
            self.frame,
            textvariable=self.label_var,
            font=('Arial', 14),
            width=20,
            bg='#3b3b3b',
            fg='white',
            insertbackground='white',
            relief='flat',
            justify='center'
        )
        self.label_entry.grid(row=0, column=0, pady=(0, 10))

        # Timer display (clickable)
        self.timer_frame = tk.Frame(
            self.frame,
            bg='#cc3333',  # Red background
            padx=30,
            pady=20,
            cursor='hand2'
        )
        self.timer_frame.grid(row=1, column=0)

        self.time_label = tk.Label(
            self.timer_frame,
            text=self.format_time(self.elapsed),
            font=('Courier New', 48, 'bold'),
            fg='black',
            bg='#cc3333'
        )
        self.time_label.pack()

        # Bind click events
        self.timer_frame.bind('<Button-1>', self.toggle)
        self.time_label.bind('<Button-1>', self.toggle)

    def toggle(self, event=None):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        self.running = True
        self.start_time = datetime.now()
        self.start_timestamp = time.time()
        # Turn green
        self.timer_frame.config(bg='#33cc33')
        self.time_label.config(bg='#33cc33')
        self.update()

    def stop(self):
        self.running = False
        stop_time = datetime.now()
        duration = time.time() - self.start_timestamp
        self.sessions.append((self.start_time, stop_time, duration))
        self.elapsed += duration
        # Turn red
        self.timer_frame.config(bg='#cc3333')
        self.time_label.config(bg='#cc3333')

    def update(self):
        if self.running:
            current_elapsed = self.elapsed + (time.time() - self.start_timestamp)
            self.time_label.config(text=self.format_time(current_elapsed))
            self.timer_frame.after(100, self.update)

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def get_label(self):
        return self.label_var.get()

    def get_sessions(self):
        return self.sessions

    def get_elapsed(self):
        if self.running:
            return self.elapsed + (time.time() - self.start_timestamp)
        return self.elapsed

    def destroy(self):
        self.frame.destroy()


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Timer")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(True, True)
        self.timers = []
        self.timer_count = 0

        # Get the config file path
        self.config_path = Path.home() / ".multi_timer_config.json"

        # Create scrollable canvas
        self.canvas = tk.Canvas(root, bg='#1e1e1e', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#1e1e1e')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind canvas resize to center content
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Enable mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Main container frame inside scrollable area
        self.main_frame = tk.Frame(self.scrollable_frame, bg='#1e1e1e')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Load and display logo image
        self.load_logo()

        # Title
        title = tk.Label(
            self.main_frame,
            text="Click timer to start/stop",
            font=('Arial', 12),
            fg='#888888',
            bg='#1e1e1e'
        )
        title.grid(row=1, column=0, pady=(10, 20))

        # Timer container frame
        self.timer_container = tk.Frame(self.main_frame, bg='#1e1e1e')
        self.timer_container.grid(row=2, column=0)
        self.timer_container.grid_columnconfigure(0, weight=1)

        # Load saved config or create default timers
        saved_config = self.load_config()
        if saved_config:
            for timer_data in saved_config:
                self.add_timer(
                    label_text=timer_data.get('label'),
                    elapsed_time=timer_data.get('elapsed', 0)
                )
        else:
            # Create three default timers
            for i in range(3):
                self.add_timer()

        # Button frame
        self.button_frame = tk.Frame(self.main_frame, bg='#1e1e1e')
        self.button_frame.grid(row=3, column=0, pady=20)

        # Add Timer button
        self.add_timer_btn = tk.Button(
            self.button_frame,
            text="+ Add Timer",
            font=('Arial', 12, 'bold'),
            bg='#5a5a5a',
            fg='black',
            activebackground='#4a4a4a',
            activeforeground='black',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.add_timer
        )
        self.add_timer_btn.grid(row=0, column=0, padx=5)

        # Save Timers button
        self.save_btn = tk.Button(
            self.button_frame,
            text="Save Timers for Next Session",
            font=('Arial', 12, 'bold'),
            bg='#6a4aaa',
            fg='black',
            activebackground='#5a3a9a',
            activeforeground='black',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.save_config
        )
        self.save_btn.grid(row=0, column=1, padx=5)

        # Export button
        self.export_btn = tk.Button(
            self.main_frame,
            text="Export to CSV",
            font=('Arial', 14, 'bold'),
            bg='#4a90d9',
            fg='black',
            activebackground='#3a7bc8',
            activeforeground='black',
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.export_csv
        )
        self.export_btn.grid(row=4, column=0, pady=20)

        # Configure grid
        self.main_frame.grid_columnconfigure(0, weight=1)

    def load_logo(self):
        """Load and display the logo image at the top of the app."""
        try:
            # Try to find the logo in various locations
            possible_paths = [
                Path(__file__).parent / "Multi-Timer App.png",
                Path.home() / "Dropbox" / "Tech Inclusion Pro" / "Applications" / "Multi-Timer App" / "Multi-Timer App.png",
                Path(__file__).parent / "resources" / "Multi-Timer App.png",
            ]

            logo_path = None
            for path in possible_paths:
                if path.exists():
                    logo_path = path
                    break

            if logo_path:
                # Open and resize the image
                img = Image.open(logo_path)
                # Resize to reasonable size for header (e.g., 100x100)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)

                logo_label = tk.Label(
                    self.main_frame,
                    image=self.logo_image,
                    bg='#1e1e1e'
                )
                logo_label.grid(row=0, column=0, pady=(0, 10))
        except Exception as e:
            # If logo can't be loaded, just skip it
            print(f"Could not load logo: {e}")

    def on_canvas_configure(self, event):
        """Center the content in the canvas."""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_timer(self, label_text=None, elapsed_time=0):
        """Add a new timer to the app."""
        self.timer_count += 1
        row = len(self.timers)
        timer = TimerWidget(
            self.timer_container,
            row,
            self.timer_count,
            label_text=label_text,
            elapsed_time=elapsed_time
        )
        self.timers.append(timer)

        # Update scroll region
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save_config(self):
        """Save current timer configurations to a file."""
        config = []
        for timer in self.timers:
            config.append({
                'label': timer.get_label(),
                'elapsed': timer.get_elapsed()
            })

        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f)
            messagebox.showinfo("Saved", "Timers saved! They will be restored next time you open the app.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save timers: {str(e)}")

    def load_config(self):
        """Load timer configurations from file if it exists."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Could not load config: {e}")
        return None

    def export_csv(self):
        # Check if there's any data to export
        has_data = any(timer.get_sessions() for timer in self.timers)

        if not has_data:
            messagebox.showwarning("No Data", "No timer sessions to export. Start and stop at least one timer first.")
            return

        # Save directly to desktop
        desktop = Path.home() / "Desktop"
        filename = desktop / f"timer_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timer Name', 'Start Time', 'Stop Time', 'Duration'])

                for timer in self.timers:
                    label = timer.get_label()
                    for start, stop, duration in timer.get_sessions():
                        formatted_duration = timer.format_time(duration)
                        writer.writerow([
                            label,
                            start.strftime('%Y-%m-%d %H:%M:%S'),
                            stop.strftime('%Y-%m-%d %H:%M:%S'),
                            formatted_duration
                        ])

            messagebox.showinfo("Export Successful", f"Timer data exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")


def main():
    root = tk.Tk()
    root.geometry("500x800")
    app = TimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
