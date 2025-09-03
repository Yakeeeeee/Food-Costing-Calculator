import customtkinter as ctk
from typing import Callable, List, Dict
from core.data_handler import DataHandler
import tkinter.messagebox as messagebox
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CalculatorPage(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataHandler, refresh_callback: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_handler = data_handler
        self.refresh_callback = refresh_callback
        self.selected_ingredients = []
        self.selected_packaging_materials = []
        self.all_ingredients = []
        self.all_packaging_materials = []
        self.include_vat_var = ctk.BooleanVar(value=False)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Changed from row 1 to row 0
        
        self._create_widgets()
        self._setup_layout()
        self._refresh_data()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable.grid_columnconfigure(0, weight=1) # Ensure content expands horizontally
        
        # Recipe information section
        self.recipe_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.recipe_title = ctk.CTkLabel(
            self.recipe_section,
            text="📝 Recipe Information",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#28a745"
        )
        
        # Recipe form
        self.recipe_form = ctk.CTkFrame(self.recipe_section, fg_color="transparent")
        
        self.recipe_name_label = ctk.CTkLabel(self.recipe_form, text="Recipe Name:", text_color="#ffffff")
        self.recipe_name_entry = ctk.CTkEntry(self.recipe_form, placeholder_text="e.g., Chocolate Cake, Pizza Margherita...")
        
        self.margin_label = ctk.CTkLabel(self.recipe_form, text="Target Margin (%):", text_color="#ffffff")
        self.margin_entry = ctk.CTkEntry(self.recipe_form, placeholder_text="50")
        self.margin_note = ctk.CTkLabel(
            self.recipe_form,
            text="💡 Tip: 50% = 1.5x markup, 100% = 2x markup",
            font=ctk.CTkFont(size=12),
            text_color="#cccccc"
        )
        
        # VAT checkbox
        self.vat_checkbox = ctk.CTkCheckBox(
            self.recipe_form,
            text="Include VAT (12%)",
            variable=self.include_vat_var,
            text_color="#ffffff",
            fg_color="#4cafef",
            hover_color="#3d8bc0"
        )
        
        # Ingredients selection section
        self.ingredients_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.ingredients_title = ctk.CTkLabel(
            self.ingredients_section,
            text="🥕 Select Ingredients",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4cafef"
        )
        
        # Search ingredients
        self.ingredients_search_frame = ctk.CTkFrame(self.ingredients_section, fg_color="transparent")
        self.ingredients_search_label = ctk.CTkLabel(self.ingredients_search_frame, text="Search:", text_color="#ffffff")
        self.ingredients_search_entry = ctk.CTkEntry(
            self.ingredients_search_frame,
            placeholder_text="Search ingredients...",
            width=300
        )
        self.ingredients_search_entry.bind("<KeyRelease>", self._on_search_ingredients)
        
        # Ingredients checklist
        self.ingredients_checklist_frame = ctk.CTkFrame(self.ingredients_section, fg_color="#3d3d3d", corner_radius=10)
        self.ingredients_checklist_container = ctk.CTkFrame(
            self.ingredients_checklist_frame,
            fg_color="transparent"
        )
        
        # Selected ingredients display
        self.selected_ingredients_frame = ctk.CTkFrame(self.ingredients_section, fg_color="#3d3d3d", corner_radius=10)
        self.selected_ingredients_title = ctk.CTkLabel(
            self.selected_ingredients_frame,
            text="✅ Selected Ingredients",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#28a745"
        )
        self.selected_ingredients_container = ctk.CTkFrame(
            self.selected_ingredients_frame,
            fg_color="transparent"
        )
        
        # Packaging materials selection section
        self.packaging_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.packaging_title = ctk.CTkLabel(
            self.packaging_section,
            text="📦 Select Packaging Materials",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ff9500"
        )
        
        # Search packaging
        self.packaging_search_frame = ctk.CTkFrame(self.packaging_section, fg_color="transparent")
        self.packaging_search_label = ctk.CTkLabel(self.packaging_search_frame, text="Search:", text_color="#ffffff")
        self.packaging_search_entry = ctk.CTkEntry(
            self.packaging_search_frame,
            placeholder_text="Search packaging materials...",
            width=300
        )
        self.packaging_search_entry.bind("<KeyRelease>", self._on_search_packaging)
        
        # Packaging checklist
        self.packaging_checklist_frame = ctk.CTkFrame(self.packaging_section, fg_color="#3d3d3d", corner_radius=10)
        self.packaging_checklist_container = ctk.CTkFrame(
            self.packaging_checklist_frame,
            fg_color="transparent"
        )
        
        # Selected packaging display
        self.selected_packaging_frame = ctk.CTkFrame(self.packaging_section, fg_color="#3d3d3d", corner_radius=10)
        self.selected_packaging_title = ctk.CTkLabel(
            self.selected_packaging_frame,
            text="✅ Selected Packaging",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#28a745"
        )
        self.selected_packaging_container = ctk.CTkFrame(
            self.selected_packaging_frame,
            fg_color="transparent"
        )
        
        # Calculate and results section
        self.calculate_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.calculate_title = ctk.CTkLabel(
            self.calculate_section,
            text="🧮 Calculate Recipe Cost",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        # Calculate button
        self.calculate_button = ctk.CTkButton(
            self.calculate_section,
            text="🚀 Calculate Recipe Cost",
            command=self._calculate_recipe,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=18, weight="bold"),
            height=50
        )
        
        # Results section
        self.results_section = ctk.CTkFrame(self.calculate_section, fg_color="#3d3d3d", corner_radius=10)
        self.results_title = ctk.CTkLabel(
            self.results_section,
            text="📊 Costing Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        # Results content
        self.results_content = ctk.CTkFrame(self.results_section, fg_color="transparent")
        
        # Save recipe button
        self.save_recipe_button = ctk.CTkButton(
            self.calculate_section,
            text="💾 Save Recipe",
            command=self._save_recipe,
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        
        # Initially hide results and save button
        self.results_section.pack_forget()
        self.save_recipe_button.pack_forget()
    
    def _setup_layout(self):
        # Main scrollable
        self.main_scrollable.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Recipe section layout
        self.recipe_section.pack(fill="x", padx=0, pady=(0, 20))
        self.recipe_title.pack(pady=(20, 20))
        
        self.recipe_form.pack(fill="x", padx=30, pady=(0, 20))
        self.recipe_form.grid_columnconfigure(1, weight=1)
        self.recipe_form.grid_columnconfigure(3, weight=1)
        
        # Recipe form layout
        self.recipe_name_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        self.recipe_name_entry.grid(row=0, column=1, padx=(0, 20), pady=10, sticky="ew")
        
        self.margin_label.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="w")
        self.margin_entry.grid(row=0, column=3, pady=10, sticky="ew")
        
        self.margin_note.grid(row=1, column=1, columnspan=3, pady=(0, 10), sticky="w")
        self.vat_checkbox.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")
        
        # Ingredients section layout
        self.ingredients_section.pack(fill="x", padx=20, pady=(0, 20))
        self.ingredients_title.pack(pady=(20, 20))
        
        # Ingredients search
        self.ingredients_search_frame.pack(fill="x", padx=30, pady=(0, 15))
        self.ingredients_search_label.pack(side="left", padx=(0, 10))
        self.ingredients_search_entry.pack(side="left")
        
        # Ingredients checklist
        self.ingredients_checklist_frame.pack(fill="x", padx=30, pady=(0, 15))
        self.ingredients_checklist_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Selected ingredients
        self.selected_ingredients_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.selected_ingredients_title.pack(pady=(15, 10))
        self.selected_ingredients_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Packaging section layout
        self.packaging_section.pack(fill="x", padx=20, pady=(0, 20))
        self.packaging_title.pack(pady=(20, 20))
        
        # Packaging search
        self.packaging_search_frame.pack(fill="x", padx=30, pady=(0, 15))
        self.packaging_search_label.pack(side="left", padx=(0, 10))
        self.packaging_search_entry.pack(side="left")
        
        # Packaging checklist
        self.packaging_checklist_frame.pack(fill="x", padx=30, pady=(0, 15))
        self.packaging_checklist_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Selected packaging
        self.selected_packaging_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.selected_packaging_title.pack(pady=(15, 10))
        self.selected_packaging_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Calculate section layout
        self.calculate_section.pack(fill="x", padx=20, pady=(0, 20))
        self.calculate_title.pack(pady=(20, 20))
        self.calculate_button.pack(pady=(0, 20))
        
        # Results layout
        self.results_section.pack(fill="x", padx=30, pady=(0, 20))
        self.results_title.pack(pady=(20, 15))
        self.results_content.pack(fill="x", padx=20, pady=(0, 20))
        
        # Save button
        self.save_recipe_button.pack(pady=(0, 20))
    
    def _refresh_data(self):
        """Refresh ingredients and packaging materials data"""
        logging.info("CalculatorPage: Refreshing data...")
        self.all_ingredients = self.data_handler.get_all_ingredients()
        self.all_packaging_materials = self.data_handler.get_all_packaging_materials()
        logging.info(f"CalculatorPage: Loaded {len(self.all_ingredients)} ingredients and {len(self.all_packaging_materials)} packaging materials.")
        self._display_ingredients_checklist(self.all_ingredients)
        self._display_packaging_checklist(self.all_packaging_materials)
        self._update_selected_displays()
    
    def _on_search_ingredients(self, event=None):
        """Handle ingredients search"""
        query = self.ingredients_search_entry.get().strip()
        if query:
            ingredients = self.data_handler.search_ingredients(query)
        else:
            ingredients = self.all_ingredients
        self._display_ingredients_checklist(ingredients)
    
    def _on_search_packaging(self, event=None):
        """Handle packaging search"""
        query = self.packaging_search_entry.get().strip()
        if query:
            materials = self.data_handler.search_packaging_materials(query)
        else:
            materials = self.all_packaging_materials
        self._display_packaging_checklist(materials)
    
    def _display_ingredients_checklist(self, ingredients: List[Dict[str, str]]):
        """Display ingredients checklist"""
        # Clear existing widgets
        for widget in self.ingredients_checklist_container.winfo_children():
            widget.destroy()
        
        if not ingredients:
            empty_label = ctk.CTkLabel(
                self.ingredients_checklist_container,
                text="No ingredients found. Add ingredients first!",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            empty_label.pack(pady=20)
            return
        
        # Create ingredient checkboxes
        for ingredient in ingredients:
            self._create_ingredient_checkbox(ingredient)
    
    def _display_packaging_checklist(self, materials: List[Dict[str, str]]):
        """Display packaging checklist"""
        # Clear existing widgets
        for widget in self.packaging_checklist_container.winfo_children():
            widget.destroy()
        
        if not materials:
            empty_label = ctk.CTkLabel(
                self.packaging_checklist_container,
                text="No packaging materials found. Add packaging first!",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            empty_label.pack(pady=20)
            return
        
        # Create packaging checkboxes
        for material in materials:
            self._create_packaging_checkbox(material)
    
    def _create_ingredient_checkbox(self, ingredient: Dict[str, str]):
        """Create a checkbox for ingredient selection"""
        frame = ctk.CTkFrame(self.ingredients_checklist_container, fg_color="transparent")
        frame.pack(fill="x", pady=2)
        
        var = ctk.BooleanVar()
        
        checkbox = ctk.CTkCheckBox(
            frame,
            text=f"{ingredient.get('Ingredient Name', '')} - ₱{ingredient.get('Cost per Recipe', '0')}",
            variable=var,
            command=lambda: self._toggle_ingredient(ingredient, var),
            text_color="#ffffff",
            fg_color="#4cafef",
            hover_color="#3d8bc0"
        )
        checkbox.pack(side="left")
        
        # Store reference to checkbox
        ingredient['checkbox_var'] = var
        ingredient['checkbox_widget'] = checkbox
    
    def _create_packaging_checkbox(self, material: Dict[str, str]):
        """Create a checkbox for packaging selection"""
        frame = ctk.CTkFrame(self.packaging_checklist_container, fg_color="transparent")
        frame.pack(fill="x", pady=2)
        
        var = ctk.BooleanVar()
        
        checkbox = ctk.CTkCheckBox(
            frame,
            text=f"{material.get('Material Name', '')} - ₱{material.get('Total Cost', '0')}",
            variable=var,
            command=lambda: self._toggle_packaging(material, var),
            text_color="#ffffff",
            fg_color="#ff9500",
            hover_color="#e6850e"
        )
        checkbox.pack(side="left")
        
        # Store reference to checkbox
        material['checkbox_var'] = var
        material['checkbox_widget'] = checkbox
    
    def _toggle_ingredient(self, ingredient: Dict[str, str], var: ctk.BooleanVar):
        """Toggle ingredient selection"""
        if var.get():
            if ingredient not in self.selected_ingredients:
                self.selected_ingredients.append(ingredient)
        else:
            if ingredient in self.selected_ingredients:
                self.selected_ingredients.remove(ingredient)
        self._update_selected_displays()
    
    def _toggle_packaging(self, material: Dict[str, str], var: ctk.BooleanVar):
        """Toggle packaging selection"""
        if var.get():
            if material not in self.selected_packaging_materials:
                self.selected_packaging_materials.append(material)
        else:
            if material in self.selected_packaging_materials:
                self.selected_packaging_materials.remove(material)
        self._update_selected_displays()
    
    def _update_selected_displays(self):
        """Update selected ingredients and packaging displays"""
        self._update_selected_ingredients_display()
        self._update_selected_packaging_display()
    
    def _update_selected_ingredients_display(self):
        """Update selected ingredients display"""
        # Clear existing widgets
        for widget in self.selected_ingredients_container.winfo_children():
            widget.destroy()
        
        if not self.selected_ingredients:
            empty_label = ctk.CTkLabel(
                self.selected_ingredients_container,
                text="No ingredients selected",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            empty_label.pack(pady=20)
            return
        
        # Display selected ingredients
        for ingredient in self.selected_ingredients:
            frame = ctk.CTkFrame(self.selected_ingredients_container, fg_color="#2d2d2d", corner_radius=5)
            frame.pack(fill="x", pady=2)
            
            label = ctk.CTkLabel(
                frame,
                text=f"🥕 {ingredient.get('Ingredient Name', '')} - ₱{ingredient.get('Cost per Recipe', '0')}",
                font=ctk.CTkFont(size=14),
                text_color="#ffffff"
            )
            label.pack(side="left", padx=10, pady=5)
            
            remove_btn = ctk.CTkButton(
                frame,
                text="❌",
                command=lambda ing=ingredient: self._remove_ingredient(ing),
                fg_color="#ff6b6b",
                hover_color="#e55555",
                width=30,
                height=25
            )
            remove_btn.pack(side="right", padx=10, pady=5)
    
    def _update_selected_packaging_display(self):
        """Update selected packaging display"""
        # Clear existing widgets
        for widget in self.selected_packaging_container.winfo_children():
            widget.destroy()
        
        if not self.selected_packaging_materials:
            empty_label = ctk.CTkLabel(
                self.selected_packaging_container,
                text="No packaging materials selected",
                font=ctk.CTkFont(size=14),
                text_color="#888888"
            )
            empty_label.pack(pady=20)
            return
        
        # Display selected packaging
        for material in self.selected_packaging_materials:
            frame = ctk.CTkFrame(self.selected_packaging_container, fg_color="#2d2d2d", corner_radius=5)
            frame.pack(fill="x", pady=2)
            
            label = ctk.CTkLabel(
                frame,
                text=f"📦 {material.get('Material Name', '')} - ₱{material.get('Total Cost', '0')}",
                font=ctk.CTkFont(size=14),
                text_color="#ffffff"
            )
            label.pack(side="left", padx=10, pady=5)
            
            remove_btn = ctk.CTkButton(
                frame,
                text="❌",
                command=lambda mat=material: self._remove_packaging(mat),
                fg_color="#ff6b6b",
                hover_color="#e55555",
                width=30,
                height=25
            )
            remove_btn.pack(side="right", padx=10, pady=5)
    
    def _remove_ingredient(self, ingredient: Dict[str, str]):
        """Remove ingredient from selection"""
        if ingredient in self.selected_ingredients:
            self.selected_ingredients.remove(ingredient)
            ingredient['checkbox_var'].set(False)
            self._update_selected_displays()
    
    def _remove_packaging(self, material: Dict[str, str]):
        """Remove packaging from selection"""
        if material in self.selected_packaging_materials:
            self.selected_packaging_materials.remove(material)
            material['checkbox_var'].set(False)
            self._update_selected_displays()
    
    def _calculate_recipe(self):
        """Calculate recipe cost"""
        try:
            # Validate inputs
            recipe_name = self.recipe_name_entry.get().strip()
            margin_text = self.margin_entry.get().strip()
            
            if not recipe_name:
                messagebox.showerror("Error", "Please enter a recipe name!")
                return
            
            if not margin_text:
                messagebox.showerror("Error", "Please enter a target margin percentage!")
                return
            
            try:
                margin_percentage = float(margin_text)
                if margin_percentage < 0:
                    messagebox.showerror("Error", "Margin percentage must be positive!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid margin percentage!")
                return
            
            if not self.selected_ingredients:
                messagebox.showerror("Error", "Please select at least one ingredient!")
                return
            
            # Calculate recipe cost
            vat_percentage = 12.0 if self.include_vat_var.get() else 0.0
            
            result = self.data_handler.calculate_recipe_cost(
                recipe_name=recipe_name,
                ingredients_used=self.selected_ingredients,
                packaging_materials_used=self.selected_packaging_materials,
                save_recipe=False,
                margin_percentage=margin_percentage,
                include_vat=self.include_vat_var.get(),
                vat_percentage=vat_percentage
            )
            
            if result:
                self._display_results(result)
                # Store result for saving
                self.current_result = result
            else:
                messagebox.showerror("Error", "Failed to calculate recipe cost!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _display_results(self, result: Dict[str, float]):
        """Display calculation results"""
        # Clear existing results
        for widget in self.results_content.winfo_children():
            widget.destroy()
        
        # Create results display
        # Row 1: Cost breakdown
        row1_frame = ctk.CTkFrame(self.results_content, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(0, 15))
        
        ingredient_cost_label = ctk.CTkLabel(
            row1_frame,
            text=f"🥕 Ingredients: ₱{result.get('Total Ingredient Cost', 0):.2f}",
            font=ctk.CTkFont(size=16),
            text_color="#4cafef"
        )
        ingredient_cost_label.pack(side="left", padx=(0, 30))
        
        packaging_cost_label = ctk.CTkLabel(
            row1_frame,
            text=f"📦 Packaging: ₱{result.get('Packaging Cost', 0):.2f}",
            font=ctk.CTkFont(size=16),
            text_color="#ff9500"
        )
        packaging_cost_label.pack(side="left", padx=(0, 30))
        
        labor_cost_label = ctk.CTkLabel(
            row1_frame,
            text=f"👷 Labor: ₱{result.get('Labor Cost (50%)', 0):.2f}",
            font=ctk.CTkFont(size=16),
            text_color="#9c27b0"
        )
        labor_cost_label.pack(side="left")
        
        # Row 2: Total cost and selling price
        row2_frame = ctk.CTkFrame(self.results_content, fg_color="transparent")
        row2_frame.pack(fill="x", pady=(0, 15))
        
        total_cost_label = ctk.CTkLabel(
            row2_frame,
            text=f"💰 Total Cost: ₱{result.get('Total Cost', 0):.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ff6b6b"
        )
        total_cost_label.pack(side="left", padx=(0, 30))
        
        selling_price_label = ctk.CTkLabel(
            row2_frame,
            text=f"💵 Selling Price: ₱{result.get('Suggested Selling Price', 0):.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#28a745"
        )
        selling_price_label.pack(side="left", padx=(0, 30))
        
        profit_label = ctk.CTkLabel(
            row2_frame,
            text=f"📈 Profit: ₱{result.get('Profit', 0):.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4cafef"
        )
        profit_label.pack(side="left")
        
        # Row 3: Additional info
        row3_frame = ctk.CTkFrame(self.results_content, fg_color="transparent")
        row3_frame.pack(fill="x")
        
        margin_label = ctk.CTkLabel(
            row3_frame,
            text=f"📊 Margin: {result.get('Margin Percentage', 0):.1f}%",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc"
        )
        margin_label.pack(side="left", padx=(0, 30))
        
        if result.get('VAT Percentage', 0) > 0:
            vat_label = ctk.CTkLabel(
                row3_frame,
                text=f"🏛️ VAT: {result.get('VAT Percentage', 0):.1f}%",
                font=ctk.CTkFont(size=14),
                text_color="#cccccc"
            )
            vat_label.pack(side="left")
        
        # Show results and save button
        self.results_section.pack(fill="x", padx=30, pady=(0, 20))
        self.save_recipe_button.pack(pady=(0, 20))
    
    def _save_recipe(self):
        """Save the calculated recipe"""
        try:
            if not hasattr(self, 'current_result'):
                messagebox.showerror("Error", "Please calculate the recipe cost first!")
                return
            
            recipe_name = self.recipe_name_entry.get().strip()
            
            # Save recipe
            success = self.data_handler.calculate_recipe_cost(
                recipe_name=recipe_name,
                ingredients_used=self.selected_ingredients,
                packaging_materials_used=self.selected_packaging_materials,
                save_recipe=True,
                margin_percentage=self.current_result.get('Margin Percentage', 150.0),
                include_vat=self.include_vat_var.get(),
                vat_percentage=self.current_result.get('VAT Percentage', 0.0)
            )
            
            if success:
                messagebox.showinfo("Success", f"Recipe '{recipe_name}' saved successfully!")
                self._clear_calculator_fields() # Clear fields after successful save
                if self.refresh_callback:
                    self.refresh_callback()
            else:
                messagebox.showerror("Error", "Failed to save recipe!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def _clear_calculator_fields(self):
        """Clear all input fields and reset selections in the calculator UI."""
        # Clear recipe information fields
        self.recipe_name_entry.delete(0, "end")
        self.margin_entry.delete(0, "end")
        self.margin_entry.insert(0, "50") # Reset to default margin
        self.include_vat_var.set(False)

        # Clear selected ingredients
        for ingredient in self.selected_ingredients:
            if 'checkbox_var' in ingredient and ingredient['checkbox_var'].get():
                ingredient['checkbox_var'].set(False)
        self.selected_ingredients.clear()
        self._update_selected_ingredients_display()
        self._display_ingredients_checklist(self.all_ingredients) # Re-display to update checkboxes

        # Clear selected packaging materials
        for material in self.selected_packaging_materials:
            if 'checkbox_var' in material and material['checkbox_var'].get():
                material['checkbox_var'].set(False)
        self.selected_packaging_materials.clear()
        self._update_selected_packaging_display()
        self._display_packaging_checklist(self.all_packaging_materials) # Re-display to update checkboxes

        # Hide results and save button
        self.results_section.pack_forget()
        self.save_recipe_button.pack_forget()
        self.current_result = None # Clear stored result
