import csv
import os
from typing import List, Dict, Optional

class DataHandler:
    def __init__(self):
        self.ingredients_file = "ingredients.csv"
        self.recipes_file = "recipes.csv"
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
        
        # Recipes file
        if not os.path.exists(self.recipes_file):
            with open(self.recipes_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Recipe Name", "Total Ingredient Cost", "Miscellaneous Cost (50%)", 
                    "Labor Cost (45%)", "Total Cost", "Suggested Selling Price", 
                    "Profit", "Ingredients Used"
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
    
    # ===== RECIPES MANAGEMENT =====
    
    def add_recipe(self, recipe_data: Dict[str, str], costing_data: Dict[str, float] = None) -> bool:
        """Add a new recipe to the CSV file"""
        try:
            if costing_data:
                # Use pre-calculated values from costing_data
                total_ingredient_cost = costing_data.get("Total Ingredient Cost", 0)
                misc_cost = costing_data.get("Miscellaneous Cost (50%)", 0)
                labor_cost = costing_data.get("Labor Cost (45%)", 0)
                total_cost = costing_data.get("Total Cost", 0)
                suggested_selling_price = costing_data.get("Suggested Selling Price", 0)
                profit = costing_data.get("Profit", 0)
            else:
                # Fallback to old calculation method (for backward compatibility)
                total_ingredient_cost = float(recipe_data.get("Total Ingredient Cost", 0))
                misc_cost = total_ingredient_cost * 0.50  # 50% miscellaneous cost
                labor_cost = total_ingredient_cost * 0.45  # 45% labor cost
                total_cost = total_ingredient_cost + misc_cost + labor_cost
                
                # Calculate selling price (typically 2.5x total cost for good profit margin)
                suggested_selling_price = total_cost * 2.5
                profit = suggested_selling_price - total_cost
            
            # Prepare row data
            row_data = [
                recipe_data.get("Recipe Name", ""),
                total_ingredient_cost,
                round(misc_cost, 2),
                round(labor_cost, 2),
                round(total_cost, 2),
                round(suggested_selling_price, 2),
                round(profit, 2),
                recipe_data.get("Ingredients Used", "")
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
                            save_recipe: bool = False, margin_percentage: float = 150.0) -> Dict[str, float]:
        """Calculate recipe cost with labor and miscellaneous costs"""
        try:
            # Calculate total ingredient cost
            total_ingredient_cost = sum(float(ingredient.get("Cost per Recipe", 0)) 
                                      for ingredient in ingredients_used)
            
            # Calculate additional costs
            misc_cost = total_ingredient_cost * 0.50  # 50% miscellaneous cost
            labor_cost = total_ingredient_cost * 0.45  # 45% labor cost
            total_cost = total_ingredient_cost + misc_cost + labor_cost
            
            # Calculate selling price and profit using custom margin percentage
            # margin_percentage = 150 means 150% markup = 2.5x total cost
            markup_multiplier = 1 + (margin_percentage / 100)
            suggested_selling_price = total_cost * markup_multiplier
            profit = suggested_selling_price - total_cost
            
            result = {
                "Total Ingredient Cost": round(total_ingredient_cost, 2),
                "Miscellaneous Cost (50%)": round(misc_cost, 2),
                "Labor Cost (45%)": round(labor_cost, 2),
                "Total Cost": round(total_cost, 2),
                "Suggested Selling Price": round(suggested_selling_price, 2),
                "Profit": round(profit, 2),
                "Margin Percentage": margin_percentage
            }
            
            # Save recipe if requested
            if save_recipe:
                ingredients_text = ", ".join([ing.get("Ingredient Name", "") for ing in ingredients_used])
                recipe_data = {
                    "Recipe Name": recipe_name,
                    "Total Ingredient Cost": str(total_ingredient_cost),
                    "Ingredients Used": ingredients_text
                }
                self.add_recipe(recipe_data, costing_data=result)
                
                # Add new ingredients to ingredients.csv if they don't exist
                for ingredient in ingredients_used:
                    existing_ingredients = [ing.get("Ingredient Name", "") 
                                          for ing in self.get_all_ingredients()]
                    if ingredient.get("Ingredient Name", "") not in existing_ingredients:
                        self.add_ingredient(ingredient)
            
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
                writer.writerow(["Miscellaneous Cost (50%)", f"${costing_data.get('Miscellaneous Cost (50%)', 0)}"])
                writer.writerow(["Labor Cost (45%)", f"${costing_data.get('Labor Cost (45%)', 0)}"])
                writer.writerow(["Total Cost", f"${costing_data.get('Total Cost', 0)}"])
                writer.writerow(["Suggested Selling Price", f"${costing_data.get('Suggested Selling Price', 0)}"])
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
