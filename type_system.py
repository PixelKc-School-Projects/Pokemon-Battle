"""
Pokemon Type System - Week 27: Inheritance and Polymorphism

YOUR TASK FOR WEEK 27:
======================
Implement all 18 Pokemon type classes using inheritance!

The Type base class is provided below. You need to create 18 type subclasses
that inherit from Type. Two examples (FireType and WaterType) are provided
to show you the pattern.

LEARNING OBJECTIVES:
- Define subclasses that inherit from a base class
- Use super().__init__() to call the parent constructor
- Understand polymorphism (all types share the same interface)
- Create a class hierarchy

INSTRUCTIONS:
1. Study the Type base class below - don't modify it!
2. Look at the two example type classes (FireType and WaterType)
3. Implement the remaining 16 type classes following the same pattern
4. Update data_loader.py to import and use your new type classes

The 18 Pokemon types you need to implement:
- NormalType
- FireType (EXAMPLE PROVIDED)
- WaterType (EXAMPLE PROVIDED)
- ElectricType
- GrassType
- IceType
- FightingType
- PoisonType
- GroundType
- FlyingType
- PsychicType
- BugType
- RockType
- GhostType
- DragonType
- DarkType
- SteelType
- FairyType
"""

import json
import os
from typing import Dict

# Load type effectiveness data once at module level (shared across all Type instances)
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
    Base Type class that all Pokemon types inherit from.

    DO NOT MODIFY THIS CLASS - It's provided for you!

    Each type knows its name and can calculate its effectiveness against other types.
    This demonstrates inheritance - all types share this interface but implement
    different behavior.
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
        return f"{self.__class__.__name__}('{self.name}')"


# =============================================================================
# EXAMPLE TYPE CLASSES - Study these to understand the pattern!
# =============================================================================

class FireType(Type):
    """
    Fire type Pokemon.

    EXAMPLE: This shows you how to create a type subclass.

    Key concepts demonstrated:
    1. Class inherits from Type using (Type) syntax
    2. __init__ method with no parameters (except self)
    3. super().__init__("fire") calls the parent Type class constructor
    4. The type name must match the key in type_effectiveness.json
    """
    def __init__(self):
        # Call the parent Type class constructor with the type name
        super().__init__("fire")


class WaterType(Type):
    """
    Water type Pokemon.

    EXAMPLE: Another example following the exact same pattern.

    Notice:
    - Class name is CapitalCase with "Type" suffix (WaterType)
    - Type name passed to super() is lowercase ("water")
    - No other methods needed - everything is inherited from Type!
    """
    def __init__(self):
        super().__init__("water")


# =============================================================================
# TODO: IMPLEMENT THE REMAINING 16 TYPE CLASSES BELOW
# =============================================================================
# Follow the same pattern as FireType and WaterType above.
# Each class should:
# 1. Inherit from Type
# 2. Have a docstring
# 3. Have an __init__ method that calls super().__init__() with the type name
#
# Remember: The type name you pass to super().__init__() must be lowercase
# and match the keys in data/type_effectiveness.json
# =============================================================================

class NormalType(Type):
    def __init__(self):
        super().__init__("normal")


class ElectricType(Type):
    def __init__(self):
        super().__init__("electric")


class GrassType(Type):
    def __init__(self):
        super().__init__("grass")


class IceType(Type):
    def __init__(self):
        super().__init__("ice")


class FightingType(Type):
    def __init__(self):
        super().__init__("fighting")


class PoisonType(Type):
    def __init__(self):
        super().__init__("poison")


class GroundType(Type):
    def __init__(self):
        super().__init__("ground")


class FlyingType(Type):
    def __init__(self):
        super().__init__("flying")


class PsychicType(Type):
    def __init__(self):
        super().__init__("psychic")


class BugType(Type):
    def __init__(self):
        super().__init__("bug")


class RockType(Type):
    def __init__(self):
        super().__init__("rock")


class GhostType(Type):
    def __init__(self):
        super().__init__("ghost")


class DragonType(Type):
    def __init__(self):
        super().__init__("dragon")


class DarkType(Type):
    def __init__(self):
        super().__init__("dark")


class SteelType(Type):
    def __init__(self):
        super().__init__("steel")


class FairyType(Type):
    def __init__(self):
        super().__init__("fairy")


# =============================================================================
# Helper function - DO NOT MODIFY
# =============================================================================

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
