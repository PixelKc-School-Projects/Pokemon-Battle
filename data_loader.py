"""
Data Loader Module

This module handles loading JSON data files and creating Python objects:
- Load Pokemon from JSON files
- Load Moves from JSON files
- Convert JSON data into Pokemon/Move dictionaries

This demonstrates separation of concerns - data loading is separate from game logic.
"""

import json
import os

# Types are strings, Moves are dictionaries, Pokemon are dictionaries
# No class imports needed - we work with plain data structures


def calculate_hp(base_hp, level=50):
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


def calculate_stat(base_stat, level=50):
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


def get_all_type_names():
    """
    Get a list of all valid Pokemon type names.

    Returns:
        list[str]: List of all type names
    """
    from type_system import get_all_type_names as _get_all_type_names
    return _get_all_type_names()


def load_pokemon_data(pokemon_name):
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


def load_move_data(move_name):
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


def create_move_from_data(move_data):
    """
    Create a move dictionary from JSON data.

    Args:
        move_data: Dictionary containing move data from JSON

    Returns:
        dict: Move dictionary with keys: name, type, power, accuracy
    """
    return {
        "name": move_data["name"],
        "type": move_data["type"],
        "power": move_data["power"],
        "accuracy": move_data["accuracy"]
    }


def create_pokemon_from_data(pokemon_data, move_name=None):
    """
    Create a Pokemon dictionary from JSON data.

    Args:
        pokemon_data: Dictionary containing Pokemon data from JSON
        move_name: Optional move name to load. If None, uses first move from pokemon_data.

    Returns:
        dict: Pokemon dictionary with all attributes
    """
    # Get Pokemon types as a list of type name strings from JSON
    pokemon_types = pokemon_data["types"]

    # Calculate actual stats from base stats at level 50
    level = 50
    stats = {
        "hp": calculate_hp(pokemon_data["stats"]["hp"], level),
        "attack": calculate_stat(pokemon_data["stats"]["attack"], level),
        "defense": calculate_stat(pokemon_data["stats"]["defense"], level),
        "speed": calculate_stat(pokemon_data["stats"]["speed"], level)
        # Note: We ignore special-attack and special-defense
    }

    # Load the move
    if move_name is None:
        # Get first move from pokemon data
        move_names = pokemon_data.get("moves", [])
        move_name = move_names[0] if move_names else None

    move = None
    if move_name:
        try:
            move_data = load_move_data(move_name)
            move = create_move_from_data(move_data)
        except FileNotFoundError:
            print(f"Warning: Move '{move_name}' not found, Pokemon will have no move.")

    # Calculate max_hp and set current_hp to full
    max_hp = stats["hp"]

    # Return Pokemon as a dictionary
    return {
        "name": pokemon_data["name"],
        "types": pokemon_types,
        "stats": stats,
        "max_hp": max_hp,
        "current_hp": max_hp,
        "level": level,
        "move": move
    }


def load_pokemon(pokemon_name):
    """
    Load a Pokemon from JSON file and create a Pokemon dictionary.

    Convenience function that combines loading data and creating the dictionary.

    Args:
        pokemon_name: Name of the Pokemon (lowercase, e.g., "pikachu")

    Returns:
        dict: Created Pokemon dictionary with all data loaded
    """
    pokemon_data = load_pokemon_data(pokemon_name)
    return create_pokemon_from_data(pokemon_data)


def load_available_pokemon():
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


def get_available_moves():
    """
    Get a list of all available move names from the data directory.

    Returns:
        list[str]: List of move names (without .json extension)
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    moves_dir = os.path.join(current_dir, 'data', 'moves')

    move_files = []
    for filename in os.listdir(moves_dir):
        if filename.endswith('.json'):
            move_name = filename[:-5]  # Remove .json extension
            move_files.append(move_name)

    return sorted(move_files)
