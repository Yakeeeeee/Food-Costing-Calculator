# Food Costing Calculator

A desktop application built with Python and CustomTkinter for managing ingredients, recipes, and calculating product costs including labor and overhead.

## Features
- Manage ingredients (add / edit / delete) with auto-calculated price-per-gram and cost-per-recipe
- Create recipes from ingredients, set Target Margin (%), compute suggested selling price and profit
- Save and export recipe costing reports (CSV)
- Modern dark UI using CustomTkinter
- CSV-based lightweight storage (no database)

## Installation

Option 1: Ready-to-Use EXE (Recommended for Windows Users)  
- Download the latest executable from the project's `dist/` folder
- To run: double-click the EXE:
  ```
  FoodCostingCalculator.exe
  ```
- If Windows blocks the file: right-click → Properties → Unblock (if present), then run again. For diagnostic output, run the EXE from an elevated command prompt.

Option 2 — Run from source (development)
Prerequisites
- Python 3.8 or higher
- pip

Setup
1. Clone or download the repository
2. Open a command prompt in the project folder
3. (Optional) Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run the app:
   ```powershell
   python main.py
   ```

Notes
- The EXE bundles Python and dependencies — no separate Python installation required for end users.
- Replace `FoodCostingCalculator.exe` with the actual EXE filename present in your `dist/` folder.

📱 Usage Guide

Getting Started
- Launch the application: Run the EXE from `dist/` or run `python main.py`.
- Open the Calculator: Navigate to the Calculator view to create recipes and run costing.
- Enter a Recipe Name and set Target Margin (%) (default is 150).

Creating Recipes
- Select Ingredients: Choose existing ingredients from the checklist.
- Add New Ingredient: Use the Add New Ingredient form to add a temporary ingredient to the current recipe (optionally saved when saving the recipe).
- Set Grams Needed: Specify grams needed per recipe for each ingredient.
- Calculate: Click "Calculate Cost" to view breakdown without saving.
- Calculate & Save: Click "Calculate & Save" to persist the recipe to `recipes.csv`.

Adding / Managing Ingredients
- Add Ingredient: Use the Ingredients view to add a new ingredient to the database with Price and Grams (price-per-gram and cost-per-recipe auto-calculated).
- Edit / Delete: Edit existing ingredients or delete them from the Ingredients view.
- Search: Use the search field to quickly filter ingredients.

Managing Saved Recipes
- View Details: Open a saved recipe to see ingredients used and full cost breakdown.
- Delete: Remove a saved recipe; deletion persists to `recipes.csv`.
- Export: Export recipe costing to CSV using the export option.

Analyzing Data
- Use the Recipes view to scan saved recipes, view suggested selling prices and profits.
- Export data for external analysis as needed.

## File Layout (project root)
- main.py
- data_handler.py
- ui_dashboard.py
- ui_ingredients.py
- ui_recipes.py
- ui_calculator.py
- requirements.txt
- README.md
- ingredients.csv (auto-created)
- recipes.csv (auto-created)
- dist/ (prebuilt EXE(s) — place the executable here for distribution)

## CSV Schemas
- Ingredients CSV headers:
  Ingredient Name, Price, Grams, Price per Gram, Grams Needed in Recipe, Cost per Recipe
- Recipes CSV headers:
  Recipe Name, Total Ingredient Cost, Miscellaneous Cost (50%), Labor Cost (45%), Total Cost, Suggested Selling Price, Margin Percentage, Profit, Ingredients Used

## Cost Formula
1. Total Ingredient Cost = sum of ingredient "Cost per Recipe"  
2. Miscellaneous Cost = 50% of Total Ingredient Cost  
3. Labor Cost = 45% of Total Ingredient Cost  
4. Total Cost = Total Ingredient Cost + Misc + Labor  
5. Suggested Selling Price = Total Cost × (1 + Margin%/100)  
6. Profit = Suggested Selling Price − Total Cost

Default Target Margin (%) = 150 (2.5×)

## Troubleshooting
- Ensure dependencies installed when running from source.
- Close programs (e.g., Excel) that lock CSV files before running the app.
- If saved recipes show numeric values where ingredient names should be, verify `recipes.csv` headers; a migration helper can be

## 🤝 Contributing

This application was developed by **John Allen Esteleydes**. For support, questions, or contributions:

- **Email**: esteleydesjohnallen0@gmail.com
- **YouTube**: [Yakee](https://www.youtube.com/@mr.yakeee)
- **Github**: [Yakeeeeee](https://github.com/Yakeeeeee)
---

## 📋 System Requirements

- **Operating System**: Windows 10/11 (64-bit recommended), recent macOS (10.14+) or modern Linux distribution
- **Python**: 3.8 or higher only required when running from source; not required for the Windows EXE
- **Memory**: 512 MB minimum, 1 GB recommended
- **Storage**: 100 MB free minimum (200 MB recommended to allow for data and exports)
- **Display**: 1200×800 minimum resolution (1366×768 or higher recommended)

- **Notes**:
  - The bundled EXE includes Python and dependencies; use it if you do not want to install Python.
  - If you encounter issues, run the EXE or Python entry script from a terminal to view logs for troubleshooting.
---

## 📄 License

This project is open source and available under the MIT License.

## 🔮 Future Enhancements

- **Sync & Backup**: Optional cloud backup with user-controlled sync, local export/import, and encrypted storage options.
- **Mobile Companion App**: Lightweight cross-platform mobile app for viewing recipes, quick costing, and scanning ingredients.
- **Advanced Reporting & Export**: PDF/CSV report generation, scheduled or on-demand email reports, and customizable templates.
- **Multi-currency & Localization**: Currency selection, exchange-rate support, and locale-aware number/date formatting.
- **Reminders & Notifications**: Optional scheduled reminders and local notifications for due dates or inventory thresholds.
- **Integrations & Extensibility**: CSV/API import-export, plugin hooks, and connectors for accounting, POS, or inventory systems.

---

**Built by John Allen Esteleydes**


