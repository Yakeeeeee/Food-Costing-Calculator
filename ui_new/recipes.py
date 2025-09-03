import customtkinter as ctk
from typing import Callable, List, Dict
from core.data_handler import DataHandler
import tkinter.messagebox as messagebox

class RecipesPage(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataHandler, refresh_callback: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_handler = data_handler
        self.refresh_callback = refresh_callback
        self.current_recipes = []
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Changed from row 1 to row 0
        
        self._create_widgets()
        self._setup_layout()
        self._refresh_recipes()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable.grid_columnconfigure(0, weight=1) # Ensure content expands horizontally
        
        # Header section
        self.header_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.header_title = ctk.CTkLabel(
            self.header_section,
            text="📝 Saved Recipes",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#28a745"
        )
        
        
        # Search section
        self.search_frame = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.search_label = ctk.CTkLabel(
            self.search_frame,
            text="🔍 Search Recipes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Type to search recipes...",
            height=40
        )
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Recipes list section
        self.list_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.list_title = ctk.CTkLabel(
            self.list_section,
            text="📋 Recipe Database",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        # Recipes container
        self.recipes_container = ctk.CTkFrame(
            self.list_section,
            fg_color="transparent"
        )
    
    def _setup_layout(self):
        # Main scrollable
        self.main_scrollable.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Header section layout
        self.header_section.pack(fill="x", padx=0, pady=(0, 20))
        self.header_title.pack(pady=(20, 10))
        
        # Search section layout
        self.search_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.search_label.pack(pady=(20, 15))
        self.search_entry.pack(fill="x", padx=30, pady=(0, 20))
        
        # List section layout
        self.list_section.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.list_title.pack(pady=(20, 15))
        self.recipes_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
    
    def _on_search(self, event=None):
        """Handle search input"""
        query = self.search_entry.get().strip()
        if query:
            recipes = self.data_handler.search_recipes(query)
        else:
            recipes = self.data_handler.get_all_recipes()
        
        self._display_recipes(recipes)
    
    def _refresh_recipes(self):
        """Refresh recipes list"""
        self.current_recipes = self.data_handler.get_all_recipes()
        self._display_recipes(self.current_recipes)
    
    def _display_recipes(self, recipes: List[Dict[str, str]]):
        """Display recipes in the container"""
        # Clear existing widgets
        for widget in self.recipes_container.winfo_children():
            widget.destroy()
        
        if not recipes:
            # Show empty state
            empty_frame = ctk.CTkFrame(self.recipes_container, fg_color="transparent")
            empty_frame.pack(expand=True, fill="both", pady=50)
            
            empty_label = ctk.CTkLabel(
                empty_frame,
                text="🍽️ No recipes found yet!",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color="#888888"
            )
            empty_label.pack(pady=(0, 10))
            
            empty_subtitle = ctk.CTkLabel(
                empty_frame,
                text="Use the Calculator to create and save your first recipe costing",
                font=ctk.CTkFont(size=16),
                text_color="#666666"
            )
            empty_subtitle.pack()
            
            return
        
        # Create recipe cards
        for i, recipe in enumerate(recipes):
            card = self._create_recipe_card(recipe, i)
            card.pack(fill="x", pady=(0, 15))
    
    def _create_recipe_card(self, recipe: Dict[str, str], index: int):
        """Create a card for displaying recipe information"""
        card = ctk.CTkFrame(self.recipes_container, fg_color="#3d3d3d", corner_radius=15)
        
        # Main content frame
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=25, pady=20)
        
        # Recipe header
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=recipe.get("Recipe Name", ""),
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#28a745"
        )
        name_label.pack(side="left")
        
        # Cost summary
        cost_frame = ctk.CTkFrame(content_frame, fg_color="#2d2d2d", corner_radius=10)
        cost_frame.pack(fill="x", pady=(0, 15))
        
        # Cost breakdown
        costs_frame = ctk.CTkFrame(cost_frame, fg_color="transparent")
        costs_frame.pack(fill="x", padx=20, pady=15)
        
        # Row 1: Ingredient and Packaging costs
        row1_frame = ctk.CTkFrame(costs_frame, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(0, 10))
        
        ingredient_cost_label = ctk.CTkLabel(
            row1_frame,
            text=f"🥕 Ingredients: ₱{recipe.get('Total Ingredient Cost', '0')}",
            font=ctk.CTkFont(size=14),
            text_color="#4cafef"
        )
        ingredient_cost_label.pack(side="left", padx=(0, 30))
        
        packaging_cost_label = ctk.CTkLabel(
            row1_frame,
            text=f"📦 Packaging: ₱{recipe.get('Packaging Cost', '0')}",
            font=ctk.CTkFont(size=14),
            text_color="#ff9500"
        )
        packaging_cost_label.pack(side="left", padx=(0, 30))
        
        labor_cost_label = ctk.CTkLabel(
            row1_frame,
            text=f"👷 Labor: ₱{recipe.get('Labor Cost (50%)', '0')}",
            font=ctk.CTkFont(size=14),
            text_color="#9c27b0"
        )
        labor_cost_label.pack(side="left")
        
        # Row 2: Total cost and selling price
        row2_frame = ctk.CTkFrame(costs_frame, fg_color="transparent")
        row2_frame.pack(fill="x", pady=(0, 10))
        
        total_cost_label = ctk.CTkLabel(
            row2_frame,
            text=f"💰 Total Cost: ₱{recipe.get('Total Cost', '0')}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ff6b6b"
        )
        total_cost_label.pack(side="left", padx=(0, 30))
        
        selling_price_label = ctk.CTkLabel(
            row2_frame,
            text=f"💵 Selling Price: ₱{recipe.get('Suggested Selling Price', '0')}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#28a745"
        )
        selling_price_label.pack(side="left", padx=(0, 30))
        
        profit_label = ctk.CTkLabel(
            row2_frame,
            text=f"📈 Profit: ₱{recipe.get('Profit', '0')}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4cafef"
        )
        profit_label.pack(side="left")
        
        # Row 3: Margin and VAT
        row3_frame = ctk.CTkFrame(costs_frame, fg_color="transparent")
        row3_frame.pack(fill="x")
        
        margin_label = ctk.CTkLabel(
            row3_frame,
            text=f"📊 Margin: {recipe.get('Margin Percentage', '0')}%",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc"
        )
        margin_label.pack(side="left", padx=(0, 30))
        
        vat_label = ctk.CTkLabel(
            row3_frame,
            text=f"🏛️ VAT: {recipe.get('VAT Percentage', '0')}%",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc"
        )
        vat_label.pack(side="left")
        
        # Ingredients and packaging used
        details_frame = ctk.CTkFrame(content_frame, fg_color="#2d2d2d", corner_radius=10)
        # Initially hide details_frame
        details_frame.pack_forget()
        
        details_title = ctk.CTkLabel(
            details_frame,
            text="📋 Recipe Details",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        details_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        ingredients_text = f"🥕 Ingredients: {recipe.get('Ingredients Used', 'None')}"
        ingredients_label = ctk.CTkLabel(
            details_frame,
            text=ingredients_text,
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            # wraplength removed to allow content to expand naturally
        )
        ingredients_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        packaging_text = f"📦 Packaging: {recipe.get('Packaging Materials Used', 'None')}"
        packaging_label = ctk.CTkLabel(
            details_frame,
            text=packaging_text,
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            # wraplength removed to allow content to expand naturally
        )
        packaging_label.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Action buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        # Details button
        details_btn = ctk.CTkButton(
            button_frame,
            text="Show Details",
            command=lambda: self._toggle_details(details_frame, details_btn),
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14),
            height=35
        )
        details_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Delete Recipe",
            command=lambda idx=index: self._delete_recipe(idx),
            fg_color="#ff6b6b",
            hover_color="#e55555",
            font=ctk.CTkFont(size=14),
            height=35
        )
        delete_btn.pack(side="right")
        
        return card

    def _toggle_details(self, details_frame: ctk.CTkFrame, button: ctk.CTkButton):
        """Toggle the visibility of recipe details."""
        if details_frame.winfo_ismapped(): # Check if the frame is currently visible
            details_frame.pack_forget()
            button.configure(text="Show Details")
        else:
            details_frame.pack(fill="x", pady=(0, 15))
            button.configure(text="Hide Details")
    
    def _delete_recipe(self, index: int):
        """Delete recipe at specified index"""
        if 0 <= index < len(self.current_recipes):
            recipe_id = self.current_recipes[index].get("Recipe ID", "")
            recipe_name = self.current_recipes[index].get("Recipe Name", "Unknown Recipe")
            
            result = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete the recipe '{recipe_name}' (ID: {recipe_id})?\n\nThis action cannot be undone."
            )
            
            if result:
                success = self.data_handler.delete_recipe(recipe_id)
                if success:
                    messagebox.showinfo("Success", f"Deleted recipe: {recipe_name}")
                    self._refresh_recipes()
                    if self.refresh_callback:
                        self.refresh_callback()
                else:
                    messagebox.showerror("Error", "Failed to delete recipe!")
