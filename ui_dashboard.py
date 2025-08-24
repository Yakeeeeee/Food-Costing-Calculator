import customtkinter as ctk
from typing import Callable, List, Dict
from data_handler import DataHandler

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataHandler, on_refresh_callback: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_handler = data_handler
        self.on_refresh_callback = on_refresh_callback
        self.current_recipes = []
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self._setup_layout()
        self._refresh_recipes()
    
    def _create_widgets(self):
        # Main card container
        self.card = ctk.CTkFrame(self, corner_radius=15, fg_color="#2d2d2d")
        self.card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Card title
        self.title_label = ctk.CTkLabel(
            self.card, 
            text="Recipe Dashboard", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        
        # Search section
        self.search_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search Recipes:", text_color="#ffffff")
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Search by recipe name...",
            width=300
        )
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Recipes table frame
        self.table_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        
        # Table headers
        self.headers_frame = ctk.CTkFrame(self.table_frame, fg_color="#3d3d3d")
        self._create_table_headers()
        
        # Recipes scrollable frame
        self.recipes_container = ctk.CTkScrollableFrame(
            self.table_frame,
            fg_color="transparent",
            height=400
        )
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.card,
            text="",
            text_color="#4cafef",
            font=ctk.CTkFont(size=14)
        )
    
    def _create_table_headers(self):
        """Create table header row"""
        headers = ["Recipe Name", "Total Cost", "Selling Price", "Profit", "Ingredients"]
        widths = [200, 120, 120, 120, 300]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = ctk.CTkLabel(
                self.headers_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffffff",
                width=width
            )
            label.grid(row=0, column=i, padx=5, pady=10, sticky="w")
    
    def _setup_layout(self):
        # Configure card grid
        self.card.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label.grid(row=0, column=0, pady=(20, 20))
        
        # Search section
        self.search_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew", padx=20)
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        self.search_entry.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        # Table section
        self.table_frame.grid(row=2, column=0, pady=(0, 20), sticky="nsew", padx=20)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Headers
        self.headers_frame.grid(row=0, column=0, sticky="ew", padx=20)
        self.headers_frame.grid_columnconfigure(0, weight=1)
        
        # Recipes container
        self.recipes_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 0))
        
        # Status
        self.status_label.grid(row=3, column=0, pady=(0, 20))
    
    def _refresh_recipes(self):
        """Refresh the recipes display"""
        # Clear existing recipes
        for widget in self.recipes_container.winfo_children():
            widget.destroy()
        
        # Get recipes from data handler
        self.current_recipes = self.data_handler.get_all_recipes()
        
        # Create recipe rows
        for i, recipe in enumerate(self.current_recipes):
            self._create_recipe_row(i, recipe)
    
    def _create_recipe_row(self, index: int, recipe: Dict[str, str]):
        """Create a row for a recipe in the table"""
        row_frame = ctk.CTkFrame(self.recipes_container, fg_color="#3d3d3d")
        row_frame.grid(row=index, column=0, sticky="ew", pady=2)
        row_frame.grid_columnconfigure(0, weight=1)
        
        # Recipe data labels
        labels = [
            recipe.get("Recipe Name", ""),
            f"${recipe.get('Total Cost', '0.00')}",
            f"${recipe.get('Suggested Selling Price', '0.00')}",
            f"${recipe.get('Profit', '0.00')}",
            recipe.get("Ingredients Used", "")
        ]
        widths = [200, 120, 120, 120, 300]
        
        for i, (label, width) in enumerate(zip(labels, widths)):
            label_widget = ctk.CTkLabel(
                row_frame,
                text=label,
                text_color="#ffffff",
                width=width
            )
            label_widget.grid(row=0, column=i, padx=5, pady=8, sticky="w")
    
    def _on_search(self, event=None):
        """Handle search input changes"""
        query = self.search_entry.get().strip()
        filtered_recipes = self.data_handler.search_recipes(query)
        
        # Clear existing recipes
        for widget in self.recipes_container.winfo_children():
            widget.destroy()
        
        # Display filtered recipes
        self.current_recipes = filtered_recipes
        for i, recipe in enumerate(filtered_recipes):
            self._create_recipe_row(i, recipe)
    
    def refresh_display(self):
        """Public method to refresh the display"""
        self._refresh_recipes()
