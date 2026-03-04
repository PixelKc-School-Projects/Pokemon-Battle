"""
Pokemon Type System

This module implements the Pokemon type system using strings and functions.
In Week 25, types are represented as simple strings like "fire", "water", "electric".
Type effectiveness is looked up from JSON data.
"""

import json
import os
from typing import Dict


# Load type effectiveness data once at module level
def _load_type_effectiveness() -> Dict[str, Dict[str, float]]:
    """Load type effectiveness data from JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'data', 'type_effectiveness.json')

    with open(json_path, 'r') as f:
        return json.load(f)

# Module-level variable storing all type effectiveness data
_TYPE_EFFECTIVENESS_DATA = _load_type_effectiveness()


def get_effectiveness_against(attacker_type_name: str, defender_type_name: str) -> float:
    """
    Calculate type effectiveness for an attacking type against a defending type.

    Args:
        attacker_type_name: The type name of the attacking move (e.g., "fire")
        defender_type_name: The type name being attacked (e.g., "grass")

    Returns:
        float: Effectiveness multiplier (2.0 = super effective, 1.0 = normal,
               0.5 = not very effective, 0.0 = no effect)
    """
    # Look up effectiveness from the shared type effectiveness data
    if attacker_type_name in _TYPE_EFFECTIVENESS_DATA:
        return _TYPE_EFFECTIVENESS_DATA[attacker_type_name].get(defender_type_name, 1.0)
    return 1.0


def calculate_dual_type_effectiveness(move_type_name: str, defender_type_names: list[str]) -> float:
    """
    Calculate type effectiveness for a move against a Pokemon that may have 1 or 2 types.

    For single-type Pokemon: Returns the effectiveness multiplier
    For dual-type Pokemon: Multiplies the effectiveness values together

    Examples:
        - Fire move vs ["grass"] (single type): 2.0x (super effective)
        - Fire move vs ["grass", "poison"] (dual type): 2.0 * 1.0 = 2.0x
        - Fire move vs ["water", "rock"] (dual type): 0.5 * 0.5 = 0.25x (quarter damage!)
        - Ground move vs ["flying", "electric"] (dual type): 0.0 * 2.0 = 0.0x (no effect due to Flying)

    Args:
        move_type_name: The type name of the attacking move (e.g., "fire")
        defender_type_names: List of type names for the defending Pokemon (1 or 2 types)

    Returns:
        float: Combined effectiveness multiplier
    """
    effectiveness = 1.0
    for defender_type_name in defender_type_names:
        effectiveness *= get_effectiveness_against(move_type_name, defender_type_name)
    return effectiveness


def get_all_type_names() -> list[str]:
    """
    Get a list of all valid Pokemon type names.

    Returns:
        list[str]: List of all type names (e.g., ["normal", "fire", "water", ...])
    """
    return list(_TYPE_EFFECTIVENESS_DATA.keys())
