#!/usr/bin/env python3
"""
Food Costing Calculator - Launcher Script
Run this script to start the new, improved Food Costing Calculator application.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main_new import FoodCostingApp
    print("Starting Food Costing Calculator - Professional Edition...")
    print("Loading application...")
    
    app = FoodCostingApp()
    app.run()
    
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("💡 Make sure you have installed the required dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"Error starting application: {e}")
    print("Please check that all files are present and try again.")
    sys.exit(1)
