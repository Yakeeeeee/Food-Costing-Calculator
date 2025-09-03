#!/usr/bin/env python3
"""
Demo script for Food Costing Calculator
This script demonstrates how to use the data handler directly
"""

from data_handler import DataHandler

def main():
    print("🍽️  Food Costing Calculator Demo")
    print("=" * 50)
    
    # Initialize data handler
    data_handler = DataHandler()
    
    # Add some sample ingredients
    print("\n📝 Adding sample ingredients...")
    
    sample_ingredients = [
        {
            "Ingredient Name": "Flour",
            "Price": "2.50",
            "Grams": "1000",
            "Grams Needed in Recipe": "250"
        },
        {
            "Ingredient Name": "Sugar",
            "Price": "3.00",
            "Grams": "1000",
            "Grams Needed in Recipe": "100"
        },
        {
            "Ingredient Name": "Eggs",
            "Price": "4.50",
            "Grams": "600",
            "Grams Needed in Recipe": "120"
        },
        {
            "Ingredient Name": "Butter",
            "Price": "5.00",
            "Grams": "500",
            "Grams Needed in Recipe": "125"
        }
    ]
    
    for ingredient in sample_ingredients:
        if data_handler.add_ingredient(ingredient):
            print(f"✅ Added: {ingredient['Ingredient Name']}")
        else:
            print(f"❌ Failed to add: {ingredient['Ingredient Name']}")
    
    # Display all ingredients
    print("\n📋 Current ingredients in database:")
    ingredients = data_handler.get_all_ingredients()
    for i, ingredient in enumerate(ingredients):
        print(f"  {i+1}. {ingredient['Ingredient Name']} - ${ingredient['Price']} for {ingredient['Grams']}g")
        print(f"     Price per gram: ${ingredient['Price per Gram']}")
        print(f"     Cost per recipe: ${ingredient['Cost per Recipe']}")
    
    # Calculate recipe cost
    print("\n🧮 Calculating recipe cost for 'Chocolate Cake'...")
    
    # Select ingredients for the recipe
    selected_ingredients = [
        ingredients[0],  # Flour
        ingredients[1],  # Sugar
        ingredients[2],  # Eggs
        ingredients[3]   # Butter
    ]
    
    # Calculate cost without saving
    costing_data = data_handler.calculate_recipe_cost(
        "Chocolate Cake", 
        selected_ingredients, 
        save_recipe=False
    )
    
    if costing_data:
        print("\n💰 Cost Breakdown:")
        print(f"  Total Ingredient Cost: ${costing_data['Total Ingredient Cost']}")
        print(f"  Miscellaneous Cost (50%): ${costing_data['Miscellaneous Cost (50%)']}")
        print(f"  Labor Cost (45%): ${costing_data['Labor Cost (45%)']}")
        print(f"  Total Cost: ${costing_data['Total Cost']}")
        print(f"  Suggested Selling Price: ${costing_data['Suggested Selling Price']}")
        print(f"  Profit: ${costing_data['Profit']}")
    
    # Save the recipe
    print("\n💾 Saving recipe to database...")
    costing_data = data_handler.calculate_recipe_cost(
        "Chocolate Cake", 
        selected_ingredients, 
        save_recipe=True
    )
    
    if costing_data:
        print("✅ Recipe saved successfully!")
    
    # Display all recipes
    print("\n📚 All saved recipes:")
    recipes = data_handler.get_all_recipes()
    for i, recipe in enumerate(recipes):
        print(f"  {i+1}. {recipe['Recipe Name']}")
        print(f"     Total Cost: ${recipe['Total Cost']}")
        print(f"     Selling Price: ${recipe['Suggested Selling Price']}")
        print(f"     Profit: ${recipe['Profit']}")
        print(f"     Ingredients: {recipe['Ingredients Used']}")
    
    print("\n🎉 Demo completed!")
    print("\nTo run the full application with GUI:")
    print("python main.py")

if __name__ == "__main__":
    main()
