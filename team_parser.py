"""
Team Parser Module

This module provides hardcoded Pokemon teams for the battle game.
"""

from data_loader import *
from team import *


def create_hardcoded_teams():
    """
    Create hardcoded teams for player and AI based on the classic team.

    Returns:
        tuple[dict, dict]: (player_team, ai_team)
    """
    # Classic team Pokemon with their first moves
    classic_pokemon = [
        ("pikachu", "thunderbolt"),
        ("charizard", "flamethrower"),
        ("blastoise", "hydro-pump"),
        ("venusaur", "solar-beam"),
        ("snorlax", "body-slam"),
        ("dragonite", "dragon-claw")
    ]

    # Create player team
    player_team = create_team()
    print("\nCreating your team...")
    for pokemon_name, move_name in classic_pokemon:
        try:
            pokemon_data = load_pokemon_data(pokemon_name)
            pokemon = create_pokemon_from_data(pokemon_data, move_name=move_name)
            success = add_pokemon(player_team, pokemon)
            if success:
                print(f"  Added {pokemon['name']} to your team")
        except Exception as e:
            print(f"  Error loading {pokemon_name}: {e}")

    # Create AI team (same as player)
    ai_team = create_team()
    print("\nCreating opponent's team...")
    for pokemon_name, move_name in classic_pokemon:
        try:
            pokemon_data = load_pokemon_data(pokemon_name)
            pokemon = create_pokemon_from_data(pokemon_data, move_name=move_name)
            success = add_pokemon(ai_team, pokemon)
            if success:
                print(f"  Added {pokemon['name']} to opponent's team")
        except Exception as e:
            print(f"  Error loading {pokemon_name}: {e}")

    return player_team, ai_team
