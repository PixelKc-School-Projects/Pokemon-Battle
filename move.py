"""
Pokemon Move System

This module implements the Move class which handles:
- Move attributes (name, type, power, accuracy, PP)
- Damage calculation with STAB bonus and type effectiveness
- Accuracy checks (moves can miss)
- PP tracking (moves can run out)

Note: Unlike the Type system, moves do NOT use inheritance. This demonstrates that
not everything needs inheritance - sometimes a single class is the right choice.
"""

import random
from type_system import Type, calculate_dual_type_effectiveness
from typing import TYPE_CHECKING

# Avoid circular import - only import Pokemon type for type hints
if TYPE_CHECKING:
    from pokemon import Pokemon


class Move:
    """
    Represents a Pokemon move with all its properties and behaviors.

    A Move knows how to:
    - Calculate damage against a defender
    - Check if it hits based on accuracy
    - Track PP (Power Points) usage
    """

    def __init__(self, name: str, move_type: Type, power: int, accuracy: int, pp: int):
        """
        Initialize a Move.

        Args:
            name: Move name (e.g., "Flamethrower")
            move_type: Type object for this move (e.g., FireType())
            power: Base power of the move (0-250+)
            accuracy: Accuracy percentage (0-100, where 100 = always hits)
            pp: Maximum Power Points (how many times the move can be used)
        """
        self.name = name
        self.move_type = move_type
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.current_pp = pp  # Starts at maximum

    def calculate_damage(self, defender: 'Pokemon', attacker: 'Pokemon') -> int:
        """
        Calculate damage using the authentic Pokemon formula.

        Formula: Damage = (((2×Level÷5+2)×Power×A÷D÷50)+2)×STAB×Type×Random

        This matches the official Pokemon damage formula from Generation III onwards.
        Includes STAB (Same Type Attack Bonus) and type effectiveness.

        Args:
            defender: Pokemon being attacked
            attacker: Pokemon using the move

        Returns:
            int: Calculated damage amount (minimum 1)
        """
        # Get stats
        level = attacker.level
        attacker_attack = attacker.get_stat("attack")
        defender_defense = defender.get_stat("defense")
        if defender_defense == 0:
            defender_defense = 1

        # Base damage calculation (Gen III+ formula)
        # Damage = (((2×Level÷5+2)×Power×A÷D÷50)+2)×Modifiers
        base_damage = (((2 * level / 5 + 2) * self.power * attacker_attack / defender_defense) / 50) + 2

        # STAB: 1.5x if move type matches any of attacker's types
        stab_multiplier = 1.5 if attacker.has_type(self.move_type.name) else 1.0

        # Type effectiveness
        type_effectiveness = calculate_dual_type_effectiveness(self.move_type, defender.types)

        # Random factor (0.85-1.0)
        random_factor = random.uniform(0.85, 1.0)

        # Calculate final damage
        final_damage = base_damage * stab_multiplier * type_effectiveness * random_factor

        # Ensure minimum damage of 1
        return max(1, int(final_damage))

    def check_hit(self) -> bool:
        """
        Check if this move hits based on its accuracy.

        Returns:
            bool: True if move hits, False if it misses
        """
        # Generate random number from 1-100, move hits if it's <= accuracy
        return random.randint(1, 100) <= self.accuracy

    def use(self) -> bool:
        """
        Use this move (decrement PP).

        Returns:
            bool: True if move was used successfully (had PP available),
                  False if no PP remaining
        """
        if self.current_pp > 0:
            self.current_pp -= 1
            return True
        return False

    def is_usable(self) -> bool:
        """
        Check if this move can be used (has PP remaining).

        Returns:
            bool: True if current_pp > 0, False otherwise
        """
        return self.current_pp > 0

    def __str__(self) -> str:
        """Return the move name as a string."""
        return self.name

    def __repr__(self) -> str:
        """Return a detailed string representation of the move."""
        return f"Move('{self.name}', {self.move_type.name}, power={self.power}, pp={self.current_pp}/{self.pp})"
