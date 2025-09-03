import customtkinter as ctk
from typing import Callable, List, Dict
from core.data_handler import DataHandler
import tkinter.messagebox as messagebox

class PackagingPage(ctk.CTkFrame):
    def __init__(self, master, data_handler: DataHandler, refresh_callback: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.data_handler = data_handler
        self.refresh_callback = refresh_callback
        self.current_materials = []
        self.editing_index = None
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Changed from row 1 to row 0
        
        self._create_widgets()
        self._setup_layout()
        self.refresh_materials()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable.grid_columnconfigure(0, weight=1) # Ensure content expands horizontally
        
        # Add packaging section
        self.add_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.add_title = ctk.CTkLabel(
            self.add_section,
            text="📦 Add Packaging Material",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ff9500"
        )
        
        # Form fields
        self.form_frame = ctk.CTkFrame(self.add_section, fg_color="transparent")
        
        # Row 1: Name and Price
        self.name_label = ctk.CTkLabel(self.form_frame, text="Material Name:", text_color="#ffffff")
        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g., Plastic Container, Paper Bag...")
        
        self.price_label = ctk.CTkLabel(self.form_frame, text="Total Price (₱):", text_color="#ffffff")
        self.price_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g., 150.00")
        
        # Row 2: Quantity
        self.quantity_label = ctk.CTkLabel(self.form_frame, text="Quantity:", text_color="#ffffff")
        self.quantity_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g., 100 pieces")
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.add_section, fg_color="transparent")
        
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="💾 Save Material",
            command=self._add_material,
            fg_color="#ff9500",
            hover_color="#e6850e",
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
            text="🔍 Search Materials",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Type to search materials...",
            height=40
        )
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Materials list section
        self.list_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.list_title = ctk.CTkLabel(
            self.list_section,
            text="📋 Packaging Materials Database",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        # Materials container
        self.materials_container = ctk.CTkFrame(
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
        self.quantity_label.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")
        self.quantity_entry.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="ew")
        
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
        self.materials_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
    
    def _add_material(self):
        """Add or update packaging material"""
        try:
            # Get form data
            name = self.name_entry.get().strip()
            price = self.price_entry.get().strip()
            quantity = self.quantity_entry.get().strip()
            
            # Validate inputs
            if not all([name, price, quantity]):
                messagebox.showerror("Error", "Please fill in all fields!")
                return
            
            try:
                price = float(price)
                quantity = float(quantity)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and quantity!")
                return
            
            if price <= 0 or quantity <= 0:
                messagebox.showerror("Error", "All values must be greater than zero!")
                return
            
            # Prepare material data
            material_data = {
                "Material Name": name,
                "Price": price,
                "Quantity": quantity
            }
            
            if self.editing_index is not None:
                # Update existing material
                success = self.data_handler.update_packaging_material(self.editing_index, material_data)
                if success:
                    messagebox.showinfo("Success", f"Updated material: {name}")
                    self._cancel_edit()
                else:
                    messagebox.showerror("Error", "Failed to update material!")
            else:
                # Add new material
                success = self.data_handler.add_packaging_material(material_data)
                if success:
                    messagebox.showinfo("Success", f"Added material: {name}")
                    self._clear_fields()
                else:
                    messagebox.showerror("Error", "Failed to add material!")
            
            self.refresh_materials()
            if self.refresh_callback:
                self.refresh_callback()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _clear_fields(self):
        """Clear all form fields"""
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.editing_index = None
        self.add_button.configure(text="💾 Save Material")
        self.cancel_edit_button.grid_remove()
    
    def _cancel_edit(self):
        """Cancel editing mode"""
        self._clear_fields()
    
    def _edit_material(self, index: int):
        """Edit material at specified index"""
        if 0 <= index < len(self.current_materials):
            material = self.current_materials[index]
            
            # Fill form with material data
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, material.get("Material Name", ""))
            
            self.price_entry.delete(0, "end")
            self.price_entry.insert(0, material.get("Price", ""))
            
            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, material.get("Quantity", ""))
            
            # Set editing mode
            self.editing_index = index
            self.add_button.configure(text="💾 Update Material")
            self.cancel_edit_button.grid()
    
    def _delete_material(self, index: int):
        """Delete material at specified index"""
        if 0 <= index < len(self.current_materials):
            material_name = self.current_materials[index].get("Material Name", "")
            
            result = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{material_name}'?"
            )
            
            if result:
                success = self.data_handler.delete_packaging_material(index)
                if success:
                    messagebox.showinfo("Success", f"Deleted material: {material_name}")
                    self.refresh_materials()
                    if self.refresh_callback:
                        self.refresh_callback()
                else:
                    messagebox.showerror("Error", "Failed to delete material!")
    
    def _on_search(self, event=None):
        """Handle search input"""
        query = self.search_entry.get().strip()
        if query:
            materials = self.data_handler.search_packaging_materials(query)
        else:
            materials = self.data_handler.get_all_packaging_materials()
        
        self._display_materials(materials)
    
    def refresh_materials(self):
        """Refresh materials list"""
        self.current_materials = self.data_handler.get_all_packaging_materials()
        self._display_materials(self.current_materials)
    
    def _display_materials(self, materials: List[Dict[str, str]]):
        """Display materials in the container"""
        # Clear existing widgets
        for widget in self.materials_container.winfo_children():
            widget.destroy()
        
        if not materials:
            # Show empty state
            empty_label = ctk.CTkLabel(
                self.materials_container,
                text="No packaging materials found. Add your first material above!",
                font=ctk.CTkFont(size=16),
                text_color="#888888"
            )
            empty_label.pack(pady=50)
            return
        
        # Create material cards
        for i, material in enumerate(materials):
            card = self._create_material_card(material, i)
            card.pack(fill="x", pady=(0, 10))
    
    def _create_material_card(self, material: Dict[str, str], index: int):
        """Create a card for displaying material information"""
        card = ctk.CTkFrame(self.materials_container, fg_color="#3d3d3d", corner_radius=10)
        
        # Main content frame
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        # Left side - material info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=material.get("Material Name", ""),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        name_label.pack(anchor="w")
        
        details_text = f"Price: ₱{material.get('Price', '0')} | Quantity: {material.get('Quantity', '0')} | Unit Cost: ₱{material.get('Unit Cost', '0')}"
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
            command=lambda idx=index: self._edit_material(idx),
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
            command=lambda idx=index: self._delete_material(idx),
            fg_color="#ff6b6b",
            hover_color="#e55555",
            font=ctk.CTkFont(size=14),
            width=80,
            height=35
        )
        delete_btn.pack(side="left")
        
        return card
