"""
Pokemon Module

This module handles Pokemon-related functionality using dictionaries and functions.

A Pokemon is represented as a dictionary with these keys:
    {
        "name": str,              # Pokemon name (e.g., "Charizard")
        "types": list[str],       # List of type names (e.g., ["fire", "flying"])
        "stats": dict,            # Stats dict with "hp", "attack", "defense", "speed"
        "max_hp": int,            # Maximum HP
        "current_hp": int,        # Current HP
        "level": int,             # Pokemon level (always 50)
        "move": dict              # Move dictionary
    }
"""


def has_type(pokemon, type_name):
    """
    Check if this Pokemon has a specific type.

    Args:
        pokemon: Pokemon dictionary
        type_name: Type name to check (e.g., "fire", "water")

    Returns:
        bool: True if Pokemon has this type, False otherwise
    """
    # TODO 3: Team State Checks
    # TODO 3.3: Check if type_name is in pokemon's types list
    pass


def get_hp_percentage(pokemon):
    """
    Get current HP as a percentage of max HP.

    Args:
        pokemon: Pokemon dictionary

    Returns:
        float: HP percentage (0.0 to 1.0)
    """
    # TODO 1.4: Return current_hp / max_hp (handle division by zero)
    pass


def take_damage(pokemon, amount):
    """
    Reduce Pokemon's HP by the given amount.

    Args:
        pokemon: Pokemon dictionary
        amount: Damage amount to subtract from current HP
    """
    # TODO 1: Pokemon State Management
    # TODO 1.1: Subtract amount from current_hp, ensure HP doesn't go below 0
    pass


def is_fainted(pokemon):
    """
    Check if this Pokemon has fainted.

    Args:
        pokemon: Pokemon dictionary

    Returns:
        bool: True if current_hp is 0, False otherwise
    """
    # TODO 1.2: Return True if current_hp <= 0
    pass


def get_stat(pokemon, stat_name):
    """
    Get a stat value by name.

    Args:
        pokemon: Pokemon dictionary
        stat_name: Stat name ("hp", "attack", "defense", "speed")

    Returns:
        int: The stat value, or 0 if stat doesn't exist
    """
    # TODO 1.3: Return stat value from stats dict, or 0 if not found
    pass
