import customtkinter as ctk

class HelpPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Changed from row 1 to row 0
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        # Main scrollable container
        self.main_scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scrollable.grid_columnconfigure(0, weight=1) # Ensure content expands horizontally
        
        # Welcome section
        self.welcome_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.welcome_title = ctk.CTkLabel(
            self.welcome_section,
            text="❓ Help & User Guide",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4cafef"
        )
        
        
        # Getting started section
        self.getting_started_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.getting_started_title = ctk.CTkLabel(
            self.getting_started_section,
            text="🚀 Getting Started",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        self.getting_started_text = ctk.CTkLabel(
            self.getting_started_section,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            wraplength=600, # Adjust wraplength as needed
            justify="left",
            anchor="w"
        )
        
        getting_started_content = """Welcome to the Food Costing Calculator! This guide will help you get started with calculating recipe costs and managing your food business finances.

Step-by-Step Process:

1. 📊 Dashboard
   • Start here to get an overview of your data
   • View statistics of your ingredients, recipes, and packaging materials
   • Use quick action buttons to navigate to different sections

2. 🥕 Add Ingredients
   • Go to the Ingredients section
   • Add your ingredients with accurate prices and quantities
   • Include the grams needed per recipe for accurate costing

3. 📦 Add Packaging Materials
   • Go to the Packaging section
   • Add packaging materials with their costs
   • This helps calculate total product costs

4. 🧮 Calculate Recipe Costs
   • Go to the Calculator section
   • Enter your recipe name and target profit margin
   • Select ingredients and packaging materials
   • Calculate and save your recipe

5. 📝 View Saved Recipes
   • Go to the Recipes section
   • View all your saved recipe costings
   • Search and manage your recipe database"""
        
        self.getting_started_text.configure(text=getting_started_content)
        
        # Detailed instructions section
        self.instructions_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.instructions_title = ctk.CTkLabel(
            self.instructions_section,
            text="📋 Detailed Instructions",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        # Instructions tabs
        self.instructions_tabs = ctk.CTkTabview(self.instructions_section)
        
        # Ingredients tab
        self.ingredients_tab = self.instructions_tabs.add("🥕 Ingredients")
        self._create_ingredients_help()
        
        # Packaging tab
        self.packaging_tab = self.instructions_tabs.add("📦 Packaging")
        self._create_packaging_help()
        
        # Calculator tab
        self.calculator_tab = self.instructions_tabs.add("🧮 Calculator")
        self._create_calculator_help()
        
        # Recipes tab
        self.recipes_tab = self.instructions_tabs.add("📝 Recipes")
        self._create_recipes_help()
        
        # Tips and best practices section
        self.tips_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.tips_title = ctk.CTkLabel(
            self.tips_section,
            text="💡 Tips & Best Practices",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        self.tips_text = ctk.CTkLabel(
            self.tips_section,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            wraplength=600, # Adjust wraplength as needed
            justify="left",
            anchor="w"
        )
        
        tips_content = """🎯 PROFIT MARGIN GUIDELINES

• 100% Margin = 2x markup (50% profit margin)
• 50% Margin = 1.5x markup (33.3% profit margin) - RECOMMENDED
• 200% Margin = 3x markup (66.7% profit margin)
• 300% Margin = 4x markup (75% profit margin)

📊 COST BREAKDOWN EXPLANATION

• Ingredient Cost: Total cost of all ingredients used in the recipe
• Packaging Cost: Cost of packaging materials per recipe
• Labor Cost: Automatically calculated as 50% of ingredient cost
• VAT: Optional 12% tax on total cost (Philippines)
• Total Cost: Sum of all costs including VAT
• Suggested Selling Price: Total cost + profit margin
• Profit: Difference between selling price and total cost

💡 BEST PRACTICES

1. ACCURATE PRICING
   • Update ingredient prices regularly
   • Use actual purchase prices, not estimates
   • Include all costs (delivery, taxes, etc.)

2. RECIPE STANDARDIZATION
   • Use consistent measurements (grams)
   • Document exact quantities for each ingredient
   • Consider yield and waste in calculations

3. PROFIT MARGIN STRATEGY
   • Start with 50% margin for most items
   • Adjust based on market competition
   • Consider seasonal price fluctuations

4. REGULAR REVIEWS
   • Review costs monthly
   • Update prices when suppliers change rates
   • Monitor profit margins and adjust as needed

5. PACKAGING CONSIDERATIONS
   • Include all packaging costs
   • Consider environmental impact
   • Factor in storage and handling costs

🔍 SEARCH FUNCTIONALITY

• Use the search boxes to quickly find ingredients, packaging, or recipes
• Search is case-insensitive
• Partial matches work (e.g., "flour" will find "all-purpose flour")

💾 DATA MANAGEMENT

• All data is stored locally in CSV files
• Backup your data folder regularly
• The application creates data files automatically
• Data is organized in the 'data' folder"""
        
        self.tips_text.configure(text=tips_content)
        
        # FAQ section
        self.faq_section = ctk.CTkFrame(self.main_scrollable, fg_color="#2d2d2d", corner_radius=15)
        
        self.faq_title = ctk.CTkLabel(
            self.faq_section,
            text="❓ Frequently Asked Questions",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        self.faq_text = ctk.CTkLabel(
            self.faq_section,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            wraplength=600, # Adjust wraplength as needed
            justify="left",
            anchor="w"
        )
        
        faq_content = """Q: How do I calculate the right profit margin?
A: Start with 150% margin (2.5x markup) and adjust based on your market, competition, and business goals.

Q: Why is labor cost set to 50% of ingredient cost?
A: This is a standard industry practice. You can adjust this in future versions or calculate manually.

Q: Should I include VAT in my calculations?
A: It depends on your business. If you're VAT-registered, include it. If not, leave it unchecked.

Q: How often should I update ingredient prices?
A: Update prices whenever you receive new supplier quotes or when prices change significantly.

Q: Can I export my data?
A: Currently, data is stored in CSV format in the 'data' folder. You can manually copy these files.

Q: What if I make a mistake in my recipe?
A: You can edit ingredients and packaging materials, or delete and recreate recipes.

Q: How do I handle seasonal price changes?
A: Update ingredient prices when they change and recalculate your recipes.

Q: Can I use different units of measurement?
A: Currently, the app uses grams for consistency. Convert your measurements to grams for best results.

Q: What's the difference between "Grams" and "Grams Needed in Recipe"?
A: "Grams" is the total package size you buy. "Grams Needed in Recipe" is how much you use per recipe.

Q: How do I handle waste and yield?
A: Factor waste into your "Grams Needed in Recipe" calculation. For example, if you lose 10% to waste, add 10% to your recipe quantity."""
        
        self.faq_text.configure(text=faq_content)
    
    def _create_ingredients_help(self):
        """Create ingredients help content"""
        content = ctk.CTkLabel(
            self.ingredients_tab,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            wraplength=600, # Adjust wraplength as needed
            justify="left",
            anchor="w"
        )
        content.pack(fill="x", padx=20, pady=20)
        
        text = """🥕 INGREDIENTS MANAGEMENT

ADDING INGREDIENTS:
1. Go to the Ingredients section
2. Fill in the ingredient name (e.g., "All-Purpose Flour")
3. Enter the total price you paid (e.g., ₱45.50)
4. Enter the total grams in the package (e.g., 1000g for 1kg)
5. Enter how many grams you use per recipe (e.g., 250g)
6. Click "Save Ingredient"

EDITING INGREDIENTS:
1. Find the ingredient in the list
2. Click the "Edit" button
3. Modify the values as needed
4. Click "Update Ingredient"

DELETING INGREDIENTS:
1. Find the ingredient in the list
2. Click the "Delete" button
3. Confirm the deletion

SEARCHING INGREDIENTS:
• Use the search box to find ingredients quickly
• Type part of the ingredient name
• Results update as you type

TIPS:
• Use consistent naming (e.g., always "All-Purpose Flour" not "flour")
• Update prices when they change
• Be accurate with quantities for precise costing"""
        
        content.configure(text=text)
    
    def _create_packaging_help(self):
        """Create packaging help content"""
        content = ctk.CTkLabel(
            self.packaging_tab,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            wraplength=600, # Adjust wraplength as needed
            justify="left",
            anchor="w"
        )
        content.pack(fill="x", padx=20, pady=20)
        
        text = """📦 PACKAGING MANAGEMENT

ADDING PACKAGING MATERIALS:
1. Go to the Packaging section
2. Enter the material name (e.g., "Plastic Container")
3. Enter the total price you paid (e.g., ₱150.00)
4. Enter the quantity you received (e.g., 100 pieces)
5. Click "Save Material"

EDITING PACKAGING:
1. Find the material in the list
2. Click the "Edit" button
3. Modify the values as needed
4. Click "Update Material"

DELETING PACKAGING:
1. Find the material in the list
2. Click the "Delete" button
3. Confirm the deletion

SEARCHING PACKAGING:
• Use the search box to find materials quickly
• Type part of the material name
• Results update as you type

COST CALCULATION:
• Unit cost is automatically calculated (Price ÷ Quantity)
• Total cost is the price you paid
• The calculator uses unit cost per recipe

TIPS:
• Include all packaging costs (containers, labels, bags, etc.)
• Consider environmental-friendly options
• Update costs when prices change
• Factor in storage and handling costs"""
        
        content.configure(text=text)
    
    def _create_calculator_help(self):
        """Create calculator help content"""
        content = ctk.CTkLabel(
            self.calculator_tab,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            wraplength=600, # Adjust wraplength as needed
            justify="left",
            anchor="w"
        )
        content.pack(fill="x", padx=20, pady=20)
        
        text = """🧮 RECIPE COST CALCULATOR

STEP 1: RECIPE INFORMATION
1. Enter your recipe name (e.g., "Chocolate Cake")
2. Set your target margin percentage (e.g., 150 for 2.5x markup)
3. Check "Include VAT" if applicable

STEP 2: SELECT INGREDIENTS
1. Use the search box to find ingredients quickly
2. Check the boxes for ingredients you use in the recipe
3. Selected ingredients appear in the "Selected Ingredients" section
4. Remove ingredients by clicking the ❌ button

STEP 3: SELECT PACKAGING
1. Use the search box to find packaging materials
2. Check the boxes for packaging you use
3. Selected packaging appears in the "Selected Packaging" section
4. Remove packaging by clicking the ❌ button

STEP 4: CALCULATE COSTS
1. Click "Calculate Recipe Cost"
2. Review the cost breakdown:
   • Ingredient costs
   • Packaging costs
   • Labor costs (50% of ingredients)
   • VAT (if included)
   • Total cost
   • Suggested selling price
   • Profit amount

STEP 5: SAVE RECIPE
1. Click "Save Recipe" to store the calculation
2. Your recipe will appear in the Recipes section

COST BREAKDOWN EXPLANATION:
• Ingredients: Sum of all selected ingredient costs
• Packaging: Sum of all selected packaging costs
• Labor: 50% of ingredient cost (industry standard)
• VAT: 12% of total cost (if enabled)
• Total Cost: All costs combined
• Selling Price: Total cost + profit margin
• Profit: Selling price minus total cost

TIPS:
• Start with 50% margin for most items
• Adjust margin based on market and competition
• Save recipes for future reference
• Update costs when prices change"""
        
        content.configure(text=text)
    
    def _create_recipes_help(self):
        """Create recipes help content"""
        content = ctk.CTkLabel(
            self.recipes_tab,
            fg_color="transparent",
            text_color="#cccccc",
            font=ctk.CTkFont(size=14),
            wraplength=600, # Adjust wraplength as needed
            justify="left",
            anchor="w"
        )
        content.pack(fill="x", padx=20, pady=20)
        
        text = """📝 RECIPES MANAGEMENT

VIEWING SAVED RECIPES:
1. Go to the Recipes section
2. All your saved recipes are displayed as cards
3. Each card shows:
   • Recipe name
   • Cost breakdown
   • Selling price and profit
   • Ingredients and packaging used

SEARCHING RECIPES:
1. Use the search box to find recipes
2. Type part of the recipe name
3. Results update as you type

RECIPE CARD INFORMATION:
• Recipe Name: The name you gave your recipe
• Cost Breakdown: Detailed cost information
• Ingredients Used: List of all ingredients in the recipe
• Packaging Used: List of all packaging materials
• Cost Summary: Total costs, selling price, and profit

DELETING RECIPES:
1. Find the recipe you want to delete
2. Click the "Delete Recipe" button
3. Confirm the deletion
4. The recipe will be permanently removed

RECIPE COSTING DETAILS:
• Total Ingredient Cost: Sum of all ingredient costs
• Packaging Cost: Sum of all packaging costs
• Labor Cost: 50% of ingredient cost
• VAT Percentage: Tax rate used (if any)
• Total Cost: All costs combined
• Suggested Selling Price: Recommended retail price
• Margin Percentage: Profit margin used
• Profit: Amount of profit per recipe

TIPS:
• Keep recipe names descriptive and consistent
• Review saved recipes regularly
• Update recipes when costs change
• Use recipes as templates for similar items
• Export data for backup purposes"""
        
        content.configure(text=text)
    
    def _setup_layout(self):
        # Main scrollable
        self.main_scrollable.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Welcome section
        self.welcome_section.pack(fill="x", padx=0, pady=(0, 20))
        self.welcome_title.pack(pady=(30, 10))
        
        # Getting started section
        self.getting_started_section.pack(fill="x", padx=20, pady=(0, 20))
        self.getting_started_title.pack(pady=(20, 15))
        self.getting_started_text.pack(fill="x", padx=20, pady=(0, 20))
        
        # Instructions section
        self.instructions_section.pack(fill="x", padx=20, pady=(0, 20))
        self.instructions_title.pack(pady=(20, 15))
        self.instructions_tabs.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tips section
        self.tips_section.pack(fill="x", padx=20, pady=(0, 20))
        self.tips_title.pack(pady=(20, 15))
        self.tips_text.pack(fill="x", padx=20, pady=(0, 20))
        
        # FAQ section
        self.faq_section.pack(fill="x", padx=20, pady=(0, 20))
        self.faq_title.pack(pady=(20, 15))
        self.faq_text.pack(fill="x", padx=20, pady=(0, 20))
