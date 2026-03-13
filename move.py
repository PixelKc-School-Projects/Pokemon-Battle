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
    Level = attacker.get('level', 1)
    Power = move.get('power', 0)
    A = attacker.get('stats', {}).get('attack', 1)
    D = defender.get('stats', {}).get('defense', 1)
    STAB = 1.5 if move.get('type', "") in attacker.get('types', []) else 1.0
    Type = calculate_dual_type_effectiveness(move.get('type', ""), defender.get('types', []))
    Random = random.uniform(0.85, 1.0)
    damage = (((2*Level/5+2)*Power*A/D/50)+2)*STAB*Type*Random

    return max(1, int(damage))

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
