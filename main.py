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
from typing import Optional

from data_loader import create_type_system, load_pokemon, get_available_pokemon, create_pokemon_from_data, load_pokemon_data
from team import Team
from battle import Battle
from pokemon import Pokemon
from move import Move
from team_parser import parse_team_file, validate_team_data, get_team_summary
from ui_helper import (
    getch, move_cursor, update_hp_bar_in_place,
    display_action_menu_screen, display_move_selection_screen,
    display_battle_readout_screen, display_pokemon_select_screen
)


# Input Handler Functions

def get_player_action() -> str:
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


def get_move_selection_input(pokemon: Pokemon) -> Optional[Move]:
    """
    Get the player's move selection.

    Args:
        pokemon: The player's current Pokemon

    Returns:
        Move | None: Selected Move, or None if player chose 'back'
    """
    while True:
        choice = input("\nChoose move (1-4) or 'back': ").strip().lower()

        if choice == 'back':
            return None

        try:
            move_num = int(choice)
            if move_num < 1 or move_num > 4:
                print("Invalid choice. Please enter 1-4 or 'back'.")
                continue

            move = pokemon.get_move(move_num)
            if move is None:
                print("That move slot is empty. Choose another.")
                continue

            if not move.is_usable():
                print("That move has no PP left. Choose another.")
                continue

            return move

        except ValueError:
            print("Invalid input. Please enter a number (1-4) or 'back'.")


# Arrow Key Navigation Input Handlers

def get_action_with_arrows(battle: Battle) -> str:
    """
    Get player action using arrow keys (no Enter needed to move selection).

    Navigation:
    - Up/Down: Toggle between FIGHT (1) and POKEMON (2)
    - Enter: Confirm selection

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


def get_move_with_arrows(battle: Battle, pokemon: Pokemon) -> Optional[Move]:
    """
    Get move selection using arrow keys with 4-way grid navigation.

    Grid positions:
        1 | 2
       ---|---
        3 | 4

    Navigation:
    - Up: 3→1, 4→2 (move up one row)
    - Down: 1→3, 2→4 (move down one row)
    - Left: 2→1, 4→3 (move left one column)
    - Right: 1→2, 3→4 (move right one column)
    - Enter: Confirm selection (if valid move with PP)
    - Escape/B: Go back to action menu

    Returns:
        Move object or None (if back to action menu)
    """
    selected = 1  # Start with move 1

    while True:
        display_move_selection_screen(battle, selected)

        key = getch()

        # Arrow key navigation (4-way grid)
        if key in ['w', 'W']:  # Up
            if selected == 3:
                selected = 1
            elif selected == 4:
                selected = 2
        elif key in ['s', 'S']:  # Down
            if selected == 1:
                selected = 3
            elif selected == 2:
                selected = 4
        elif key in ['a', 'A']:  # Left
            if selected == 2:
                selected = 1
            elif selected == 4:
                selected = 3
        elif key in ['d', 'D']:  # Right
            if selected == 1:
                selected = 2
            elif selected == 3:
                selected = 4
        elif key in ['\r', '\n']:  # Enter - confirm selection
            move = pokemon.get_move(selected)
            if move is None:
                # Empty slot - stay in loop
                continue
            if not move.is_usable():
                # No PP left - stay in loop
                continue
            return move
        elif key in ['\x1b', 'b', 'B']:  # Escape or B key - go back
            return None


def get_pokemon_selection_with_arrows(team: Team, allow_cancel: bool = True) -> Optional[int]:
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
        team: The player's team
        allow_cancel: Whether Cancel option is available (default True)

    Returns:
        int | None: Index of Pokemon to switch to (0-5), or None if cancelled
    """
    # Find first valid Pokemon to start selection on
    selected = 1  # Default to slot 1
    for i in range(6):
        if i < len(team.pokemon_list):
            pokemon = team.pokemon_list[i]
            if not pokemon.is_fainted() and i != team.current_pokemon_index:
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
            if index >= len(team.pokemon_list):
                # Empty slot - stay in loop
                continue

            pokemon = team.pokemon_list[index]
            if pokemon.is_fainted():
                # Fainted Pokemon - stay in loop
                continue

            if index == team.current_pokemon_index:
                # Already active - stay in loop
                continue

            return index
        elif key in ['\x1b', 'b', 'B']:  # Escape or B key - cancel
            if allow_cancel:
                return None


# Note: All display functions have been moved to ui_helper.py


def get_forced_switch_choice(team: Team) -> int:
    """
    Force the player to choose a Pokemon when current one faints.
    Uses arrow key navigation with Pokemon select screen.

    Args:
        team: The player's team

    Returns:
        int: Index of Pokemon to switch to
    """
    # Use arrow key navigation, but don't allow cancel (forced switch)
    while True:
        index = get_pokemon_selection_with_arrows(team, allow_cancel=False)
        if index is not None:
            return index
        # If somehow None is returned despite allow_cancel=False, loop again


def ai_select_move(pokemon: Pokemon) -> Optional[Move]:
    """
    AI randomly selects a move from available moves.

    Args:
        pokemon: The AI's current Pokemon

    Returns:
        Move | None: Selected Move, or None if no moves available
    """
    available_moves = pokemon.get_available_moves()

    if not available_moves:
        return None

    _, move = random.choice(available_moves)
    return move


def ai_select_switch(team: Team) -> int:
    """
    AI randomly selects a non-fainted Pokemon to switch to.

    Args:
        team: The AI's team

    Returns:
        int: Index of Pokemon to switch to
    """
    available = team.get_available_for_switch()

    if not available:
        # This shouldn't happen, but just in case
        return team.current_pokemon_index

    index, _ = random.choice(available)
    return index


def create_default_teams(type_system: dict) -> tuple[Team, Team]:
    """
    Create default teams for player and AI.

    Args:
        type_system: Dictionary mapping type names to Type objects

    Returns:
        tuple[Team, Team]: (player_team, ai_team)
    """
    # Get available Pokemon
    available_pokemon = get_available_pokemon()

    if len(available_pokemon) < 12:
        print(f"Warning: Only {len(available_pokemon)} Pokemon available. Need at least 12 for two full teams.")

    # Player team - first 6 Pokemon
    player_team = Team()
    print("\nCreating your team...")
    for pokemon_name in available_pokemon[:6]:
        try:
            pokemon = load_pokemon(pokemon_name, type_system)
            player_team.add_pokemon(pokemon)
            print(f"  Added {pokemon.name} to your team")
        except Exception as e:
            print(f"  Error loading {pokemon_name}: {e}")

    # AI team - next 6 Pokemon (or repeat if not enough)
    ai_team = Team()
    print("\nCreating opponent's team...")
    ai_pokemon_names = available_pokemon[6:12] if len(available_pokemon) >= 12 else available_pokemon[:6]
    for pokemon_name in ai_pokemon_names:
        try:
            pokemon = load_pokemon(pokemon_name, type_system)
            ai_team.add_pokemon(pokemon)
            print(f"  Added {pokemon.name} to opponent's team")
        except Exception as e:
            print(f"  Error loading {pokemon_name}: {e}")

    return player_team, ai_team


def get_team_files() -> list[str]:
    """
    Get list of team files from teams/ directory.

    Returns:
        List of team file paths
    """
    # Use absolute path based on script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    teams_dir = os.path.join(script_dir, "teams")

    if not os.path.exists(teams_dir):
        return []

    team_files = []
    for filename in os.listdir(teams_dir):
        if filename.endswith('.txt'):
            team_files.append(os.path.join(teams_dir, filename))

    return sorted(team_files)


def create_team_from_file(team_file: str, type_system: dict) -> Optional[Team]:
    """
    Create a team from a team file using the team parser.

    Args:
        team_file: Path to team file
        type_system: Dictionary mapping type names to Type objects

    Returns:
        Team object, or None if loading failed
    """
    try:
        # Parse team file
        team_data = parse_team_file(team_file)

        # Get available Pokemon and moves for validation
        available_pokemon = get_available_pokemon()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        available_moves_dir = os.path.join(script_dir, "data", "moves")
        available_moves = [f[:-5] for f in os.listdir(available_moves_dir) if f.endswith('.json')]

        # Validate team
        is_valid, errors = validate_team_data(team_data, available_pokemon, available_moves)

        if not is_valid:
            print(f"\n✗ Team file validation failed:")
            for error in errors:
                print(f"  - {error}")
            return None

        # Create team
        team = Team()
        print(f"\nLoading team from {os.path.basename(team_file)}...")

        for entry in team_data:
            pokemon_name = entry["pokemon"]
            move_names = entry["moves"]

            try:
                # Load Pokemon data
                pokemon_data = load_pokemon_data(pokemon_name)

                # Create Pokemon with custom moves
                pokemon = create_pokemon_from_data(pokemon_data, type_system, move_names=move_names)

                team.add_pokemon(pokemon)
                print(f"  ✓ Added {pokemon.name} with custom moves")

            except Exception as e:
                print(f"  ✗ Error loading {pokemon_name}: {e}")
                return None

        print(f"✓ Team loaded successfully ({len(team)} Pokemon)")
        return team

    except FileNotFoundError:
        print(f"\n✗ Team file not found: {team_file}")
        return None
    except ValueError as e:
        print(f"\n✗ Team file error: {e}")
        return None
    except Exception as e:
        print(f"\n✗ Unexpected error loading team: {e}")
        return None


def select_team_file() -> Optional[str]:
    """
    Display team files and let user select one.

    Returns:
        Selected team file path, or None if cancelled
    """
    team_files = get_team_files()

    if not team_files:
        print("\n✗ No team files found in teams/ directory")
        return None

    print("\nAvailable team files:")
    print("-" * 60)
    for i, team_file in enumerate(team_files, 1):
        filename = os.path.basename(team_file)
        print(f"  {i}. {filename}")

    print("\n  0. Cancel")
    print("-" * 60)

    while True:
        try:
            choice = input("\nSelect team file (0 to cancel): ").strip()
            choice_num = int(choice)

            if choice_num == 0:
                return None

            if 1 <= choice_num <= len(team_files):
                return team_files[choice_num - 1]
            else:
                print(f"Invalid choice. Please enter 0-{len(team_files)}")

        except ValueError:
            print("Invalid input. Please enter a number.")


def show_team_selection_menu() -> str:
    """
    Show main menu for team selection.

    Returns:
        str: 'default', 'custom', or 'exit'
    """
    print("\n" + "=" * 60)
    print("TEAM SELECTION")
    print("=" * 60)
    print("\n1. Quick Battle (default teams)")
    print("2. Custom Team Battle (load from file)")
    print("\n0. Exit")
    print("-" * 60)

    while True:
        choice = input("\nSelect option: ").strip()

        if choice == '1':
            return 'default'
        elif choice == '2':
            return 'custom'
        elif choice == '0':
            return 'exit'
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")


def select_and_create_team(
    team_label: str,
    type_system: dict,
    allow_exit_on_failure: bool = False
) -> Optional[Team]:
    """
    Unified function to select and create a team (player or AI).

    Handles the complete flow:
    - Display team selection menu
    - Load team from file
    - Fallback to default team if needed
    - Show team summary

    Args:
        team_label: Label for the team (e.g., "PLAYER" or "AI")
        type_system: Type system dictionary
        allow_exit_on_failure: If True, returns None on failure instead of falling back to default

    Returns:
        Team object, or None if allow_exit_on_failure=True and loading failed
    """
    print(f"\n--- {team_label} TEAM SELECTION ---")
    team_file = select_team_file()

    if team_file is None:
        print(f"\nNo team selected for {team_label}. Using default team...")
        team, _ = create_default_teams(type_system)
        return team

    team = create_team_from_file(team_file, type_system)

    if team is None:
        if allow_exit_on_failure:
            print(f"\nFailed to load {team_label} team.")
            return None
        else:
            print(f"\nFailed to load {team_label} team. Using default team...")
            team, _ = create_default_teams(type_system)
            return team

    # Show team summary
    team_data = parse_team_file(team_file)
    print(f"\n{team_label}'s team:")
    print(get_team_summary(team_data))

    return team


def setup_teams(type_system: dict) -> Optional[tuple[Team, Team]]:
    """
    Handle entire team setup process.

    Orchestrates team selection menu and team creation for both player and AI.

    Args:
        type_system: Type system dictionary

    Returns:
        Tuple of (player_team, ai_team), or None if setup failed/cancelled
    """
    menu_choice = show_team_selection_menu()

    if menu_choice == 'exit':
        return None

    if menu_choice == 'default':
        print("\nUsing default teams...")
        return create_default_teams(type_system)

    # Custom team selection
    player_team = select_and_create_team("PLAYER", type_system, allow_exit_on_failure=True)
    if player_team is None:
        return None

    ai_team = select_and_create_team("AI", type_system, allow_exit_on_failure=False)

    # Validate teams
    if len(player_team) == 0 or len(ai_team) == 0:
        print("\n✗ One or both teams are empty! Cannot start battle.")
        return None

    return player_team, ai_team


def run_battle(player_team: Team, ai_team: Team) -> None:
    """
    Run the battle loop.

    Handles the complete battle flow from start to finish:
    - Initialize battle
    - Run turn-based battle loop
    - Handle player actions (fight/switch)
    - Handle AI actions
    - Display battle results

    Args:
        player_team: Player's team
        ai_team: AI's team
    """
    # Initialize battle
    battle = Battle(player_team, ai_team)

    print("\n" + "=" * 60)
    print("BATTLE START!")
    print("=" * 60)
    input("\nPress Enter to begin...")

    # Main battle loop
    while True:
        # Check if battle is over first
        result = battle.check_battle_over()
        if result:
            if result == "player_wins":
                print("\n🎉 YOU WIN! 🎉")
                print("All opponent's Pokemon have fainted!")
            else:
                print("\n💀 YOU LOSE! 💀")
                print("All your Pokemon have fainted!")

            print("\n" + battle.get_battle_summary())
            break

        # State 1: Action Menu (with arrow key navigation)
        action = get_action_with_arrows(battle)

        player_pokemon = player_team.get_current_pokemon()
        ai_pokemon = ai_team.get_current_pokemon()

        if action == 'fight':
            # State 2: Move Selection (with arrow key navigation)
            player_move = get_move_with_arrows(battle, player_pokemon)

            if player_move is None:
                continue  # Player pressed 'back', return to action menu

            # Get AI move
            ai_move = ai_select_move(ai_pokemon)

            if ai_move is None:
                print("\nOpponent has no moves available!")
                continue

            # State 3: Battle Readout - Sequential Attacks
            turn_result = battle.execute_turn(player_move, ai_move)

            # Display first attack (HP bar shows pre-attack HP)
            first_attack = turn_result["first_attack"]
            display_battle_readout_screen(battle, first_attack["messages"])

            # Apply first attack damage while messages are showing
            if first_attack["hit"] and first_attack["damage"] > 0:
                if first_attack["defender"] == "player":
                    defender = battle.player_team.get_current_pokemon()
                else:
                    defender = battle.ai_team.get_current_pokemon()
                if defender:
                    defender.take_damage(first_attack["damage"])
                    # Update the HP bar in place to show damage
                    update_hp_bar_in_place(battle, first_attack["defender"])

            # Move cursor to bottom for input prompt
            move_cursor(18, 1)
            input("│ Press Enter to continue...")

            # Display second attack (if it happened) - HP bar now shows post-first-attack HP
            if turn_result["second_attack"] is not None:
                second_attack = turn_result["second_attack"]
                display_battle_readout_screen(battle, second_attack["messages"])

                # Apply second attack damage while messages are showing
                if second_attack["hit"] and second_attack["damage"] > 0:
                    if second_attack["defender"] == "player":
                        defender = battle.player_team.get_current_pokemon()
                    else:
                        defender = battle.ai_team.get_current_pokemon()
                    if defender:
                        defender.take_damage(second_attack["damage"])
                        # Update the HP bar in place to show damage
                        update_hp_bar_in_place(battle, second_attack["defender"])

                # Move cursor to bottom for input prompt
                move_cursor(18, 1)
                input("│ Press Enter to continue...")

            # Handle fainting - check both attacks for fainted status
            first_defender_fainted = first_attack["defender_fainted"]
            second_defender_fainted = (turn_result["second_attack"] is not None and
                                      turn_result["second_attack"]["defender_fainted"])

            # Determine which Pokemon fainted based on attack results
            if first_attack["defender"] == "player" and first_defender_fainted:
                # Player's Pokemon fainted
                if not player_team.all_fainted():
                    switch_index = get_forced_switch_choice(player_team)
                    battle.switch_pokemon(player_team, switch_index)
            elif first_attack["defender"] == "ai" and first_defender_fainted:
                # AI's Pokemon fainted
                if not ai_team.all_fainted():
                    switch_index = ai_select_switch(ai_team)
                    battle.switch_pokemon(ai_team, switch_index)

            # Check second attack fainting (only if it occurred)
            if second_defender_fainted:
                if turn_result["second_attack"]["defender"] == "player":
                    # Player's Pokemon fainted
                    if not player_team.all_fainted():
                        switch_index = get_forced_switch_choice(player_team)
                        battle.switch_pokemon(player_team, switch_index)
                elif turn_result["second_attack"]["defender"] == "ai":
                    # AI's Pokemon fainted
                    if not ai_team.all_fainted():
                        switch_index = ai_select_switch(ai_team)
                        battle.switch_pokemon(ai_team, switch_index)

        elif action == 'pokemon':
            # Switch Pokemon flow using arrow key navigation
            switch_index = get_pokemon_selection_with_arrows(player_team, allow_cancel=True)
            if switch_index is not None:
                battle.switch_pokemon(player_team, switch_index)


def main() -> None:
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

    # Initialize type system
    print("\nInitializing type system...")
    type_system = create_type_system()
    print("✓ Type system loaded")

    # Set up teams
    teams = setup_teams(type_system)
    if teams is None:
        print("\nGoodbye!")
        return

    player_team, ai_team = teams

    # Run battle
    run_battle(player_team, ai_team)

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
