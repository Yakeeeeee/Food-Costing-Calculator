import customtkinter as ctk
import webbrowser

class HelpFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Main card container
        self.card = ctk.CTkFrame(self.main_scrollable, corner_radius=15, fg_color="#2d2d2d")
        self.card.pack(fill="x", padx=15, pady=15)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.card, 
            text="How to Use Food Costing Calculator", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4cafef"
        )
        
        # Getting Started section
        self.getting_started_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.getting_started_title = ctk.CTkLabel(
            self.getting_started_frame,
            text="🚀 Getting Started",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.getting_started_text = ctk.CTkLabel(
            self.getting_started_frame,
            text="1. Launch the Food Costing Calculator application\n"
                 "2. The Dashboard will show an overview of your ingredients and recipes\n"
                 "3. Start by adding ingredients to your database\n"
                 "4. Create recipes using the Calculator feature\n"
                 "5. View and manage your saved recipes",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
        
        # Ingredients Management section
        self.ingredients_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.ingredients_title = ctk.CTkLabel(
            self.ingredients_frame,
            text="🥘 Ingredients Management",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.ingredients_text = ctk.CTkLabel(
            self.ingredients_frame,
            text="Adding Ingredients:\n"
                 "• Navigate to the 'Ingredients' tab\n"
                 "• Fill in: Ingredient Name, Price, Grams, Grams Needed in Recipe\n"
                 "• Click 'Add Ingredient' to save\n\n"
                 "Managing Ingredients:\n"
                 "• Use the search bar to find specific ingredients\n"
                 "• Click 'Edit' to modify ingredient details\n"
                 "• Click 'Delete' to remove ingredients\n\n"
                 "Note: Price per Gram and Cost per Recipe are calculated automatically",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
        
        # Recipe Calculator section
        self.calculator_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.calculator_title = ctk.CTkLabel(
            self.calculator_frame,
            text="🧮 Recipe Calculator",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.calculator_text = ctk.CTkLabel(
            self.calculator_frame,
            text="Creating a Recipe:\n"
                 "• Navigate to the 'Calculator' tab\n"
                 "• Enter a Recipe Name\n"
                 "• Select ingredients from the checklist (use search to find them)\n"
                 "• Add new ingredients if they're not in your database\n"
                 "• Click 'Calculate Cost' to see pricing breakdown\n"
                 "• Click 'Calculate & Save Recipe' to save the recipe\n\n"
                 "Cost Calculation:\n"
                 "• Total Ingredient Cost = Sum of all ingredient costs\n"
                 "• Miscellaneous Cost = 50% of ingredient cost\n"
                 "• Labor Cost = 45% of ingredient cost\n"
                 "• Total Cost = Ingredient + Misc + Labor costs\n"
                 "• Suggested Selling Price = Total Cost × (1 + Target Margin/100)\n"
                 "  - Set Target Margin (%) in the Calculator (default 150% → 2.5×)\n"
                 "• Profit = Suggested Selling Price - Total Cost",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
        
        # Recipes Management section
        self.recipes_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.recipes_title = ctk.CTkLabel(
            self.recipes_frame,
            text="📋 Recipes Management",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.recipes_text = ctk.CTkLabel(
            self.recipes_frame,
            text="Viewing Recipes:\n"
                 "• Navigate to the 'Recipes' tab\n"
                 "• See all saved recipes with cost breakdown\n"
                 "• Use search to find specific recipes\n"
                 "• Click 'View Details' to see full costing information\n\n"
                 "Recipe Details Include:\n"
                 "• Complete cost breakdown\n"
                 "• Pricing information\n"
                 "• List of ingredients used",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
        
        # Data Management section
        self.data_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.data_title = ctk.CTkLabel(
            self.data_frame,
            text="💾 Data Management",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.data_text = ctk.CTkLabel(
            self.data_frame,
            text="Data Storage:\n"
                 "• All data is stored in CSV files in the application directory\n"
                 "• ingredients.csv - Contains all ingredient information\n"
                 "• recipes.csv - Contains all saved recipe data\n"
                 "• Data persists between application sessions\n\n"
                 "Backup Recommendations:\n"
                 "• Regularly backup your CSV files\n"
                 "• Store backups in a separate location\n"
                 "• CSV files can be opened in Excel or Google Sheets",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
        
        # Tips and Best Practices section
        self.tips_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.tips_title = ctk.CTkLabel(
            self.tips_frame,
            text="💡 Tips & Best Practices",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.tips_text = ctk.CTkLabel(
            self.tips_frame,
            text="• Keep ingredient prices updated for accurate calculations\n"
                 "• Use descriptive recipe names for easy identification\n"
                 "• Regularly review and update your ingredient database\n"
                 "• Default markup is 150% (2.5×). Adjust the Target Margin (%) in the Calculator to fit your pricing strategy\n"
                 "• Use the search function to quickly find ingredients and recipes\n"
                 "• Export your data regularly for backup purposes",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
        
        # Support section
        self.support_frame = ctk.CTkFrame(self.card, fg_color="#3d3d3d", corner_radius=10)
        self.support_title = ctk.CTkLabel(
            self.support_frame,
            text="🆘 Need Help?",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        
        self.support_text = ctk.CTkLabel(
            self.support_frame,
            text="If you need assistance or have questions please contact:",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
        
        # Email only
        self.email_frame = ctk.CTkFrame(self.support_frame, fg_color="transparent")
        self.email_label = ctk.CTkLabel(
            self.email_frame,
            text="📧 Email:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        self.email_value = ctk.CTkLabel(
            self.email_frame,
            text="esteleydesjohnallen0@gmail.com",
            font=ctk.CTkFont(size=14),
            text_color="#4cafef"
        )
        
        self.final_note = ctk.CTkLabel(
            self.support_frame,
            text="Visit the 'About' page for more contact information.",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc",
            justify="left"
        )
    
    def _setup_layout(self):
        # Configure main scrollable frame
        self.main_scrollable.grid_columnconfigure(0, weight=1)
        
        # Configure card grid
        self.card.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label.pack(pady=(20, 25))
        
        # Getting Started section
        self.getting_started_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.getting_started_title.pack(pady=(15, 15))
        self.getting_started_text.pack(pady=(0, 15), padx=20)
        
        # Ingredients Management section
        self.ingredients_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.ingredients_title.pack(pady=(15, 15))
        self.ingredients_text.pack(pady=(0, 15), padx=20)
        
        # Recipe Calculator section
        self.calculator_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.calculator_title.pack(pady=(15, 15))
        self.calculator_text.pack(pady=(0, 15), padx=20)
        
        # Recipes Management section
        self.recipes_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.recipes_title.pack(pady=(15, 15))
        self.recipes_text.pack(pady=(0, 15), padx=20)
        
        # Data Management section
        self.data_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.data_title.pack(pady=(15, 15))
        self.data_text.pack(pady=(0, 15), padx=20)
        
        # Tips and Best Practices section
        self.tips_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.tips_title.pack(pady=(15, 15))
        self.tips_text.pack(pady=(0, 15), padx=20)
        
        # Support section
        self.support_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.support_title.pack(pady=(15, 15))
        self.support_text.pack(pady=(0, 15), padx=20)
        
        # Email only
        self.email_frame.pack(anchor="center", pady=(0, 8))
        self.email_label.pack(side="top", padx=(0, 10))
        self.email_value.pack(side="top")
        
        # Final note
        self.final_note.pack(pady=(0, 20), padx=20)
