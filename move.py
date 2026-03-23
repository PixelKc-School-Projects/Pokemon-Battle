"""
Pokemon Move System

This module handles move-related functionality using dictionaries and pure functions.

A move is represented as a dictionary with these keys:
    {
        "name": str,           # Move name (e.g., "Thunderbolt")
        "type": str,           # Type name string (e.g., "electric")
        "power": int,          # Base power (0-250+)
        "accuracy": int        # Accuracy percentage (0-100)
    }

Functions:
- calculate_damage() - Damage calculation with STAB and type effectiveness
- check_hit() - Check if move hits based on accuracy
"""

import random
from type_system import *


def calculate_damage(move, attacker, defender):
    """
    Calculate damage using the authentic Pokemon formula.

    Formula: Damage = (((2×Level÷5+2)×Power×A÷D÷50)+2)×STAB×Type×Random

    This matches the official Pokemon damage formula from Generation III onwards.
    Includes STAB (Same Type Attack Bonus) and type effectiveness.

    Args:
        move: Move dictionary being used
        attacker: Pokemon dictionary using the move
        defender: Pokemon dictionary being attacked

    Returns:
        int: Calculated damage amount (minimum 1)
    """
    # Get stats
    level = attacker["level"]
    attacker_attack = attacker["stats"].get("attack", 0)
    defender_defense = defender["stats"].get("defense", 1)
    if defender_defense == 0:
        defender_defense = 1

    # Base damage calculation (Gen III+ formula)
    # Damage = (((2×Level÷5+2)×Power×A÷D÷50)+2)×Modifiers
    base_damage = (((2 * level / 5 + 2) * move["power"] * attacker_attack / defender_defense) / 50) + 2

    # STAB: 1.5x if move type matches any of attacker's types
    move_type_name = move["type"]  # Type is a string like "electric"
    has_stab = move_type_name in attacker["types"]  # types is list of strings
    stab_multiplier = 1.5 if has_stab else 1.0

    # Type effectiveness (pass type name string and list of type name strings)
    type_effectiveness = calculate_dual_type_effectiveness(move_type_name, defender["types"])

    # Random factor (0.85-1.0)
    random_factor = random.uniform(0.85, 1.0)

    # Calculate final damage
    final_damage = base_damage * stab_multiplier * type_effectiveness * random_factor

    # Ensure minimum damage of 1
    return max(1, int(final_damage))


def check_hit(move):
    """
    Check if this move hits based on its accuracy.

    Args:
        move: Move dictionary

    Returns:
        bool: True if move hits, False if it misses
    """
    random_number = random.randint(1, 100)
    return random_number <= move["accuracy"]
