import customtkinter as ctk
from typing import Callable, List, Dict
from core.data_handler import DataHandler
import tkinter.messagebox as messagebox

class IngredientsPage(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataHandler, refresh_callback: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_handler = data_handler
        self.refresh_callback = refresh_callback
        self.current_ingredients = []
        self.editing_index = None
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Changed from row 1 to row 0
        
        self._create_widgets()
        self._setup_layout()
        self.refresh_ingredients()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable.grid_columnconfigure(0, weight=1) # Ensure content expands horizontally
        
        # Add ingredient section
        self.add_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.add_title = ctk.CTkLabel(
            self.add_section,
            text="➕ Add New Ingredient",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4cafef"
        )
        
        # Form fields
        self.form_frame = ctk.CTkFrame(self.add_section, fg_color="transparent")
        
        # Row 1: Name and Price
        self.name_label = ctk.CTkLabel(self.form_frame, text="Ingredient Name:", text_color="#ffffff")
        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g., Flour, Sugar, Eggs...")
        
        self.price_label = ctk.CTkLabel(self.form_frame, text="Price (₱):", text_color="#ffffff")
        self.price_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g., 45.50")
        
        # Row 2: Grams and Grams Needed
        self.grams_label = ctk.CTkLabel(self.form_frame, text="Total Grams:", text_color="#ffffff")
        self.grams_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g., 1000 (1kg)")
        
        self.grams_needed_label = ctk.CTkLabel(self.form_frame, text="Grams per Recipe:", text_color="#ffffff")
        self.grams_needed_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g., 250")
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.add_section, fg_color="transparent")
        
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="💾 Save Ingredient",
            command=self._add_ingredient,
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45
        )
        
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="🗑️ Clear Form",
            command=self._clear_fields,
            fg_color="#666666",
            hover_color="#555555",
            font=ctk.CTkFont(size=16),
            height=45
        )
        
        self.cancel_edit_button = ctk.CTkButton(
            self.button_frame,
            text="❌ Cancel Edit",
            command=self._cancel_edit,
            fg_color="#ff6b6b",
            hover_color="#e55555",
            font=ctk.CTkFont(size=16),
            height=45
        )
        
        # Search section
        self.search_frame = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.search_label = ctk.CTkLabel(
            self.search_frame,
            text="🔍 Search Ingredients",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Type to search ingredients...",
            height=40
        )
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Ingredients list section
        self.list_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.list_title = ctk.CTkLabel(
            self.list_section,
            text="📋 Ingredients Database",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        # Ingredients container
        self.ingredients_container = ctk.CTkFrame(
            self.list_section,
            fg_color="transparent"
        )
    
    def _setup_layout(self):
        # Main scrollable
        self.main_scrollable.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Add section layout
        self.add_section.pack(fill="x", padx=0, pady=(0, 20))
        self.add_title.pack(pady=(20, 20))
        
        # Form layout
        self.form_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(3, weight=1)
        
        # Row 1
        self.name_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        self.name_entry.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        self.price_label.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="w")
        self.price_entry.grid(row=0, column=3, padx=(0, 0), pady=10, sticky="ew")
        
        # Row 2
        self.grams_label.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        self.grams_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        self.grams_needed_label.grid(row=1, column=2, padx=(0, 10), pady=10, sticky="w")
        self.grams_needed_entry.grid(row=1, column=3, padx=(0, 0), pady=10, sticky="ew")
        
        # Button layout
        self.button_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        
        self.add_button.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")
        self.clear_button.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        self.cancel_edit_button.grid(row=0, column=2, padx=(0, 0), pady=10, sticky="ew")
        
        # Initially hide cancel edit button
        self.cancel_edit_button.grid_remove()
        
        # Search section layout
        self.search_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.search_label.pack(pady=(20, 15))
        self.search_entry.pack(fill="x", padx=30, pady=(0, 20))
        
        # List section layout
        self.list_section.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.list_title.pack(pady=(20, 15))
        self.ingredients_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
    
    def _add_ingredient(self):
        """Add or update ingredient"""
        try:
            # Get form data
            name = self.name_entry.get().strip()
            price = self.price_entry.get().strip()
            grams = self.grams_entry.get().strip()
            grams_needed = self.grams_needed_entry.get().strip()
            
            # Validate inputs
            if not all([name, price, grams, grams_needed]):
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            try:
                price = float(price)
                grams = float(grams)
                grams_needed = float(grams_needed)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and grams!")
                return
            
            if price <= 0 or grams <= 0 or grams_needed <= 0:
                messagebox.showerror("Error", "All values must be greater than zero!")
                return
            
            # Prepare ingredient data
            ingredient_data = {
                "Ingredient Name": name,
                "Price": price,
                "Grams": grams,
                "Grams Needed in Recipe": grams_needed
            }
            
            if self.editing_index is not None:
                # Update existing ingredient
                success = self.data_handler.update_ingredient(self.editing_index, ingredient_data)
                if success:
                    messagebox.showinfo("Success", f"Updated ingredient: {name}")
                    self._cancel_edit()
                else:
                    messagebox.showerror("Error", "Failed to update ingredient!")
            else:
                # Add new ingredient
                success = self.data_handler.add_ingredient(ingredient_data)
                if success:
                    messagebox.showinfo("Success", f"Added ingredient: {name}")
                    self._clear_fields()
                else:
                    messagebox.showerror("Error", "Failed to add ingredient!")
            
            self.refresh_ingredients()
            if self.refresh_callback:
                self.refresh_callback()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _clear_fields(self):
        """Clear all form fields"""
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.grams_entry.delete(0, "end")
        self.grams_needed_entry.delete(0, "end")
        self.editing_index = None
        self.add_button.configure(text="💾 Save Ingredient")
        self.cancel_edit_button.grid_remove()
    
    def _cancel_edit(self):
        """Cancel editing mode"""
        self._clear_fields()
    
    def _edit_ingredient(self, index: int):
        """Edit ingredient at specified index"""
        if 0 <= index < len(self.current_ingredients):
            ingredient = self.current_ingredients[index]
            
            # Fill form with ingredient data
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, ingredient.get("Ingredient Name", ""))
            
            self.price_entry.delete(0, "end")
            self.price_entry.insert(0, ingredient.get("Price", ""))
            
            self.grams_entry.delete(0, "end")
            self.grams_entry.insert(0, ingredient.get("Grams", ""))
            
            self.grams_needed_entry.delete(0, "end")
            self.grams_needed_entry.insert(0, ingredient.get("Grams Needed in Recipe", ""))
            
            # Set editing mode
            self.editing_index = index
            self.add_button.configure(text="💾 Update Ingredient")
            self.cancel_edit_button.grid()
    
    def _delete_ingredient(self, index: int):
        """Delete ingredient at specified index"""
        if 0 <= index < len(self.current_ingredients):
            ingredient_name = self.current_ingredients[index].get("Ingredient Name", "")
            
            result = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{ingredient_name}'?"
            )
            
            if result:
                success = self.data_handler.delete_ingredient(index)
                if success:
                    messagebox.showinfo("Success", f"Deleted ingredient: {ingredient_name}")
                    self.refresh_ingredients()
                    if self.refresh_callback:
                        self.refresh_callback()
                else:
                    messagebox.showerror("Error", "Failed to delete ingredient!")
    
    def _on_search(self, event=None):
        """Handle search input"""
        query = self.search_entry.get().strip()
        if query:
            ingredients = self.data_handler.search_ingredients(query)
        else:
            ingredients = self.data_handler.get_all_ingredients()
        
        self._display_ingredients(ingredients)
    
    def refresh_ingredients(self):
        """Refresh ingredients list"""
        self.current_ingredients = self.data_handler.get_all_ingredients()
        self._display_ingredients(self.current_ingredients)
    
    def _display_ingredients(self, ingredients: List[Dict[str, str]]):
        """Display ingredients in the container"""
        # Clear existing widgets
        for widget in self.ingredients_container.winfo_children():
            widget.destroy()
        
        if not ingredients:
            # Show empty state
            empty_label = ctk.CTkLabel(
                self.ingredients_container,
                text="No ingredients found. Add your first ingredient above!",
                font=ctk.CTkFont(size=16),
                text_color="#888888"
            )
            empty_label.pack(pady=50)
            return
        
        # Create ingredient cards
        for i, ingredient in enumerate(ingredients):
            card = self._create_ingredient_card(ingredient, i)
            card.pack(fill="x", pady=(0, 10))
    
    def _create_ingredient_card(self, ingredient: Dict[str, str], index: int):
        """Create a card for displaying ingredient information"""
        card = ctk.CTkFrame(self.ingredients_container, fg_color="#3d3d3d", corner_radius=10)
        
        # Main content frame
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        # Left side - ingredient info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=ingredient.get("Ingredient Name", ""),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        name_label.pack(anchor="w")
        
        details_text = f"Price: ₱{ingredient.get('Price', '0')} | Total: {ingredient.get('Grams', '0')}g | Per Recipe: {ingredient.get('Grams Needed in Recipe', '0')}g"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=ctk.CTkFont(size=14),
            text_color="#cccccc"
        )
        details_label.pack(anchor="w", pady=(5, 0))
        
        # Right side - action buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=(20, 0))
        
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Edit",
            command=lambda idx=index: self._edit_ingredient(idx),
            fg_color="#ff9500",
            hover_color="#e6850e",
            font=ctk.CTkFont(size=14),
            width=80,
            height=35
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            command=lambda idx=index: self._delete_ingredient(idx),
            fg_color="#ff6b6b",
            hover_color="#e55555",
            font=ctk.CTkFont(size=14),
            width=80,
            height=35
        )
        delete_btn.pack(side="left")
        
        return card
