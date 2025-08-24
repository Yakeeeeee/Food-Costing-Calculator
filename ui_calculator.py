import customtkinter as ctk
from typing import Callable, List, Dict
from data_handler import DataHandler

class CalculatorFrame(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataHandler, on_refresh_callback: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_handler = data_handler
        self.on_refresh_callback = on_refresh_callback
        self.selected_ingredients = []
        self.all_ingredients = []
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self._setup_layout()
        self._refresh_ingredients()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Main card container
        self.card = ctk.CTkFrame(self.main_scrollable, corner_radius=15, fg_color="#2d2d2d")
        self.card.pack(fill="x", padx=20, pady=20)
        
        # Card title
        self.title_label = ctk.CTkLabel(
            self.card, 
            text="Food Costing Calculator", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        
        # Recipe name section
        self.recipe_section = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.recipe_title = ctk.CTkLabel(
            self.recipe_section,
            text="Recipe Information",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.recipe_name_label = ctk.CTkLabel(self.recipe_section, text="Recipe Name:", text_color="#ffffff")
        self.recipe_name_entry = ctk.CTkEntry(self.recipe_section, placeholder_text="Enter recipe name")
        
        # Target margin percentage
        self.margin_label = ctk.CTkLabel(self.recipe_section, text="Target Margin (%):", text_color="#ffffff")
        self.margin_entry = ctk.CTkEntry(self.recipe_section, placeholder_text="150")
        self.margin_note = ctk.CTkLabel(
            self.recipe_section, 
            text="(e.g., 150 = 2.5x markup, 100 = 2x markup)", 
            text_color="#cccccc",
            font=ctk.CTkFont(size=12)
        )
        
        # Ingredients selection section
        self.ingredients_section = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.ingredients_title = ctk.CTkLabel(
            self.ingredients_section,
            text="Select Ingredients",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        # Search ingredients section
        self.search_frame = ctk.CTkFrame(self.ingredients_section, fg_color="transparent")
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search:", text_color="#ffffff")
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Search ingredients...",
            width=300
        )
        self.search_entry.bind("<KeyRelease>", self._on_search_ingredients)
        
        # Ingredients checklist frame
        self.checklist_frame = ctk.CTkFrame(self.ingredients_section, fg_color="#2d2d2d")
        self.checklist_container = ctk.CTkScrollableFrame(
            self.checklist_frame,
            fg_color="transparent",
            height=200
        )
        
        # Add new ingredient section
        self.add_ingredient_section = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.add_ingredient_title = ctk.CTkLabel(
            self.add_ingredient_section,
            text="Add New Ingredient (if not in system)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        
        # Create a frame for the 2x2 grid layout
        self.fields_frame = ctk.CTkFrame(self.add_ingredient_section, fg_color="transparent")
        
        # Left column frame
        self.left_column = ctk.CTkFrame(self.fields_frame, fg_color="transparent")
        
        # Right column frame
        self.right_column = ctk.CTkFrame(self.fields_frame, fg_color="transparent")
        
        # New ingredient fields - Left column
        self.new_name_label = ctk.CTkLabel(self.left_column, text="Name:", text_color="#ffffff")
        self.new_name_entry = ctk.CTkEntry(self.left_column, placeholder_text="Ingredient name")
        
        self.new_grams_label = ctk.CTkLabel(self.left_column, text="Grams:", text_color="#ffffff")
        self.new_grams_entry = ctk.CTkEntry(self.left_column, placeholder_text="Total grams")
        
        # New ingredient fields - Right column
        self.new_price_label = ctk.CTkLabel(self.right_column, text="Price ($):", text_color="#ffffff")
        self.new_price_entry = ctk.CTkEntry(self.right_column, placeholder_text="Price")
        
        self.new_grams_needed_label = ctk.CTkLabel(self.right_column, text="Grams Needed:", text_color="#ffffff")
        self.new_grams_needed_entry = ctk.CTkEntry(self.right_column, placeholder_text="Grams for recipe")
        
        self.add_new_ingredient_btn = ctk.CTkButton(
            self.add_ingredient_section,
            text="Add to Recipe",
            command=self._add_new_ingredient_to_recipe,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=14)
        )
        
        # Cost breakdown section
        self.breakdown_section = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.breakdown_title = ctk.CTkLabel(
            self.breakdown_section,
            text="Cost Breakdown",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        # Breakdown display
        self.breakdown_display = ctk.CTkFrame(self.breakdown_section, fg_color="#2d2d2d")
        self.breakdown_container = ctk.CTkScrollableFrame(
            self.breakdown_display,
            fg_color="transparent",
            height=150
        )
        
        # Total cost section
        self.total_frame = ctk.CTkFrame(self.card, fg_color="#4cafef")
        self.total_label = ctk.CTkLabel(
            self.total_frame,
            text="Total Cost: $0.00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        # Action buttons
        self.buttons_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.calculate_button = ctk.CTkButton(
            self.buttons_frame,
            text="Calculate Cost",
            command=self._calculate_cost,
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.calculate_save_button = ctk.CTkButton(
            self.buttons_frame,
            text="Calculate & Save Recipe",
            command=self._calculate_and_save,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.clear_button = ctk.CTkButton(
            self.buttons_frame,
            text="Clear All",
            command=self._clear_all,
            fg_color="#666666",
            hover_color="#555555",
            font=ctk.CTkFont(size=16)
        )
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.card,
            text="",
            text_color="#4cafef",
            font=ctk.CTkFont(size=14)
        )
    
    def _setup_layout(self):
        # Configure main scrollable frame
        self.main_scrollable.grid_columnconfigure(0, weight=1)
        
        # Configure card grid
        self.card.grid_columnconfigure(0, weight=1)
        
        # Title - reduced padding
        self.title_label.pack(pady=(15, 15))
        
        # Recipe name section - reduced padding
        self.recipe_section.pack(fill="x", padx=15, pady=(0, 15))
        self.recipe_title.pack(pady=(10, 10))
        self.recipe_name_label.pack(anchor="w", padx=15, pady=(0, 3))
        self.recipe_name_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Target margin percentage - reduced padding
        self.margin_label.pack(anchor="w", padx=15, pady=(0, 3))
        self.margin_entry.pack(fill="x", padx=15, pady=(0, 10))
        self.margin_note.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Ingredients selection section - reduced padding
        self.ingredients_section.pack(fill="x", padx=15, pady=(0, 15))
        self.ingredients_title.pack(pady=(10, 10))
        
        # Search section - reduced padding
        self.search_frame.pack(fill="x", padx=15, pady=(0, 10))
        self.search_label.pack(side="left", padx=(0, 8))
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # Checklist frame - reduced padding
        self.checklist_frame.pack(fill="x", padx=15, pady=(0, 10))
        self.checklist_container.pack(fill="x", padx=8, pady=8)
        
        # Add new ingredient section - reduced padding
        self.add_ingredient_section.pack(fill="x", padx=15, pady=(0, 15))
        self.add_ingredient_title.pack(pady=(10, 10))
        
        # Pack the fields frame
        self.fields_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Pack left and right columns side by side
        self.left_column.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.right_column.pack(side="right", fill="x", expand=True, padx=(8, 0))
        
        # Left column: Name and Grams - reduced padding
        self.new_name_label.pack(anchor="w", pady=(0, 3))
        self.new_name_entry.pack(fill="x", pady=(0, 8))
        
        self.new_grams_label.pack(anchor="w", pady=(0, 3))
        self.new_grams_entry.pack(fill="x", pady=(0, 8))
        
        # Right column: Price and Grams Needed - reduced padding
        self.new_price_label.pack(anchor="w", pady=(0, 3))
        self.new_price_entry.pack(fill="x", pady=(0, 8))
        
        self.new_grams_needed_label.pack(anchor="w", pady=(0, 3))
        self.new_grams_needed_entry.pack(fill="x", pady=(0, 8))
        
        # Add button - reduced padding
        self.add_new_ingredient_btn.pack(pady=(0, 10))
        
        # Cost breakdown section - reduced padding
        self.breakdown_section.pack(fill="x", padx=15, pady=(0, 15))
        self.breakdown_title.pack(pady=(10, 10))
        self.breakdown_display.pack(fill="x", padx=15, pady=(0, 10))
        self.breakdown_container.pack(fill="x", padx=8, pady=8)
        
        # Total cost section - reduced padding
        self.total_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.total_label.pack(pady=10)
        
        # Action buttons - reduced padding
        self.buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)
        self.buttons_frame.grid_columnconfigure(2, weight=1)
        
        self.calculate_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.calculate_save_button.grid(row=0, column=1, padx=4, sticky="ew")
        self.clear_button.grid(row=0, column=2, padx=(8, 0), sticky="ew")
        
        # Status - reduced padding
        self.status_label.pack(pady=(0, 15))
    
    def _refresh_ingredients(self):
        """Refresh the ingredients checklist"""
        self.all_ingredients = self.data_handler.get_all_ingredients()
        self._update_checklist()
    
    def _on_search_ingredients(self, event=None):
        """Handle search input changes for ingredients"""
        query = self.search_entry.get().strip().lower()
        
        # Clear existing checkboxes
        for widget in self.checklist_container.winfo_children():
            widget.destroy()
        
        # Filter ingredients based on search query
        if query:
            filtered_ingredients = [
                ing for ing in self.all_ingredients 
                if query in ing.get("Ingredient Name", "").lower()
            ]
        else:
            filtered_ingredients = self.all_ingredients
        
        # Create checkboxes for filtered ingredients
        for i, ingredient in enumerate(filtered_ingredients):
            # compute global index by matching name (safer when filtering)
            try:
                global_index = next(idx for idx, ing in enumerate(self.all_ingredients) if ing.get("Ingredient Name") == ingredient.get("Ingredient Name"))
            except StopIteration:
                global_index = i
            self._create_ingredient_checkbox(i, ingredient, global_index=global_index)
    
    def _update_checklist(self):
        """Update the ingredients checklist display"""
        # Clear existing checkboxes
        for widget in self.checklist_container.winfo_children():
            widget.destroy()
        
        # Create checkboxes for each ingredient
        for i, ingredient in enumerate(self.all_ingredients):
            self._create_ingredient_checkbox(i, ingredient, global_index=i)
    
    def _create_ingredient_checkbox(self, index: int, ingredient: Dict[str, str], global_index: int = None):
        """Create a checkbox for an ingredient"""
        checkbox_frame = ctk.CTkFrame(self.checklist_container, fg_color="transparent")
        checkbox_frame.pack(fill="x", pady=2)
        
        # Determine global index (index into self.all_ingredients) if not provided
        if global_index is None:
            try:
                global_index = next(idx for idx, ing in enumerate(self.all_ingredients) if ing.get("Ingredient Name") == ingredient.get("Ingredient Name"))
            except StopIteration:
                global_index = index
        
        # Checkbox
        var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="",
            variable=var,
            command=lambda idx=global_index, checked=var: self._on_ingredient_selection(idx, checked.get()),
            fg_color="#4cafef",
            hover_color="#3d8bc0"
        )
        checkbox.pack(side="left", padx=(0, 10))
        
        # Ingredient cost text: support multiple possible keys, fall back to '0.00'
        cost_val = ingredient.get('Cost per Recipe') or ingredient.get('Cost per recipe') or ingredient.get('Price') or ingredient.get('Cost') or "0.00"
        try:
            # normalize to two decimals if numeric string/number
            cost_str = f"{float(cost_val):.2f}"
        except Exception:
            cost_str = str(cost_val)
        
        # Ingredient info
        ingredient_text = f"{ingredient.get('Ingredient Name', '')} - ${cost_str} per recipe"
        ingredient_label = ctk.CTkLabel(
            checkbox_frame,
            text=ingredient_text,
            text_color="#ffffff"
        )
        ingredient_label.pack(side="left", fill="x", expand=True)
        
        # Store reference to checkbox variable and global index for later clearing or state checks
        checkbox_frame.var = var
        checkbox_frame.index = global_index
        checkbox_frame.ingredient_name = ingredient.get("Ingredient Name")
    
    def _on_ingredient_selection(self, index: int, selected: bool):
        """Handle ingredient selection/deselection"""
        # Always store actual ingredient dicts in selected_ingredients so DataHandler receives expected shape.
        if selected:
            if 0 <= index < len(self.all_ingredients):
                ingredient = self.all_ingredients[index]
                name = ingredient.get("Ingredient Name", "")
                if not any(ing.get("Ingredient Name", "") == name for ing in self.selected_ingredients):
                    self.selected_ingredients.append(ingredient)
        else:
            # remove by ingredient name (safe across filtered lists)
            if 0 <= index < len(self.all_ingredients):
                name = self.all_ingredients[index].get("Ingredient Name", "")
                self.selected_ingredients = [ing for ing in self.selected_ingredients if ing.get("Ingredient Name", "") != name]
    
    def _add_new_ingredient_to_recipe(self):
        """Add a new ingredient to the recipe"""
        # Get values from entries
        name = self.new_name_entry.get().strip()
        price = self.new_price_entry.get().strip()
        grams = self.new_grams_entry.get().strip()
        grams_needed = self.new_grams_needed_entry.get().strip()
        
        # Validate inputs
        if not all([name, price, grams, grams_needed]):
            self._show_status("Please fill in all fields for new ingredient", error=True)
            return
        
        try:
            # Validate numeric fields
            float(price)
            float(grams)
            float(grams_needed)
        except ValueError:
            self._show_status("Price, Grams, and Grams Needed must be valid numbers", error=True)
            return
        
        # Calculate price per gram and cost per recipe
        price_per_gram = float(price) / float(grams)
        cost_per_recipe = price_per_gram * float(grams_needed)
        
        # Create ingredient data
        ingredient_data = {
            "Ingredient Name": name,
            "Price": price,
            "Grams": grams,
            "Price per Gram": round(price_per_gram, 4),
            "Grams Needed in Recipe": grams_needed,
            "Cost per Recipe": round(cost_per_recipe, 2)
        }
        
        # Add to selected ingredients (store raw dict so calculator reads cost)
        self.selected_ingredients.append(ingredient_data)
        
        # Clear fields
        self.new_name_entry.delete(0, "end")
        self.new_price_entry.delete(0, "end")
        self.new_grams_entry.delete(0, "end")
        self.new_grams_needed_entry.delete(0, "end")
        
        self._show_status(f"'{name}' added to recipe!", error=False)
    
    def _calculate_cost(self):
        """Calculate recipe cost without saving"""
        if not self.selected_ingredients:
            self._show_status("Please select at least one ingredient", error=True)
            return
        
        recipe_name = self.recipe_name_entry.get().strip()
        if not recipe_name:
            self._show_status("Please enter a recipe name", error=True)
            return
        
        # Get margin percentage
        margin_text = self.margin_entry.get().strip()
        if not margin_text:
            margin_text = "150"  # Default to 150% (2.5x markup)
        
        try:
            margin_percentage = float(margin_text)
            if margin_percentage < 0:
                self._show_status("Margin percentage must be positive", error=True)
                return
        except ValueError:
            self._show_status("Margin percentage must be a valid number", error=True)
            return
        
        # Calculate cost with custom margin
        costing_data = self.data_handler.calculate_recipe_cost(
            recipe_name, 
            self.selected_ingredients, 
            save_recipe=False,
            margin_percentage=margin_percentage
        )
        
        if costing_data:
            self._display_cost_breakdown(costing_data)
            self._show_status("Cost calculation completed!", error=False)
        else:
            self._show_status("Error calculating cost", error=True)
    
    def _calculate_and_save(self):
        """Calculate recipe cost and save the recipe"""
        if not self.selected_ingredients:
            self._show_status("Please select at least one ingredient", error=True)
            return
        
        recipe_name = self.recipe_name_entry.get().strip()
        if not recipe_name:
            self._show_status("Please enter a recipe name", error=True)
            return
        
        # Get margin percentage
        margin_text = self.margin_entry.get().strip()
        if not margin_text:
            margin_text = "150"  # Default to 150% (2.5x markup)
        
        try:
            margin_percentage = float(margin_text)
            if margin_percentage < 0:
                self._show_status("Margin percentage must be positive", error=True)
                return
        except ValueError:
            self._show_status("Margin percentage must be a valid number", error=True)
            return
        
        # Calculate and save cost with custom margin
        costing_data = self.data_handler.calculate_recipe_cost(
            recipe_name, 
            self.selected_ingredients, 
            save_recipe=True,
            margin_percentage=margin_percentage
        )
        
        if costing_data:
            self._display_cost_breakdown(costing_data)
            self._show_status("Recipe saved successfully!", error=False)
            
            # Clear form
            self._clear_recipe_form()
            
            # Refresh other displays
            if self.on_refresh_callback:
                self.on_refresh_callback()
        else:
            self._show_status("Error saving recipe", error=True)
    
    def _display_cost_breakdown(self, costing_data: Dict[str, float]):
        """Display the cost breakdown"""
        # Clear previous breakdown
        for widget in self.breakdown_container.winfo_children():
            widget.destroy()
        
        # Create breakdown rows
        breakdown_items = [
            ("Total Ingredient Cost", costing_data.get("Total Ingredient Cost", 0), "#4cafef"),
            ("Miscellaneous Cost (50%)", costing_data.get("Miscellaneous Cost (50%)", 0), "#ff9500"),
            ("Labor Cost (45%)", costing_data.get("Labor Cost (45%)", 0), "#ff9500"),
            ("Total Cost", costing_data.get("Total Cost", 0), "#ff6b6b"),
            ("Suggested Selling Price", costing_data.get("Suggested Selling Price", 0), "#28a745"),
            ("Profit", costing_data.get("Profit", 0), "#28a745")
        ]
        
        for label, value, color in breakdown_items:
            row_frame = ctk.CTkFrame(self.breakdown_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            label_widget = ctk.CTkLabel(
                row_frame,
                text=label,
                text_color="#ffffff",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            label_widget.pack(side="left", padx=(0, 20))
            
            value_widget = ctk.CTkLabel(
                row_frame,
                text=f"${value:.2f}",
                text_color=color,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            value_widget.pack(side="right")
        
        # Update total cost display
        total_cost = costing_data.get("Total Cost", 0)
        self.total_label.configure(text=f"Total Cost: ${total_cost:.2f}")
    
    def _clear_recipe_form(self):
        """Clear the recipe form"""
        self.recipe_name_entry.delete(0, "end")
        self.margin_entry.delete(0, "end")
        self.margin_entry.insert(0, "150")  # Reset to default 150%
        self.selected_ingredients = []
        
        # Uncheck all checkboxes
        for widget in self.checklist_container.winfo_children():
            if hasattr(widget, 'var'):
                try:
                    widget.var.set(False)
                except Exception:
                    pass
        
        # Clear breakdown
        for widget in self.breakdown_container.winfo_children():
            widget.destroy()
        
        # Reset total
        self.total_label.configure(text="Total Cost: $0.00")
    
    def _clear_all(self):
        """Clear all form fields and selections"""
        self._clear_recipe_form()
        
        # Clear new ingredient fields
        self.new_name_entry.delete(0, "end")
        self.new_price_entry.delete(0, "end")
        self.new_grams_entry.delete(0, "end")
        self.new_grams_needed_entry.delete(0, "end")
        
        # Clear status
        self.status_label.configure(text="")
    
    def _show_status(self, message: str, error: bool = False):
        """Show status message"""
        color = "#ff6b6b" if error else "#4cafef"
        self.status_label.configure(text=message, text_color=color)
        
        # Clear status after 3 seconds
        self.after(3000, lambda: self.status_label.configure(text=""))