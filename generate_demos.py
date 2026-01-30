import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip

def create_terminal_frame(text, width=640, height=360):
    """Creates a single frame that looks like a terminal."""
    # Dark background
    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        # Common paths for linux/mac
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
        if not os.path.exists(font_path):
            font_path = "/System/Library/Fonts/Menlo.ttc" # Mac
        font = ImageFont.truetype(font_path, 18)
    except:
        font = ImageFont.load_default()

    # Draw text
    draw.text((20, 20), text, fill=(50, 255, 50), font=font)
    return np.array(img)

def generate_video(lines, output_path):
    """Generates a typewriter-style video from a list of lines."""
    frames = []
    current_text = ""
    
    for line in lines:
        # Typewriter effect for each line
        for char in line:
            current_text += char
            # Add a frame every character (might be too many, let's do every 2)
            if len(current_text) % 2 == 0:
                frames.append(create_terminal_frame(current_text))
        
        current_text += "\n"
        # Pause at the end of a line
        for _ in range(5):
            frames.append(create_terminal_frame(current_text))

    # Final pause
    for _ in range(20):
        frames.append(create_terminal_frame(current_text))

    clip = ImageSequenceClip(frames, fps=24)
    clip.write_videofile(output_path, codec="libx264", audio=False, logger=None)
    print(f"✅ Video saved to {output_path}")

# --- DEMO DATA ---

cricket_lines = [
    "Welcome to Bengaluru Tech Titans Arena! 🏟️",
    "Match: Student vs Computer",
    "",
    "Enter your name: Virat",
    "Ready, Virat? Over 1, Ball 1...",
    "",
    "Computer bowls...",
    "Virat swings his bat... 🏏",
    "IT'S A HUGE SIX! 🚀🚀🚀",
    "",
    "Score: 6/0 (0.1 Overs)",
    "Master the logic to build this game!"
]

blog_lines = [
    "Generating Food Blog... 🌐",
    "",
    "Scanning favorites: ['Vidyarthi Bhavan', 'CTR']",
    "",
    "Building HTML structure...",
    "Adding CSS for Bangalore vibe...",
    "",
    "Success! index.html created.",
    "Previewing: <h1>Best Dosa in South BLR</h1>",
    "Learn to automate the web!"
]

tracker_lines = [
    "💰 Kharcha Tracker v1.0",
    "------------------------",
    "1. Add Expense",
    "2. Show Total",
    "3. Exit",
    "",
    "Action: 1",
    "Item: Auto to Indiranagar",
    "Amount: 120",
    "",
    "Action: 2",
    "Total Spend: ₹120 🛺",
    "Master data and tracking!"
]

if __name__ == "__main__":
    os.makedirs("static/demos", exist_ok=True)
    generate_video(cricket_lines, "static/demos/cricket_demo.mp4")
    generate_video(blog_lines, "static/demos/blog_demo.mp4")
    generate_video(tracker_lines, "static/demos/tracker_demo.mp4")
