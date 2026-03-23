"""
Quick test script to verify the new UI screens render correctly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import create_type_system, load_pokemon
from team import Team
from battle import Battle

# Create type system
print("Loading type system...")
type_system = create_type_system()

# Create simple teams
print("Creating teams...")
player_team = Team()
player_team.add_pokemon(load_pokemon("aerodactyl", type_system))

ai_team = Team()
ai_team.add_pokemon(load_pokemon("gyarados", type_system))

# Create battle
battle = Battle(player_team, ai_team)

# Import the UI functions
from main import (
    draw_pokemon_header,
    draw_action_menu,
    draw_move_grid,
    draw_message_area
)

print("\n" + "=" * 60)
print("TEST 1: Pokemon Header")
print("=" * 60)
header = draw_pokemon_header(battle)
for line in header:
    print(line)

print("\n" + "=" * 60)
print("TEST 2: Action Menu")
print("=" * 60)
header = draw_pokemon_header(battle)
menu = draw_action_menu("Aerodactyl")
for line in header + menu:
    print(line)

print("\n" + "=" * 60)
print("TEST 3: Move Grid (Move 1 selected)")
print("=" * 60)
player_pokemon = player_team.get_current_pokemon()
header = draw_pokemon_header(battle)
move_grid = draw_move_grid(player_pokemon, 1)
for line in header + move_grid:
    print(line)

print("\n" + "=" * 60)
print("TEST 4: Move Grid (Move 4 selected)")
print("=" * 60)
header = draw_pokemon_header(battle)
move_grid = draw_move_grid(player_pokemon, 4)
for line in header + move_grid:
    print(line)

print("\n" + "=" * 60)
print("TEST 5: Message Area")
print("=" * 60)
header = draw_pokemon_header(battle)
message_box = draw_message_area()
for line in header + message_box:
    print(line)

print("\nAll UI components rendered successfully!")
print("\nTo test cursor-positioned messages, run the full battle simulator.")
print("Note: The actual slow text animation will appear during gameplay.")
