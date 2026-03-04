"""
Pokemon Battle Simulator - Main Game

This is the main entry point for the Pokemon Battle Simulator.
It handles:
- Player input and game flow
- AI opponent logic
- Game loop and battle orchestration

All UI code has been extracted to ui_helper.py module.

Run this file to start a Pokemon battle!
"""

import random
import os

from data_loader import *
from team import *
from battle import *
from pokemon import *
from move import *
from team_parser import *
from ui_helper import *


# Input Handler Functions

def get_player_action():
    """
    Get the player's action choice (FIGHT or POKEMON).

    Returns:
        str: 'fight' or 'pokemon'
    """
    while True:
        choice = input("\nChoose action (1=FIGHT, 2=POKEMON): ").strip()

        if choice == '1' or choice.lower() == 'fight':
            return 'fight'
        elif choice == '2' or choice.lower() == 'pokemon':
            return 'pokemon'
        else:
            print("Invalid choice. Please enter 1 or 2.")


# Arrow Key Navigation Input Handlers

def get_action_with_arrows(battle):
    """
    Get player action using arrow keys (no Enter needed to move selection).

    Navigation:
    - Up/Down: Toggle between FIGHT (1) and POKEMON (2)
    - Enter: Confirm selection

    Args:
        battle: Battle dictionary

    Returns:
        str: 'fight' or 'pokemon'
    """
    selected = 1  # Start with FIGHT

    while True:
        display_action_menu_screen(battle, selected)

        key = getch()

        if key in ['w', 'W']:  # Up arrow (mapped to W)
            selected = 1  # FIGHT
        elif key in ['s', 'S']:  # Down arrow (mapped to S)
            selected = 2  # POKEMON
        elif key in ['\r', '\n']:  # Enter key
            return 'fight' if selected == 1 else 'pokemon'


def get_pokemon_selection_with_arrows(team, allow_cancel=True):
    """
    Get Pokemon selection using arrow keys with 2x3 grid navigation + Cancel button.

    Grid positions:
        1 | 2
       ---|---
        3 | 4
       ---|---
        5 | 6
           |
        Cancel (7)

    Navigation:
    - Up/Down/Left/Right: Navigate the grid
    - From slot 6, can go down to Cancel
    - From Cancel, can go up to slot 6
    - Enter: Confirm selection (if valid - not fainted and not current)
    - Escape/B: Cancel (same as selecting Cancel)

    Args:
        team: The player's team dictionary
        allow_cancel: Whether Cancel option is available (default True)

    Returns:
        int | None: Index of Pokemon to switch to (0-5), or None if cancelled
    """
    # Find first valid Pokemon to start selection on
    selected = 1  # Default to slot 1
    pokemon_list = team["pokemon_list"]
    current_index = team["current_pokemon_index"]

    for i in range(6):
        if i < len(pokemon_list):
            pokemon = pokemon_list[i]
            if not is_fainted(pokemon) and i != current_index:
                selected = i + 1  # Slots are 1-indexed
                break

    while True:
        display_pokemon_select_screen(team, selected)

        key = getch()

        # Arrow key navigation (2x3 grid + Cancel)
        if key in ['w', 'W']:  # Up
            if selected == 3:
                selected = 1
            elif selected == 4:
                selected = 2
            elif selected == 5:
                selected = 3
            elif selected == 6:
                selected = 4
            elif selected == 7:  # From Cancel up to slot 6
                selected = 6
        elif key in ['s', 'S']:  # Down
            if selected == 1:
                selected = 3
            elif selected == 2:
                selected = 4
            elif selected == 3:
                selected = 5
            elif selected == 4:
                selected = 6
            elif selected == 6 and allow_cancel:
                selected = 7  # From slot 6 down to Cancel
        elif key in ['a', 'A']:  # Left
            if selected == 2:
                selected = 1
            elif selected == 4:
                selected = 3
            elif selected == 6:
                selected = 5
        elif key in ['d', 'D']:  # Right
            if selected == 1:
                selected = 2
            elif selected == 3:
                selected = 4
            elif selected == 5:
                selected = 6
        elif key in ['\r', '\n']:  # Enter - confirm selection
            if selected == 7:  # Cancel selected
                return None

            # Convert slot to index (1-indexed to 0-indexed)
            index = selected - 1

            # Validate selection
            if index >= len(pokemon_list):
                # Empty slot - stay in loop
                continue

            pokemon = pokemon_list[index]
            if is_fainted(pokemon):
                # Fainted Pokemon - stay in loop
                continue

            if index == current_index:
                # Already active - stay in loop
                continue

            return index
        elif key in ['\x1b', 'b', 'B']:  # Escape or B key - cancel
            if allow_cancel:
                return None


# Note: All display functions have been moved to ui_helper.py


def get_forced_switch_choice(team):
    """
    Force the player to choose a Pokemon when current one faints.
    Uses arrow key navigation with Pokemon select screen.

    Args:
        team: The player's team dictionary

    Returns:
        int: Index of Pokemon to switch to
    """
    # Use arrow key navigation, but don't allow cancel (forced switch)
    while True:
        index = get_pokemon_selection_with_arrows(team, allow_cancel=False)
        if index is not None:
            return index
        # If somehow None is returned despite allow_cancel=False, loop again


def ai_select_switch(team):
    """
    AI randomly selects a non-fainted Pokemon to switch to.

    Args:
        team: The AI's team dictionary

    Returns:
        int: Index of Pokemon to switch to
    """
    available = get_available_for_switch(team)

    if not available:
        # This shouldn't happen, but just in case
        return team["current_pokemon_index"]

    index, _ = random.choice(available)
    return index


def setup_teams():
    """
    Create hardcoded teams for the battle.

    Returns:
        Tuple of (player_team, ai_team)
    """
    return create_hardcoded_teams()


def run_battle(player_team, ai_team):
    """
    Run the battle loop.

    Handles the complete battle flow from start to finish:
    - Initialize battle
    - Run turn-based battle loop
    - Handle player actions (fight/switch)
    - Handle AI actions
    - Display battle results

    Args:
        player_team: Player's team dictionary
        ai_team: AI's team dictionary
    """
    # Initialize battle
    battle = create_battle(player_team, ai_team)

    print("\n" + "=" * 60)
    print("BATTLE START!")
    print("=" * 60)
    input("\nPress Enter to begin...")

    # Main battle loop
    while True:
        # Check if battle is over first (inline check)
        if all_fainted(battle["ai_team"]):
            print("\n🎉 YOU WIN! 🎉")
            print("All opponent's Pokemon have fainted!")
            break
        elif all_fainted(battle["player_team"]):
            print("\n💀 YOU LOSE! 💀")
            print("All your Pokemon have fainted!")
            break

        # State 1: Action Menu (with arrow key navigation)
        action = get_action_with_arrows(battle)

        player_pokemon = get_current_pokemon(battle["player_team"])
        ai_pokemon = get_current_pokemon(battle["ai_team"])

        if action == 'fight':
            # State 2: Battle Readout - Simplified turn (player always goes first)
            # Player attacks first
            first_attack = execute_single_attack(battle, "player", "ai")
            display_battle_readout_screen(battle, first_attack["messages"])

            if first_attack["hit"] and first_attack["damage"] > 0:
                update_hp_bar_in_place(battle, first_attack["defender"])

            move_cursor(18, 1)
            input("│ Press Enter to continue...")

            # AI attacks second (if not fainted)
            if not first_attack["defender_fainted"]:
                second_attack = execute_single_attack(battle, "ai", "player")
                display_battle_readout_screen(battle, second_attack["messages"])

                if second_attack["hit"] and second_attack["damage"] > 0:
                    update_hp_bar_in_place(battle, second_attack["defender"])

                move_cursor(18, 1)
                input("│ Press Enter to continue...")

                # Handle AI Pokemon fainting
                if second_attack["defender_fainted"]:
                    if not all_fainted(battle["player_team"]):
                        switch_index = get_forced_switch_choice(battle["player_team"])
                        switch_pokemon(battle["player_team"], switch_index)

            # Handle Player Pokemon fainting from first attack
            if first_attack["defender_fainted"]:
                if not all_fainted(battle["ai_team"]):
                    switch_index = ai_select_switch(battle["ai_team"])
                    switch_pokemon(battle["ai_team"], switch_index)

        elif action == 'pokemon':
            # Switch Pokemon flow using arrow key navigation
            switch_index = get_pokemon_selection_with_arrows(battle["player_team"], allow_cancel=True)
            if switch_index is not None:
                switch_pokemon(battle["player_team"], switch_index)


def main():
    """
    Main game loop.

    Orchestrates the high-level game flow:
    1. Initialize game systems
    2. Set up teams
    3. Run battle
    """
    # Welcome message
    print("=" * 60)
    print("POKEMON BATTLE SIMULATOR")
    print("=" * 60)
    print("\nWelcome to the Pokemon Battle Simulator!")

    # Set up teams
    player_team, ai_team = setup_teams()

    # Run battle
    run_battle(player_team, ai_team)

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
