# 🍽️ Food Costing Calculator - Professional Edition

A modern, user-friendly application for calculating recipe costs and managing food business finances. Built with Python and CustomTkinter for a beautiful, intuitive interface.

## ✨ Features

### 🥕 Ingredient Management
- Add, edit, and delete ingredients with accurate pricing
- Track ingredient quantities and costs per recipe
- Search and filter ingredients quickly
- Automatic price per gram calculations

### 📦 Packaging Management
- Manage packaging materials and their costs
- Track quantities and unit costs
- Include packaging in recipe calculations
- Search and organize packaging materials

### 🧮 Smart Recipe Calculator
- Calculate total recipe costs including ingredients, packaging, and labor
- Customizable profit margins (50% to 300%+)
- Optional VAT calculations (12% for Philippines)
- Real-time cost breakdown and profit analysis

### 📝 Recipe Storage
- Save and organize your recipe costings
- View detailed cost breakdowns
- Search and manage saved recipes
- Export recipe data for backup

### 📊 Dashboard & Analytics
- Overview of your ingredient and recipe database
- Quick statistics and insights
- Easy navigation to all features
- Professional tips and guidance

### 🎯 User-Friendly Interface
- Modern, dark-themed UI
- Intuitive navigation with icons
- Responsive design
- Beginner-friendly with comprehensive help system

## 🚀 Quick Start

### Prerequisites
- Windows (recommended), macOS, or Linux

### Installation

#### Option 1: Download the Executable (Windows Only)
1. Download `Food Costing Calculator.exe` from the `dist` folder.
2. Double-click to launch the application—no installation required!

#### Option 2: Run from Source (Python 3.8+ Required)
1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd FoodCostingCalculator
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**
   ```bash
   python run_app.py
   ```
   Or run the new version directly:
   ```bash
   python main_new.py
   ```

## 📖 How to Use

### 1. Getting Started
- Launch the application
- Start with the Dashboard to get an overview
- Add your first ingredients and packaging materials

### 2. Adding Ingredients
1. Go to **🥕 Ingredients** section
2. Fill in ingredient details:
   - Name (e.g., "All-Purpose Flour")
   - Price (e.g., ₱45.50)
   - Total grams (e.g., 1000g for 1kg)
   - Grams per recipe (e.g., 250g)
3. Click "Save Ingredient"

### 3. Adding Packaging Materials
1. Go to **📦 Packaging** section
2. Fill in packaging details:
   - Material name (e.g., "Plastic Container")
   - Total price (e.g., ₱150.00)
   - Quantity (e.g., 100 pieces)
3. Click "Save Material"

### 4. Calculating Recipe Costs
1. Go to **🧮 Calculator** section
2. Enter recipe information:
   - Recipe name
   - Target margin percentage (50% recommended)
   - Include VAT if applicable
3. Select ingredients and packaging materials
4. Click "Calculate Recipe Cost"
5. Review the cost breakdown
6. Save the recipe

### 5. Managing Recipes
- Go to **📝 Recipes** section
- View all saved recipes
- Search and filter recipes
- Delete recipes as needed

## 💡 Profit Margin Guidelines

- **100% Margin** = 2x markup (50% profit margin)
- **50% Margin** = 1.5x markup (33.3% profit margin) - **RECOMMENDED**
- **200% Margin** = 3x markup (66.7% profit margin)
- **300% Margin** = 4x markup (75% profit margin)

## 📊 Cost Breakdown

The application calculates:
- **Ingredient Cost**: Sum of all selected ingredients
- **Packaging Cost**: Sum of all selected packaging materials
- **Labor Cost**: 50% of ingredient cost (industry standard)
- **VAT**: 12% of total cost (optional, Philippines)
- **Total Cost**: All costs combined
- **Suggested Selling Price**: Total cost + profit margin
- **Profit**: Difference between selling price and total cost

## 🔧 Technical Details

### Technology Stack
- **Python 3.8+**
- **CustomTkinter** - Modern GUI framework
- **CSV Data Storage** - Simple, portable data format

### Data Storage
The application automatically creates and manages:
- `data/ingredients.csv` - Ingredient database
- `data/recipes.csv` - Saved recipe costings
- `data/packaging.csv` - Packaging materials
- `data/price_history.csv` - Price change tracking

### File Structure
```
FoodCostingCalculator/
├── dist/
│   └── Food Costing Calculator.exe   # Windows executable
├── main_new.py                      # New main application
├── run_app.py                       # Launcher script
├── core/
│   └── data_handler.py              # Data management
├── ui_new/                          # New UI components
│   ├── dashboard.py                 # Dashboard page
│   ├── ingredients.py               # Ingredients management
│   ├── packaging.py                 # Packaging management
│   ├── calculator.py                # Recipe calculator
│   ├── recipes.py                   # Recipe storage
│   ├── about.py                     # About page
│   └── help_page.py                 # Help and guide
├── data/                            # Data files (auto-created)
│   ├── ingredients.csv
│   ├── recipes.csv
│   ├── packaging.csv
│   └── price_history.csv
└── requirements.txt                 # Dependencies
```

## 🆕 What's New in Version 2.0

### ✨ Complete UI Redesign
- Modern, professional interface
- Dark theme with accent colors
- Intuitive navigation with icons
- Responsive layout

### 🎯 Enhanced User Experience
- Step-by-step guidance
- Comprehensive help system
- Better error handling
- Improved data validation

### 📊 Better Data Management
- Automatic data folder creation
- Improved search functionality
- Better data organization
- Enhanced recipe storage

### 🧮 Improved Calculator
- More intuitive ingredient selection
- Better packaging integration
- Clearer cost breakdowns
- Enhanced profit analysis

## 💡 Best Practices

### Accurate Pricing
- Update ingredient prices regularly
- Use actual purchase prices, not estimates
- Include all costs (delivery, taxes, etc.)

### Recipe Standardization
- Use consistent measurements (grams)
- Document exact quantities for each ingredient
- Consider yield and waste in calculations

### Profit Margin Strategy
- Start with 50% margin for most items
- Adjust based on market competition
- Consider seasonal price fluctuations

### Regular Reviews
- Review costs monthly
- Update prices when suppliers change rates
- Monitor profit margins and adjust as needed

## 🤝 Contributing

This application is designed to help food businesses make better pricing decisions. If you have suggestions for improvements or find any issues, please feel free to contribute!

## 📄 License

This project is open source and available under the MIT License.

---
