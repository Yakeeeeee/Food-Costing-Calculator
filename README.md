---

# 🍴 Food Costing Calculator

A **desktop application** built with **Python** and **CustomTkinter** for managing ingredients, recipes, and calculating product costs — including **labor and overhead** — with a modern lightweight design.

---

## ✨ Features

* **Ingredient Management**

  * Add, edit, and delete ingredients
  * Auto-calculated *price per gram* and *cost per recipe*

* **Recipe Management**

  * Create recipes using saved ingredients
  * Set **Target Margin (%)** and compute suggested selling price
  * Save recipes with full cost breakdown

* **Costing & Analysis**

  * View ingredient cost, labor, and overhead
  * Auto-suggested selling price with profit calculation
  * Export reports to **CSV** for analysis

* **UI & Storage**

  * Modern **dark mode UI** with CustomTkinter
  * **CSV-based storage** (lightweight, no database needed)

---

## 🚀 Installation

### Option 1: Ready-to-Use EXE (Recommended for Windows)

1. Download the latest executable from the `dist/` folder.
2. Run the application by double-clicking:

   ```bash
   FoodCostingCalculator.exe
   ```
3. If Windows blocks the file:

   * Right-click → **Properties** → **Unblock** → Run again.
   * For logs, run the EXE via an elevated command prompt.

✅ No Python installation required.

---

### Option 2: Run from Source (Development)

#### Prerequisites

* Python **3.8+**
* pip (Python package manager)

#### Setup

```powershell
# 1. Clone or download this repository
git clone https://github.com/Yakeeeeee/FoodCostingCalculator.git
cd FoodCostingCalculator

# 2. (Optional) Create & activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

---

## 📖 Usage Guide

### Getting Started

* **Launch** the application (`EXE` or `python main.py`).
* Navigate to the **Calculator** view.
* Enter a **Recipe Name** and **Target Margin (%)** (default: 150%).

### Creating Recipes

1. **Select Ingredients** from the checklist.
2. **Add New Ingredient** if needed (temporary or saved).
3. Enter **grams needed per recipe**.
4. Click:

   * **Calculate Cost** → view breakdown (not saved).
   * **Calculate & Save** → store recipe in `recipes.csv`.

### Managing Ingredients

* **Add** new ingredient with price & grams.
* **Edit/Delete** existing ingredients.
* **Search** ingredients quickly.

### Managing Saved Recipes

* **View Details** → see full breakdown.
* **Delete** → remove recipe from `recipes.csv`.
* **Export** → save costing report to CSV.

---

## 📂 Project Structure

```
📦 FoodCostingCalculator
 ┣ main.py
 ┣ data_handler.py
 ┣ ui_dashboard.py
 ┣ ui_ingredients.py
 ┣ ui_recipes.py
 ┣ ui_calculator.py
 ┣ requirements.txt
 ┣ README.md
 ┣ ingredients.csv   # Auto-created
 ┣ recipes.csv       # Auto-created
 ┗ dist/             # Prebuilt executables
```

---

## 📊 CSV Schemas

### Ingredients (`ingredients.csv`)

\| Ingredient Name | Price | Grams | Price per Gram | Grams Needed in Recipe | Cost per Recipe |

### Recipes (`recipes.csv`)

\| Recipe Name | Total Ingredient Cost | Miscellaneous Cost (50%) | Labor Cost (45%) | Total Cost | Suggested Selling Price | Margin Percentage | Profit | Ingredients Used |

---

## 🧮 Costing Formula

1. **Total Ingredient Cost** = Σ(ingredient cost per recipe)
2. **Miscellaneous Cost** = 50% × Total Ingredient Cost
3. **Labor Cost** = 45% × Total Ingredient Cost
4. **Total Cost** = Ingredients + Miscellaneous + Labor
5. **Selling Price** = Total Cost × (1 + Margin% ÷ 100)
6. **Profit** = Selling Price − Total Cost

➡️ Default **Target Margin = 150%** (2.5×)

---

## 🛠 Troubleshooting

* CSV locked? → Close Excel or other apps using it.
* Missing data in recipes? → Check CSV headers.
* EXE not running? → Run via **Command Prompt** to see logs.

---

## 🤝 Contributing

Developed by **John Allen Esteleydes**.

* 📧 Email: [esteleydesjohnallen0@gmail.com](mailto:esteleydesjohnallen0@gmail.com)
* 🎥 YouTube: [Yakee](https://www.youtube.com/@mr.yakeee)
* 💻 GitHub: [Yakeeeeee](https://github.com/Yakeeeeee)

---

## 💻 System Requirements

* **OS**: Windows 10/11 (64-bit), macOS 10.14+, or Linux
* **Python**: 3.8+ (only for source build)
* **Memory**: 512 MB (1 GB recommended)
* **Storage**: 100 MB minimum (200 MB recommended)
* **Display**: 1200×800 minimum (1366×768+ recommended)

---

## 📄 License

Licensed under the **MIT License**.

---

## 🔮 Roadmap / Future Enhancements

* ☁️ **Sync & Backup**: Cloud backup, encrypted local storage
* 📱 **Mobile Companion App**: Quick costing, ingredient scanning
* 📑 **Advanced Reporting**: PDF/CSV reports, email export
* 💱 **Multi-currency & Localization**
* 🔔 **Reminders & Notifications**
* 🔌 **Integrations**: POS, accounting, API connectors

---

👨‍💻 **Built with passion by John Allen Esteleydes**

---

