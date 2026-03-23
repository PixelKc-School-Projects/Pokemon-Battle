"""
Team Class

This module implements the Team class which manages a team of up to 6 Pokemon.

A Team:
- Holds up to 6 Pokemon in a list
- Tracks which Pokemon is currently active
- Handles switching between Pokemon
- Checks if all Pokemon have fainted (battle loss condition)

This demonstrates composition - a Team contains Pokemon objects.
"""

from pokemon import Pokemon
from typing import Optional


class Team:
    """
    Represents a team of Pokemon (up to 6).

    The team tracks which Pokemon is currently in battle and provides
    methods for managing the team during battle.
    """

    def __init__(self):
        """Initialize an empty team."""
        self.pokemon_list = []
        self.current_pokemon_index = 0

    def add_pokemon(self, pokemon: Pokemon) -> bool:
        """
        Add a Pokemon to the team.

        Args:
            pokemon: Pokemon object to add

        Returns:
            bool: True if Pokemon was added, False if team is full (6 Pokemon)
        """
        if len(self.pokemon_list) < 6:
            self.pokemon_list.append(pokemon)
            return True
        return False

    def get_current_pokemon(self) -> Optional[Pokemon]:
        """
        Get the currently active Pokemon.

        Returns:
            Pokemon | None: The active Pokemon, or None if team is empty or index invalid
        """
        return self.pokemon_list[self.current_pokemon_index] if 0 <= self.current_pokemon_index < len(self.pokemon_list) else None

    def switch_pokemon(self, index: int) -> bool:
        """
        Switch to a different Pokemon by index.

        Args:
            index: Index of Pokemon to switch to (0-5)

        Returns:
            bool: True if switch was successful, False if index is invalid
                  or Pokemon at that index doesn't exist
        """
        if 0 <= self.current_pokemon_index < len(self.pokemon_list):
            self.current_pokemon_index = index
            return True
        return False

    def all_fainted(self) -> bool:
        """
        Check if all Pokemon in the team have fainted.

        Returns:
            bool: True if all Pokemon are fainted, False otherwise
        """
        for pokemon in self.pokemon_list:
            if not pokemon.is_fainted():
                return False
        return True

    # NOTE: The methods below are HELPER METHODS (pre-implemented)
    # You don't need to implement these in Week 26!

    def get_available_pokemon(self) -> list[tuple[int, Pokemon]]:
        """
        Get all non-fainted Pokemon in the team.

        Returns:
            list[tuple[int, Pokemon]]: List of (index, Pokemon) tuples for non-fainted Pokemon
        """
        available = []
        for i, pokemon in enumerate(self.pokemon_list):
            if not pokemon.is_fainted():
                available.append((i, pokemon))
        return available

    def get_available_for_switch(self) -> list[tuple[int, Pokemon]]:
        """
        Get all non-fainted Pokemon that aren't currently active.

        Returns:
            list[tuple[int, Pokemon]]: List of (index, Pokemon) tuples for non-fainted,
                                       non-active Pokemon
        """
        available = []
        for i, pokemon in enumerate(self.pokemon_list):
            if not pokemon.is_fainted() and i != self.current_pokemon_index:
                available.append((i, pokemon))
        return available

    def __len__(self) -> int:
        """
        Get the number of Pokemon in the team.

        Returns:
            int: Number of Pokemon in pokemon_list
        """
        return len(self.pokemon_list)

    def __str__(self) -> str:
        """Return a string representation of the team."""
        if not self.pokemon_list:
            return "Team (empty)"

        pokemon_names = ', '.join([p.name for p in self.pokemon_list])
        return f"Team ({len(self.pokemon_list)} Pokemon: {pokemon_names})"

    def __repr__(self) -> str:
        """Return a detailed string representation of the team."""
        return f"Team(pokemon_count={len(self.pokemon_list)}, current_index={self.current_pokemon_index})"
