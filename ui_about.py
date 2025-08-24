import customtkinter as ctk
import webbrowser

class AboutFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        # Main card container
        self.card = ctk.CTkFrame(self, corner_radius=15, fg_color="#2d2d2d")
        self.card.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        # App title and version
        self.app_title = ctk.CTkLabel(
            self.card, 
            text="Food Costing Calculator", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4cafef"
        )
        
        self.version_label = ctk.CTkLabel(
            self.card,
            text="Version 1.0.0",
            font=ctk.CTkFont(size=16),
            text_color="#cccccc"
        )
        
        # Description
        self.description_label = ctk.CTkLabel(
            self.card,
            text="A comprehensive desktop application for managing ingredients, calculating recipe costs, and determining optimal selling prices using a configurable Target Margin (%) input from the Calculator.",
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
            wraplength=600,
            justify="center"
        )
        
        # Developer section
        self.developer_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.developer_title = ctk.CTkLabel(
            self.developer_frame,
            text="Developer",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        self.developer_name = ctk.CTkLabel(
            self.developer_frame,
            text="John Allen Esteleydes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4cafef"
        )
        
        # Contact information
        self.contact_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.contact_title = ctk.CTkLabel(
            self.contact_frame,
            text="Contact Information",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        # Email
        self.email_frame = ctk.CTkFrame(self.contact_frame, fg_color="transparent")
        self.email_label = ctk.CTkLabel(
            self.email_frame,
            text="📧 Email:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        self.email_value = ctk.CTkLabel(
            self.email_frame,
            text="esteleydesjohnallen0@gmail.com",
            font=ctk.CTkFont(size=14),
            text_color="#4cafef"
        )
        
        # YouTube
        self.youtube_frame = ctk.CTkFrame(self.contact_frame, fg_color="transparent")
        self.youtube_label = ctk.CTkLabel(
            self.youtube_frame,
            text="📺 YouTube:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        self.youtube_link = ctk.CTkButton(
            self.youtube_frame,
            text="Yakee",
            command=lambda: webbrowser.open("https://www.youtube.com/@mr.yakeee"),
            fg_color="#ff6b6b",
            hover_color="#e55555",
            text_color="#ffffff",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=30,
            width=100,
            corner_radius=8
        )
        
        # GitHub
        self.github_frame = ctk.CTkFrame(self.contact_frame, fg_color="transparent")
        self.github_label = ctk.CTkLabel(
            self.github_frame,
            text="💻 GitHub:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        self.github_link = ctk.CTkButton(
            self.github_frame,
            text="Yakeeeeee",
            command=lambda: webbrowser.open("https://github.com/Yakeeeeee"),
            fg_color="#28a745",
            hover_color="#218838",
            text_color="#ffffff",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=30,
            width=100,
            corner_radius=8
        )
        
        # Beacons.ai (All Socials)
        self.beacons_frame = ctk.CTkFrame(self.contact_frame, fg_color="transparent")
        self.beacons_label = ctk.CTkLabel(
            self.beacons_frame,
            text="🔗 All Socials:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        self.beacons_link = ctk.CTkButton(
            self.beacons_frame,
            text="beacons.ai/yakee",
            command=lambda: webbrowser.open("https://beacons.ai/yakee"),
            fg_color="#9c27b0",
            hover_color="#7b1fa2",
            text_color="#ffffff",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=30,
            width=140,
            corner_radius=8
        )
        
        # Features section
        self.features_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.features_title = ctk.CTkLabel(
            self.features_frame,
            text="Key Features",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.features_list = ctk.CTkLabel(
            self.features_frame,
            text="• Ingredient Management\n• Recipe Cost Calculation\n• Configurable Automatic Pricing (Target Margin % — default 150% → 2.5×)\n• Labor & Miscellaneous Cost Inclusion\n• CSV Data Storage\n• Search & Filter Functionality\n• Professional Dark Theme UI",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
        
        # Copyright
        self.copyright_label = ctk.CTkLabel(
            self.card,
            text="© 2025 John Allen Esteleydes. All rights reserved.",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
    
    def _setup_layout(self):
        # Configure card grid
        self.card.grid_columnconfigure(0, weight=1)
        
        # App title and version
        self.app_title.pack(pady=(20, 5))
        self.version_label.pack(pady=(0, 20))
        
        # Description
        self.description_label.pack(pady=(0, 25), padx=20)
        
        # Developer section
        self.developer_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.developer_title.pack(pady=(15, 10))
        self.developer_name.pack(pady=(0, 15))
        
        # Contact information
        self.contact_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.contact_title.pack(pady=(15, 15))
        
        # Email
        self.email_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.email_label.pack(side="left", padx=(0, 10))
        self.email_value.pack(side="left")
        
        # YouTube
        self.youtube_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.youtube_label.pack(side="left", padx=(0, 10))
        self.youtube_link.pack(side="left")
        
        # GitHub
        self.github_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.github_label.pack(side="left", padx=(0, 10))
        self.github_link.pack(side="left")
        
        # Beacons.ai
        self.beacons_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.beacons_label.pack(side="left", padx=(0, 10))
        self.beacons_link.pack(side="left")
        
        # Features section
        self.features_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.features_title.pack(pady=(15, 15))
        self.features_list.pack(pady=(0, 15), padx=20)
        
        # Copyright
        self.copyright_label.pack(pady=(0, 20))
