from game import Game
import pygame
import sys
import os

def check_files():
    """Check if all necessary graphic files exist"""
    import os
    
    required_files = [
        "graphics/bullet.png",
        "graphics/green-tank-00.png",
        "graphics/green-tank-01.png",
        "graphics/green-tank-02.png",
        "graphics/green-tank-03.png",
        "graphics/green-tank-04.png",
        "graphics/green-tank-05.png",
        "graphics/red-tank-00.png",
        "graphics/red-tank-01.png",
        "graphics/red-tank-02.png",
        "graphics/red-tank-03.png",
        "graphics/red-tank-04.png",
        "graphics/red-tank-05.png",
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("WARNING: The following graphic files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("The game may not run correctly without these files.")
        print("Please make sure these files exist in the 'graphics' folder.")
        input("Press Enter to continue anyway...")

def check_directories():
    """Check if required directories exist and create them if they don't"""
    directories = [
        "graphics",
        "static",
        "static/font",
        "static/design",
        "static/music"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created '{directory}' directory.")

if __name__ == "__main__":
    print("Starting Tank Battle...")
    
    check_directories()
    check_files()
    
    pygame.init()
    
    game = Game()
    game.run()