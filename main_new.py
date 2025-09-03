import customtkinter as ctk
import os
from core.data_handler import DataHandler
from ui_new.dashboard import DashboardPage
from ui_new.ingredients import IngredientsPage
from ui_new.recipes import RecipesPage
from ui_new.calculator import CalculatorPage
from ui_new.packaging import PackagingPage
from ui_new.about import AboutPage
from ui_new.help_page import HelpPage

class FoodCostingApp:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize data handler
        self.data_handler = DataHandler()
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Food Costing Calculator - Professional Edition")
        self.root.geometry("1600x1000")
        self.root.configure(fg_color="#1a1a1a")
        
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Current active page
        self.current_page = None
        self.pages = {}
        
        self._create_widgets()
        self._setup_layout()
        
        # Bind mouse wheel events for global scrolling
        self.root.bind("<MouseWheel>", self._on_mouse_wheel) # For Windows and macOS
        self.root.bind("<Button-4>", self._on_mouse_wheel)   # For Linux scroll up
        self.root.bind("<Button-5>", self._on_mouse_wheel)   # For Linux scroll down
        
        # Show dashboard by default
        self._show_page("dashboard")
    
    def _create_widgets(self):
        # Create modern sidebar
        self._create_sidebar()
        
        # Create main content area
        self._create_main_content()
        
        # Initialize all pages
        self._initialize_pages()
    
    def _create_sidebar(self):
        # Sidebar container
        self.sidebar = ctk.CTkFrame(
            self.root, 
            fg_color="#2d2d2d", 
            corner_radius=0,
            width=280
        )
        
        # App logo and title
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        self.app_title = ctk.CTkLabel(
            self.logo_frame,
            text="🍽️ Food Costing",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4cafef"
        )
        
        self.app_subtitle = ctk.CTkLabel(
            self.logo_frame,
            text="Professional Calculator",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        
        # Navigation menu
        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        # Navigation buttons with icons
        self.nav_buttons = {}
        
        nav_items = [
            ("dashboard", "📊 Dashboard", self._show_dashboard),
            ("ingredients", "🥕 Ingredients", self._show_ingredients),
            ("recipes", "📝 Recipes", self._show_recipes),
            ("packaging", "📦 Packaging", self._show_packaging),
            ("calculator", "🧮 Calculator", self._show_calculator),
            ("help", "❓ Help", self._show_help),
            ("about", "ℹ️ About", self._show_about)
        ]
        
        for i, (key, text, command) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.nav_frame,
                text=text,
                command=command,
                fg_color="transparent",
                hover_color="#3d3d3d",
                font=ctk.CTkFont(size=16),
                height=50,
                anchor="w",
                text_color="#ffffff"
            )
            self.nav_buttons[key] = btn
        
        # Exit button
        self.exit_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Exit Application",
            command=self.root.quit,
            fg_color="#ff6b6b",
            hover_color="#e55555",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50
        )
    
    def _create_main_content(self):
        # Main content area
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Header
        self.header = ctk.CTkFrame(self.main_frame, fg_color="#2d2d2d", height=80)
        
        self.page_title = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
    
    def _initialize_pages(self):
        """Initialize all application pages"""
        # Create a unified refresh callback for all data-dependent pages
        def _refresh_all_data_pages():
            if "dashboard" in self.pages and hasattr(self.pages["dashboard"], 'refresh_stats'):
                self.pages["dashboard"].refresh_stats()
            if "ingredients" in self.pages and hasattr(self.pages["ingredients"], 'refresh_ingredients'):
                self.pages["ingredients"].refresh_ingredients()
            if "packaging" in self.pages and hasattr(self.pages["packaging"], 'refresh_materials'):
                self.pages["packaging"].refresh_materials()
            if "recipes" in self.pages and hasattr(self.pages["recipes"], '_refresh_recipes'):
                self.pages["recipes"]._refresh_recipes()
            if "calculator" in self.pages and hasattr(self.pages["calculator"], '_refresh_data'):
                self.pages["calculator"]._refresh_data()

        # Initialize pages, passing the unified refresh callback
        self.pages = {
            "dashboard": DashboardPage(self.content_frame, self.data_handler, _refresh_all_data_pages),
            "ingredients": IngredientsPage(self.content_frame, self.data_handler, _refresh_all_data_pages),
            "recipes": RecipesPage(self.content_frame, self.data_handler, _refresh_all_data_pages),
            "packaging": PackagingPage(self.content_frame, self.data_handler, _refresh_all_data_pages),
            "calculator": CalculatorPage(self.content_frame, self.data_handler, _refresh_all_data_pages),
            "help": HelpPage(self.content_frame),
            "about": AboutPage(self.content_frame)
        }
    
    def _setup_layout(self):
        # Sidebar layout
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(2, weight=1)  # Push exit button to bottom
        self.sidebar.grid_columnconfigure(0, weight=1)
        
        # Logo frame
        self.logo_frame.grid(row=0, column=0, padx=20, pady=(30, 40), sticky="ew")
        self.app_title.pack(pady=(0, 5))
        self.app_subtitle.pack()
        
        # Navigation frame
        self.nav_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.nav_frame.grid_columnconfigure(0, weight=1)
        
        # Navigation buttons
        for i, (key, btn) in enumerate(self.nav_buttons.items()):
            btn.grid(row=i, column=0, padx=0, pady=(0, 10), sticky="ew")
        
        # Exit button
        self.exit_btn.grid(row=2, column=0, padx=20, pady=(0, 30), sticky="ew")
        
        # Main content layout
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_rowconfigure(0, weight=1)
        
        self.page_title.grid(row=0, column=0, padx=30, pady=(20, 5), sticky="w")
        
        
        # Content frame
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def _show_page(self, page_name: str):
        """Show the specified page"""
        if self.current_page:
            self.current_page.grid_remove()
        
        if page_name in self.pages:
            self.current_page = self.pages[page_name]
            self.current_page.grid(row=0, column=0, sticky="nsew")
            self._update_navigation(page_name)
            # Trigger a refresh for the newly shown page if it's a data page
            if page_name == "ingredients" and hasattr(self.current_page, 'refresh_ingredients'):
                self.current_page.refresh_ingredients()
            elif page_name == "packaging" and hasattr(self.current_page, 'refresh_materials'):
                self.current_page.refresh_materials()
            elif page_name == "recipes" and hasattr(self.current_page, '_refresh_recipes'):
                self.current_page._refresh_recipes()
            elif page_name == "dashboard" and hasattr(self.current_page, 'refresh_stats'):
                self.current_page.refresh_stats()
            elif page_name == "calculator" and hasattr(self.current_page, '_refresh_data'):
                self.current_page._refresh_data()
    
    def _show_dashboard(self):
        self._show_page("dashboard")
        self.page_title.configure(text="📊 Dashboard")
        
    
    def _show_ingredients(self):
        self._show_page("ingredients")
        self.page_title.configure(text="🥕 Ingredients")
        
    
    def _show_recipes(self):
        self._show_page("recipes")
        self.page_title.configure(text="📝 Recipes")
        
    
    def _show_packaging(self):
        self._show_page("packaging")
        self.page_title.configure(text="📦 Packaging")
        
    
    def _show_calculator(self):
        self._show_page("calculator")
        self.page_title.configure(text="🧮 Calculator")
        
    
    def _show_help(self):
        self._show_page("help")
        self.page_title.configure(text="❓ Help & Guide")
        
    
    def _show_about(self):
        self._show_page("about")
        self.page_title.configure(text="ℹ️ About")
        
    
    def _update_navigation(self, active_page: str):
        """Update navigation button states"""
        for key, btn in self.nav_buttons.items():
            if key == active_page:
                btn.configure(fg_color="#4cafef", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color="#ffffff")
    
    # Removed _update_stats as its functionality is now integrated into _refresh_all_data_pages
    # def _update_stats(self):
    #     """Update dashboard statistics"""
    #     if "dashboard" in self.pages:
    #         self.pages["dashboard"].refresh_stats()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

    def _on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling for the current page's scrollable frame."""
        if self.current_page and hasattr(self.current_page, 'winfo_children'):
            # Iterate through children to find a CTkScrollableFrame
            for widget in self.current_page.winfo_children():
                if isinstance(widget, ctk.CTkScrollableFrame):
                    # Determine scroll direction and amount
                    if event.num == 4 or event.delta > 0:  # Scroll up
                        widget._parent_canvas.yview_scroll(-1, "units")
                    elif event.num == 5 or event.delta < 0:  # Scroll down
                        widget._parent_canvas.yview_scroll(1, "units")
                    break # Only scroll the first scrollable frame found

if __name__ == "__main__":
    app = FoodCostingApp()
    app.run()
