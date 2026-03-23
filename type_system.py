"""
Pokemon Type System

This module implements the Pokemon type system.
All types are instances of the Type class.
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


class Type:
    """
    Represents a Pokemon type (Fire, Water, Electric, etc.).

    Each type knows its name and can calculate effectiveness against other types.
    """

    def __init__(self, name: str):
        """
        Initialize a Type with its name.

        Args:
            name: The type name (e.g., "fire", "water", "grass")
        """
        self.name = name

    def get_effectiveness_against(self, defender_type: 'Type') -> float:
        """
        Calculate this type's effectiveness against a defender type.

        Args:
            defender_type: The Type object being attacked

        Returns:
            float: Effectiveness multiplier (2.0 = super effective, 1.0 = normal,
                   0.5 = not very effective, 0.0 = no effect)
        """
        # Look up effectiveness from the shared type effectiveness data
        if self.name in _TYPE_EFFECTIVENESS_DATA:
            return _TYPE_EFFECTIVENESS_DATA[self.name].get(defender_type.name, 1.0)
        return 1.0

    def __str__(self) -> str:
        """Return the type name as a string."""
        return self.name

    def __repr__(self) -> str:
        """Return a detailed string representation of the type."""
        return f"Type('{self.name}')"


# Helper function for calculating dual-type effectiveness
def calculate_dual_type_effectiveness(move_type: Type, defender_types: list[Type]) -> float:
    """
    Calculate type effectiveness for a move against a Pokemon that may have 1 or 2 types.

    For single-type Pokemon: Returns the effectiveness multiplier
    For dual-type Pokemon: Multiplies the effectiveness values together

    Examples:
        - Fire move vs Grass (single type): 2.0x (super effective)
        - Fire move vs Grass/Poison (dual type): 2.0 * 1.0 = 2.0x
        - Fire move vs Water/Rock (dual type): 0.5 * 0.5 = 0.25x (quarter damage!)
        - Ground move vs Flying/Electric (dual type): 0.0 * 2.0 = 0.0x (no effect due to Flying)

    Args:
        move_type: The Type object of the attacking move
        defender_types: List of Type objects for the defending Pokemon (1 or 2 types)

    Returns:
        float: Combined effectiveness multiplier
    """
    effectiveness = 1.0
    for defender_type in defender_types:
        effectiveness *= move_type.get_effectiveness_against(defender_type)
    return effectiveness
