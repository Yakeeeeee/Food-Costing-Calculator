import csv
import os
from typing import List, Dict, Optional
import uuid

class DataHandler:
    def __init__(self):
        # Create data directory if it doesn't exist
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.ingredients_file = os.path.join(self.data_dir, "ingredients.csv")
        self.recipes_file = os.path.join(self.data_dir, "recipes.csv")
        self.packaging_file = os.path.join(self.data_dir, "packaging.csv")
        self.price_history_file = os.path.join(self.data_dir, "price_history.csv") # New: Price history file
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create CSV files with headers if they don't exist"""
        # Ingredients file
        if not os.path.exists(self.ingredients_file):
            with open(self.ingredients_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Ingredient Name", "Price", "Grams", "Price per Gram",
                    "Grams Needed in Recipe", "Cost per Recipe"
                ])
            # Add sample ingredients if the file was just created
            if os.stat(self.ingredients_file).st_size == 0: # Check if file is empty (only header)
                self.add_ingredient({"Ingredient Name": "Flour", "Price": "50.00", "Grams": "1000", "Grams Needed in Recipe": "250"})
                self.add_ingredient({"Ingredient Name": "Sugar", "Price": "75.00", "Grams": "500", "Grams Needed in Recipe": "100"})
                self.add_ingredient({"Ingredient Name": "Eggs", "Price": "120.00", "Grams": "600", "Grams Needed in Recipe": "150"})
        
        # Recipes file
        if not os.path.exists(self.recipes_file):
            with open(self.recipes_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Include Margin Percentage so saved recipes record the Target Margin used
                writer.writerow([
                    "Recipe ID", "Recipe Name", "Total Ingredient Cost", "Packaging Cost",
                    "Labor Cost (50%)", "VAT Percentage", "Currency", "Total Cost", "Suggested Selling Price",
                    "Margin Percentage", "Profit", "Ingredients Used", "Packaging Materials Used"
                ])
        
        # Packaging file
        if not os.path.exists(self.packaging_file):
            with open(self.packaging_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Material Name", "Price", "Quantity", "Unit Cost", "Total Cost"
                ])
            # Add sample packaging materials if the file was just created
            if os.stat(self.packaging_file).st_size == 0: # Check if file is empty (only header)
                self.add_packaging_material({"Material Name": "Plastic Container", "Price": "150.00", "Quantity": "10"})
                self.add_packaging_material({"Material Name": "Paper Bag (Small)", "Price": "50.00", "Quantity": "20"})
        
        # Price History file (New)
        if not os.path.exists(self.price_history_file):
            with open(self.price_history_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Ingredient Name", "Old Price", "New Price", "Change Date"
                ])
    
    # ===== INGREDIENTS MANAGEMENT =====
    
    def add_ingredient(self, ingredient_data: Dict[str, str]) -> bool:
        """Add a new ingredient to the CSV file"""
        try:
            # Calculate price per gram
            price = float(ingredient_data.get("Price", 0))
            grams = float(ingredient_data.get("Grams", 0))
            price_per_gram = price / grams if grams > 0 else 0
            
            # Calculate cost per recipe
            grams_needed = float(ingredient_data.get("Grams Needed in Recipe", 0))
            cost_per_recipe = price_per_gram * grams_needed
            
            # Prepare row data
            row_data = [
                ingredient_data.get("Ingredient Name", ""),
                price,
                grams,
                round(price_per_gram, 4),
                grams_needed,
                round(cost_per_recipe, 2)
            ]
            
            with open(self.ingredients_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row_data)
            return True
        except Exception as e:
            print(f"Error adding ingredient: {e}")
            return False
    
    def get_all_ingredients(self) -> List[Dict[str, str]]:
        """Retrieve all ingredients from the CSV file"""
        ingredients = []
        try:
            with open(self.ingredients_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    ingredients.append(row)
        except Exception as e:
            print(f"Error reading ingredients: {e}")
        return ingredients
    
    def update_ingredient(self, index: int, ingredient_data: Dict[str, str]) -> bool:
        """Update an existing ingredient at the specified index"""
        try:
            ingredients = self.get_all_ingredients()
            if 0 <= index < len(ingredients):
                old_ingredient = ingredients[index]
                old_price = float(old_ingredient.get("Price", 0))
                
                # Calculate price per gram
                price = float(ingredient_data.get("Price", 0))
                grams = float(ingredient_data.get("Grams", 0))
                price_per_gram = price / grams if grams > 0 else 0
                
                # Calculate cost per recipe
                grams_needed = float(ingredient_data.get("Grams Needed in Recipe", 0))
                cost_per_recipe = price_per_gram * grams_needed
                
                # Update ingredient data
                ingredients[index] = {
                    "Ingredient Name": ingredient_data.get("Ingredient Name", ""),
                    "Price": price,
                    "Grams": grams,
                    "Price per Gram": round(price_per_gram, 4),
                    "Grams Needed in Recipe": grams_needed,
                    "Cost per Recipe": round(cost_per_recipe, 2)
                }
                
                # Log price change if price has changed
                if price != old_price:
                    self._log_price_change(
                        ingredient_data.get("Ingredient Name", ""),
                        old_price,
                        price
                    )
                
                # Rewrite the entire file
                with open(self.ingredients_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=[
                        "Ingredient Name", "Price", "Grams", "Price per Gram",
                        "Grams Needed in Recipe", "Cost per Recipe"
                    ])
                    writer.writeheader()
                    writer.writerows(ingredients)
                return True
        except Exception as e:
            print(f"Error updating ingredient: {e}")
        return False
    
    def delete_ingredient(self, index: int) -> bool:
        """Delete an ingredient at the specified index"""
        try:
            ingredients = self.get_all_ingredients()
            if 0 <= index < len(ingredients):
                ingredients.pop(index)
                
                # Rewrite the entire file
                with open(self.ingredients_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=[
                        "Ingredient Name", "Price", "Grams", "Price per Gram",
                        "Grams Needed in Recipe", "Cost per Recipe"
                    ])
                    writer.writeheader()
                    writer.writerows(ingredients)
                return True
        except Exception as e:
            print(f"Error deleting ingredient: {e}")
        return False
    
    def search_ingredients(self, query: str) -> List[Dict[str, str]]:
        """Search ingredients by name"""
        if not query.strip():
            return self.get_all_ingredients()
        
        query = query.lower()
        ingredients = self.get_all_ingredients()
        filtered_ingredients = []
        
        for ingredient in ingredients:
            if query in ingredient.get("Ingredient Name", "").lower():
                filtered_ingredients.append(ingredient)
        
        return filtered_ingredients
    
    def _log_price_change(self, ingredient_name: str, old_price: float, new_price: float):
        """Log an ingredient price change to price_history.csv"""
        from datetime import datetime
        try:
            with open(self.price_history_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    ingredient_name,
                    f"{old_price:.2f}",
                    f"{new_price:.2f}",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
        except Exception as e:
            print(f"Error logging price change: {e}")

    def get_price_history(self, ingredient_name: str) -> List[Dict[str, str]]:
        """Retrieve price history for a specific ingredient"""
        history = []
        try:
            with open(self.price_history_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get("Ingredient Name") == ingredient_name:
                        history.append(row)
        except FileNotFoundError:
            pass # File might not exist yet
        except Exception as e:
            print(f"Error reading price history: {e}")
        return history

    # ===== PACKAGING MANAGEMENT =====

    def add_packaging_material(self, material_data: Dict[str, str]) -> bool:
        """Add a new packaging material to the CSV file"""
        try:
            # Calculate unit cost and total cost
            price = float(material_data.get("Price", 0))
            quantity = float(material_data.get("Quantity", 0))
            unit_cost = price / quantity if quantity > 0 else 0
            total_cost = price
            
            # Prepare row data
            row_data = [
                material_data.get("Material Name", ""),
                price,
                quantity,
                round(unit_cost, 4),
                round(total_cost, 2)
            ]
            
            with open(self.packaging_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row_data)
            return True
        except Exception as e:
            print(f"Error adding packaging material: {e}")
            return False

    def get_all_packaging_materials(self) -> List[Dict[str, str]]:
        """Retrieve all packaging materials from the CSV file"""
        materials = []
        try:
            with open(self.packaging_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    materials.append(row)
        except Exception as e:
            print(f"Error reading packaging materials: {e}")
        return materials

    def update_packaging_material(self, index: int, material_data: Dict[str, str]) -> bool:
        """Update an existing packaging material at the specified index"""
        try:
            materials = self.get_all_packaging_materials()
            if 0 <= index < len(materials):
                # Calculate unit cost and total cost
                price = float(material_data.get("Price", 0))
                quantity = float(material_data.get("Quantity", 0))
                unit_cost = price / quantity if quantity > 0 else 0
                total_cost = price
                
                # Update material data
                materials[index] = {
                    "Material Name": material_data.get("Material Name", ""),
                    "Price": price,
                    "Quantity": quantity,
                    "Unit Cost": round(unit_cost, 4),
                    "Total Cost": round(total_cost, 2)
                }
                
                # Rewrite the entire file
                with open(self.packaging_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=[
                        "Material Name", "Price", "Quantity", "Unit Cost", "Total Cost"
                    ])
                    writer.writeheader()
                    writer.writerows(materials)
                return True
        except Exception as e:
            print(f"Error updating packaging material: {e}")
        return False

    def delete_packaging_material(self, index: int) -> bool:
        """Delete a packaging material at the specified index"""
        try:
            materials = self.get_all_packaging_materials()
            if 0 <= index < len(materials):
                materials.pop(index)
                
                # Rewrite the entire file
                with open(self.packaging_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=[
                        "Material Name", "Price", "Quantity", "Unit Cost", "Total Cost"
                    ])
                    writer.writeheader()
                    writer.writerows(materials)
                return True
        except Exception as e:
            print(f"Error deleting packaging material: {e}")
        return False

    def search_packaging_materials(self, query: str) -> List[Dict[str, str]]:
        """Search packaging materials by name"""
        if not query.strip():
            return self.get_all_packaging_materials()
        
        query = query.lower()
        materials = self.get_all_packaging_materials()
        filtered_materials = []
        
        for material in materials:
            if query in material.get("Material Name", "").lower():
                filtered_materials.append(material)
        
        return filtered_materials

    # ===== RECIPES MANAGEMENT =====
    
    def add_recipe(self, recipe_data: Dict[str, str], costing_data: Dict[str, float] = None) -> bool:
        """Add a new recipe to the CSV file"""
        try:
            currency = "PHP" # Initialize currency with a default value
            if costing_data:
                # Use pre-calculated values from costing_data
                total_ingredient_cost = costing_data.get("Total Ingredient Cost", 0)
                packaging_cost = costing_data.get("Packaging Cost", 0)
                labor_cost = costing_data.get("Labor Cost (50%)", 0)
                vat_percentage = costing_data.get("VAT Percentage", 0)
                currency = costing_data.get("Currency", "PHP") # Get currency from costing_data
                total_cost = costing_data.get("Total Cost", 0)
                suggested_selling_price = costing_data.get("Suggested Selling Price", 0)
                margin_percentage = costing_data.get("Margin Percentage", 150.0)
                profit = costing_data.get("Profit", 0)
            else:
                # Fallback to old calculation method (for backward compatibility)
                total_ingredient_cost = float(recipe_data.get("Total Ingredient Cost", 0))
                packaging_cost = 0.0 # Default to 0 for legacy calls
                labor_cost = total_ingredient_cost * 0.50  # 50% labor cost
                vat_percentage = 0.0 # Default to 0 for legacy calls
                # currency is already initialized to "PHP"
                total_cost = total_ingredient_cost + packaging_cost + labor_cost
                
                # Calculate selling price (typically 2.5x total cost for good profit margin)
                # Use default margin 150% for legacy calls (2.5x)
                margin_percentage = 150.0
                suggested_selling_price = total_cost * (1 + margin_percentage / 100)
                profit = suggested_selling_price - total_cost
            
            # Generate a unique ID for the recipe
            recipe_id = str(uuid.uuid4())

            # Prepare row data
            row_data = [
                recipe_id,
                recipe_data.get("Recipe Name", ""),
                total_ingredient_cost,
                round(packaging_cost, 2),
                round(labor_cost, 2),
                round(vat_percentage, 2),
                currency, # Now currency is always defined
                round(total_cost, 2),
                round(suggested_selling_price, 2),
                round(margin_percentage, 2),
                round(profit, 2),
                recipe_data.get("Ingredients Used", ""),
                recipe_data.get("Packaging Materials Used", "")
            ]
            
            with open(self.recipes_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row_data)
            return True
        except Exception as e:
            print(f"Error adding recipe: {e}")
            return False
    
    def get_all_recipes(self) -> List[Dict[str, str]]:
        """Retrieve all recipes from the CSV file"""
        recipes = []
        try:
            with open(self.recipes_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    recipes.append(row)
        except Exception as e:
            print(f"Error reading recipes: {e}")
        return recipes
    
    def search_recipes(self, query: str) -> List[Dict[str, str]]:
        """Search recipes by name"""
        if not query.strip():
            return self.get_all_recipes()
        
        query = query.lower()
        recipes = self.get_all_recipes()
        filtered_recipes = []
        
        for recipe in recipes:
            if query in recipe.get("Recipe Name", "").lower():
                filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    # ===== COST CALCULATION =====
    
    def calculate_recipe_cost(self, recipe_name: str, ingredients_used: List[Dict[str, str]],
                            packaging_materials_used: List[Dict[str, str]],
                            save_recipe: bool = False, margin_percentage: float = 150.0,
                            include_vat: bool = False, vat_percentage: float = 12.0) -> Dict[str, float]:
        """Calculate recipe cost with labor, packaging, and optional VAT"""
        try:
            # Calculate total ingredient cost
            total_ingredient_cost = sum(float(ingredient.get("Cost per Recipe", 0))
                                      for ingredient in ingredients_used)
            
            # Calculate total packaging cost
            total_packaging_cost = sum(float(material.get("Total Cost", 0))
                                       for material in packaging_materials_used)
            
            # Calculate additional costs
            labor_cost = total_ingredient_cost * 0.50  # 50% labor cost
            
            # Total cost before VAT
            total_cost_before_vat = total_ingredient_cost + total_packaging_cost + labor_cost
            
            # Calculate VAT if included
            vat_amount = 0.0
            if include_vat:
                vat_amount = total_cost_before_vat * (vat_percentage / 100)
            
            total_cost = total_cost_before_vat + vat_amount
            
            # Calculate selling price and profit using custom margin percentage
            markup_multiplier = 1 + (margin_percentage / 100)
            suggested_selling_price = total_cost * markup_multiplier
            profit = suggested_selling_price - total_cost
            
            result = {
                "Total Ingredient Cost": round(total_ingredient_cost, 2),
                "Packaging Cost": round(total_packaging_cost, 2),
                "Labor Cost (50%)": round(labor_cost, 2),
                "VAT Percentage": round(vat_percentage if include_vat else 0.0, 2),
                "VAT Amount": round(vat_amount, 2),
                "Currency": "PHP",
                "Total Cost": round(total_cost, 2),
                "Suggested Selling Price": round(suggested_selling_price, 2),
                "Profit": round(profit, 2),
                "Margin Percentage": margin_percentage
            }
            
            # Save recipe if requested
            if save_recipe:
                ingredients_text = ", ".join([ing.get("Ingredient Name", "") for ing in ingredients_used])
                packaging_materials_text = ", ".join([mat.get("Material Name", "") for mat in packaging_materials_used])
                recipe_data = {
                    "Recipe Name": recipe_name,
                    "Total Ingredient Cost": str(total_ingredient_cost),
                    "Packaging Cost": str(total_packaging_cost),
                    "Labor Cost (50%)": str(labor_cost),
                    "VAT Percentage": str(vat_percentage if include_vat else 0.0),
                    "Currency": "PHP",
                    "Total Cost": str(total_cost),
                    "Suggested Selling Price": str(suggested_selling_price),
                    "Margin Percentage": str(margin_percentage),
                    "Profit": str(profit),
                    "Ingredients Used": ingredients_text,
                    "Packaging Materials Used": packaging_materials_text
                }
                self.add_recipe(recipe_data, costing_data=result)
                
                # Add new ingredients to ingredients.csv if they don't exist
                for ingredient in ingredients_used:
                    existing_ingredients = [ing.get("Ingredient Name", "")
                                          for ing in self.get_all_ingredients()]
                    if ingredient.get("Ingredient Name", "") not in existing_ingredients:
                        self.add_ingredient(ingredient)
                
                # Add new packaging materials to packaging.csv if they don't exist
                for material in packaging_materials_used:
                    existing_materials = [mat.get("Material Name", "")
                                          for mat in self.get_all_packaging_materials()]
                    if material.get("Material Name", "") not in existing_materials:
                        self.add_packaging_material(material)
            
            return result
        except Exception as e:
            print(f"Error calculating recipe cost: {e}")
            return {}
    
    def export_recipe_costing(self, recipe_name: str, costing_data: Dict[str, float], 
                             ingredients_used: List[Dict[str, str]], 
                             filename: str = "recipe_costing.csv") -> bool:
        """Export recipe costing result to CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Recipe Costing Report"])
                writer.writerow([])
                writer.writerow(["Recipe Name", recipe_name])
                writer.writerow([])
                writer.writerow(["Cost Breakdown"])
                writer.writerow(["Item", "Amount"])
                writer.writerow(["Total Ingredient Cost", f"${costing_data.get('Total Ingredient Cost', 0)}"])
                writer.writerow(["Packaging Cost", f"${costing_data.get('Packaging Cost', 0)}"])
                writer.writerow(["Labor Cost (50%)", f"${costing_data.get('Labor Cost (50%)', 0)}"])
                if costing_data.get('VAT Percentage', 0) > 0: # Check if VAT was included in calculation
                    writer.writerow(["VAT Percentage", f"{costing_data.get('VAT Percentage', 0)}%"])
                    writer.writerow(["VAT Amount", f"{costing_data.get('Currency', '$')}{costing_data.get('VAT Amount', 0)}"])
                writer.writerow(["Currency", costing_data.get('Currency', 'USD')])
                writer.writerow(["Total Cost", f"${costing_data.get('Total Cost', 0)}"])
                writer.writerow(["Suggested Selling Price", f"${costing_data.get('Suggested Selling Price', 0)}"])
                writer.writerow(["Margin Percentage", f"{costing_data.get('Margin Percentage', 150)}%"])
                writer.writerow(["Profit", f"${costing_data.get('Profit', 0)}"])
                writer.writerow([])
                writer.writerow(["Ingredients Used"])
                writer.writerow(["Ingredient", "Grams Needed", "Cost per Recipe"])
                for ingredient in ingredients_used:
                    writer.writerow([
                        ingredient.get("Ingredient Name", ""),
                        ingredient.get("Grams Needed in Recipe", ""),
                        f"${ingredient.get('Cost per Recipe', '')}"
                    ])
            
            return True
        except Exception as e:
            print(f"Error exporting recipe costing: {e}")
            return False
    
    def delete_recipe(self, recipe_id: str) -> bool:
        """Delete a recipe by its unique ID from the recipes CSV file."""
        try:
            recipes = self.get_all_recipes()
            # Filter out recipes that match the given ID
            filtered = [r for r in recipes if r.get("Recipe ID", "") != recipe_id]
            if len(filtered) == len(recipes):
                # No recipe with the given ID was found
                return False

            # Re-write the file using the canonical header (includes Recipe ID and Margin Percentage)
            fieldnames = [
                "Recipe ID", "Recipe Name", "Total Ingredient Cost", "Packaging Cost",
                "Labor Cost (50%)", "VAT Percentage", "Currency", "Total Cost", "Suggested Selling Price",
                "Margin Percentage", "Profit", "Ingredients Used", "Packaging Materials Used"
            ]
            with open(self.recipes_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(filtered)
            return True
        except Exception as e:
            print(f"Error deleting recipe: {e}")
            return False