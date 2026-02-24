"""
TEST ARENA - Quiz Application
Main Application File
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import Database
import collections
import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class QuizApp:
    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("TEST ARENA")
        # Start maximized in Windows
        self.root.state('zoomed')
        

        # Modern Color Palette
        self.bg_color = "#f4f6f9"      
        self.card_color = "#ffffff"    
        self.primary_color = "#2563eb" # Royal Blue
        self.primary_dark = "#1d4ed8"  # Darker Royal Blue
        self.secondary_color = "#1e293b" # Slate 800
        self.accent_color = "#ef4444"  # Red 500
        self.text_color = "#334155"    # Slate 700
        self.text_light = "#64748b"    # Slate 500
        
        self.root.configure(bg=self.bg_color)
        
        self.current_user = None
        self.current_exam = None
        self.questions = []
        self.user_answers = {}
        self.start_time = None
        self.current_question_index = 0
        self.start_time = None
        self.current_question_index = 0
        self.quiz_mode = None
        self.timer_id = None
        
        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Load Logo
        self.logo_image = None
        self.logo_small = None
        try:
            # Try to load logo (assuming it's a PNG)
            # Use a raw string for path or just filename if in same dir
            self.logo_image = tk.PhotoImage(file="log.png")
            # Create a smaller version for the dashboard header
            # Note: subsample(x, y) reduces size by keeping every x-th pixel
            # We'll assume the logo is around 400-500px and we want it smaller
            self.logo_small = self.logo_image.subsample(8, 8)  # For header (approx 50-60px)
            self.logo_medium = self.logo_image.subsample(3, 3) # For login/signup (approx 150px)
            
            # Set Window Icon
            self.root.iconphoto(False, self.logo_image)
        except Exception as e:
            print(f"Logo not found or invalid: {e}")
            self.logo_image = None
        
        # Configure Frame Styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_color, relief="groove", borderwidth=1)
        
        # Configure Label Styles
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=('Segoe UI', 10))
        self.style.configure("Card.TLabel", background=self.card_color, foreground=self.text_color, font=('Segoe UI', 10))
        self.style.configure("Title.TLabel", background=self.bg_color, foreground=self.secondary_color, font=('Segoe UI', 28, 'bold'))
        self.style.configure("PageTitle.TLabel", background=self.bg_color, foreground=self.primary_color, font=('Segoe UI', 20, 'bold'))
        self.style.configure("Header.TLabel", background=self.card_color, foreground=self.secondary_color, font=('Segoe UI', 22, 'bold'))
        self.style.configure("SubHeader.TLabel", background=self.card_color, foreground=self.text_light, font=('Segoe UI', 10))
        self.style.configure("Error.TLabel", background=self.card_color, foreground=self.accent_color, font=('Segoe UI', 10))
        
        # Configure Button Styles
        self.style.configure("TButton", font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=12)
        self.style.map("TButton",
            foreground=[('pressed', 'white'), ('active', 'white')],
            background=[('pressed', '!disabled', self.secondary_color), ('active', self.primary_color)]
        )
        self.style.configure("Primary.TButton", background=self.primary_color, foreground="white")
        self.style.map("Primary.TButton", background=[('active', self.primary_dark)])
        
        self.style.configure("Secondary.TButton", background=self.secondary_color, foreground="white")
        
        # Entry Style
        self.style.configure("TEntry", fieldbackground="white", borderwidth=0)
        
        # Notebook Tab Style
        self.style.configure("TNotebook", background="white")
        self.style.configure("TNotebook.Tab", background="#f8fafc", foreground=self.secondary_color, font=('Segoe UI', 11, 'bold'), padding=[20, 10])
        self.style.map("TNotebook.Tab", 
            background=[('selected', self.primary_color)], 
            foreground=[('selected', 'white')]
        )


    def clear_window(self):
        """Clear all widgets from the window"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.root.unbind("<Return>")
            
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_modern_entry(self, parent, label_text, show_char=None):
        """Create a Material Design style entry (bottom border only)"""
        container = tk.Frame(parent, bg="white")
        container.pack(fill=tk.X, pady=(0, 20))
        
        # Label
        tk.Label(container, text=label_text, bg="white", fg=self.text_light, font=('Segoe UI', 9, 'bold')).pack(anchor="w", pady=(0, 2))
        
        # Entry Frame (for border)
        border_frame = tk.Frame(container, bg="#e2e8f0", height=2) # Default border color
        border_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Entry Widget
        entry = tk.Entry(container, font=('Segoe UI', 11), bd=0, bg="white", highlightthickness=0)
        entry.pack(fill=tk.X, pady=(0, 2)) # Spacing above line
        
        if show_char:
            entry.configure(show=show_char)
            
        def on_focus(e):
            border_frame.configure(bg=self.primary_color, height=2)
            
        def on_leave(e):
            border_frame.configure(bg="#e2e8f0", height=2)
            
        entry.bind("<FocusIn>", on_focus, add='+')
        entry.bind("<FocusOut>", on_leave, add='+')
        
        return entry

    def create_gradient_sidebar(self, parent):
        """Create a stylish sidebar with a gradient feel using canvas"""
        sidebar = tk.Canvas(parent, bg=self.primary_color, highlightthickness=0)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Draw some modern shapes for background interest
        sidebar.create_oval(-50, -50, 300, 300, fill="#3b82f6", outline="") # Lighter blue circle
        sidebar.create_oval(200, 400, 600, 800, fill="#1d4ed8", outline="") # Darker blue circle
        
        # App Branding
        sidebar.create_text(200, 250, text="TEST ARENA", font=('Segoe UI', 32, 'bold'), fill="white")
        sidebar.create_text(200, 300, text="Master Your Competitive Exams", font=('Segoe UI', 12), fill="#bfdbfe")
        
        # Feature List
        features = ["✓ Real Exam Simulation", "✓ Performance Analytics", "✓ Detailed Solutions"]
        y_pos = 400
        for feature in features:
            sidebar.create_text(200, y_pos, text=feature, font=('Segoe UI', 11), fill="white")
            y_pos += 40
            
        return sidebar

    def create_header(self, title):
        """Create a standard header"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, pady=20)
        
        lbl_title = ttk.Label(header_frame, text=title, style="PageTitle.TLabel")
        lbl_title.pack()
        
        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, padx=50, pady=10)

    def start(self):
        """Start the application"""
        if not self.db.connect():
            messagebox.showerror("Database Error", "Failed to connect to database.\nPlease check your configuration.")
            return
        
        self.show_login_menu()
        self.root.mainloop()
        self.db.disconnect()

    def show_login_menu(self):
        self.clear_window()
        
        # Main Container (Centered)
        container = ttk.Frame(self.root)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # App Title
        ttk.Label(container, text="TEST ARENA", style="Title.TLabel").pack(pady=(0, 5))
        ttk.Label(container, text="Master Your Competitive Exams", font=('Segoe UI', 12), foreground="#7f8c8d").pack(pady=(0, 30))
        
        # Login Card
        card = ttk.Frame(container, style="Card.TFrame", padding=40)
        card.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(card, text="Welcome Back", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(card, text="Please login to access your quizzes", style="SubHeader.TLabel").pack(pady=(0, 20))
        
        # Buttons
        ttk.Button(card, text="Login", style="Primary.TButton", command=self.show_login, width=30).pack(pady=10)
        ttk.Button(card, text="Create Account", style="Secondary.TButton", command=self.show_signup, width=30).pack(pady=10)
        
        ttk.Separator(card, orient='horizontal').pack(fill=tk.X, pady=20)
        
        ttk.Button(card, text="Exit Application", command=self.root.quit, width=30).pack(pady=(0, 0))

    def show_login(self):
        self.clear_window()
        
        # Split Layout Container
        main_container = tk.Frame(self.root, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left Sidebar (40%)
        left_frame = tk.Frame(main_container, width=400, bg=self.primary_color)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False) # Force width
        
        self.create_gradient_sidebar(left_frame)
        
        # Right Content (60%)
        right_frame = tk.Frame(main_container, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Login Form Centered in Right Frame
        form_wrapper = tk.Frame(right_frame, bg="white", padx=60)
        form_wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)
        
        # Logo (if available)
        if self.logo_image:
            logo_lbl = tk.Label(form_wrapper, image=self.logo_medium, bg="white")
            logo_lbl.pack(pady=(0, 20))
        
        # Header
        tk.Label(form_wrapper, text="Welcome Back", font=('Segoe UI', 24, 'bold'), bg="white", fg=self.secondary_color).pack(anchor="w", pady=(0, 5))
        tk.Label(form_wrapper, text="Please enter your details to sign in.", font=('Segoe UI', 10), bg="white", fg=self.text_light).pack(anchor="w", pady=(0, 30))
        
        # Inputs
        self.entry_user_login = self.create_modern_entry(form_wrapper, "USERNAME")
        self.entry_pass_login = self.create_modern_entry(form_wrapper, "PASSWORD", show_char="*")
        
        # Forgot Password Link (Visual Only)
        tk.Label(form_wrapper, text="Forgot Password?", font=('Segoe UI', 9), bg="white", fg=self.primary_color, cursor="hand2").pack(anchor="e", pady=(0, 20))

        def attempt_login(event=None):
            username = self.entry_user_login.get().strip()
            password = self.entry_pass_login.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password.")
                return
                
            user = self.db.verify_user(username, password)
            if user:
                self.current_user = user
                # messagebox.showinfo("Success", f"Welcome back, {user['name']}!") # Removed popup for smoother UX
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password!")

        self.root.unbind("<Return>")
        
        def focus_password(event=None):
            self.entry_pass_login.focus_set()
            return "break"
            
        self.entry_user_login.bind("<Return>", focus_password)
        self.entry_pass_login.bind("<Return>", attempt_login)

        # Login Button
        login_btn = tk.Button(form_wrapper, text="Sign In", 
                             font=('Segoe UI', 11, 'bold'), 
                             bg=self.primary_color, fg="white", 
                             activebackground=self.primary_dark, activeforeground="white",
                             bd=0, pady=12, cursor="hand2",
                             command=attempt_login)
        login_btn.pack(fill=tk.X, pady=(10, 20))
        
        # Footer
        footer_frame = tk.Frame(form_wrapper, bg="white")
        footer_frame.pack()
        tk.Label(footer_frame, text="Don't have an account?", font=('Segoe UI', 10), bg="white", fg=self.text_light).pack(side=tk.LEFT)
        
        signup_link = tk.Label(footer_frame, text="Sign up for free", font=('Segoe UI', 10, 'bold'), bg="white", fg=self.primary_color, cursor="hand2")
        signup_link.pack(side=tk.LEFT, padx=5)
        signup_link.bind("<Button-1>", lambda e: self.show_signup())
        
        # Back to Home
        back_link = tk.Label(form_wrapper, text="← Back to Home", font=('Segoe UI', 9), bg="white", fg=self.text_light, cursor="hand2")
        back_link.pack(pady=30)
        back_link.bind("<Button-1>", lambda e: self.show_login_menu())

        self.entry_user_login.focus_set()


    def create_form_row(self, parent):
        """Create a row container for 2-column form layout"""
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=(0, 10))
        return row

    def create_form_col(self, parent):
        """Create a column container for form inputs"""
        col = tk.Frame(parent, bg="white")
        col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        return col

    def show_signup(self):
        self.clear_window()
        
        # Split Layout Container
        main_container = tk.Frame(self.root, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left Sidebar (40%)
        left_frame = tk.Frame(main_container, width=400, bg=self.primary_color)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False) # Force width
        
        self.create_gradient_sidebar(left_frame)
        
        # Right Content (60%)
        right_frame = tk.Frame(main_container, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Signup Form Centered
        form_wrapper = tk.Frame(right_frame, bg="white", padx=50)
        form_wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)
        
        # Logo (if available)
        if self.logo_image:
            logo_lbl = tk.Label(form_wrapper, image=self.logo_medium, bg="white")
            logo_lbl.pack(pady=(0, 20))
        
        # Header
        tk.Label(form_wrapper, text="Create Account", font=('Segoe UI', 22, 'bold'), bg="white", fg=self.secondary_color).pack(anchor="w", pady=(0, 5))
        tk.Label(form_wrapper, text="Join us to start your preparation journey.", font=('Segoe UI', 10), bg="white", fg=self.text_light).pack(anchor="w", pady=(0, 25))
        
        self.entries = {}
        
        # Row 1: Name & Username
        row1 = self.create_form_row(form_wrapper)
        col1 = self.create_form_col(row1)
        col2 = self.create_form_col(row1)
        self.entries["Full Name"] = self.create_modern_entry(col1, "FULL NAME")
        self.entries["Username"] = self.create_modern_entry(col2, "USERNAME")
        
        # Row 2: Email & Phone
        row2 = self.create_form_row(form_wrapper)
        col3 = self.create_form_col(row2)
        col4 = self.create_form_col(row2)
        self.entries["Email"] = self.create_modern_entry(col3, "EMAIL")
        self.entries["Phone"] = self.create_modern_entry(col4, "PHONE")
        
        # Row 3: Password & Confirm
        row3 = self.create_form_row(form_wrapper)
        col5 = self.create_form_col(row3)
        col6 = self.create_form_col(row3)
        self.entries["Password"] = self.create_modern_entry(col5, "PASSWORD", show_char="*")
        self.entries["Confirm Password"] = self.create_modern_entry(col6, "CONFIRM PASSWORD", show_char="*")
            
        def attempt_signup():
            name = self.entries["Full Name"].get().strip()
            username = self.entries["Username"].get().strip()
            password = self.entries["Password"].get().strip()
            confirm = self.entries["Confirm Password"].get().strip()
            email = self.entries["Email"].get().strip()
            phone = self.entries["Phone"].get().strip()
            
            if not name or not username or not password or not email or not phone:
                messagebox.showerror("Error", "Please fill in all required fields.")
                return
                
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Error", "Please enter a valid email address.")
                return
                
            if not phone.isdigit() or len(phone) < 10 or len(phone) > 15:
                messagebox.showerror("Error", "Please enter a valid phone number (10-15 digits).")
                return
                
            if self.db.check_username_exists(username):
                messagebox.showerror("Error", "Username already exists!")
                return
                
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match!")
                return
                
            # --- START OTP VERIFICATION ---
            generated_otp = str(random.randint(100000, 999999))
            
            def send_otp():
                sender_email = "your_email@gmail.com"
                sender_password = "your_app_password" # Use an App Password if using Gmail
                
                try:
                    if sender_password == "your_app_password":
                        # If credentials are not configured, simulate it so the app still works!
                        print(f"DEBUG: Simulated OTP is {generated_otp}")
                        messagebox.showinfo("OTP Simulation", f"Email credentials not set in main.py.\n\nSimulated Email to {email}:\nYour OTP is: {generated_otp}")
                        return True
                        
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = email
                    msg['Subject'] = "Test Arena - Verification OTP"
                    
                    body = f"Hello {name},\n\nYour Verification OTP for Test Arena is: {generated_otp}\n\nPlease do not share this code with anyone.\n\nBest,\nTest Arena Team"
                    msg.attach(MIMEText(body, 'plain'))
                    
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()
                    return True
                except Exception as e:
                    messagebox.showerror("Email Error", f"Failed to send OTP email: {e}")
                    return False

            if not send_otp():
                return
                
            self.show_otp_verification(name, username, password, email, phone, generated_otp)
            # --- END OTP GENERATION ---

        # Create Account Button
        signup_btn = tk.Button(form_wrapper, text="Create Account", 
                             font=('Segoe UI', 11, 'bold'), 
                             bg=self.primary_color, fg="white", 
                             activebackground=self.primary_dark, activeforeground="white",
                             bd=0, pady=12, cursor="hand2",
                             command=attempt_signup)
        signup_btn.pack(fill=tk.X, pady=(20, 20))
        
        # Footer
        footer_frame = tk.Frame(form_wrapper, bg="white")
        footer_frame.pack()
        tk.Label(footer_frame, text="Already have an account?", font=('Segoe UI', 10), bg="white", fg=self.text_light).pack(side=tk.LEFT)
        
        login_link = tk.Label(footer_frame, text="Sign In", font=('Segoe UI', 10, 'bold'), bg="white", fg=self.primary_color, cursor="hand2")
        login_link.pack(side=tk.LEFT, padx=5)
        login_link.bind("<Button-1>", lambda e: self.show_login())

    def show_otp_verification(self, name, username, password, email, phone, generated_otp):
        self.clear_window()
        
        # Split Layout Container
        main_container = tk.Frame(self.root, bg="white")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left Sidebar (40%)
        left_frame = tk.Frame(main_container, width=400, bg=self.primary_color)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False) # Force width
        
        self.create_gradient_sidebar(left_frame)
        
        # Right Content (60%)
        right_frame = tk.Frame(main_container, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # OTP Form Centered
        form_wrapper = tk.Frame(right_frame, bg="white", padx=50)
        form_wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)
        
        if self.logo_image:
            logo_lbl = tk.Label(form_wrapper, image=self.logo_medium, bg="white")
            logo_lbl.pack(pady=(0, 20))
            
        tk.Label(form_wrapper, text="Verify Your Email", font=('Segoe UI', 24, 'bold'), bg="white", fg=self.secondary_color).pack(anchor="w", pady=(0, 5))
        tk.Label(form_wrapper, text=f"We've sent a 6-digit code to {email}\nPlease enter it below to verify your account.", font=('Segoe UI', 10), bg="white", fg=self.text_light).pack(anchor="w", pady=(0, 30))
        
        otp_entry = self.create_modern_entry(form_wrapper, "ENTER OTP")
        
        def attempt_verify(event=None):
            entered_otp = otp_entry.get().strip()
            if entered_otp == generated_otp:
                if self.db.create_user(name, username, password, email, phone):
                    messagebox.showinfo("Success", "Account verified and created! Please sign in.")
                    self.show_login()
                else:
                    messagebox.showerror("Error", "Failed to create account.")
            else:
                messagebox.showerror("Error", "Invalid OTP. Please try again.")

        otp_entry.bind("<Return>", attempt_verify)
        
        verify_btn = tk.Button(form_wrapper, text="Verify & Create Account", 
                             font=('Segoe UI', 11, 'bold'), 
                             bg=self.primary_color, fg="white", 
                             activebackground=self.primary_dark, activeforeground="white",
                             bd=0, pady=12, cursor="hand2",
                             command=attempt_verify)
        verify_btn.pack(fill=tk.X, pady=(20, 20))
        
        # Back Link
        back_link = tk.Label(form_wrapper, text="← Go back to Sign Up", font=('Segoe UI', 9), bg="white", fg=self.text_light, cursor="hand2")
        back_link.pack()
        back_link.bind("<Button-1>", lambda e: self.show_signup())

    def create_dashboard_card(self, parent, title, subtitle, command, color, icon_text):
        """Create a clickable card for the dashboard"""
        card = tk.Frame(parent, bg="white", cursor="hand2")
        # card.pack_propagate(False) # Let it expand naturally
        
        # Inner padding frame
        inner = tk.Frame(card, bg="white", padx=20, pady=20)
        inner.pack(fill=tk.BOTH, expand=True)

        # Icon/Color Strip (Top Border)
        strip = tk.Frame(card, bg=color, height=4)
        strip.pack(side=tk.TOP, fill=tk.X)
        
        # Content
        # Icon
        icon_lbl = tk.Label(inner, text=icon_text, font=('Segoe UI Symbol', 28), bg="white", fg=color)
        icon_lbl.pack(anchor="w", pady=(0, 10))
        
        # Title
        title_lbl = tk.Label(inner, text=title, font=('Segoe UI', 14, 'bold'), bg="white", fg=self.text_color)
        title_lbl.pack(anchor="w", pady=(0, 5))
        
        # Subtitle
        sub_lbl = tk.Label(inner, text=subtitle, font=('Segoe UI', 10), bg="white", fg=self.text_light, wraplength=200, justify="left")
        sub_lbl.pack(anchor="w")
        
        # Hover Effect
        def on_enter(e):
            card.configure(bg="#f1f5f9") # Light slate background
            inner.configure(bg="#f1f5f9")
            icon_lbl.configure(bg="#f1f5f9")
            title_lbl.configure(bg="#f1f5f9")
            sub_lbl.configure(bg="#f1f5f9")
            
        def on_leave(e):
            card.configure(bg="white")
            inner.configure(bg="white")
            icon_lbl.configure(bg="white")
            title_lbl.configure(bg="white")
            sub_lbl.configure(bg="white")
            
        def on_click(e):
            command()
            
        # Bind events to all widgets in the card
        for widget in [card, inner, icon_lbl, title_lbl, sub_lbl]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
            
        return card

    def show_main_menu(self):
        self.clear_window()
        
        # Top Navigation Bar
        nav_bar = tk.Frame(self.root, bg="white", height=70) # Increased height
        nav_bar.pack(fill=tk.X, side=tk.TOP)
        nav_bar.pack_propagate(False)
        
        # Shadow Line
        tk.Frame(self.root, bg="#e2e8f0", height=1).pack(fill=tk.X, side=tk.TOP)
        
        # Logo Area (Left)
        logo_frame = tk.Frame(nav_bar, bg="white")
        logo_frame.pack(side=tk.LEFT, padx=30, pady=15)
        
        if self.logo_small:
            tk.Label(logo_frame, image=self.logo_small, bg="white").pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(logo_frame, text="TEST", font=('Segoe UI', 16, 'bold'), bg="white", fg=self.secondary_color).pack(side=tk.LEFT)
        tk.Label(logo_frame, text="ARENA", font=('Segoe UI', 16, 'bold'), bg="white", fg=self.primary_color).pack(side=tk.LEFT, padx=(2, 0))
        
        # User Profile Area (Right)
        if self.current_user: # Safety check
            user_frame = tk.Frame(nav_bar, bg="white")
            user_frame.pack(side=tk.RIGHT, padx=30)
            
            # Avatar Circle (Simulated)
            avatar = tk.Label(user_frame, text=self.current_user['name'][0].upper(), 
                            font=('Segoe UI', 12, 'bold'), bg=self.primary_color, fg="white", 
                            width=3, pady=5)
            # avatar.pack(side=tk.LEFT, padx=(0, 10)) # Simple circle simulation
            
            tk.Label(user_frame, text=f"Hello, {self.current_user['name'].split()[0]}", font=('Segoe UI', 11, 'bold'), bg="white", fg=self.text_color).pack(side=tk.LEFT, padx=15)
            
            # Modern Logout Button
            logout_btn = tk.Button(user_frame, text="Logout", font=('Segoe UI', 9, 'bold'), 
                                 bg="white", fg=self.accent_color, bd=1, relief="solid", 
                                 padx=15, pady=5, cursor="hand2",
                                 command=self.logout)
            logout_btn.configure(activebackground="#fee2e2", activeforeground=self.accent_color)
            logout_btn.pack(side=tk.LEFT)
        
        # Main Dashboard Content
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Welcome Section
        tk.Label(content, text="Dashboard", font=('Segoe UI', 26, 'bold'), bg=self.bg_color, fg=self.secondary_color).pack(anchor="w", pady=(0, 5))
        tk.Label(content, text="Select an option below to get started.", font=('Segoe UI', 11), bg=self.bg_color, fg=self.text_light).pack(anchor="w", pady=(0, 30))
        
        # Cards Grid
        grid_frame = tk.Frame(content, bg=self.bg_color) # Transparent background
        grid_frame.pack(fill=tk.X)
        
        # Define Cards
        # Card 1: Start Quiz (Blue)
        c1 = self.create_dashboard_card(grid_frame, 
                                      "Start New Quiz", 
                                      "Choose a subject and challenge yourself with timed exams.", 
                                      self.show_exam_selection,
                                      self.primary_color, "📝")
        c1.grid(row=0, column=0, padx=(0, 20), sticky="nsew")
        
        # Card 2: View Scores (Green)
        c2 = self.create_dashboard_card(grid_frame, 
                                      "Performance Stats", 
                                      "Track your progress and review detailed analytics.", 
                                      self.show_scores,
                                      "#10b981", "📊") # Emerald Green
        c2.grid(row=0, column=1, padx=(0, 20), sticky="nsew")
        
        # Card 3: About (Purple)
        c3 = self.create_dashboard_card(grid_frame, 
                                      "About Platform", 
                                      "Learn more about Test Arena features and updates.", 
                                      self.show_about,
                                      "#8b5cf6", "ℹ️") # Violet
        c3.grid(row=0, column=2, padx=0, sticky="nsew")
        
        # Configure Grid Weights so cards expand equally
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(2, weight=1)

    def logout(self):
        self.current_user = None
        self.show_login_menu()

    def create_exam_card(self, parent, exam, command):
        """Create a stylized card for an exam"""
        colors = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ef4444", "#ec4899"]
        # Use exam name hash to pick a consistent color
        color = colors[hash(exam['exam_name']) % len(colors)]
        
        card = tk.Frame(parent, bg="white", cursor="hand2", highlightbackground="#e2e8f0", highlightthickness=1)
        
        # Color Strip
        tk.Frame(card, bg=color, height=6).pack(fill=tk.X)
        
        content = tk.Frame(card, bg="white", padx=20, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Exam Name (Large)
        tk.Label(content, text=exam['exam_name'], font=('Segoe UI', 18, 'bold'), bg="white", fg=self.secondary_color).pack(anchor="w", pady=(0, 5))
        
        # Description (truncated if needed)
        desc = exam.get('description', 'No description available')
        tk.Label(content, text=desc, font=('Segoe UI', 10), bg="white", fg=self.text_light, wraplength=220, justify="left").pack(anchor="w", pady=(0, 15))
        
        # Stats Row
        stats = tk.Frame(content, bg="white")
        stats.pack(fill=tk.X, pady=(0, 15))
        
        # Duration
        tk.Label(stats, text="⏱️", font=('Segoe UI', 10), bg="white").pack(side=tk.LEFT)
        tk.Label(stats, text=f"{exam['duration_minutes']} min", font=('Segoe UI', 10, 'bold'), bg="white", fg=self.text_color).pack(side=tk.LEFT, padx=(5, 15))
        
        # Questions
        tk.Label(stats, text="❓", font=('Segoe UI', 10), bg="white").pack(side=tk.LEFT)
        tk.Label(stats, text=f"{exam['total_questions']} Qs", font=('Segoe UI', 10, 'bold'), bg="white", fg=self.text_color).pack(side=tk.LEFT, padx=(5, 0))
        
        # Action Button (Fake, for visual)
        btn = tk.Label(content, text="Start Exam →", font=('Segoe UI', 10, 'bold'), bg="#f1f5f9", fg=self.primary_color, padx=15, pady=8)
        btn.pack(fill=tk.X)
        
        # Hover & Click Logic
        def on_enter(e):
            card.configure(highlightbackground=color, highlightthickness=2)
            btn.configure(bg=color, fg="white")
            
        def on_leave(e):
            card.configure(highlightbackground="#e2e8f0", highlightthickness=1)
            btn.configure(bg="#f1f5f9", fg=self.primary_color)
            
        def on_click(e):
            command(exam)
            
        for widget in [card, content, btn] + list(content.winfo_children()) + list(stats.winfo_children()):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
            
        return card

    def show_exam_selection(self):
        self.clear_window()
        
        # Simple Top Bar
        top_bar = tk.Frame(self.root, bg="white", height=60, pady=10, padx=30)
        top_bar.pack(fill=tk.X)
        
        tk.Button(top_bar, text="← Back", font=('Segoe UI', 10), bg="white", fg=self.text_light, bd=0, cursor="hand2", 
                 command=self.show_main_menu).pack(side=tk.LEFT)
        
        tk.Label(top_bar, text="Select Exam", font=('Segoe UI', 16, 'bold'), bg="white", fg=self.secondary_color).pack(side=tk.LEFT, padx=20)
        
        # Main Content Area
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Scrollable Area
        canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        exams = self.db.get_all_exams()
        
        if not exams:
            tk.Label(scrollable_frame, text="No exams found.", font=('Segoe UI', 14), bg=self.bg_color, fg=self.text_light).pack(pady=50)
            return

        # Grid Layout Logic
        columns = 3
        for i, exam in enumerate(exams):
            row = i // columns
            col = i % columns
            
            card = self.create_exam_card(scrollable_frame, exam, self.show_mode_selection)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
        # Configure columns to expand
        for i in range(columns):
            scrollable_frame.grid_columnconfigure(i, weight=1)

    def create_mode_card(self, parent, title, subtitle, icon, color, command):
        """Create a large clickable card for mode selection"""
        card = tk.Frame(parent, bg="white", cursor="hand2", highlightbackground="#e2e8f0", highlightthickness=1)
        
        # Icon Area (Left)
        left = tk.Frame(card, bg=color, width=100)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)
        
        tk.Label(left, text=icon, font=('Segoe UI Symbol', 32), bg=color, fg="white").place(relx=0.5, rely=0.5, anchor="center")
        
        # Content Area (Right)
        right = tk.Frame(card, bg="white", padx=30, pady=30)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text=title, font=('Segoe UI', 18, 'bold'), bg="white", fg=self.text_color).pack(anchor="w", pady=(0, 5))
        tk.Label(right, text=subtitle, font=('Segoe UI', 11), bg="white", fg=self.text_light, justify="left", wraplength=400).pack(anchor="w", pady=(0, 20))
        
        # Button/Indicator
        btn = tk.Label(right, text="Select Mode →", font=('Segoe UI', 11, 'bold'), bg="#f1f5f9", fg=color, padx=20, pady=10)
        btn.pack(anchor="w")
        
        # Interactions
        def on_enter(e):
            card.configure(highlightbackground=color, highlightthickness=2)
            btn.configure(bg=color, fg="white")
            
        def on_leave(e):
            card.configure(highlightbackground="#e2e8f0", highlightthickness=1)
            btn.configure(bg="#f1f5f9", fg=color)
            
        def on_click(e):
            command()
            
        # Recursive bind
        def bind_all(widget):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
            for child in widget.winfo_children():
                bind_all(child)
        
        bind_all(card)
        return card

    def show_mode_selection(self, exam):
        self.current_exam = exam
        self.clear_window()
        
        # Header
        header = tk.Frame(self.root, bg="white", height=80, padx=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Back Button
        tk.Button(header, text="← Back", font=('Segoe UI', 11), bg="white", fg=self.text_light, bd=0, cursor="hand2", 
                 command=self.show_exam_selection).pack(side=tk.LEFT)
        
        # Title
        tk.Label(header, text=f"{exam['exam_name']} - Select Mode", font=('Segoe UI', 20, 'bold'), bg="white", fg=self.secondary_color).pack(side=tk.LEFT, padx=30)

        # Content Container
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Mode Cards
        # Exam Mode
        card1 = self.create_mode_card(content, 
            "Exam Mode", 
            "Simulate real exam conditions. Strict time limits, no feedback until submission, and detailed scorecard at the end.",
            "⏱️", 
            self.accent_color,
            lambda: self.start_quiz("Exam")
        )
        card1.pack(fill=tk.X, pady=(0, 20))
        
        # Free Trial Mode
        card2 = self.create_mode_card(content, 
            "Practice Mode", 
            "Learn at your own pace. Get immediate feedback on every question, view solutions, and no time pressure.",
            "🎓", 
            "#10b981", # Green
            lambda: self.start_quiz("Free Trial")
        )
        card2.pack(fill=tk.X)

    def start_quiz(self, mode):
        self.quiz_mode = mode
        self.questions = self.db.get_questions_by_exam(self.current_exam['exam_id'])
        
        if not self.questions:
            messagebox.showwarning("Warning", "No questions available for this exam.")
            return
            
        self.questions = self.questions[:self.current_exam['total_questions']]
        self.user_answers = {}
        self.current_question_index = 0
        self.start_time = datetime.now()
        
        self.show_question()

    def create_option_card(self, parent, text, value):
        """Create a clickable option card that mimics a radio button behavior"""
        
        card = tk.Frame(parent, bg="white", cursor="hand2", highlightbackground="#e2e8f0", highlightthickness=1)
        card.pack(fill=tk.X, pady=6)
        
        # Layout: [Radio Circle] [Text]
        inner = tk.Frame(card, bg="white", padx=15, pady=12)
        inner.pack(fill=tk.BOTH, expand=True)
        
        # Fake Radio Circle
        circle = tk.Canvas(inner, width=20, height=20, bg="white", highlightthickness=0)
        circle.pack(side=tk.LEFT)
        circle_id = circle.create_oval(2, 2, 18, 18, outline="#cbd5e1", width=2)
        fill_id = circle.create_oval(5, 5, 15, 15, fill="white", outline="") # Initially hidden/white
        
        # Option Label
        lbl = tk.Label(inner, text=text, font=('Segoe UI', 11), bg="white", fg=self.text_color, justify="left", wraplength=600)
        lbl.pack(side=tk.LEFT, padx=15)
        
        # Check State
        def update_state(*args):
            current = self.var_answer.get()
            if current == value:
                card.configure(highlightbackground=self.primary_color, highlightthickness=2, bg="#eff6ff")
                inner.configure(bg="#eff6ff")
                circle.configure(bg="#eff6ff")
                lbl.configure(bg="#eff6ff", fg=self.primary_color, font=('Segoe UI', 11, 'bold'))
                circle.itemconfig(circle_id, outline=self.primary_color)
                circle.itemconfig(fill_id, fill=self.primary_color)
            else:
                card.configure(highlightbackground="#e2e8f0", highlightthickness=1, bg="white")
                inner.configure(bg="white")
                circle.configure(bg="white")
                lbl.configure(bg="white", fg=self.text_color, font=('Segoe UI', 11))
                circle.itemconfig(circle_id, outline="#cbd5e1")
                circle.itemconfig(fill_id, fill="white") # Or transparent effect
        
        # Initial check
        update_state()
        
        # Listen for changes
        self.var_answer.trace_add("write", update_state)
        
        # Click Handler
        def on_click(e):
            self.var_answer.set(value)
            
        for w in [card, inner, circle, lbl]:
            w.bind("<Button-1>", on_click)
            
        return card

    def show_question(self):
        self.clear_window()
        
        if self.current_question_index >= len(self.questions):
            self.finish_quiz()
            # return # Wait, finish_quiz clears window? Yes.
            return
            
        question = self.questions[self.current_question_index]
        
        # --- Top Bar (Timer & Progress) ---
        top_bar = tk.Frame(self.root, bg="white", height=60, padx=30)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Progress
        tk.Label(top_bar, text=f"Question {self.current_question_index + 1} of {len(self.questions)}", 
                font=('Segoe UI', 14, 'bold'), bg="white", fg=self.text_color).pack(side=tk.LEFT)
                
        # Subject Badge
        tk.Label(top_bar, text=question['subject_name'], font=('Segoe UI', 10, 'bold'), 
                bg="#f1f5f9", fg=self.text_light, padx=10, pady=4).pack(side=tk.LEFT, padx=20)
        
        # Timer (Right)
        self.lbl_timer = tk.Label(top_bar, text="", font=('Segoe UI', 14, 'bold'), bg="white", fg=self.accent_color)
        self.lbl_timer.pack(side=tk.RIGHT)
        
        if self.quiz_mode == "Exam":
            self.update_timer()
        else:
            self.lbl_timer.config(text="Free Practice Mode", fg=self.primary_color)
            
        # --- Main Content ---
        main_content = tk.Frame(self.root, bg=self.bg_color)
        main_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Question Card
        q_card = tk.Frame(main_content, bg="white", padx=30, pady=30, highlightbackground="#e2e8f0", highlightthickness=1)
        q_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(q_card, text=question['question_text'], font=('Segoe UI', 16), bg="white", fg=self.secondary_color, wraplength=800, justify="left").pack(anchor="w")
        
        # Options Container
        self.options_frame = tk.Frame(main_content, bg=self.bg_color)
        self.options_frame.pack(fill=tk.X)
        
        self.var_answer = tk.StringVar(value=self.user_answers.get(question['question_id'], "N"))
        
        for opt, text in [('A', question['option_a']), ('B', question['option_b']), 
                          ('C', question['option_c']), ('D', question['option_d'])]:
            self.create_option_card(self.options_frame, text, opt) # Use option letter as value
            
        # Solution/Feedback Area (Initially hidden/empty)
        self.solution_frame = tk.Frame(main_content, bg=self.bg_color, pady=20)
        self.solution_frame.pack(fill=tk.X)
            
        # --- Bottom Navigation ---
        nav_bar = tk.Frame(self.root, bg="white", height=70, padx=30)
        nav_bar.pack(fill=tk.X, side=tk.BOTTOM)
        nav_bar.pack_propagate(False)
        
        # Exit Quiz Button
        tk.Button(nav_bar, text="Exit Quiz", font=('Segoe UI', 11, 'bold'), 
                  bg="#ef4444", fg="white", bd=0, padx=20, pady=10, 
                  command=self.confirm_exit_quiz, cursor="hand2").pack(side=tk.LEFT)
        
        
        # Next / Finish Button
        btn_text = "Finish Quiz" if self.current_question_index == len(self.questions) - 1 else "Next Question →"
        btn_cmd = self.finish_quiz if self.current_question_index == len(self.questions) - 1 else self.next_question
        
        # If Free Trial, check answer button
        if self.quiz_mode == "Free Trial":
             self.check_btn = tk.Button(nav_bar, text="Check Answer", font=('Segoe UI', 11, 'bold'), 
                      bg=self.primary_color, fg="white", bd=0, padx=20, pady=10, 
                      command=self.check_answer_trial, cursor="hand2")
             self.check_btn.pack(side=tk.RIGHT)
             
             # Also add a Next button if they want to skip
             self.skip_btn = tk.Button(nav_bar, text="Skip", font=('Segoe UI', 11), 
                      bg="white", fg=self.text_color, bd=0, padx=20, 
                      command=self.next_question, cursor="hand2")
             self.skip_btn.pack(side=tk.RIGHT, padx=10)
        else:
            # Exam Mode
            tk.Button(nav_bar, text=btn_text, font=('Segoe UI', 11, 'bold'), 
                     bg=self.secondary_color, fg="white", bd=0, padx=25, pady=10, 
                     command=self.next_question, cursor="hand2").pack(side=tk.RIGHT)

    def update_timer(self):
        if self.quiz_mode != "Exam":
            return
            
        duration = self.current_exam['duration_minutes']
        end_time = self.start_time + timedelta(minutes=duration)
        remaining = end_time - datetime.now()
        
        if remaining.total_seconds() <= 0:
            self.finish_quiz()
            return
            
        minutes = int(remaining.total_seconds() // 60)
        seconds = int(remaining.total_seconds() % 60)
        if hasattr(self, 'lbl_timer') and self.lbl_timer.winfo_exists():
            self.lbl_timer.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")
            self.timer_id = self.root.after(1000, self.update_timer)


    def check_answer_trial(self):
        selected = self.var_answer.get()
        question = self.questions[self.current_question_index]
        
        # Clear previous feedback if any
        for widget in self.solution_frame.winfo_children():
            widget.destroy()
            
        if selected == "N":
            messagebox.showinfo("Skipped", "Please select an answer first.")
            return

        is_correct = (selected == question['correct_option'])
        
        # Determine styles
        bg_color = "#dcfce7" if is_correct else "#fee2e2" # Green-100 vs Red-100
        border_color = "#10b981" if is_correct else "#ef4444" 
        text_color = "#14532d" if is_correct else "#7f1d1d"
        title = "Correct Answer!" if is_correct else "Incorrect Answer"
        icon = "✅" if is_correct else "❌"
        
        # Create Feedback Card
        card = tk.Frame(self.solution_frame, bg=bg_color, highlightbackground=border_color, highlightthickness=1, padx=20, pady=20)
        card.pack(fill=tk.X)
        
        # Header Row
        header = tk.Frame(card, bg=bg_color)
        header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header, text=icon, font=('Segoe UI Symbol', 14), bg=bg_color).pack(side=tk.LEFT)
        tk.Label(header, text=title, font=('Segoe UI', 12, 'bold'), bg=bg_color, fg=text_color).pack(side=tk.LEFT, padx=10)
        
        # Explanation / Solution Text
        sol_text = ""
        if not is_correct:
            sol_text += f"The correct option is {question['correct_option']}.\n\n"
            
        if question['solution']:
            sol_text += f"Explanation: {question['solution']}"
        else:
            sol_text += "No detailed solution available."
            
        tk.Label(card, text=sol_text, font=('Segoe UI', 11), bg=bg_color, fg=text_color, justify="left", wraplength=700).pack(anchor="w")
            
        # Save Answer
        self.user_answers[question['question_id']] = selected
        
        # Change Button to Next
        self.check_btn.configure(text="Next Question →", command=self.next_question, bg=self.secondary_color)
        self.skip_btn.pack_forget() # Hide skip button since we are moving to next anyway

    def next_question(self):
        selected = self.var_answer.get()
        question = self.questions[self.current_question_index]
        self.user_answers[question['question_id']] = selected
        self.current_question_index += 1
        self.show_question()

    def confirm_exit_quiz(self):
        if messagebox.askyesno("Exit Quiz", "Are you sure you want to exit the quiz? Your progress will not be saved."):
            if hasattr(self, 'timer_id'):
                try:
                    self.root.after_cancel(self.timer_id)
                except Exception:
                    pass
            self.show_main_menu()


    def create_stat_card(self, parent, title, value, icon, color):
        """Create a small statistic card for results"""
        card = tk.Frame(parent, bg="white", padx=20, pady=20, highlightbackground="#e2e8f0", highlightthickness=1)
        
        # Icon
        tk.Label(card, text=icon, font=('Segoe UI Symbol', 24), bg="white", fg=color).pack(anchor="w", pady=(0, 5))
        
        # Value
        tk.Label(card, text=value, font=('Segoe UI', 22, 'bold'), bg="white", fg=self.secondary_color).pack(anchor="w")
        
        # Title
        tk.Label(card, text=title, font=('Segoe UI', 10), bg="white", fg=self.text_light).pack(anchor="w")
        
        return card

    def finish_quiz(self):
        self.clear_window()
        
        correct = 0
        wrong = 0
        unanswered = 0
        
        for question in self.questions:
            answer = self.user_answers.get(question['question_id'], 'N')
            if answer == 'N':
                unanswered += 1
            elif answer == question['correct_option']:
                correct += 1
            else:
                wrong += 1
                
        total_questions = len(self.questions)
        total_marks = correct
        time_taken = int((datetime.now() - self.start_time).total_seconds() / 60)
        percentage = int((correct / total_questions) * 100) if total_questions > 0 else 0
        
        # Save Score
        self.db.save_score(
            self.current_user['user_id'],
            self.current_exam['exam_id'],
            self.quiz_mode,
            total_marks,
            correct,
            wrong,
            unanswered,
            time_taken
        )
        
        # --- UI Design ---
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=150)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Quiz Completed!", font=('Segoe UI', 28, 'bold'), bg=self.primary_color, fg="white").pack(pady=(30, 5))
        tk.Label(header, text=f"Great job finishing the {self.current_exam['exam_name']} exam.", font=('Segoe UI', 12), bg=self.primary_color, fg="#bfdbfe").pack()
        
        # Main Content
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40) # Push content up to overlap heade if using place, but pack is easier
        
        # Score Summary Card (Large)
        score_card = tk.Frame(content, bg="white", padx=40, pady=30, highlightbackground="#e2e8f0", highlightthickness=1)
        score_card.pack(fill=tk.X, pady=(0, 30))
        
        # Score Layout: [Circle/Percentage] [Text Details]
        score_left = tk.Frame(score_card, bg="white")
        score_left.pack(side=tk.LEFT)
        
        score_right = tk.Frame(score_card, bg="white", padx=40)
        score_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Big Percentage Display
        color = "#10b981" if percentage >= 70 else "#f59e0b" if percentage >= 40 else "#ef4444"
        tk.Label(score_left, text=f"{percentage}%", font=('Segoe UI', 48, 'bold'), bg="white", fg=color).pack()
        tk.Label(score_left, text="Total Score", font=('Segoe UI', 12), bg="white", fg=self.text_light).pack()
        
        # Details
        tk.Label(score_right, text=f"You answered {correct} out of {total_questions} questions correctly.", 
                font=('Segoe UI', 14), bg="white", fg=self.text_color).pack(anchor="w", pady=(0, 10))
        
        time_str = f"{time_taken} minutes" if time_taken > 0 else "Less than a minute"
        tk.Label(score_right, text=f"Time Taken: {time_str}", font=('Segoe UI', 11), bg="white", fg=self.text_light).pack(anchor="w")
        
        # Grid of Stats
        stats_frame = tk.Frame(content, bg=self.bg_color)
        stats_frame.pack(fill=tk.X)
        
        # Stat Cards
        c1 = self.create_stat_card(stats_frame, "Correct Answers", str(correct), "✅", "#10b981")
        c1.grid(row=0, column=0, padx=(0, 20), sticky="nsew")
        
        c2 = self.create_stat_card(stats_frame, "Wrong Answers", str(wrong), "❌", "#ef4444")
        c2.grid(row=0, column=1, padx=(0, 20), sticky="nsew")
        
        c3 = self.create_stat_card(stats_frame, "Unanswered", str(unanswered), "⭕", "#94a3b8")
        c3.grid(row=0, column=2, padx=0, sticky="nsew")
        
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
        
        # Action Buttons (Fixed Footer)
        footer = tk.Frame(self.root, bg="white", height=80, pady=15, padx=40)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)
        
        tk.Button(footer, text="Return to Dashboard", font=('Segoe UI', 11, 'bold'), 
                 bg=self.primary_color, fg="white", bd=0, padx=30, pady=12, 
                 command=self.show_main_menu, cursor="hand2").pack(side=tk.RIGHT)
                 
        tk.Button(footer, text="Retry Exam", font=('Segoe UI', 11), 
                 bg="white", fg=self.text_color, bd=0, padx=30, pady=12, 
                 command=lambda: self.start_quiz(self.quiz_mode), cursor="hand2").pack(side=tk.RIGHT, padx=20)

    def show_scores(self):
        self.clear_window()
        
        # Header (Consistent Top Bar)
        header = tk.Frame(self.root, bg="white", height=80, padx=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Back Button
        tk.Button(header, text="← Back", font=('Segoe UI', 11), bg="white", fg=self.text_light, bd=0, cursor="hand2", 
                 command=self.show_main_menu).pack(side=tk.LEFT)
        
        # Title
        tk.Label(header, text="Your Performance History", font=('Segoe UI', 20, 'bold'), bg="white", fg=self.secondary_color).pack(side=tk.LEFT, padx=30)
        
        # Main Content Area
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        scores = self.db.get_user_scores(self.current_user['user_id'])
        
        # --- Analytics Summary Frame ---
        summary_frame = tk.Frame(content, bg=self.bg_color)
        summary_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Calculate Stats
        total_quizzes = len(scores)
        best_score = max([int(s['total_marks']) for s in scores]) if scores else 0
        avg_score = int(sum([int(s['total_marks']) for s in scores]) / total_quizzes) if total_quizzes > 0 else 0
        
        # Reuse create_stat_card logic but customize slightly for here
        def create_mini_card(parent, title, value, color):
            card = tk.Frame(parent, bg="white", padx=20, pady=15, highlightbackground="#e2e8f0", highlightthickness=1)
            tk.Label(card, text=value, font=('Segoe UI', 20, 'bold'), bg="white", fg=color).pack(anchor="w")
            tk.Label(card, text=title, font=('Segoe UI', 10), bg="white", fg=self.text_light).pack(anchor="w")
            return card
            
        c1 = create_mini_card(summary_frame, "Total Quizzes", str(total_quizzes), self.primary_color)
        c1.grid(row=0, column=0, padx=(0, 20), sticky="nsew")
        
        c2 = create_mini_card(summary_frame, "Best Score", str(best_score), "#10b981")
        c2.grid(row=0, column=1, padx=(0, 20), sticky="nsew")
        
        c3 = create_mini_card(summary_frame, "Average Score", str(avg_score), "#f59e0b")
        c3.grid(row=0, column=2, padx=0, sticky="nsew")
        
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)
        summary_frame.grid_columnconfigure(2, weight=1)

        # Custom Modern Tabs Navigation
        tab_nav_frame = tk.Frame(content, bg=self.bg_color)
        tab_nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Main Content Container 
        main_content_area = tk.Frame(content, bg="white", padx=20, pady=20, highlightbackground="#e2e8f0", highlightthickness=1)
        main_content_area.pack(fill=tk.BOTH, expand=True)
        
        history_tab = tk.Frame(main_content_area, bg="white")
        graph_tab = tk.Frame(main_content_area, bg="white")
        
        # Tab Controller
        def set_tab(tab_name):
            if tab_name == "history":
                history_tab.pack(fill=tk.BOTH, expand=True)
                graph_tab.pack_forget()
                btn_history_line.configure(bg=self.primary_color)
                btn_history_lbl.configure(fg=self.primary_color, font=('Segoe UI', 12, 'bold'))
                btn_graph_line.configure(bg=self.bg_color)
                btn_graph_lbl.configure(fg=self.text_light, font=('Segoe UI', 12))
            else:
                graph_tab.pack(fill=tk.BOTH, expand=True)
                history_tab.pack_forget()
                btn_graph_line.configure(bg=self.primary_color)
                btn_graph_lbl.configure(fg=self.primary_color, font=('Segoe UI', 12, 'bold'))
                btn_history_line.configure(bg=self.bg_color)
                btn_history_lbl.configure(fg=self.text_light, font=('Segoe UI', 12))
                
        # History Tab Button
        btn_history_container = tk.Frame(tab_nav_frame, bg=self.bg_color, cursor="hand2")
        btn_history_container.pack(side=tk.LEFT, padx=(0, 20))
        btn_history_lbl = tk.Label(btn_history_container, text="Recent Activity", font=('Segoe UI', 12, 'bold'), bg=self.bg_color, fg=self.primary_color)
        btn_history_lbl.pack(pady=(0, 5))
        btn_history_line = tk.Frame(btn_history_container, bg=self.primary_color, height=3)
        btn_history_line.pack(fill=tk.X)
        btn_history_container.bind("<Button-1>", lambda e: set_tab("history"))
        btn_history_lbl.bind("<Button-1>", lambda e: set_tab("history"))
        
        # Graph Tab Button
        btn_graph_container = tk.Frame(tab_nav_frame, bg=self.bg_color, cursor="hand2")
        btn_graph_container.pack(side=tk.LEFT)
        btn_graph_lbl = tk.Label(btn_graph_container, text="Performance Graph", font=('Segoe UI', 12), bg=self.bg_color, fg=self.text_light)
        btn_graph_lbl.pack(pady=(0, 5))
        btn_graph_line = tk.Frame(btn_graph_container, bg=self.bg_color, height=3)
        btn_graph_line.pack(fill=tk.X)
        btn_graph_container.bind("<Button-1>", lambda e: set_tab("graph"))
        btn_graph_lbl.bind("<Button-1>", lambda e: set_tab("graph"))
        
        # Initialize viewing history tab
        history_tab.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable Area for History
        history_canvas = tk.Canvas(history_tab, bg="white", highlightthickness=0)
        history_scrollbar = ttk.Scrollbar(history_tab, orient="vertical", command=history_canvas.yview)
        history_scrollable_frame = tk.Frame(history_canvas, bg="white")
        
        history_scrollable_frame.bind(
            "<Configure>",
            lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all"))
        )
        
        # We want the window to take the full width
        canvas_window = history_canvas.create_window((0, 0), window=history_scrollable_frame, anchor="nw")
        
        def on_canvas_configure(event):
            # Update the width of the frame to match the canvas width so it stretches
            history_canvas.itemconfig(canvas_window, width=event.width)
            
        history_canvas.bind("<Configure>", on_canvas_configure)
        history_canvas.configure(yscrollcommand=history_scrollbar.set)
        
        def _on_mousewheel(event):
            # For windows: event.delta is usually 120 or -120
            # For Linux: handled by Button-4/Button-5
            if history_canvas.winfo_height() < history_scrollable_frame.winfo_reqheight():
                if event.num == 5 or event.delta < 0:
                    history_canvas.yview_scroll(1, "units")
                elif event.num == 4 or event.delta > 0:
                    history_canvas.yview_scroll(-1, "units")
                    
        def bind_to_mousewheel(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", _on_mousewheel)
            widget.bind("<Button-5>", _on_mousewheel)
        
        history_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        history_scrollbar.pack(side="right", fill="y")
        
        bind_to_mousewheel(history_canvas)
        bind_to_mousewheel(history_scrollable_frame)
        
        if not scores:
            tk.Label(history_scrollable_frame, text="No recent activity found.", bg="white", fg=self.text_light, font=('Segoe UI', 12)).pack(pady=40)
            
        for score in scores:
            raw_date = score['attempt_date']
            if isinstance(raw_date, str):
                date_str = raw_date.split('.')[0]
            elif hasattr(raw_date, 'strftime'):
                date_str = raw_date.strftime('%b %d, %Y • %I:%M %p')
            else:
                date_str = str(raw_date)

            mode_tag = score['mode']

            # Create Modern Card for each activity
            act_card = tk.Frame(history_scrollable_frame, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
            act_card.pack(fill=tk.X, pady=(0, 10), padx=5)
            
            # Left accent based on score
            try:
                numeric_score = int(score['total_marks'])
                if numeric_score > 80:
                    accent_col = "#10b981" # Green
                elif numeric_score > 50:
                    accent_col = "#f59e0b" # Yellow
                else:
                    accent_col = "#ef4444" # Red
            except:
                accent_col = self.primary_color
                
            tk.Frame(act_card, bg=accent_col, width=6).pack(side=tk.LEFT, fill=tk.Y)
            
            # Content Frame
            content_fr = tk.Frame(act_card, bg="white", padx=20, pady=15)
            content_fr.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Top row: Exam name & Score
            top_row = tk.Frame(content_fr, bg="white")
            top_row.pack(fill=tk.X)
            
            tk.Label(top_row, text=score['exam_name'], font=('Segoe UI', 12, 'bold'), bg="white", fg=self.secondary_color).pack(side=tk.LEFT)
            
            score_fr = tk.Frame(top_row, bg="#f1f5f9", padx=10, pady=4)
            score_fr.pack(side=tk.RIGHT)
            tk.Label(score_fr, text=f"Score: {score['total_marks']}", font=('Segoe UI', 11, 'bold'), bg="#f1f5f9", fg=self.primary_color).pack()
            
            # Bottom row: Extra info
            bot_row = tk.Frame(content_fr, bg="white")
            bot_row.pack(fill=tk.X, pady=(8, 0))
            
            # Mode Tag
            mode_color = "#3b82f6" if mode_tag.lower() == "exam" else "#8b5cf6"
            mode_fr = tk.Frame(bot_row, bg=mode_color, padx=8, pady=2)
            mode_fr.pack(side=tk.LEFT)
            tk.Label(mode_fr, text=mode_tag, font=('Segoe UI', 9, 'bold'), bg=mode_color, fg="white").pack()
            
            # Attempt
            tk.Label(bot_row, text=f"Attempt: #{score['attempt_number']}", font=('Segoe UI', 10), bg="white", fg=self.text_color).pack(side=tk.LEFT, padx=(15, 0))
            
            # Date
            tk.Label(bot_row, text=date_str, font=('Segoe UI', 10), bg="white", fg=self.text_light).pack(side=tk.RIGHT)
            
            # Hover effect for card
            def create_hover_effect(card_widget, inner_frame):
                def on_enter(e):
                    card_widget.configure(highlightbackground=accent_col, highlightthickness=1)
                    card_widget.configure(bg="#f8fafc")
                    inner_frame.configure(bg="#f8fafc")
                    for child in inner_frame.winfo_children():
                        child.configure(bg="#f8fafc")
                        if child.__class__.__name__ == 'Frame' and child.cget('bg') == "#f1f5f9":
                            pass # keep score frame color
                        
                def on_leave(e):
                    card_widget.configure(highlightbackground="#e2e8f0", highlightthickness=1)
                    card_widget.configure(bg="white")
                    inner_frame.configure(bg="white")
                    for child in inner_frame.winfo_children():
                        child.configure(bg="white")
                        
                card_widget.bind("<Enter>", on_enter)
                card_widget.bind("<Leave>", on_leave)
                # We can skip deep binding for this simple card since it's just visual
            
            create_hover_effect(act_card, content_fr)
            
            # Bind all children of this card to mousewheel event so scrolling works anywhere
            for widget in [act_card, content_fr, top_row, score_fr, bot_row, mode_fr] + \
                          list(top_row.winfo_children()) + list(score_fr.winfo_children()) + \
                          list(bot_row.winfo_children()) + list(mode_fr.winfo_children()):
                bind_to_mousewheel(widget)
            
        # --- Graph Tab Header is not needed, we have custom top tabs now ---
        
        # Top bar for filters
        filter_frame = tk.Frame(graph_tab, bg="white")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.current_canvas_widget = None
        
        def draw_graph(period="daily"):
            if self.current_canvas_widget:
                self.current_canvas_widget.destroy()
                
            data = collections.defaultdict(list)
            for s in scores:
                raw_date = s['attempt_date']
                try:
                    if isinstance(raw_date, str):
                        try:
                            dt = datetime.strptime(raw_date.split('.')[0], "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            dt = datetime.strptime(raw_date.split('.')[0], "%Y-%m-%d")
                    elif hasattr(raw_date, 'strftime'):
                        dt = raw_date
                    else:
                        continue
                except Exception:
                    continue
                    
                if period == "daily":
                    key = dt.strftime("%Y-%m-%d")
                elif period == "weekly":
                    key = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
                else: # monthly
                    key = dt.strftime("%Y-%m")
                    
                data[key].append(int(s['total_marks']))
                
            if not data:
                lbl = tk.Label(graph_tab, text="Not enough data to form a graph.", bg="white", fg=self.text_light)
                lbl.pack(pady=20)
                self.current_canvas_widget = lbl
                return
                
            sorted_keys = sorted(data.keys())
            x_vals = []
            for k in sorted_keys:
                if period == "daily":
                    dt_obj = datetime.strptime(k, "%Y-%m-%d")
                    # Display as Date Month Year
                    x_vals.append(dt_obj.strftime("%d %m %Y"))
                elif period == "monthly":
                    dt_obj = datetime.strptime(k, "%Y-%m")
                    # Display as Month Year
                    x_vals.append(dt_obj.strftime("%m %Y"))
                elif period == "weekly":
                    year, week = k.split('-W')
                    try:
                        # Get Monday of that week
                        dt_obj = datetime.fromisocalendar(int(year), int(week), 1)
                        x_vals.append(dt_obj.strftime("Week %W: %d %m %Y"))
                    except AttributeError:
                        x_vals.append(f"Week {week}, {year}")
                else:
                    x_vals.append(k)
                    
            y_vals = [sum(data[k])/len(data[k]) for k in sorted_keys]
            
            fig = Figure(figsize=(6, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(x_vals, y_vals, marker='o', linestyle='-', color=self.primary_color)
            ax.set_title(f"Average Score ({period.capitalize()})")
            ax.set_xlabel("Time Period")
            ax.set_ylabel("Average Score")
            ax.grid(True, linestyle='--', alpha=0.6)
            fig.autofmt_xdate(rotation=45)
            fig.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=graph_tab)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.pack(fill=tk.BOTH, expand=True)
            self.current_canvas_widget = widget

        # Segmented Control for filters
        seg_control = tk.Frame(filter_frame, bg="#f1f5f9", padx=4, pady=4)
        seg_control.pack(side=tk.LEFT)
        
        self.active_filter_btn = None
        
        def set_filter(btn, period):
            if self.active_filter_btn:
                self.active_filter_btn.configure(bg="#f1f5f9", fg=self.text_light, font=('Segoe UI', 10))
            btn.configure(bg="white", fg=self.primary_color, font=('Segoe UI', 10, 'bold'))
            self.active_filter_btn = btn
            draw_graph(period)
            
        btn_day = tk.Button(seg_control, text="Daily", bg="white", fg=self.primary_color, font=('Segoe UI', 10, 'bold'), bd=0, padx=15, pady=6, cursor="hand2")
        btn_day.pack(side=tk.LEFT, padx=2)
        btn_day.configure(command=lambda b=btn_day: set_filter(b, "daily"))
        self.active_filter_btn = btn_day
        
        btn_week = tk.Button(seg_control, text="Weekly", bg="#f1f5f9", fg=self.text_light, font=('Segoe UI', 10), bd=0, padx=15, pady=6, cursor="hand2")
        btn_week.pack(side=tk.LEFT, padx=2)
        btn_week.configure(command=lambda b=btn_week: set_filter(b, "weekly"))
        
        btn_month = tk.Button(seg_control, text="Monthly", bg="#f1f5f9", fg=self.text_light, font=('Segoe UI', 10), bd=0, padx=15, pady=6, cursor="hand2")
        btn_month.pack(side=tk.LEFT, padx=2)
        btn_month.configure(command=lambda b=btn_month: set_filter(b, "monthly"))
        
        # Initial draw
        draw_graph("daily")

    def show_about(self):
        self.clear_window()
        
        # Header (Consistent Top Bar)
        header = tk.Frame(self.root, bg="white", height=80, padx=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Back Button
        tk.Button(header, text="← Back", font=('Segoe UI', 11), bg="white", fg=self.text_light, bd=0, cursor="hand2", 
                 command=self.show_main_menu).pack(side=tk.LEFT)
        
        # Content Container
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True) # expand=True center aligns if we use place, or pack allows stacking
        
        # About Card Centered
        card = tk.Frame(content, bg="white", padx=50, pady=50, highlightbackground="#e2e8f0", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6)
        
        # App Branding
        if self.logo_image:
            tk.Label(card, image=self.logo_medium, bg="white").pack(pady=(0, 20))
            
        tk.Label(card, text="TEST ARENA", font=('Segoe UI', 32, 'bold'), bg="white", fg=self.primary_color).pack()
        tk.Label(card, text="Version 1.0", font=('Segoe UI', 10, 'bold'), bg="#f1f5f9", fg=self.text_light, padx=12, pady=4).pack(pady=(0, 20))
        
        # Description
        desc = ("Test Arena is a comprehensive assessment platform designed to help students "
               "excel in competitive exams. With realistic exam simulations and detailed "
               "performance analytics, we make preparation smarter and more effective.")
        tk.Label(card, text=desc, font=('Segoe UI', 11), bg="white", fg=self.text_color, wraplength=500, justify="center").pack(pady=(0, 30))
        
        # Features Grid (2x2)
        features_frame = tk.Frame(card, bg="white")
        features_frame.pack()
        
        features = [
            ("⚡", "Real-time Exam Simulation"),
            ("📊", "Detailed Performance Analytics"),
            ("🎯", "Topic-wise Practice Mode"),
            ("📱", "Responsive User Interface")
        ]
        
        for i, (icon, text) in enumerate(features):
            row = i // 2
            col = i % 2
            f_item = tk.Frame(features_frame, bg="white", padx=20, pady=10)
            f_item.grid(row=row, column=col, sticky="w")
            
            tk.Label(f_item, text=icon, font=('Segoe UI Symbol', 14), bg="white").pack(side=tk.LEFT)
            tk.Label(f_item, text=text, font=('Segoe UI', 10, 'bold'), bg="white", fg=self.secondary_color).pack(side=tk.LEFT, padx=10)
            
        # Footer / Credits
        tk.Label(card, text="Developed as a DBMS Project", font=('Segoe UI', 9), bg="white", fg=self.text_light).pack(side=tk.BOTTOM, pady=(40, 0))


if __name__ == "__main__":
    app = QuizApp()
    app.start()
