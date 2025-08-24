import customtkinter as ctk
from typing import Callable, List, Dict
from data_handler import DataHandler
import re

class RecipesFrame(ctk.CTkFrame):
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
            text="Saved Recipes", 
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
        headers = ["Recipe Name", "Total Cost", "Selling Price", "Profit", "Ingredients", "Actions"]
        widths = [200, 120, 120, 120, 300, 120]
        
        # Configure column weights for headers
        for i in range(len(headers)):
            self.headers_frame.grid_columnconfigure(i, weight=0, minsize=widths[i])
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = ctk.CTkLabel(
                self.headers_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#ffffff",
                width=width
            )
            label.grid(row=0, column=i, padx=5, pady=8, sticky="w")  # Reduced pady from 10 to 8
    
    def _setup_layout(self):
        # Configure card grid
        self.card.grid_columnconfigure(0, weight=1)
        
        # Title - reduced padding
        self.title_label.grid(row=0, column=0, pady=(15, 15))
        
        # Search section - reduced padding
        self.search_frame.grid(row=1, column=0, pady=(0, 15), sticky="ew", padx=15)
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_label.grid(row=0, column=0, padx=(15, 8), pady=8)
        self.search_entry.grid(row=0, column=1, padx=(0, 15), pady=8, sticky="ew")
        
        # Table section - reduced padding
        self.table_frame.grid(row=2, column=0, pady=(0, 15), sticky="nsew", padx=15)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Headers
        self.headers_frame.grid(row=0, column=0, sticky="ew", padx=15)
        
        # Recipes container - reduced padding
        self.recipes_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(8, 0))
        
        # Status - reduced padding
        self.status_label.grid(row=3, column=0, pady=(0, 15))
    
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
    
    def _safe_currency(self, raw):
        """Try to format a raw value (string/number) as currency string like $12.34."""
        try:
            return f"${float(str(raw).replace('$','').strip()):.2f}"
        except Exception:
            return str(raw)

    def _find_field(self, record: Dict[str, str], candidates: List[str]) -> str:
        """Return the first matching non-empty field value from record for any candidate name.
           If none found, do a fuzzy search for keys that contain candidate substrings."""
        for name in candidates:
            v = record.get(name)
            if v not in (None, ""):
                return v
        # fuzzy search by key name
        for key, v in record.items():
            if any(c.lower() in key.lower() for c in candidates) and v not in (None, ""):
                return v
        return ""

    def _create_recipe_row(self, index: int, recipe: Dict[str, str]):
        """Create a row for a recipe in the table"""
        row_frame = ctk.CTkFrame(self.recipes_container, fg_color="#3d3d3d")
        row_frame.grid(row=index, column=0, sticky="ew", pady=1)

        # Configure column weights for consistent alignment with headers
        widths = [200, 120, 120, 120, 300, 120]
        for i in range(len(widths)):
            row_frame.grid_columnconfigure(i, weight=0, minsize=widths[i])

        # Safely obtain values (handles variations in CSV headers / old files)
        total_cost_raw = self._find_field(recipe, ["Total Cost", "Total Ingredient Cost", "Total"])
        selling_price_raw = self._find_field(recipe, ["Suggested Selling Price", "Selling Price", "Suggested Price"])
        profit_raw = self._find_field(recipe, ["Profit", "Net Profit"])
        ingredients_raw = self._find_field(recipe, ["Ingredients Used", "Ingredients", "Ingredient List"])

        # If ingredients field looks like a numeric value (means columns/headers were shifted),
        # try to recover a text-like field from the record
        if ingredients_raw and re.match(r'^\$?\s*[\d\.,]+$', str(ingredients_raw).strip()):
            # search for any value that contains letters or commas (likely ingredient list)
            for v in recipe.values():
                if v and any(ch.isalpha() for ch in str(v)):
                    if not re.match(r'^\$?\s*[\d\.,]+$', str(v).strip()):
                        ingredients_raw = v
                        break

        labels = [
            recipe.get("Recipe Name", ""),
            self._safe_currency(total_cost_raw) if total_cost_raw else "$0.00",
            self._safe_currency(selling_price_raw) if selling_price_raw else "$0.00",
            self._safe_currency(profit_raw) if profit_raw else "$0.00",
            ingredients_raw or ""
        ]

        for i, (label, width) in enumerate(zip(labels, widths[:-1])):  # Exclude Actions column
            label_widget = ctk.CTkLabel(
                row_frame,
                text=label,
                text_color="#ffffff",
                width=width
            )
            label_widget.grid(row=0, column=i, padx=5, pady=6, sticky="w")

        # Action buttons
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=5, padx=5, pady=4)

        view_btn = ctk.CTkButton(
            actions_frame,
            text="View Details",
            command=lambda r=recipe: self._view_recipe_details_by_recipe(r),
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            width=80,
            height=28,
            font=ctk.CTkFont(size=12)
        )
        view_btn.pack(side="left", padx=2)

        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Delete",
            command=lambda r=recipe: self._confirm_delete_dialog(r),
            fg_color="#ff6b6b",
            hover_color="#e55555",
            width=70,
            height=28,
            font=ctk.CTkFont(size=12)
        )
        delete_btn.pack(side="left", padx=2)
    
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
    
    def _view_recipe_details(self, index: int):
        """View detailed costing information for a recipe"""
        if 0 <= index < len(self.current_recipes):
            recipe = self.current_recipes[index]
            self._show_recipe_details_dialog(recipe)
    
    def _view_recipe_details_by_recipe(self, recipe: Dict[str, str]):
        """View details when recipe object is known"""
        self._show_recipe_details_dialog(recipe)
    
    def _confirm_delete_dialog(self, recipe: Dict[str, str]):
        """Show confirmation dialog before deleting a recipe"""
        name = recipe.get("Recipe Name", "")
        if not name:
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Delete")
        dialog.geometry("420x140")
        dialog.configure(fg_color="#1e1e1e")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        msg = ctk.CTkLabel(dialog, text=f"Delete recipe '{name}'?\nThis action cannot be undone.", wraplength=380, justify="left")
        msg.pack(pady=(20, 10), padx=20)
        
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(pady=(0, 10))
        
        yes_btn = ctk.CTkButton(
            buttons_frame,
            text="Yes, Delete",
            fg_color="#ff6b6b",
            hover_color="#e55555",
            command=lambda: (self._delete_recipe(recipe), dialog.destroy()),
            width=120
        )
        yes_btn.pack(side="left", padx=8)
        
        no_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            fg_color="#666666",
            hover_color="#555555",
            command=dialog.destroy,
            width=120
        )
        no_btn.pack(side="left", padx=8)
    
    def _delete_recipe(self, recipe: Dict[str, str]):
        """Delete recipe via DataHandler.delete_recipe if available, otherwise remove from in-memory list and refresh"""
        name = recipe.get("Recipe Name", "")
        if not name:
            self.status_label.configure(text="Invalid recipe selected")
            return
        try:
            deleted = False
            if hasattr(self.data_handler, "delete_recipe"):
                # DataHandler.delete_recipe(recipe_name) -> bool
                deleted = self.data_handler.delete_recipe(name)
            else:
                # Fallback: remove from current_recipes and attempt to persist via on_refresh_callback
                self.current_recipes = [r for r in self.current_recipes if r.get("Recipe Name") != name]
                deleted = True

            if not deleted:
                self.status_label.configure(text="Recipe not found or could not be deleted")
                return
        except Exception as e:
            # Report error in status label
            self.status_label.configure(text=f"Error deleting recipe: {e}")
            return

        # Refresh UI and notify parent
        self._refresh_recipes()
        if self.on_refresh_callback:
            try:
                self.on_refresh_callback()
            except Exception:
                pass
    
    def _show_recipe_details_dialog(self, recipe: Dict[str, str]):
        """Show detailed recipe costing dialog"""
        # Create details dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Recipe Details: {recipe.get('Recipe Name', '')}")
        dialog.geometry("600x700")
        dialog.configure(fg_color="#1e1e1e")
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.transient(self)
        dialog.grab_set()
        
        # Dialog content
        title_label = ctk.CTkLabel(
            dialog, 
            text=f"Recipe: {recipe.get('Recipe Name', '')}", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=(20, 30))
        
        # Cost breakdown section
        breakdown_frame = ctk.CTkFrame(dialog, fg_color="#2d2d2d", corner_radius=10)
        breakdown_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        breakdown_title = ctk.CTkLabel(
            breakdown_frame,
            text="Cost Breakdown",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        breakdown_title.pack(pady=(15, 20))
        
        # Cost details
        costs_frame = ctk.CTkFrame(breakdown_frame, fg_color="transparent")
        costs_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Row 1: Ingredient Cost
        row1 = ctk.CTkFrame(costs_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        ingredient_cost_label = ctk.CTkLabel(
            row1, 
            text="Total Ingredient Cost:", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        ingredient_cost_label.pack(side="left", padx=(0, 20))
        
        ingredient_cost_value = ctk.CTkLabel(
            row1, 
            text=f"${recipe.get('Total Ingredient Cost', '0.00')}", 
            font=ctk.CTkFont(size=14),
            text_color="#4cafef"
        )
        ingredient_cost_value.pack(side="right")
        
        # Row 2: Miscellaneous Cost
        row2 = ctk.CTkFrame(costs_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        misc_cost_label = ctk.CTkLabel(
            row2, 
            text="Miscellaneous Cost (50%):", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        misc_cost_label.pack(side="left", padx=(0, 20))
        
        misc_cost_value = ctk.CTkLabel(
            row2, 
            text=f"${recipe.get('Miscellaneous Cost (50%)', '0.00')}", 
            font=ctk.CTkFont(size=14),
            text_color="#ff9500"
        )
        misc_cost_value.pack(side="right")
        
        # Row 3: Labor Cost
        row3 = ctk.CTkFrame(costs_frame, fg_color="transparent")
        row3.pack(fill="x", pady=5)
        
        labor_cost_label = ctk.CTkLabel(
            row3, 
            text="Labor Cost (45%):", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        labor_cost_label.pack(side="left", padx=(0, 20))
        
        labor_cost_value = ctk.CTkLabel(
            row3, 
            text=f"${recipe.get('Labor Cost (45%)', '0.00')}", 
            font=ctk.CTkFont(size=14),
            text_color="#ff9500"
        )
        labor_cost_value.pack(side="right")
        
        # Row 4: Total Cost
        row4 = ctk.CTkFrame(costs_frame, fg_color="transparent")
        row4.pack(fill="x", pady=5)
        
        total_cost_label = ctk.CTkLabel(
            row4, 
            text="Total Cost:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        total_cost_label.pack(side="left", padx=(0, 20))
        
        total_cost_value = ctk.CTkLabel(
            row4, 
            text=f"${recipe.get('Total Cost', '0.00')}", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ff6b6b"
        )
        total_cost_value.pack(side="right")
        
        # Pricing section
        pricing_frame = ctk.CTkFrame(dialog, fg_color="#2d2d2d", corner_radius=10)
        pricing_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        pricing_title = ctk.CTkLabel(
            pricing_frame,
            text="Pricing Information",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        pricing_title.pack(pady=(15, 20))
        
        # Pricing details
        pricing_details_frame = ctk.CTkFrame(pricing_frame, fg_color="transparent")
        pricing_details_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Row 1: Selling Price
        price_row1 = ctk.CTkFrame(pricing_details_frame, fg_color="transparent")
        price_row1.pack(fill="x", pady=5)
        
        selling_price_label = ctk.CTkLabel(
            price_row1, 
            text="Suggested Selling Price:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        selling_price_label.pack(side="left", padx=(0, 20))
        
        selling_price_value = ctk.CTkLabel(
            price_row1, 
            text=f"${recipe.get('Suggested Selling Price', '0.00')}", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#28a745"
        )
        selling_price_value.pack(side="right")
        
        # Row 2: Margin Percentage (Target Margin)
        margin_row = ctk.CTkFrame(pricing_details_frame, fg_color="transparent")
        margin_row.pack(fill="x", pady=5)
        
        margin_label = ctk.CTkLabel(
            margin_row,
            text="Target Margin (%):",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        margin_label.pack(side="left", padx=(0, 20))
        
        # Support multiple header names for margin
        margin_raw = self._find_field(recipe, ["Margin Percentage", "Target Margin", "Margin %"])
        try:
            margin_val = float(str(margin_raw).replace('%', '').strip())
            margin_text = f"{margin_val:.0f}%"
        except Exception:
            margin_text = str(margin_raw) if margin_raw not in (None, "") else "N/A"
        
        margin_value = ctk.CTkLabel(
            margin_row,
            text=margin_text,
            font=ctk.CTkFont(size=14),
            text_color="#4cafef"
        )
        margin_value.pack(side="right")
        
        # Row 3: Profit
        price_row2 = ctk.CTkFrame(pricing_details_frame, fg_color="transparent")
        price_row2.pack(fill="x", pady=5)
        
        profit_label = ctk.CTkLabel(
            price_row2, 
            text="Profit:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        profit_label.pack(side="left", padx=(0, 20))
        
        profit_value = ctk.CTkLabel(
            price_row2, 
            text=f"${recipe.get('Profit', '0.00')}", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#28a745"
        )
        profit_value.pack(side="right")
        
        # Ingredients section
        ingredients_frame = ctk.CTkFrame(dialog, fg_color="#2d2d2d", corner_radius=10)
        ingredients_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ingredients_title = ctk.CTkLabel(
            ingredients_frame,
            text="Ingredients Used",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        ingredients_title.pack(pady=(15, 20))
        
        ingredients_text = ctk.CTkLabel(
            ingredients_frame,
            text=recipe.get("Ingredients Used", "No ingredients listed"),
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            wraplength=500
        )
        ingredients_text.pack(pady=(0, 20))
        
        # Close button
        close_button = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            fg_color="#666666",
            hover_color="#555555",
            font=ctk.CTkFont(size=16),
            height=40
        )
        close_button.pack(pady=(0, 20))
    
    def refresh_display(self):
        """Public method to refresh the display"""
        self._refresh_recipes()