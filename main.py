import customtkinter as ctk
from data_handler import DataHandler
from ui_dashboard import DashboardFrame
from ui_ingredients import IngredientsFrame
from ui_recipes import RecipesFrame
from ui_calculator import CalculatorFrame
from ui_about import AboutFrame
from ui_help import HelpFrame

class FoodCostingCalculator:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize data handler
        self.data_handler = DataHandler()
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Food Costing Calculator")
        self.root.geometry("1400x900")
        self.root.configure(fg_color="#1e1e1e")
        
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Current active frame
        self.current_frame = None
        
        self._create_widgets()
        self._setup_layout()
        
        # Show dashboard by default
        self._show_dashboard()
    
    def _create_widgets(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.root, fg_color="#2d2d2d", corner_radius=0)
        
        # App title in sidebar
        self.app_title = ctk.CTkLabel(
            self.sidebar,
            text="Food Costing\nCalculator",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        # Navigation buttons
        self.dashboard_btn = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            command=self._show_dashboard,
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40
        )
        
        self.ingredients_btn = ctk.CTkButton(
            self.sidebar,
            text="Ingredients",
            command=self._show_ingredients,
            fg_color="transparent",
            hover_color="#3d3d3d",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        self.recipes_btn = ctk.CTkButton(
            self.sidebar,
            text="Recipes",
            command=self._show_recipes,
            fg_color="transparent",
            hover_color="#3d3d3d",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        self.calculator_btn = ctk.CTkButton(
            self.sidebar,
            text="Calculator",
            command=self._show_calculator,
            fg_color="transparent",
            hover_color="#3d3d3d",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        # About button
        self.about_btn = ctk.CTkButton(
            self.sidebar,
            text="About",
            command=self._show_about,
            fg_color="transparent",
            hover_color="#3d3d3d",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        # Help button
        self.help_btn = ctk.CTkButton(
            self.sidebar,
            text="How to Use",
            command=self._show_help,
            fg_color="transparent",
            hover_color="#3d3d3d",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        # Exit button
        self.exit_btn = ctk.CTkButton(
            self.sidebar,
            text="Exit",
            command=self.root.quit,
            fg_color="#ff6b6b",
            hover_color="#e55555",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Dashboard content
        self.dashboard_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        # Dashboard title
        self.dashboard_title = ctk.CTkLabel(
            self.dashboard_frame,
            text="Welcome to Food Costing Calculator",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        
        # Dashboard subtitle
        self.dashboard_subtitle = ctk.CTkLabel(
            self.dashboard_frame,
            text="Manage your ingredients, recipes, and calculate product costs efficiently",
            font=ctk.CTkFont(size=18),
            text_color="#cccccc"
        )
        
        # Dashboard stats
        self.stats_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="#2d2d2d", corner_radius=15)
        
        self.total_ingredients_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total Ingredients: 0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4cafef"
        )
        
        self.total_recipes_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total Recipes: 0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#28a745"
        )
        
        # Quick actions
        self.quick_actions_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="#2d2d2d", corner_radius=15)
        
        self.quick_actions_label = ctk.CTkLabel(
            self.quick_actions_frame,
            text="Quick Actions",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        
        self.quick_ingredients_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="Manage Ingredients",
            command=self._show_ingredients,
            fg_color="#4cafef",
            hover_color="#3d8bc0",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        self.quick_calculator_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="Calculate Recipe Cost",
            command=self._show_calculator,
            fg_color="#28a745",
            hover_color="#218838",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        self.quick_recipes_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="View All Recipes",
            command=self._show_recipes,
            fg_color="#ff9500",
            hover_color="#e6850e",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        self.quick_about_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="About",
            command=self._show_about,
            fg_color="#9c27b0",
            hover_color="#7b1fa2",
            font=ctk.CTkFont(size=16),
            height=40
        )
        
        self.quick_help_btn = ctk.CTkButton(
            self.quick_actions_frame,
            text="How to Use",
            command=self._show_help,
            fg_color="#607d8b",
            hover_color="#455a64",
            font=ctk.CTkFont(size=16),
            height=40
        )
    
    def _setup_layout(self):
        # Sidebar layout - reduced padding
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(6, weight=1)  # Push exit button to bottom
        
        self.app_title.grid(row=0, column=0, padx=15, pady=(20, 25))
        
        self.dashboard_btn.grid(row=1, column=0, padx=15, pady=(0, 8), sticky="ew")
        self.ingredients_btn.grid(row=2, column=0, padx=15, pady=(0, 8), sticky="ew")
        self.recipes_btn.grid(row=3, column=0, padx=15, pady=(0, 8), sticky="ew")
        self.calculator_btn.grid(row=4, column=0, padx=15, pady=(0, 8), sticky="ew")
        self.about_btn.grid(row=5, column=0, padx=15, pady=(0, 8), sticky="ew")
        self.help_btn.grid(row=6, column=0, padx=15, pady=(0, 8), sticky="ew")
        
        self.exit_btn.grid(row=7, column=0, padx=15, pady=(0, 20), sticky="ew")
        
        # Main content area - reduced padding
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Dashboard layout
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        
        # Dashboard title and subtitle - reduced padding
        self.dashboard_title.grid(row=0, column=0, pady=(30, 8))
        self.dashboard_subtitle.grid(row=1, column=0, pady=(0, 30))
        
        # Stats frame - reduced padding
        self.stats_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew", padx=30)
        self.stats_frame.grid_columnconfigure(0, weight=1)
        self.stats_frame.grid_columnconfigure(1, weight=1)
        
        self.total_ingredients_label.grid(row=0, column=0, padx=20, pady=20)
        self.total_recipes_label.grid(row=0, column=1, padx=20, pady=20)
        
        # Quick actions frame - reduced padding
        self.quick_actions_frame.grid(row=3, column=0, pady=(0, 30), sticky="ew", padx=30)
        self.quick_actions_frame.grid_columnconfigure(0, weight=1)
        
        self.quick_actions_label.grid(row=0, column=0, pady=(15, 15))
        
        # Quick action buttons - reduced padding
        self.quick_ingredients_btn.grid(row=1, column=0, padx=30, pady=(0, 10), sticky="ew")
        self.quick_calculator_btn.grid(row=2, column=0, padx=30, pady=(0, 10), sticky="ew")
        self.quick_recipes_btn.grid(row=3, column=0, padx=30, pady=(0, 15), sticky="ew")
        self.quick_about_btn.grid(row=4, column=0, padx=30, pady=(0, 10), sticky="ew")
        self.quick_help_btn.grid(row=5, column=0, padx=30, pady=(0, 15), sticky="ew")
    
    def _show_dashboard(self):
        """Show dashboard view"""
        self._hide_current_frame()
        self._update_navigation_buttons("dashboard")
        self._update_dashboard_stats()
        self.dashboard_frame.grid()
        self.current_frame = self.dashboard_frame
    
    def _show_ingredients(self):
        """Show ingredients management view"""
        self._hide_current_frame()
        self._update_navigation_buttons("ingredients")
        
        ingredients_frame = IngredientsFrame(
            self.main_frame,
            self.data_handler,
            on_refresh_callback=self._on_data_refreshed
        )
        ingredients_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = ingredients_frame
    
    def _show_recipes(self):
        """Show recipes view"""
        self._hide_current_frame()
        self._update_navigation_buttons("recipes")
        
        recipes_frame = RecipesFrame(
            self.main_frame,
            self.data_handler,
            on_refresh_callback=self._on_data_refreshed
        )
        recipes_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = recipes_frame
    
    def _show_calculator(self):
        """Show calculator view"""
        self._hide_current_frame()
        self._update_navigation_buttons("calculator")
        
        calculator_frame = CalculatorFrame(
            self.main_frame,
            self.data_handler,
            on_refresh_callback=self._on_data_refreshed
        )
        calculator_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = calculator_frame
    
    def _show_about(self):
        """Show About view"""
        self._hide_current_frame()
        self._update_navigation_buttons("about")
        
        about_frame = AboutFrame(self.main_frame)
        about_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = about_frame
    
    def _show_help(self):
        """Show Help view"""
        self._hide_current_frame()
        self._update_navigation_buttons("help")
        
        help_frame = HelpFrame(self.main_frame)
        help_frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = help_frame
    
    def _hide_current_frame(self):
        """Hide the current active frame"""
        if self.current_frame:
            self.current_frame.grid_remove()
            self.current_frame = None
    
    def _update_navigation_buttons(self, active_view: str):
        """Update navigation button states"""
        # Reset all buttons to transparent
        buttons = {
            "dashboard": self.dashboard_btn,
            "ingredients": self.ingredients_btn,
            "recipes": self.recipes_btn,
            "calculator": self.calculator_btn,
            "about": self.about_btn,
            "help": self.help_btn
        }
        
        for btn in buttons.values():
            btn.configure(fg_color="transparent")
        
        # Set active button color
        if active_view in buttons:
            buttons[active_view].configure(fg_color="#4cafef")
    
    def _update_dashboard_stats(self):
        """Update dashboard statistics"""
        ingredients = self.data_handler.get_all_ingredients()
        recipes = self.data_handler.get_all_recipes()
        
        total_ingredients = len(ingredients)
        total_recipes = len(recipes)
        
        self.total_ingredients_label.configure(text=f"Total Ingredients: {total_ingredients}")
        self.total_recipes_label.configure(text=f"Total Recipes: {total_recipes}")
    
    def _on_data_refreshed(self):
        """Callback when data is refreshed"""
        self._update_dashboard_stats()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = FoodCostingCalculator()
    app.run()
