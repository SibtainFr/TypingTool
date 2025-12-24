#!/usr/bin/env python3


import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
import sys
import subprocess
import webbrowser
from difflib import SequenceMatcher
from datetime import datetime

# Auto-install dependencies
def check_and_install_dependencies():
    """Check and install required packages"""
    required = ['requests']
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

check_and_install_dependencies()
import requests

class TypingTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Tester")
        
       
        self.root.overrideredirect(True)
        
        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set transparency (0.97 = 97% opaque)
        self.root.attributes('-alpha', 0.97)
        
        # Deep black background
        self.root.configure(bg='#000000')
        
        # Colors
        self.bg_primary = '#000000'      # Deep black
        self.bg_secondary = '#0A0A0A'    # Slightly lighter black
        self.cyan = '#00FFFF'            # Bright cyan
        self.white = '#FFFFFF'           # Pure white
        self.cyan_dim = '#00CED1'        # Dimmed cyan
        self.gray = '#808080'            # Gray for subtle elements
        
        # Variables
        self.mode = None
        self.difficulty = "medium"
        self.duration = 60
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.timer_id = None
        self.remaining_time = 0
        self.last_wpm = 0
        self.keystroke_count = 0
        self.target_text = ""
        
        # Word lists
        self.easy_words = [
            "the", "and", "for", "are", "but", "not", "you", "all", "can", "her",
            "was", "one", "our", "out", "day", "get", "has", "him", "his", "how",
            "man", "new", "now", "old", "see", "two", "way", "who", "boy", "did"
        ]
        
        self.medium_words = [
            "about", "after", "again", "below", "could", "every", "first", "found",
            "great", "house", "learn", "never", "other", "place", "right", "small",
            "sound", "spell", "still", "study", "their", "there", "these", "thing",
            "think", "three", "water", "where", "which", "world", "would", "write"
        ]
        
        self.hard_symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+"]
        
        self.hard_words = [
            "algorithm", "structure", "function", "variable", "exception", "dictionary",
            "implementation", "configuration", "authentication", "synchronization",
            "optimization", "initialization", "documentation", "specification"
        ]
        
        # For window dragging
        self.drag_x = 0
        self.drag_y = 0
        
        self.create_widgets()
        self.log_message("Application initialized successfully")
        self.log_message("Press ESC to exit fullscreen")
        
    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y
        
    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.drag_x
        y = self.root.winfo_y() + event.y - self.drag_y
        self.root.geometry(f"+{x}+{y}")
        
    def log_message(self, message):
        """Add message to terminal log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_display.config(state=tk.NORMAL)
        self.log_display.insert(tk.END, log_entry)
        self.log_display.see(tk.END)
        self.log_display.config(state=tk.DISABLED)
        
    def create_widgets(self):
        """Create all GUI elements"""
        
        # Main container
        container = tk.Frame(self.root, bg=self.bg_primary)
        container.pack(fill=tk.BOTH, expand=True)
        
        # === CUSTOM TITLE BAR ===
        titlebar = tk.Frame(container, bg=self.bg_secondary, height=40)
        titlebar.pack(fill=tk.X, side=tk.TOP)
        titlebar.pack_propagate(False)
        
        # Bind dragging
        titlebar.bind('<Button-1>', self.start_drag)
        titlebar.bind('<B1-Motion>', self.do_drag)
        
        # Title
        title_label = tk.Label(titlebar, text="⌨️ Typing Tester", 
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.bg_secondary, fg=self.cyan)
        title_label.pack(side=tk.LEFT, padx=15)
        title_label.bind('<Button-1>', self.start_drag)
        title_label.bind('<B1-Motion>', self.do_drag)
        
        # Window controls
        btn_frame = tk.Frame(titlebar, bg=self.bg_secondary)
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        minimize_btn = tk.Label(btn_frame, text="─", font=('Segoe UI', 12, 'bold'),
                               bg=self.bg_secondary, fg=self.white,
                               cursor='hand2', padx=10)
        minimize_btn.pack(side=tk.LEFT)
        minimize_btn.bind('<Button-1>', lambda e: self.root.iconify())
        
        close_btn = tk.Label(btn_frame, text="✕", font=('Segoe UI', 12, 'bold'),
                            bg=self.bg_secondary, fg=self.white,
                            cursor='hand2', padx=10)
        close_btn.pack(side=tk.LEFT)
        close_btn.bind('<Button-1>', lambda e: self.root.quit())
        
        # === MAIN CONTENT ===
        content = tk.Frame(container, bg=self.bg_primary)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Main app
        left_panel = tk.Frame(content, bg=self.bg_primary)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel - Terminal
        right_panel = tk.Frame(content, bg=self.bg_primary, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, pady=0)
        right_panel.pack_propagate(False)
        
      
        
        
        header = tk.Label(left_panel, text="TYPING SPEED TEST",
                         font=('Segoe UI', 36, 'bold'),
                         bg=self.bg_primary, fg=self.cyan)
        header.pack(pady=(20, 5))
        
        subtitle = tk.Label(left_panel, text="Test your speed • Track your progress • Master your skills",
                           font=('Segoe UI', 11),
                           bg=self.bg_primary, fg=self.white)
        subtitle.pack(pady=(0, 30))
        
       
        
       
        self.display_frame = tk.Frame(left_panel, bg=self.bg_secondary, 
                                     highlightbackground=self.cyan,
                                     highlightthickness=1)
        self.display_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        
        display_label = tk.Label(self.display_frame, text="TEXT TO TYPE",
                                font=('Segoe UI', 10, 'bold'),
                                bg=self.bg_secondary, fg=self.white)
        display_label.pack(pady=(10, 5))
        
        self.text_display = tk.Text(self.display_frame,
                                   font=('Consolas', 12),
                                   bg=self.bg_secondary, fg=self.white,
                                   insertbackground=self.cyan,
                                   selectbackground=self.cyan,
                                   selectforeground=self.bg_primary,
                                   wrap=tk.WORD,
                                   height=5,
                                   relief=tk.FLAT,
                                   bd=0,
                                   state=tk.DISABLED)
        self.text_display.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        
        self.text_display.tag_config('correct', background='#003333', foreground=self.cyan)
        self.text_display.tag_config('incorrect', background='#330000', foreground='#FF6666')
        self.text_display.tag_config('untyped', foreground=self.white)
        
        # Input area (where you type) - RIGHT BELOW TEXT
        self.input_frame = tk.Frame(left_panel, bg=self.bg_primary)
        self.input_frame.pack(fill=tk.X, padx=0, pady=(0, 15))
        
        input_label = tk.Label(self.input_frame, text="TYPE HERE",
                              font=('Segoe UI', 10, 'bold'),
                              bg=self.bg_primary, fg=self.white)
        input_label.pack(pady=(10, 5))
        
        input_container = tk.Frame(self.input_frame, bg=self.bg_secondary,
                                  highlightbackground=self.cyan,
                                  highlightthickness=1)
        input_container.pack(fill=tk.X, padx=0, pady=5)
        
        self.input_text = tk.Text(input_container,
                                 font=('Consolas', 12),
                                 bg=self.bg_secondary, fg=self.cyan,
                                 insertbackground=self.cyan,
                                 selectbackground=self.cyan,
                                 selectforeground=self.bg_primary,
                                 wrap=tk.WORD,
                                 height=4,
                                 relief=tk.FLAT,
                                 bd=0,
                                 state=tk.DISABLED)
        self.input_text.pack(fill=tk.X, padx=15, pady=15)
        self.input_text.bind('<KeyRelease>', self.on_key_press)
        
       
        mode_label = tk.Label(left_panel, text="SELECT MODE",
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.bg_primary, fg=self.white)
        mode_label.pack(pady=(5, 10))
        
        mode_frame = tk.Frame(left_panel, bg=self.bg_primary)
        mode_frame.pack(pady=5)
        
        self.mode1_btn = tk.Button(mode_frame, text="🎲 RANDOM WORDS",
                                   command=lambda: self.select_mode(1),
                                   font=('Segoe UI', 10, 'bold'),
                                   bg=self.bg_secondary, fg=self.cyan,
                                   activebackground=self.cyan,
                                   activeforeground=self.bg_primary,
                                   relief=tk.FLAT,
                                   bd=0,
                                   width=18, height=1,
                                   cursor='hand2')
        self.mode1_btn.pack(side=tk.LEFT, padx=10)
        
        self.mode2_btn = tk.Button(mode_frame, text="📖 PARAGRAPH",
                                   command=lambda: self.select_mode(2),
                                   font=('Segoe UI', 10, 'bold'),
                                   bg=self.bg_secondary, fg=self.cyan,
                                   activebackground=self.cyan,
                                   activeforeground=self.bg_primary,
                                   relief=tk.FLAT,
                                   bd=0,
                                   width=18, height=1,
                                   cursor='hand2')
        self.mode2_btn.pack(side=tk.LEFT, padx=10)
        
        # Difficulty selection
        self.difficulty_frame = tk.Frame(left_panel, bg=self.bg_primary)
        
        diff_label = tk.Label(self.difficulty_frame, text="DIFFICULTY",
                             font=('Segoe UI', 9, 'bold'),
                             bg=self.bg_primary, fg=self.white)
        diff_label.pack(pady=(5, 8))
        
        diff_buttons = tk.Frame(self.difficulty_frame, bg=self.bg_primary)
        diff_buttons.pack()
        
        self.easy_btn = tk.Button(diff_buttons, text="EASY",
                                 command=lambda: self.set_difficulty("easy"),
                                 font=('Segoe UI', 9, 'bold'),
                                 bg=self.bg_secondary, fg=self.white,
                                 activebackground=self.cyan,
                                 activeforeground=self.bg_primary,
                                 relief=tk.FLAT, bd=0,
                                 width=12, cursor='hand2')
        self.easy_btn.pack(side=tk.LEFT, padx=5)
        
        self.medium_btn = tk.Button(diff_buttons, text="MEDIUM",
                                   command=lambda: self.set_difficulty("medium"),
                                   font=('Segoe UI', 9, 'bold'),
                                   bg=self.bg_secondary, fg=self.cyan,
                                   activebackground=self.cyan,
                                   activeforeground=self.bg_primary,
                                   relief=tk.FLAT, bd=0,
                                   width=12, cursor='hand2')
        self.medium_btn.pack(side=tk.LEFT, padx=5)
        
        self.hard_btn = tk.Button(diff_buttons, text="HARD",
                                 command=lambda: self.set_difficulty("hard"),
                                 font=('Segoe UI', 9, 'bold'),
                                 bg=self.bg_secondary, fg=self.white,
                                 activebackground=self.cyan,
                                 activeforeground=self.bg_primary,
                                 relief=tk.FLAT, bd=0,
                                 width=12, cursor='hand2')
        self.hard_btn.pack(side=tk.LEFT, padx=5)
        
        # Duration selection
        self.duration_frame = tk.Frame(left_panel, bg=self.bg_primary)
        
        dur_label = tk.Label(self.duration_frame, text="DURATION",
                            font=('Segoe UI', 9, 'bold'),
                            bg=self.bg_primary, fg=self.white)
        dur_label.pack(pady=(5, 8))
        
        duration_buttons = tk.Frame(self.duration_frame, bg=self.bg_primary)
        duration_buttons.pack()
        
        for mins in [1, 2, 3, 4, 5]:
            btn = tk.Button(duration_buttons, text=f"{mins}m",
                          command=lambda m=mins: self.set_duration(m),
                          font=('Segoe UI', 9, 'bold'),
                          bg=self.bg_secondary, fg=self.white,
                          activebackground=self.cyan,
                          activeforeground=self.bg_primary,
                          relief=tk.FLAT, bd=0,
                          width=8, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=3)
        
        # Stats 
        stats_frame = tk.Frame(left_panel, bg=self.bg_primary)
        stats_frame.pack(pady=10)
        
        self.timer_label = tk.Label(stats_frame, text="0:00",
                                   font=('Segoe UI', 24, 'bold'),
                                   bg=self.bg_primary, fg=self.cyan)
        self.timer_label.pack(side=tk.LEFT, padx=15)
        
        self.wpm_label = tk.Label(stats_frame, text="0 WPM",
                                 font=('Segoe UI', 24, 'bold'),
                                 bg=self.bg_primary, fg=self.white)
        self.wpm_label.pack(side=tk.LEFT, padx=15)
        
        self.accuracy_label = tk.Label(stats_frame, text="0%",
                                      font=('Segoe UI', 24, 'bold'),
                                      bg=self.bg_primary, fg=self.cyan)
        self.accuracy_label.pack(side=tk.LEFT, padx=15)
        
        # Control buttons
        control_frame = tk.Frame(left_panel, bg=self.bg_primary)
        control_frame.pack(pady=10)
        
        self.start_btn = tk.Button(control_frame, text="▶ START",
                                   command=self.start_test,
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.cyan, fg=self.bg_primary,
                                   activebackground=self.white,
                                   activeforeground=self.bg_primary,
                                   relief=tk.FLAT, bd=0,
                                   width=15, height=2,
                                   cursor='hand2',
                                   state=tk.DISABLED)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_btn = tk.Button(control_frame, text="🔄 RESET",
                                   command=self.reset_test,
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.bg_secondary, fg=self.white,
                                   activebackground=self.cyan,
                                   activeforeground=self.bg_primary,
                                   relief=tk.FLAT, bd=0,
                                   width=15, height=2,
                                   cursor='hand2')
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        
        # Result label
        self.result_label = tk.Label(left_panel, text="",
                                    font=('Segoe UI', 13, 'bold'),
                                    bg=self.bg_primary, fg=self.cyan)
        
        #logs
        terminal_header = tk.Frame(right_panel, bg=self.bg_secondary, height=40)
        terminal_header.pack(fill=tk.X)
        terminal_header.pack_propagate(False)
        
        term_title = tk.Label(terminal_header, text="📊 SYSTEM",
                             font=('Consolas', 11, 'bold'),
                             bg=self.bg_secondary, fg=self.cyan)
        term_title.pack(pady=10)
        
        log_container = tk.Frame(right_panel, bg=self.bg_secondary)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_display = tk.Text(log_container,
                                  font=('Consolas', 9),
                                  bg=self.bg_primary, fg=self.cyan,
                                  insertbackground=self.cyan,
                                  wrap=tk.WORD,
                                  relief=tk.FLAT,
                                  bd=0,
                                  highlightthickness=0,
                                  state=tk.DISABLED)
        self.log_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # social
        footer = tk.Frame(container, bg=self.bg_secondary, height=35)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        footer_text = tk.Label(footer, text="Created by",
                              font=('Segoe UI', 9),
                              bg=self.bg_secondary, fg=self.gray)
        footer_text.pack(side=tk.LEFT, padx=15)
        
        github_link = tk.Label(footer, text="GitHub: @Pineapple",
                              font=('Segoe UI', 9, 'bold'),
                              bg=self.bg_secondary, fg=self.cyan,
                              cursor='hand2')
        github_link.pack(side=tk.LEFT, padx=5)
        github_link.bind('<Button-1>', 
                        lambda e: webbrowser.open('https://github.com/SibtainFr'))
        
        separator = tk.Label(footer, text="•",
                            font=('Segoe UI', 9),
                            bg=self.bg_secondary, fg=self.gray)
        separator.pack(side=tk.LEFT, padx=5)
        
        instagram_link = tk.Label(footer, text="Instagram: @yourhandle",
                                 font=('Segoe UI', 9, 'bold'),
                                 bg=self.bg_secondary, fg=self.cyan,
                                 cursor='hand2')
        instagram_link.pack(side=tk.LEFT, padx=5)
        instagram_link.bind('<Button-1>',
                           lambda e: webbrowser.open('https://www.instagram.com/sibtain.fr/'))
        
        # Bind ESC to exit
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
    def select_mode(self, mode):
        """Select test mode"""
        self.mode = mode
        
        if mode == 1:
            self.mode1_btn.config(bg=self.cyan, fg=self.bg_primary)
            self.mode2_btn.config(bg=self.bg_secondary, fg=self.cyan)
            self.log_message("Mode selected: Random Words")
            
        elif mode == 2:
            self.mode1_btn.config(bg=self.bg_secondary, fg=self.cyan)
            self.mode2_btn.config(bg=self.cyan, fg=self.bg_primary)
            self.log_message("Mode selected: Paragraph Practice")
        
        self.difficulty_frame.pack(pady=5)
        self.duration_frame.pack(pady=5)
        self.result_label.pack(pady=5)
        
        self.generate_text()
        self.start_btn.config(state=tk.NORMAL)
        
    def set_difficulty(self, diff):
        """Set difficulty level"""
        self.difficulty = diff
        
        self.easy_btn.config(bg=self.bg_secondary, fg=self.white)
        self.medium_btn.config(bg=self.bg_secondary, fg=self.white)
        self.hard_btn.config(bg=self.bg_secondary, fg=self.white)
        
        if diff == "easy":
            self.easy_btn.config(bg=self.cyan, fg=self.bg_primary)
        elif diff == "medium":
            self.medium_btn.config(bg=self.cyan, fg=self.bg_primary)
        elif diff == "hard":
            self.hard_btn.config(bg=self.cyan, fg=self.bg_primary)
        
        self.log_message(f"Difficulty set to: {diff.upper()}")
        if self.mode:
            self.generate_text()
        
    def set_duration(self, minutes):
        """Set test duration"""
        self.duration = minutes * 60
        self.log_message(f"Duration set to: {minutes} minute(s)")
        if self.mode:
            self.generate_text()
        
    def generate_text(self):
        """Generate text based on mode and difficulty"""
        self.log_message("Generating text...")
        
        if self.mode == 1:
            self.generate_random_words()
        elif self.mode == 2:
            self.generate_paragraph_text()
        
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.target_text)
        
        # Apply untyped tag to all text initially
        self.text_display.tag_add('untyped', '1.0', tk.END)
        
        self.text_display.config(state=tk.DISABLED)
        
        word_count = len(self.target_text.split())
        self.log_message(f"Text loaded: {word_count} words")
        
    def generate_random_words(self):
        """Generate random words based on difficulty"""
        avg_wpm = 40
        word_count = int((self.duration / 60) * avg_wpm * 1.5)
        
        words = []
        
        if self.difficulty == "easy":
            words = random.choices(self.easy_words, k=word_count)
        elif self.difficulty == "medium":
            words = random.choices(self.medium_words, k=word_count)
        elif self.difficulty == "hard":
            for _ in range(word_count):
                if random.random() < 0.3:
                    words.append(random.choice(self.hard_symbols))
                else:
                    words.append(random.choice(self.hard_words))
        
        self.target_text = ' '.join(words)
        
    def generate_paragraph_text(self):
        """Generate paragraph text"""
        try:
            avg_wpm = 40
            target_words = int((self.duration / 60) * avg_wpm * 1.8)
            
            if self.difficulty == "easy":
                target_words = int(target_words * 0.8)
            elif self.difficulty == "hard":
                target_words = int(target_words * 1.3)
            
            self.log_message("Fetching text from online source...")
            
            paragraphs_needed = max(2, target_words // 50)
            
            response = requests.get(
                f"https://loripsum.net/api/{paragraphs_needed}/medium/plaintext",
                timeout=5
            )
            
            if response.status_code == 200:
                text = response.text.strip()
                
                words = text.split()
                if len(words) > target_words:
                    words = words[:target_words]
                text = ' '.join(words)
                
                if self.difficulty == "hard":
                    words = text.split()
                    for i in range(len(words)):
                        if random.random() < 0.15:
                            words[i] += random.choice(self.hard_symbols)
                    text = ' '.join(words)
                elif self.difficulty == "easy":
                    text = text.lower()
                
                self.target_text = text
                self.log_message("Text fetched successfully")
            else:
                raise Exception("API error")
                
        except Exception as e:
            self.log_message(f"API fetch failed: {str(e)}")
            self.generate_fallback_paragraph()
    
    def generate_fallback_paragraph(self):
        """Generate paragraph from local content"""
        paragraphs = [
            "The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet and is often used for typing practice. Practice makes perfect, and the more you type, the faster you will become. Consistent practice is the key to improving your typing speed and accuracy.",
            
            "Programming requires logical thinking and attention to detail. Every programmer starts as a beginner, but with consistent practice, anyone can master it. Learning to code opens up countless opportunities in the modern digital world. The journey may be challenging, but it is incredibly rewarding.",
            
            "Technology is transforming the world around us at an unprecedented pace. Machine learning and artificial intelligence are revolutionizing industries from healthcare to finance. The future is full of possibilities for those willing to learn and adapt to new technologies. Innovation drives progress and creates new opportunities.",
            
            "Touch typing is a valuable skill in the digital age. By learning to type without looking at the keyboard, you can significantly increase your productivity and reduce typing errors. Start slowly and gradually build up your speed. With time and practice, touch typing will become second nature.",
            
            "The art of communication has evolved dramatically with the advent of digital technology. From email to instant messaging, we now have countless ways to connect with others. Clear and effective writing skills are more important than ever in our interconnected world. Mastering these skills can open doors to new opportunities.",
            
            "Data science combines statistics, programming, and domain expertise to extract insights from data. Organizations across all industries are leveraging data to make better decisions. The demand for skilled data professionals continues to grow. Learning data analysis tools and techniques is a valuable investment in your future.",
        ]
        
        avg_wpm = 40
        target_words = int((self.duration / 60) * avg_wpm * 1.8)
        
        if self.difficulty == "easy":
            target_words = int(target_words * 0.8)
            num_paragraphs = max(2, min(3, target_words // 60))
        elif self.difficulty == "medium":
            num_paragraphs = max(3, min(4, target_words // 50))
        else:
            target_words = int(target_words * 1.3)
            num_paragraphs = max(4, min(6, target_words // 45))
        
        selected = random.sample(paragraphs, min(num_paragraphs, len(paragraphs)))
        text = ' '.join(selected)
        
        words = text.split()
        if len(words) > target_words:
            words = words[:target_words]
        text = ' '.join(words)
        
        if self.difficulty == "hard":
            words = text.split()
            for i in range(len(words)):
                if random.random() < 0.15:
                    words[i] += random.choice(self.hard_symbols)
            text = ' '.join(words)
        elif self.difficulty == "easy":
            text = text.lower()
        
        self.target_text = text
        
    def start_test(self):
        """Start the typing test"""
        self.is_running = True
        self.start_time = time.time()
        self.remaining_time = self.duration
        self.keystroke_count = 0
        
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete(1.0, tk.END)
        self.input_text.focus()
        
        self.mode1_btn.config(state=tk.DISABLED)
        self.mode2_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        
        self.log_message("Test started!")
        self.log_message("=" * 40)
        self.update_timer()
        
    def update_timer(self):
        """Update countdown timer"""
        if self.is_running and self.remaining_time > 0 and self.start_time is not None:
            elapsed = time.time() - self.start_time
            self.remaining_time = max(0, self.duration - elapsed)
            
            mins = int(self.remaining_time // 60)
            secs = int(self.remaining_time % 60)
            self.timer_label.config(text=f"{mins}:{secs:02d}")
            
            self.update_live_stats()
            
            self.timer_id = self.root.after(100, self.update_timer)
        elif self.is_running:
            self.finish_test()
            
    def update_live_stats(self):
        """Update WPM and accuracy in real-time"""
        typed_text = self.input_text.get(1.0, tk.END).strip()
        
        if typed_text and self.start_time is not None:
            elapsed = time.time() - self.start_time
            minutes = elapsed / 60
            
            # Standard WPM calculation: (characters typed / 5) / minutes
            chars_typed = len(typed_text)
            words_typed = chars_typed / 5.0
            wpm = int(words_typed / minutes) if minutes > 0 else 0
            
            accuracy = self.calculate_accuracy(self.target_text, typed_text)
            
            self.wpm_label.config(text=f"{wpm} WPM")
            self.accuracy_label.config(text=f"{accuracy:.0f}%")
            
            # Update highlighting in real-time
            self.update_text_highlighting(typed_text)
            
            if wpm != self.last_wpm and wpm % 10 == 0:
                self.log_message(f"WPM: {wpm} | Accuracy: {accuracy:.1f}%")
                self.last_wpm = wpm
            
    def update_text_highlighting(self, typed_text):
        """Update highlighting in the text display based on typed text"""
        self.text_display.config(state=tk.NORMAL)
        
        # Remove all existing tags
        self.text_display.tag_remove('correct', '1.0', tk.END)
        self.text_display.tag_remove('incorrect', '1.0', tk.END)
        self.text_display.tag_remove('untyped', '1.0', tk.END)
        
        target = self.target_text
        typed_len = len(typed_text)
        
        # Highlight character by character
        for i in range(len(target)):
            start_idx = f"1.0 + {i} chars"
            end_idx = f"1.0 + {i + 1} chars"
            
            if i < typed_len:
                # Compare character at this exact position
                if i < len(typed_text) and typed_text[i] == target[i]:
                    # Character matches - show as correct (faint cyan)
                    self.text_display.tag_add('correct', start_idx, end_idx)
                else:
                    # Character doesn't match - show as incorrect (faint red)
                    self.text_display.tag_add('incorrect', start_idx, end_idx)
            else:
                # Not yet typed - normal white text
                self.text_display.tag_add('untyped', start_idx, end_idx)
        
        self.text_display.config(state=tk.DISABLED)
            
    def on_key_press(self, event):
        """Handle key press events"""
        if not self.is_running:
            return
        
        self.keystroke_count += 1
        
        if self.keystroke_count % 50 == 0:
            self.log_message(f"Keystrokes: {self.keystroke_count}")
            
    def finish_test(self):
        """Finish test and show results"""
        self.is_running = False
        self.end_time = time.time()
        
        self.input_text.config(state=tk.DISABLED)
        
        typed_text = self.input_text.get(1.0, tk.END).strip()
        self.calculate_results(typed_text)
        
        self.mode1_btn.config(state=tk.NORMAL)
        self.mode2_btn.config(state=tk.NORMAL)
        
        self.log_message("=" * 40)
        self.log_message("Test completed!")
        
    def calculate_results(self, typed_text):
        """Calculate WPM and accuracy"""
        if self.end_time is None or self.start_time is None:
            return
        
        time_taken = self.end_time - self.start_time
        minutes = time_taken / 60
        
        # Standard WPM: (total characters typed / 5) / minutes
        chars_typed = len(typed_text)
        words_typed = chars_typed / 5.0
        
        wpm = int(words_typed / minutes) if minutes > 0 else 0
        accuracy = self.calculate_accuracy(self.target_text, typed_text)
        
        # Calculate incorrect characters/words
        incorrect_chars = self.count_incorrect_chars(self.target_text, typed_text)
        
        result_text = f"🎯 {wpm} WPM  •  {accuracy:.1f}% Accuracy  •  {incorrect_chars} Errors"
        self.result_label.config(text=result_text)
        
        self.log_message(f"Final WPM: {wpm}")
        self.log_message(f"Final Accuracy: {accuracy:.1f}%")
        self.log_message(f"Incorrect Characters: {incorrect_chars}")
        self.log_message(f"Total Keystrokes: {self.keystroke_count}")
        self.log_message(f"Time: {time_taken:.1f} seconds ({minutes:.2f} minutes)")
        
        self.show_results_popup(wpm, accuracy, time_taken, chars_typed, incorrect_chars)
    
    def count_incorrect_chars(self, target, typed):
        """Count number of incorrect characters"""
        if not typed:
            return 0
        
        incorrect = 0
        min_len = min(len(target), len(typed))
        
        for i in range(min_len):
            if typed[i] != target[i]:
                incorrect += 1
        
        # Count missing or extra characters
        if len(typed) < len(target):
            incorrect += len(target) - len(typed)
        elif len(typed) > len(target):
            incorrect += len(typed) - len(target)
        
        return incorrect
        
    def calculate_accuracy(self, target, typed):
        """Calculate typing accuracy"""
        if not typed:
            return 0.0
        
        matcher = SequenceMatcher(None, target[:len(typed)], typed)
        accuracy = matcher.ratio() * 100
        
        return accuracy
        
    def show_results_popup(self, wpm, accuracy, time_taken, chars_typed, incorrect_chars):
        """Show detailed results popup"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Test Results")
        result_window.geometry("500x450")
        result_window.configure(bg=self.bg_primary)
        result_window.overrideredirect(True)
        result_window.attributes('-alpha', 0.97)
        
        result_window.update_idletasks()
        x = (result_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (result_window.winfo_screenheight() // 2) - (450 // 2)
        result_window.geometry(f"500x450+{x}+{y}")
        
        # Title bar with close button
        titlebar = tk.Frame(result_window, bg=self.bg_secondary, height=40)
        titlebar.pack(fill=tk.X)
        titlebar.pack_propagate(False)
        
        title = tk.Label(titlebar, text="📊 TEST RESULTS",
                        font=('Segoe UI', 11, 'bold'),
                        bg=self.bg_secondary, fg=self.cyan)
        title.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Close button (X)
        close_x_btn = tk.Label(titlebar, text="✕", 
                              font=('Segoe UI', 14, 'bold'),
                              bg=self.bg_secondary, fg=self.white,
                              cursor='hand2', padx=10)
        close_x_btn.pack(side=tk.RIGHT, padx=10)
        close_x_btn.bind('<Button-1>', lambda e: result_window.destroy())
        close_x_btn.bind('<Enter>', lambda e: close_x_btn.config(fg=self.cyan))
        close_x_btn.bind('<Leave>', lambda e: close_x_btn.config(fg=self.white))
        
        # Content
        content = tk.Frame(result_window, bg=self.bg_primary)
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Success icon
        tk.Label(content, text="✓",
                font=('Segoe UI', 60, 'bold'),
                bg=self.bg_primary, fg=self.cyan).pack(pady=10)
        
        tk.Label(content, text="TEST COMPLETE",
                font=('Segoe UI', 20, 'bold'),
                bg=self.bg_primary, fg=self.white).pack(pady=5)
        
        # Results frame
        results_frame = tk.Frame(content, bg=self.bg_secondary,
                                highlightbackground=self.cyan,
                                highlightthickness=1)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # WPM (main stat)
        stat_row1 = tk.Frame(results_frame, bg=self.bg_secondary)
        stat_row1.pack(pady=15)
        
        tk.Label(stat_row1, text=f"{wpm}",
                font=('Segoe UI', 40, 'bold'),
                bg=self.bg_secondary, fg=self.cyan).pack()
        tk.Label(stat_row1, text="Words Per Minute",
                font=('Segoe UI', 11),
                bg=self.bg_secondary, fg=self.white).pack()
        
        # Separator
        tk.Frame(results_frame, bg=self.cyan, height=1).pack(fill=tk.X, padx=40, pady=10)
        
        # Other stats grid
        stats_grid = tk.Frame(results_frame, bg=self.bg_secondary)
        stats_grid.pack(pady=10)
        
        # Accuracy
        acc_frame = tk.Frame(stats_grid, bg=self.bg_secondary)
        acc_frame.grid(row=0, column=0, padx=30, pady=10)
        tk.Label(acc_frame, text=f"{accuracy:.1f}%",
                font=('Segoe UI', 18, 'bold'),
                bg=self.bg_secondary, fg=self.white).pack()
        tk.Label(acc_frame, text="Accuracy",
                font=('Segoe UI', 9),
                bg=self.bg_secondary, fg=self.gray).pack()
        
        # Errors
        error_frame = tk.Frame(stats_grid, bg=self.bg_secondary)
        error_frame.grid(row=0, column=1, padx=30, pady=10)
        tk.Label(error_frame, text=f"{incorrect_chars}",
                font=('Segoe UI', 18, 'bold'),
                bg=self.bg_secondary, fg=self.white).pack()
        tk.Label(error_frame, text="Errors",
                font=('Segoe UI', 9),
                bg=self.bg_secondary, fg=self.gray).pack()
        
        # Time
        time_frame = tk.Frame(stats_grid, bg=self.bg_secondary)
        time_frame.grid(row=1, column=0, padx=30, pady=10)
        tk.Label(time_frame, text=f"{int(time_taken//60)}:{int(time_taken%60):02d}",
                font=('Segoe UI', 18, 'bold'),
                bg=self.bg_secondary, fg=self.white).pack()
        tk.Label(time_frame, text="Time Taken",
                font=('Segoe UI', 9),
                bg=self.bg_secondary, fg=self.gray).pack()
        
        # Characters
        char_frame = tk.Frame(stats_grid, bg=self.bg_secondary)
        char_frame.grid(row=1, column=1, padx=30, pady=10)
        tk.Label(char_frame, text=f"{chars_typed}",
                font=('Segoe UI', 18, 'bold'),
                bg=self.bg_secondary, fg=self.white).pack()
        tk.Label(char_frame, text="Characters",
                font=('Segoe UI', 9),
                bg=self.bg_secondary, fg=self.gray).pack()
        
        # Rating
        if wpm >= 70 and accuracy >= 95:
            rating = "🏆 EXCELLENT!"
            rating_color = self.cyan
        elif wpm >= 50 and accuracy >= 90:
            rating = "⭐ GREAT!"
            rating_color = self.cyan
        elif wpm >= 30 and accuracy >= 80:
            rating = "👍 GOOD!"
            rating_color = self.white
        else:
            rating = "💪 KEEP PRACTICING!"
            rating_color = self.white
        
        tk.Label(content, text=rating,
                font=('Segoe UI', 14, 'bold'),
                bg=self.bg_primary, fg=rating_color).pack(pady=10)
        
        # Close button
        close_btn = tk.Button(content, text="CLOSE",
                             command=result_window.destroy,
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.cyan, fg=self.bg_primary,
                             activebackground=self.white,
                             activeforeground=self.bg_primary,
                             relief=tk.FLAT, bd=0,
                             width=20, height=2,
                             cursor='hand2')
        close_btn.pack(pady=10)
        
    def reset_test(self):
        """Reset the test"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        self.is_running = False
        self.start_time = None
        self.end_time = None
        self.keystroke_count = 0
        
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete(1.0, tk.END)
        self.input_text.config(state=tk.DISABLED)
        
        self.timer_label.config(text="0:00")
        self.wpm_label.config(text="0 WPM")
        self.accuracy_label.config(text="0%")
        self.result_label.config(text="")
        
        self.mode1_btn.config(state=tk.NORMAL)
        self.mode2_btn.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.NORMAL)
        
        if self.mode:
            self.generate_text()
        
        self.log_message("Test reset - Ready for new attempt")

def main():
    root = tk.Tk()
    app = TypingTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()