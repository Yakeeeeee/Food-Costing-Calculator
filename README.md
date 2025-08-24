# Food Costing Calculator

A comprehensive desktop application built with Python and CustomTkinter for managing food ingredients, recipes, and calculating detailed product costs including labor and overhead expenses.

## Features

### 🏠 Dashboard
- **Overview**: Welcome screen with application statistics
- **Quick Stats**: Total ingredients count and total recipes count
- **Quick Actions**: Fast access to main features

### 🥘 Ingredients Management
- **Ingredient Database**: Add, edit, and delete ingredients with detailed pricing
- **Fields Include**:
  - Ingredient Name
  - Price (total cost)
  - Grams (total quantity)
  - Price per Gram (auto-calculated)
  - Grams Needed in Recipe
  - Cost per Recipe (auto-calculated)
- **Search & Filter**: Find ingredients quickly
- **Real-time Updates**: Automatic calculations and validation

### 📋 Recipes View
- **Saved Recipes**: View all saved recipes with detailed costing
- **Cost Breakdown**: See ingredient costs, labor costs, and miscellaneous expenses
- **Detailed View**: Click "View Details" for comprehensive recipe analysis
- **Search Functionality**: Find recipes by name

### 🧮 Food Costing Calculator
- **Recipe Creation**: Input recipe name and select ingredients
- **Ingredient Selection**: Choose from existing ingredients or add new ones
- **New Ingredient Addition**: Add ingredients not yet in the system
- **Cost Calculation**: Automatic calculation including:
  - Total Ingredient Cost
  - Miscellaneous Cost (50% of ingredient cost)
  - Labor Cost (45% of ingredient cost)
  - Total Cost
- **Suggested Selling Price**: Computed using the Target Margin (%) entered in the Calculator (default 150% → 2.5×)
- **Profit Margin**
- **Two Modes**:
  - **Calculate Cost**: Calculate without saving
  - **Calculate & Save**: Calculate and save recipe to database

## Technical Features

- **Dark Mode UI**: Modern dark theme with accent colors
- **Card-based Design**: Clean, organized interface layout
- **CSV Storage**: Simple data persistence without database
- **Responsive Layout**: Adapts to different window sizes
- **Error Handling**: Comprehensive validation and user feedback
- **Auto-calculations**: Automatic price per gram and cost per recipe calculations

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup
1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies
- `customtkinter==5.2.0` - Modern Tkinter widgets
- `Pillow==10.0.1` - Image processing (required by CustomTkinter)

## Usage

### Starting the Application
```bash
python main.py
```

### Navigation
- Use the sidebar navigation to switch between different views
- The active view is highlighted in blue
- All views maintain their state when switching

### Managing Ingredients
1. Navigate to "Ingredients" from the sidebar
2. Add new ingredients with:
   - Ingredient Name (required)
   - Price (total cost in dollars)
   - Grams (total quantity)
   - Grams Needed in Recipe
3. Use "Add Ingredient" to save
4. Edit or delete existing ingredients as needed
5. Use search to find specific ingredients

### Creating and Calculating Recipe Costs
1. Navigate to "Calculator"
2. Enter recipe name
3. Select ingredients from the checklist
4. Optionally add new ingredients not in the system
5. Set the "Target Margin (%)" to control automatic pricing (default 150 → 2.5×)
6. Choose calculation mode:
   - **Calculate Cost**: See breakdown without saving
   - **Calculate & Save Recipe**: Save recipe to database

### Viewing Saved Recipes
1. Go to "Recipes" to see all saved recipes
2. Use search to filter recipes
3. Click "View Details" for comprehensive cost breakdown
4. See ingredient costs, labor costs, and profit margins

## File Structure

```
Food Costing Calculator/
├── main.py              # Main application entry point
├── data_handler.py      # CSV data management and calculations
├── ui_dashboard.py      # Dashboard UI module
├── ui_ingredients.py    # Ingredients management UI module
├── ui_recipes.py        # Recipes view UI module
├── ui_calculator.py     # Cost calculator UI module
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── ingredients.csv     # Ingredients database (created automatically)
└── recipes.csv         # Saved recipes database (created automatically)
```

## Data Storage

### Ingredients CSV
- **Headers**: Ingredient Name, Price, Grams, Price per Gram, Grams Needed in Recipe, Cost per Recipe
- **Auto-creation**: File created automatically on first run
- **Calculations**: Price per gram and cost per recipe calculated automatically

### Recipes CSV
- **Headers**: Recipe Name, Total Ingredient Cost, Miscellaneous Cost (50%), Labor Cost (45%), Total Cost, Suggested Selling Price, Profit, Ingredients Used
- **Auto-creation**: File created automatically on first run
- **Cost Structure**: Includes labor and overhead calculations

## Cost Calculation Formula

The application uses a comprehensive cost calculation system:

1. **Total Ingredient Cost** = Sum of all ingredient costs for the recipe
2. **Miscellaneous Cost** = 50% of Total Ingredient Cost
3. **Labor Cost** = 45% of Total Ingredient Cost
4. **Total Cost** = Total Ingredient Cost + Miscellaneous Cost + Labor Cost
5. **Suggested Selling Price** = Total Cost × (1 + Margin%/100)
   - The Calculator exposes a "Target Margin (%)" field. Default is 150 (which results in a 2.5× multiplier).
6. **Profit** = Suggested Selling Price - Total Cost

## Customization

### Colors
The application uses a consistent color scheme:
- **Background**: #1e1e1e (dark)
- **Cards**: #2d2d2d (medium dark)
- **Accent**: #4cafef (blue)
- **Success**: #28a745 (green)
- **Warning**: #ff9500 (orange)
- **Error**: #ff6b6b (red)

### Window Size
Default window size is 1400x900 pixels, but the application is responsive and adapts to different sizes.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **CSV Errors**: Check file permissions and ensure CSV files aren't open in other applications
3. **UI Issues**: Try resizing the window or restarting the application
4. **Calculation Errors**: Verify that all numeric inputs are valid numbers

### Performance
- Large datasets may slow down the ingredients and recipes screens
- Consider archiving old data for better performance

## Future Enhancements

Potential improvements for future versions:
- Recipe templates and categories
- Cost history tracking
- Multiple currency support
- Recipe scaling (different batch sizes)
- Ingredient inventory management
- Backup and restore features
- User preferences and settings
- Export to PDF reports

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Ensure all dependencies are correctly installed
4. Verify CSV file permissions

### Tips and Best Practices
- Keep ingredient prices updated for accurate calculations
- Use descriptive recipe names for easy identification
- Regularly review and update your ingredient database
- Default markup is 150% (2.5×). Adjust the Target Margin (%) in the Calculator to suit your business needs
- Use the search function to quickly find ingredients and recipes
- Export your data regularly for backup purposes

---

**Note**: This application is designed for desktop use and requires a graphical interface. It's not suitable for headless servers or command-line-only environments.

