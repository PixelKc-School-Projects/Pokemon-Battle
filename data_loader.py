"""
Data Loader Module

This module handles loading JSON data files and creating Python objects:
- Load Pokemon from JSON files
- Load Moves from JSON files
- Create the type system (all 18 Type objects)
- Convert JSON data into Pokemon/Move objects

This demonstrates separation of concerns - data loading is separate from game logic.
"""

import json
import os
from typing import Dict, Any, Optional

from type_system import Type
from pokemon import Pokemon
from move import Move


def calculate_hp(base_hp: int, level: int = 50) -> int:
    """
    Calculate actual HP from base stat using simplified Pokemon formula (no IVs/EVs).

    Formula: HP = floor((2 × base_hp) × level / 100) + level + 10

    Args:
        base_hp: Base HP stat from Pokemon species data
        level: Pokemon level (default 50)

    Returns:
        int: Calculated HP value
    """
    return ((2 * base_hp) * level // 100) + level + 10


def calculate_stat(base_stat: int, level: int = 50) -> int:
    """
    Calculate actual stat from base stat using simplified Pokemon formula (no IVs/EVs).

    Formula: Stat = floor((2 × base_stat) × level / 100) + 5

    Args:
        base_stat: Base stat value from Pokemon species data
        level: Pokemon level (default 50)

    Returns:
        int: Calculated stat value
    """
    return ((2 * base_stat) * level // 100) + 5


def create_type_system() -> Dict[str, Type]:
    """
    Create all 18 Type objects and return them in a dictionary.

    Returns:
        dict[str, Type]: Dictionary mapping type names (strings) to Type objects
    """
    return {
        "normal": Type("normal"),
        "fire": Type("fire"),
        "water": Type("water"),
        "electric": Type("electric"),
        "grass": Type("grass"),
        "ice": Type("ice"),
        "fighting": Type("fighting"),
        "poison": Type("poison"),
        "ground": Type("ground"),
        "flying": Type("flying"),
        "psychic": Type("psychic"),
        "bug": Type("bug"),
        "rock": Type("rock"),
        "ghost": Type("ghost"),
        "dragon": Type("dragon"),
        "dark": Type("dark"),
        "steel": Type("steel"),
        "fairy": Type("fairy")
    }


def load_pokemon_data(pokemon_name: str) -> Dict[str, Any]:
    """
    Load Pokemon data from JSON file.

    Args:
        pokemon_name: Name of the Pokemon (lowercase, e.g., "pikachu")

    Returns:
        dict: Pokemon data from JSON file

    Raises:
        FileNotFoundError: If Pokemon JSON file doesn't exist
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'pokemon', f'{pokemon_name}.json')

    with open(json_path, 'r') as f:
        return json.load(f)


def load_move_data(move_name: str) -> Dict[str, Any]:
    """
    Load Move data from JSON file.

    Args:
        move_name: Name of the move (lowercase with hyphens, e.g., "thunder-bolt")

    Returns:
        dict: Move data from JSON file

    Raises:
        FileNotFoundError: If Move JSON file doesn't exist
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'moves', f'{move_name}.json')

    with open(json_path, 'r') as f:
        return json.load(f)


def create_move_from_data(move_data: Dict[str, Any], type_system: Dict[str, Type]) -> Move:
    """
    Create a Move object from JSON data.

    Args:
        move_data: Dictionary containing move data from JSON
        type_system: Dictionary mapping type names to Type objects

    Returns:
        Move: Created Move object
    """
    move_type = type_system.get(move_data["type"], type_system["normal"])

    return Move(
        name=move_data["name"],
        move_type=move_type,
        power=move_data["power"],
        accuracy=move_data["accuracy"],
        pp=move_data["pp"]
    )


def create_pokemon_from_data(
    pokemon_data: Dict[str, Any],
    type_system: Dict[str, Type],
    move_names: Optional[list[str]] = None
) -> Pokemon:
    """
    Create a Pokemon object from JSON data.

    Args:
        pokemon_data: Dictionary containing Pokemon data from JSON
        type_system: Dictionary mapping type names to Type objects
        move_names: Optional list of move names to load (1-4 moves).
                    If None, uses moves from pokemon_data.

    Returns:
        Pokemon: Created Pokemon object with moves loaded
    """
    # Get Pokemon types
    pokemon_types = []
    for type_name in pokemon_data["types"]:
        if type_name in type_system:
            pokemon_types.append(type_system[type_name])

    # Calculate actual stats from base stats at level 50
    level = 50
    stats = {
        "hp": calculate_hp(pokemon_data["stats"]["hp"], level),
        "attack": calculate_stat(pokemon_data["stats"]["attack"], level),
        "defense": calculate_stat(pokemon_data["stats"]["defense"], level),
        "speed": calculate_stat(pokemon_data["stats"]["speed"], level)
        # Note: We ignore special-attack and special-defense
    }

    # Load moves (up to 4)
    if move_names is None:
        move_names = pokemon_data.get("moves", [])

    moves = []
    for move_name in move_names[:4]:  # Take only first 4 moves
        try:
            move_data = load_move_data(move_name)
            move = create_move_from_data(move_data, type_system)
            moves.append(move)
        except FileNotFoundError:
            # Skip moves that don't have JSON files
            print(f"Warning: Move '{move_name}' not found, skipping.")
            continue

    # Create Pokemon with up to 4 moves
    move1 = moves[0] if len(moves) > 0 else None
    move2 = moves[1] if len(moves) > 1 else None
    move3 = moves[2] if len(moves) > 2 else None
    move4 = moves[3] if len(moves) > 3 else None

    return Pokemon(
        name=pokemon_data["name"],
        types=pokemon_types,
        stats=stats,
        move1=move1,
        move2=move2,
        move3=move3,
        move4=move4,
        sprite_url=pokemon_data.get("sprite_url", ""),
        sprite_url_back=pokemon_data.get("sprite_url_back", "")
    )


def load_pokemon(pokemon_name: str, type_system: Dict[str, Type]) -> Pokemon:
    """
    Load a Pokemon from JSON file and create a Pokemon object.

    Convenience function that combines loading data and creating the object.

    Args:
        pokemon_name: Name of the Pokemon (lowercase, e.g., "pikachu")
        type_system: Dictionary mapping type names to Type objects

    Returns:
        Pokemon: Created Pokemon object with all data loaded
    """
    pokemon_data = load_pokemon_data(pokemon_name)
    return create_pokemon_from_data(pokemon_data, type_system)


def get_available_pokemon() -> list[str]:
    """
    Get a list of all available Pokemon names from the data directory.

    Returns:
        list[str]: List of Pokemon names (without .json extension)
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pokemon_dir = os.path.join(current_dir, 'data', 'pokemon')

    pokemon_files = []
    for filename in os.listdir(pokemon_dir):
        if filename.endswith('.json'):
            pokemon_name = filename[:-5]  # Remove .json extension
            pokemon_files.append(pokemon_name)

    return sorted(pokemon_files)
