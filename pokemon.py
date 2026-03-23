"""
Pokemon Class

This module implements the Pokemon class which represents an individual Pokemon with:
- Stats (HP, Attack, Defense, Speed)
- Types (1 or 2 Type objects)
- Moves (4 individual move slots: move1, move2, move3, move4)
- HP tracking
- Sprite URLs for display

Note: This demonstrates composition - Pokemon contains Type and Move objects.
"""

from type_system import Type
from move import Move
from typing import Optional


class Pokemon:
    """
    Represents an individual Pokemon with all its stats, types, and moves.

    Key Design Decisions:
    - Moves are stored as move1, move2, move3, move4 (NOT a list)
    - Only uses HP, Attack, Defense, Speed (ignores special-attack/special-defense)
    - Types is a list (can have 1 or 2 types)
    """

    def __init__(
        self,
        name: str,
        types: list[Type],
        stats: dict[str, int],
        move1: Optional[Move] = None,
        move2: Optional[Move] = None,
        move3: Optional[Move] = None,
        move4: Optional[Move] = None,
        sprite_url: str = "",
        sprite_url_back: str = ""
    ):
        """
        Initialize a Pokemon.

        Args:
            name: Pokemon name (e.g., "Charizard")
            types: List of Type objects (1 or 2 types)
            stats: Dictionary with keys: "hp", "attack", "defense", "speed"
            move1: First move slot (optional)
            move2: Second move slot (optional)
            move3: Third move slot (optional)
            move4: Fourth move slot (optional)
            sprite_url: URL for forward-facing sprite
            sprite_url_back: URL for backward-facing sprite
        """
        self.name: str = name
        self.types: list[Type] = types
        self.stats: dict[str, int] = stats
        self.move1: Optional[Move] = move1
        self.move2: Optional[Move] = move2
        self.move3: Optional[Move] = move3
        self.move4: Optional[Move] = move4
        self.sprite_url: str = sprite_url
        self.sprite_url_back: str = sprite_url_back
        self.level: int = 50
        self.max_hp: int = stats.get("hp", 0)
        self.current_hp: int = self.max_hp

    def take_damage(self, amount: int) -> None:
        """
        Reduce Pokemon's HP by the given amount.

        Args:
            amount: Damage amount to subtract from current HP
        """
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0

    def is_fainted(self) -> bool:
        """
        Check if this Pokemon has fainted.

        Returns:
            bool: True if current_hp is 0, False otherwise
        """
        return self.current_hp == 0

    def get_stat(self, stat_name: str) -> int:
        """
        Get a stat value by name.

        Args:
            stat_name: Stat name ("hp", "attack", "defense", "speed")

        Returns:
            int: The stat value, or 0 if stat doesn't exist
        """
        return self.stats.get(stat_name, 0)

    def get_move(self, move_number: int) -> Optional[Move]:
        """
        Get a move by its number (1-4).

        Args:
            move_number: Move slot number (1, 2, 3, or 4)

        Returns:
            Move | None: The Move object, or None if slot is empty or invalid number
        """
        return {1: self.move1, 2: self.move2, 3: self.move3, 4: self.move4}.get(move_number)

    # NOTE: The methods below are HELPER METHODS (pre-implemented)
    # You don't need to implement these in Week 26!

    def has_type(self, type_name: str) -> bool:
        """
        Check if this Pokemon has a specific type.

        Args:
            type_name: Type name to check (e.g., "fire", "water")

        Returns:
            bool: True if Pokemon has this type, False otherwise
        """
        for pokemon_type in self.types:
            if pokemon_type.name == type_name:
                return True
        return False

    def get_available_moves(self) -> list[tuple[int, Move]]:
        """
        Get all moves that have PP remaining.

        Returns:
            list[tuple[int, Move]]: List of (move_number, Move) tuples for usable moves
        """
        available = []

        if self.move1 is not None and self.move1.is_usable():
            available.append((1, self.move1))
        if self.move2 is not None and self.move2.is_usable():
            available.append((2, self.move2))
        if self.move3 is not None and self.move3.is_usable():
            available.append((3, self.move3))
        if self.move4 is not None and self.move4.is_usable():
            available.append((4, self.move4))

        return available

    def get_all_moves(self) -> list[tuple[int, Move]]:
        """
        Get all moves regardless of PP.

        Returns:
            list[tuple[int, Move]]: List of (move_number, Move) tuples for all moves
        """
        moves = []

        if self.move1 is not None:
            moves.append((1, self.move1))
        if self.move2 is not None:
            moves.append((2, self.move2))
        if self.move3 is not None:
            moves.append((3, self.move3))
        if self.move4 is not None:
            moves.append((4, self.move4))

        return moves

    def get_hp_percentage(self) -> float:
        """
        Get current HP as a percentage of max HP.

        Returns:
            float: HP percentage (0.0 to 1.0)
        """
        return self.current_hp / self.max_hp if self.max_hp > 0 else 0.0

    def __str__(self) -> str:
        """Return the Pokemon name as a string."""
        return self.name

    def __repr__(self) -> str:
        """Return a detailed string representation of the Pokemon."""
        type_names = '/'.join([t.name for t in self.types])
        return f"Pokemon('{self.name}', types={type_names}, hp={self.current_hp}/{self.max_hp}, level={self.level})"
