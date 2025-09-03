import customtkinter as ctk
import webbrowser

class AboutPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Changed from row 1 to row 0
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable.grid_columnconfigure(0, weight=1) # Ensure content expands horizontally
        
        # App info section
        self.app_info_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.app_title = ctk.CTkLabel(
            self.app_info_section,
            text="🍽️ Food Costing Calculator",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4cafef"
        )
        
        
        self.version_label = ctk.CTkLabel(
            self.app_info_section,
            text="Version 2.0.0",
            font=ctk.CTkFont(size=16),
            text_color="#888888"
        )
        
        # Description section
        self.description_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.description_title = ctk.CTkLabel(
            self.description_section,
            text="📖 About This Application",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        self.description_text = ctk.CTkLabel(
            self.description_section,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            # wraplength removed to allow content to expand naturally
            justify="left",
            anchor="w"
        )
        
        description_content = """Welcome to the Food Costing Calculator! This easy-to-use app helps anyone who makes or sells food figure out their costs and set the right prices. Whether you run a restaurant, a small food business, or just love cooking at home, this tool makes managing your food expenses simple.
        
        Here’s what you can do:
        •   **Manage Ingredients:** Keep track of all your ingredients, their prices, and how much you use.
        •   **Track Packaging:** Don't forget the cost of your boxes, bags, and other packaging.
        •   **Calculate Recipe Costs:** Quickly find out the total cost of any recipe, including ingredients, packaging, and even a bit for your time.
        •   **Set Selling Prices:** Easily set prices for your dishes to make sure you're making a good profit.
        •   **Save Your Recipes:** Store all your recipe costs in one place for quick access later.
        •   **Find Anything Fast:** Search for ingredients, packaging, or recipes in a snap.
        •   **See Cost Details:** Get a clear breakdown of all your expenses, including sales tax (VAT) if you need it.
        
        Our goal is to help you make smart pricing decisions and keep your food business profitable without needing to be a math wizard!"""
        
        self.description_text.configure(text=description_content)
        
        # Features section
        self.features_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.features_title = ctk.CTkLabel(
            self.features_section,
            text="✨ Key Features",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        # Features grid
        self.features_grid = ctk.CTkFrame(self.features_section, fg_color="transparent")
        
        features = [
            ("🥕", "Ingredient Management", "Add, edit, and manage your ingredient database with accurate pricing"),
            ("📦", "Packaging Tracking", "Include packaging costs in your recipe calculations"),
            ("🧮", "Smart Calculator", "Automated cost calculations with labor and overhead considerations"),
            ("📊", "Profit Analysis", "Determine optimal selling prices with customizable margins"),
            ("💾", "Recipe Storage", "Save and organize your recipe costings for easy access"),
            ("🔍", "Search & Filter", "Quickly find ingredients, packaging, and recipes"),
            ("📈", "Cost Breakdown", "Detailed breakdown of all costs including VAT"),
            ("🎯", "User-Friendly", "Intuitive interface designed for beginners and professionals")
        ]
        
        self.feature_cards = []
        for i, (icon, title, description) in enumerate(features):
            card = self._create_feature_card(icon, title, description)
            self.feature_cards.append(card)
        
        # Contribution section
        self.credits_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.credits_title = ctk.CTkLabel(
            self.credits_section,
            text="👨‍💻 Developer & Contact",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        self.credits_text = ctk.CTkLabel(
            self.credits_section,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            # wraplength removed to allow content to expand naturally
            justify="left",
            anchor="w"
        )
        
        credits_content = """Developer: John Allen Esteleydes
                
        Connect with me:
        •   GitHub: Yakeeeeee
        •   Email: esteleydesjohnallen0@gmail.com
        """
        
        self.credits_text.configure(text=credits_content)

        self.youtube_button = ctk.CTkButton(
            self.credits_section,
            text="▶️ Watch on YouTube",
            command=self._open_youtube_link,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#ff0000",
            hover_color="#cc0000",
            text_color="#ffffff",
            corner_radius=10
        )

    def _open_youtube_link(self):
        """Open the YouTube channel link in a web browser."""
        webbrowser.open_new_tab("https://www.youtube.com/@mr.yakeee")
    
    def _create_feature_card(self, icon: str, title: str, description: str):
        """Create a feature card"""
        card = ctk.CTkFrame(self.features_grid, fg_color="#3d3d3d", corner_radius=10)
        
        # Icon and title
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=ctk.CTkFont(size=24),
            text_color="#4cafef"
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(side="left")
        
        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            # wraplength removed to allow content to expand naturally
        )
        desc_label.pack(padx=15, pady=(0, 15), fill="x")
        
        return card
    
    def _setup_layout(self):
        # Main scrollable
        self.main_scrollable.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # App info section
        self.app_info_section.pack(fill="x", padx=0, pady=(0, 20))
        self.app_title.pack(pady=(30, 10))
        self.version_label.pack(pady=(0, 30))
        
        # Description section
        self.description_section.pack(fill="x", padx=20, pady=(0, 20))
        self.description_title.pack(pady=(20, 15))
        self.description_text.pack(fill="x", padx=20, pady=(0, 20))
        
        # Features section
        self.features_section.pack(fill="x", padx=20, pady=(0, 20))
        self.features_title.pack(pady=(20, 20))
        
        self.features_grid.pack(fill="x", padx=20, pady=(0, 20))
        # Configure grid for 2 columns, allowing responsiveness
        self.features_grid.grid_columnconfigure(0, weight=1)
        self.features_grid.grid_columnconfigure(1, weight=1)
        
        # Layout feature cards in a 2-column grid
        for i, card in enumerate(self.feature_cards):
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Contribution section
        self.credits_section.pack(fill="x", padx=20, pady=(0, 20))
        self.credits_title.pack(pady=(20, 15))
        self.credits_text.pack(fill="x", padx=20, pady=(0, 20))
        self.youtube_button.pack(pady=(10, 20))
