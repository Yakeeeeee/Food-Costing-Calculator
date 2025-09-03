import customtkinter as ctk
from typing import Callable
from core.data_handler import DataHandler

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataHandler, refresh_callback: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_handler = data_handler
        self.refresh_callback = refresh_callback
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Changed from row 1 to row 0
        
        self._create_widgets()
        self._setup_layout()
        self.refresh_stats()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable_frame.grid_columnconfigure(0, weight=1) # Ensure content expands horizontally

        # Welcome section
        self.welcome_frame = ctk.CTkFrame(self.main_scrollable_frame, fg_color="transparent")
        
        self.welcome_title = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome to Food Costing Calculator! 🎉",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4cafef"
        )
        
        
        # Statistics cards
        self.stats_frame = ctk.CTkFrame(self.main_scrollable_frame, fg_color="transparent")
        
        # Ingredients stats card
        self.ingredients_card = self._create_stat_card(
            self.stats_frame,
            "🥕 Ingredients",
            "Total ingredients in your database",
            "0",
            "#4cafef"
        )
        
        # Recipes stats card
        self.recipes_card = self._create_stat_card(
            self.stats_frame,
            "📝 Recipes",
            "Saved recipes ready for costing",
            "0",
            "#28a745"
        )
        
        # Packaging stats card
        self.packaging_card = self._create_stat_card(
            self.stats_frame,
            "📦 Packaging",
            "Packaging materials available",
            "0",
            "#ff9500"
        )
        
        # Quick actions section
        self.actions_frame = ctk.CTkFrame(self.main_scrollable_frame, fg_color="transparent")
        
        self.actions_title = ctk.CTkLabel(
            self.actions_frame,
            text="🚀 Quick Actions",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        
        # Quick action buttons
        self.quick_actions = ctk.CTkFrame(self.actions_frame, fg_color="#2d2d2d", corner_radius=15)
        
        self.add_ingredient_btn = ctk.CTkButton(
            self.quick_actions,
            text="➕ Add New Ingredient",
            command=self._add_ingredient_action,
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        )
        
        self.calculate_recipe_btn = ctk.CTkButton(
            self.quick_actions,
            text="🧮 Calculate Recipe Cost",
            command=self._calculate_recipe_action,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        )
        
        self.view_recipes_btn = ctk.CTkButton(
            self.quick_actions,
            text="📋 View All Recipes",
            command=self._view_recipes_action,
            fg_color="#ff9500",
            hover_color="#e6850e",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        )
        
        self.add_packaging_btn = ctk.CTkButton(
            self.quick_actions,
            text="📦 Add Packaging Material",
            command=self._add_packaging_action,
            fg_color="#9c27b0",
            hover_color="#7b1fa2",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        )
        
        # Tips section
        self.tips_frame = ctk.CTkFrame(self.main_scrollable_frame, fg_color="#2d2d2d", corner_radius=15)
        
        self.tips_title = ctk.CTkLabel(
            self.tips_frame,
            text="💡 Pro Tips",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        self.tips_text = ctk.CTkLabel(
            self.tips_frame,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            wraplength=600, # Adjust wraplength as needed
            justify="left",
            anchor="w"
        )
        
        # Insert tips
        tips_content = """• Start by adding your ingredients with accurate prices and quantities
• Use the calculator to determine optimal selling prices for your recipes
• Regularly update ingredient prices to maintain accurate costings
• Save your recipes to build a database of your menu items
• Consider packaging costs when calculating final product prices
• Use the 50% margin as a starting point, then adjust based on your market"""
        
        self.tips_text.configure(text=tips_content)
    
    def _create_stat_card(self, parent, title, subtitle, value, color):
        """Create a statistics card"""
        card = ctk.CTkFrame(parent, fg_color="#2d2d2d", corner_radius=15)
        
        # Card content
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=color
        )
        
        # Store the value label for updating
        card.value_label = value_label
        
        # Layout
        title_label.pack(pady=(20, 5))
        value_label.pack(pady=(0, 20))
        
        return card
    
    def _setup_layout(self):
        # Main scrollable frame layout
        self.main_scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Welcome section
        self.welcome_frame.pack(fill="x", padx=0, pady=(0, 30))
        self.welcome_title.pack(pady=(0, 10))
        
        # Statistics section
        self.stats_frame.pack(fill="x", padx=20, pady=(0, 30))
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_frame.grid_columnconfigure(1, weight=1)
        self.stats_frame.grid_columnconfigure(2, weight=1)
        
        self.ingredients_card.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        self.recipes_card.grid(row=0, column=1, padx=(0, 15), sticky="ew")
        self.packaging_card.grid(row=0, column=2, sticky="ew")
        
        # Quick actions section
        self.actions_frame.pack(fill="x", padx=20, pady=(0, 30))
        self.actions_title.pack(pady=(0, 20))
        
        self.quick_actions.pack(fill="x")
        self.quick_actions.grid_columnconfigure(0, weight=1)
        self.quick_actions.grid_columnconfigure(1, weight=1)
        self.quick_actions.grid_columnconfigure(2, weight=1)
        self.quick_actions.grid_columnconfigure(3, weight=1)
        
        self.add_ingredient_btn.grid(row=0, column=0, padx=15, pady=20, sticky="ew")
        self.calculate_recipe_btn.grid(row=0, column=1, padx=15, pady=20, sticky="ew")
        self.view_recipes_btn.grid(row=0, column=2, padx=15, pady=20, sticky="ew")
        self.add_packaging_btn.grid(row=0, column=3, padx=15, pady=20, sticky="ew")
        
        # Tips section
        self.tips_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.tips_title.pack(pady=(20, 15))
        self.tips_text.pack(fill="x", padx=20, pady=(0, 20))
    
    def refresh_stats(self):
        """Refresh dashboard statistics"""
        try:
            ingredients = self.data_handler.get_all_ingredients()
            recipes = self.data_handler.get_all_recipes()
            packaging_materials = self.data_handler.get_all_packaging_materials()
            
            self.ingredients_card.value_label.configure(text=str(len(ingredients)))
            self.recipes_card.value_label.configure(text=str(len(recipes)))
            self.packaging_card.value_label.configure(text=str(len(packaging_materials)))
        except Exception as e:
            print(f"Error refreshing stats: {e}")
    
    def _add_ingredient_action(self):
        """Navigate to ingredients page"""
        if self.refresh_callback:
            self.refresh_callback("ingredients")
    
    def _calculate_recipe_action(self):
        """Navigate to calculator page"""
        if self.refresh_callback:
            self.refresh_callback("calculator")
    
    def _view_recipes_action(self):
        """Navigate to recipes page"""
        if self.refresh_callback:
            self.refresh_callback("recipes")
    
    def _add_packaging_action(self):
        """Navigate to packaging page"""
        if self.refresh_callback:
            self.refresh_callback("packaging")
