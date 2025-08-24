import customtkinter as ctk
from typing import Callable, List, Dict
from data_handler import DataHandler

class IngredientsFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataHandler, on_refresh_callback: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_handler = data_handler
        self.on_refresh_callback = on_refresh_callback
        self.current_ingredients = []
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self._setup_layout()
        self._refresh_ingredients()
    
    def _create_widgets(self):
        # Main card container
        self.card = ctk.CTkFrame(self, corner_radius=15, fg_color="#2d2d2d")
        self.card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Card title
        self.title_label = ctk.CTkLabel(
            self.card, 
            text="Ingredients Management", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        
        # Add ingredient section
        self.add_section = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.add_title = ctk.CTkLabel(
            self.add_section,
            text="Add New Ingredient",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        # Input fields
        self.name_label = ctk.CTkLabel(self.add_section, text="Ingredient Name:", text_color="#ffffff")
        self.name_entry = ctk.CTkEntry(self.add_section, placeholder_text="Enter ingredient name")
        
        self.price_label = ctk.CTkLabel(self.add_section, text="Price ($):", text_color="#ffffff")
        self.price_entry = ctk.CTkEntry(self.add_section, placeholder_text="Enter price")
        
        self.grams_label = ctk.CTkLabel(self.add_section, text="Grams:", text_color="#ffffff")
        self.grams_entry = ctk.CTkEntry(self.add_section, placeholder_text="Enter grams")
        
        self.grams_needed_label = ctk.CTkLabel(self.add_section, text="Grams Needed in Recipe:", text_color="#ffffff")
        self.grams_needed_entry = ctk.CTkEntry(self.add_section, placeholder_text="Enter grams needed")
        
        # Buttons
        self.add_button = ctk.CTkButton(
            self.add_section,
            text="Add Ingredient",
            command=self._add_ingredient,
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.clear_button = ctk.CTkButton(
            self.add_section,
            text="Clear",
            command=self._clear_fields,
            fg_color="#666666",
            hover_color="#555555",
            font=ctk.CTkFont(size=16)
        )
        
        # Search section
        self.search_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search:", text_color="#ffffff")
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Search by ingredient name...",
            width=300
        )
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Ingredients table frame
        self.table_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        
        # Table headers
        self.headers_frame = ctk.CTkFrame(self.table_frame, fg_color="#3d3d3d")
        self._create_table_headers()
        
        # Ingredients scrollable frame
        self.ingredients_container = ctk.CTkScrollableFrame(
            self.table_frame,
            fg_color="transparent",
            height=300
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
        headers = ["Ingredient Name", "Price ($)", "Grams", "Price/Gram", "Grams Needed", "Cost/Recipe", "Actions"]
        widths = [150, 80, 80, 100, 120, 100, 120]
        
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
        
        # Add ingredient section - reduced padding
        self.add_section.grid(row=1, column=0, pady=(0, 15), sticky="ew", padx=15)
        self.add_section.grid_columnconfigure(0, weight=1)
        self.add_section.grid_columnconfigure(1, weight=1)
        
        self.add_title.grid(row=0, column=0, columnspan=2, pady=(10, 15))
        
        # Row 1: Name and Price - reduced padding
        self.name_label.grid(row=1, column=0, padx=(15, 8), pady=(0, 3), sticky="w")
        self.name_entry.grid(row=1, column=0, padx=(15, 8), pady=(0, 10), sticky="ew")
        
        self.price_label.grid(row=1, column=1, padx=(8, 15), pady=(0, 3), sticky="w")
        self.price_entry.grid(row=1, column=1, padx=(8, 15), pady=(0, 10), sticky="ew")
        
        # Row 2: Grams and Grams Needed - reduced padding
        self.grams_label.grid(row=2, column=0, padx=(15, 8), pady=(0, 3), sticky="w")
        self.grams_entry.grid(row=2, column=0, padx=(15, 8), pady=(0, 10), sticky="ew")
        
        self.grams_needed_label.grid(row=2, column=1, padx=(8, 15), pady=(0, 3), sticky="w")
        self.grams_needed_entry.grid(row=2, column=1, padx=(8, 15), pady=(0, 10), sticky="ew")
        
        # Row 3: Buttons - reduced padding
        self.add_button.grid(row=3, column=0, padx=(15, 8), pady=(0, 15), sticky="ew")
        self.clear_button.grid(row=3, column=1, padx=(8, 15), pady=(0, 15), sticky="ew")
        
        # Search section - reduced padding
        self.search_frame.grid(row=2, column=0, pady=(0, 15), sticky="ew", padx=15)
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_label.grid(row=0, column=0, padx=(15, 8), pady=8)
        self.search_entry.grid(row=0, column=1, padx=(0, 15), pady=8, sticky="ew")
        
        # Table section - reduced padding
        self.table_frame.grid(row=3, column=0, pady=(0, 15), sticky="nsew", padx=15)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # Headers
        self.headers_frame.grid(row=0, column=0, sticky="ew", padx=15)
        
        # Ingredients container - reduced padding
        self.ingredients_container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(8, 0))
        
        # Status - reduced padding
        self.status_label.grid(row=4, column=0, pady=(0, 15))
    
    def _add_ingredient(self):
        """Add a new ingredient"""
        # Get values from entries
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        grams = self.grams_entry.get().strip()
        grams_needed = self.grams_needed_entry.get().strip()
        
        # Validate inputs
        if not all([name, price, grams, grams_needed]):
            self._show_status("Please fill in all fields", error=True)
            return
        
        try:
            # Validate numeric fields
            float(price)
            float(grams)
            float(grams_needed)
        except ValueError:
            self._show_status("Price, Grams, and Grams Needed must be valid numbers", error=True)
            return
        
        # Prepare ingredient data
        ingredient_data = {
            "Ingredient Name": name,
            "Price": price,
            "Grams": grams,
            "Grams Needed in Recipe": grams_needed
        }
        
        # Save to CSV
        if self.data_handler.add_ingredient(ingredient_data):
            self._show_status("Ingredient added successfully!", error=False)
            self._clear_fields()
            self._refresh_ingredients()
            if self.on_refresh_callback:
                self.on_refresh_callback()
        else:
            self._show_status("Error adding ingredient. Please try again.", error=True)
    
    def _clear_fields(self):
        """Clear all input fields"""
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.grams_entry.delete(0, "end")
        self.grams_needed_entry.delete(0, "end")
        self.status_label.configure(text="")
    
    def _refresh_ingredients(self):
        """Refresh the ingredients display"""
        # Clear existing ingredients
        for widget in self.ingredients_container.winfo_children():
            widget.destroy()
        
        # Get ingredients from data handler
        self.current_ingredients = self.data_handler.get_all_ingredients()
        
        # Create ingredient rows
        for i, ingredient in enumerate(self.current_ingredients):
            self._create_ingredient_row(i, ingredient)
    
    def _create_ingredient_row(self, index: int, ingredient: Dict[str, str]):
        """Create a row for an ingredient in the table"""
        row_frame = ctk.CTkFrame(self.ingredients_container, fg_color="#3d3d3d")
        row_frame.grid(row=index, column=0, sticky="ew", pady=1)  # Reduced pady from 2 to 1
        
        # Configure column weights for consistent alignment with headers
        widths = [150, 80, 80, 100, 120, 100, 120]
        for i in range(len(widths)):
            row_frame.grid_columnconfigure(i, weight=0, minsize=widths[i])
        
        # Ingredient data labels
        labels = [
            ingredient.get("Ingredient Name", ""),
            f"${ingredient.get('Price', '0.00')}",
            ingredient.get("Grams", ""),
            f"${ingredient.get('Price per Gram', '0.0000')}",
            ingredient.get("Grams Needed in Recipe", ""),
            f"${ingredient.get('Cost per Recipe', '0.00')}"
        ]
        
        for i, (label, width) in enumerate(zip(labels, widths[:-1])):  # Exclude Actions column
            label_widget = ctk.CTkLabel(
                row_frame,
                text=label,
                text_color="#ffffff",
                width=width
            )
            label_widget.grid(row=0, column=i, padx=5, pady=6, sticky="w")  # Reduced pady from 8 to 6
        
        # Action buttons
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=6, padx=5, pady=4)  # Reduced pady from 5 to 4
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            command=lambda idx=index: self._edit_ingredient(idx),
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            width=50,
            height=28,  # Reduced height from 30 to 28
            font=ctk.CTkFont(size=12)
        )
        edit_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Delete",
            command=lambda idx=index: self._delete_ingredient(idx),
            fg_color="#ff6b6b",
            hover_color="#e55555",
            width=50,
            height=28,  # Reduced height from 30 to 28
            font=ctk.CTkFont(size=12)
        )
        delete_btn.pack(side="left", padx=2)
    
    def _on_search(self, event=None):
        """Handle search input changes"""
        query = self.search_entry.get().strip()
        filtered_ingredients = self.data_handler.search_ingredients(query)
        
        # Clear existing ingredients
        for widget in self.ingredients_container.winfo_children():
            widget.destroy()
        
        # Display filtered ingredients
        self.current_ingredients = filtered_ingredients
        for i, ingredient in enumerate(filtered_ingredients):
            self._create_ingredient_row(i, ingredient)
    
    def _edit_ingredient(self, index: int):
        """Open edit dialog for ingredient at index"""
        if 0 <= index < len(self.current_ingredients):
            ingredient = self.current_ingredients[index]
            self._show_edit_dialog(index, ingredient)
    
    def _show_edit_dialog(self, index: int, ingredient: Dict[str, str]):
        """Show edit dialog for an ingredient"""
        # Create edit dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Ingredient")
        dialog.geometry("400x500")
        dialog.configure(fg_color="#1e1e1e")
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.transient(self)
        dialog.grab_set()
        
        # Dialog content
        title_label = ctk.CTkLabel(
            dialog, 
            text="Edit Ingredient", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=(20, 30))
        
        # Input fields
        fields_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20)
        
        # Ingredient Name
        name_label = ctk.CTkLabel(fields_frame, text="Ingredient Name:", text_color="#ffffff")
        name_label.pack(anchor="w", pady=(0, 5))
        name_entry = ctk.CTkEntry(fields_frame, width=350)
        name_entry.insert(0, ingredient.get("Ingredient Name", ""))
        name_entry.pack(fill="x", pady=(0, 15))
        
        # Price
        price_label = ctk.CTkLabel(fields_frame, text="Price ($):", text_color="#ffffff")
        price_label.pack(anchor="w", pady=(0, 5))
        price_entry = ctk.CTkEntry(fields_frame, width=350)
        price_entry.insert(0, ingredient.get("Price", ""))
        price_entry.pack(fill="x", pady=(0, 15))
        
        # Grams
        grams_label = ctk.CTkLabel(fields_frame, text="Grams:", text_color="#ffffff")
        grams_label.pack(anchor="w", pady=(0, 5))
        grams_entry = ctk.CTkEntry(fields_frame, width=350)
        grams_entry.insert(0, ingredient.get("Grams", ""))
        grams_entry.pack(fill="x", pady=(0, 15))
        
        # Grams Needed in Recipe
        grams_needed_label = ctk.CTkLabel(fields_frame, text="Grams Needed in Recipe:", text_color="#ffffff")
        grams_needed_label.pack(anchor="w", pady=(0, 5))
        grams_needed_entry = ctk.CTkEntry(fields_frame, width=350)
        grams_needed_entry.insert(0, ingredient.get("Grams Needed in Recipe", ""))
        grams_needed_entry.pack(fill="x", pady=(0, 30))
        
        # Buttons
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save",
            command=lambda: self._save_edit(
                dialog, index, {
                    "Ingredient Name": name_entry.get(),
                    "Price": price_entry.get(),
                    "Grams": grams_entry.get(),
                    "Grams Needed in Recipe": grams_needed_entry.get()
                }
            ),
            fg_color="#4cafef",
            hover_color="#3d8bc0"
        )
        save_btn.pack(side="left", padx=(0, 10), expand=True)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="#666666",
            hover_color="#555555"
        )
        cancel_btn.pack(side="right", expand=True)
    
    def _save_edit(self, dialog, index: int, ingredient_data: Dict[str, str]):
        """Save edited ingredient data"""
        # Validate inputs
        if not all([ingredient_data["Ingredient Name"], ingredient_data["Price"], 
                   ingredient_data["Grams"], ingredient_data["Grams Needed in Recipe"]]):
            return
        
        try:
            float(ingredient_data["Price"])
            float(ingredient_data["Grams"])
            float(ingredient_data["Grams Needed in Recipe"])
        except ValueError:
            return
        
        # Update ingredient
        if self.data_handler.update_ingredient(index, ingredient_data):
            dialog.destroy()
            self._refresh_ingredients()
            self._show_status("Ingredient updated successfully!", error=False)
            if self.on_refresh_callback:
                self.on_refresh_callback()
        else:
            self._show_status("Error updating ingredient", error=True)
    
    def _delete_ingredient(self, index: int):
        """Delete ingredient at index"""
        if 0 <= index < len(self.current_ingredients):
            ingredient_name = self.current_ingredients[index].get("Ingredient Name", "")
            
            # Confirm deletion
            if self._confirm_delete(ingredient_name):
                if self.data_handler.delete_ingredient(index):
                    self._refresh_ingredients()
                    self._show_status(f"'{ingredient_name}' deleted successfully!", error=False)
                    if self.on_refresh_callback:
                        self.on_refresh_callback()
                else:
                    self._show_status("Error deleting ingredient", error=True)
    
    def _confirm_delete(self, ingredient_name: str) -> bool:
        """Show confirmation dialog for deletion"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Delete")
        dialog.geometry("300x150")
        dialog.configure(fg_color="#1e1e1e")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Dialog content
        message = ctk.CTkLabel(
            dialog,
            text=f"Are you sure you want to delete\n'{ingredient_name}'?",
            text_color="#ffffff",
            font=ctk.CTkFont(size=14)
        )
        message.pack(pady=(20, 20))
        
        result = [False]  # Use list to store result
        
        def confirm():
            result[0] = True
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        # Buttons
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Delete",
            command=confirm,
            fg_color="#ff6b6b",
            hover_color="#e55555"
        )
        confirm_btn.pack(side="left", padx=(0, 10), expand=True)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=cancel,
            fg_color="#666666",
            hover_color="#555555"
        )
        cancel_btn.pack(side="right", expand=True)
        
        # Wait for dialog to close
        dialog.wait_window()
        return result[0]
    
    def _show_status(self, message: str, error: bool = False):
        """Show status message"""
        color = "#ff6b6b" if error else "#4cafef"
        self.status_label.configure(text=message, text_color=color)
        
        # Clear status after 3 seconds
        self.after(3000, lambda: self.status_label.configure(text=""))
