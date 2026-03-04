"""
Team Module

This module handles team-related functionality using dictionaries and functions.

A Team is represented as a dictionary with these keys:
    {
        "pokemon_list": list[dict],      # List of Pokemon dictionaries (max 6)
        "current_pokemon_index": int     # Index of currently active Pokemon
    }

Functions:
- create_team() - Create a new empty team
- add_pokemon() - Add a Pokemon to the team (max 6)
- get_current_pokemon() - Get the currently active Pokemon
- switch_pokemon() - Switch to a different Pokemon
- all_fainted() - Check if all Pokemon have fainted
- get_available_pokemon() - Get all non-fainted Pokemon
- get_available_for_switch() - Get non-fainted Pokemon except current
"""

from pokemon import *


def create_team():
    """
    Create a new empty team.

    Returns:
        dict: Empty team dictionary
    """
    # TODO 2: Team Management
    # TODO 2.1: Return dict with empty pokemon_list and current_pokemon_index = 0
    pass


def add_pokemon(team, pokemon):
    """
    Add a Pokemon to the team.

    Args:
        team: Team dictionary
        pokemon: Pokemon dictionary to add

    Returns:
        bool: True if Pokemon was added, False if team is full (6 Pokemon)
    """
    # TODO 2.2: Check if team has < 6 Pokemon, append if yes, return True/False
    pass


def get_current_pokemon(team):
    """
    Get the currently active Pokemon.

    Args:
        team: Team dictionary

    Returns:
        dict | None: The active Pokemon dictionary, or None if team is empty or index invalid
    """
    # TODO 2.3: Get pokemon at current_pokemon_index, return None if invalid
    pass


def switch_pokemon(team, index):
    """
    Switch to a different Pokemon by index.

    Args:
        team: Team dictionary
        index: Index of Pokemon to switch to (0-5)

    Returns:
        bool: True if switch was successful, False if index is invalid
    """
    # TODO 2.4: Validate index, set current_pokemon_index if valid, return True/False
    pass


def all_fainted(team):
    """
    Check if all Pokemon in the team have fainted.

    Args:
        team: Team dictionary

    Returns:
        bool: True if all Pokemon are fainted, False otherwise
    """
    # TODO 3: Team State Checks
    # TODO 3.1: Loop through pokemon_list, return False if any not fainted
    pass


def get_available_pokemon(team):
    """
    Get all non-fainted Pokemon in the team.

    Args:
        team: Team dictionary

    Returns:
        list[tuple[int, dict]]: List of (index, pokemon_dict) tuples for non-fainted Pokemon
    """
    available = []
    for i, pokemon in enumerate(team["pokemon_list"]):
        if not is_fainted(pokemon):
            available.append((i, pokemon))
    return available


def get_available_for_switch(team):
    """
    Get all non-fainted Pokemon that aren't currently active.

    Args:
        team: Team dictionary

    Returns:
        list[tuple[int, dict]]: List of (index, pokemon_dict) tuples for non-fainted,
                                non-active Pokemon
    """
    available = []
    for i, pokemon in enumerate(team["pokemon_list"]):
        if not is_fainted(pokemon) and i != team["current_pokemon_index"]:
            available.append((i, pokemon))
    return available


def get_team_size(team):
    """
    Get the number of Pokemon in the team.

    Args:
        team: Team dictionary

    Returns:
        int: Number of Pokemon in pokemon_list
    """
    # TODO 3.2: Return length of pokemon_list
    pass


def team_to_string(team):
    """
    Get a string representation of the team.

    Args:
        team: Team dictionary

    Returns:
        str: String representation showing number of Pokemon and their names
    """
    if not team["pokemon_list"]:
        return "Team (empty)"

    pokemon_names = ', '.join([p["name"] for p in team["pokemon_list"]])
    return f"Team ({len(team['pokemon_list'])} Pokemon: {pokemon_names})"
