"""
UI Helper Module

This module contains all user interface code for the Pokemon Battle game.
Students should NOT need to understand or modify this code - it's pre-implemented
to handle complex cross-platform keyboard input and screen rendering.

This module provides:
- Cross-platform keyboard input (getch with arrow key support)
- Screen clearing and cursor positioning
- Pokemon-style slow text animation
- Battle screen layouts and grids
- HP bar rendering
- Menu and selection screens

Students can use these functions without needing to understand the implementation.
"""

import os
import sys
import time
from typing import Optional, TYPE_CHECKING

# Avoid circular imports
if TYPE_CHECKING:
    from battle import Battle
    from team import Team
    from pokemon import Pokemon
    from move import Move

# Configuration
ENABLE_TEXT_ANIMATION = True  # Toggle for Pokemon-style slow text printing


# Cross-platform single character input (no Enter required)
# Supports both WASD and arrow keys
if sys.platform == 'win32':
    import msvcrt

    def getch():
        """Get a single character from keyboard on Windows.
        Supports WASD and arrow keys.
        """
        key = msvcrt.getch()

        # Check for arrow keys (Windows sends \xe0 followed by direction)
        if key == b'\xe0':
            arrow = msvcrt.getch()
            if arrow == b'H':  # Up arrow
                return 'w'
            elif arrow == b'P':  # Down arrow
                return 's'
            elif arrow == b'K':  # Left arrow
                return 'a'
            elif arrow == b'M':  # Right arrow
                return 'd'

        # Regular key
        try:
            return key.decode('utf-8').lower()
        except (UnicodeDecodeError, AttributeError):
            return key.decode('latin-1').lower()
else:
    import termios
    import tty

    def getch():
        """Get a single character from keyboard on Unix/Mac.
        Supports WASD and arrow keys.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

            # Check for arrow keys (Unix/Mac sends escape sequence)
            if ch == '\x1b':  # ESC character
                # Read the next two characters
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)

                # Arrow keys send: \x1b[A (up), \x1b[B (down), \x1b[C (right), \x1b[D (left)
                # Or: \x1bOA, \x1bOB, \x1bOC, \x1bOD (application mode)
                if ch2 == '[':
                    if ch3 == 'A':  # Up arrow
                        return 'w'
                    elif ch3 == 'B':  # Down arrow
                        return 's'
                    elif ch3 == 'C':  # Right arrow
                        return 'd'
                    elif ch3 == 'D':  # Left arrow
                        return 'a'
                elif ch2 == 'O':
                    if ch3 == 'A':  # Up arrow (application mode)
                        return 'w'
                    elif ch3 == 'B':  # Down arrow (application mode)
                        return 's'
                    elif ch3 == 'C':  # Right arrow (application mode)
                        return 'd'
                    elif ch3 == 'D':  # Left arrow (application mode)
                        return 'a'

                # If it's not an arrow key, return the ESC character
                return ch.lower()

            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# Screen Utilities

def clear_screen():
    """
    Clear the terminal screen for clean display.
    Works on both Windows and Unix-based systems.
    """
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


def move_cursor(row: int, col: int):
    """Move cursor to specific position (1-indexed)."""
    print(f'\033[{row};{col}H', end='')
    sys.stdout.flush()


def update_hp_bar_in_place(battle: 'Battle', defender_owner: str):
    """
    Update the HP bar in place using cursor positioning.

    Args:
        battle: The Battle object
        defender_owner: "player" or "ai" - whose HP bar to update
    """
    if defender_owner == "ai":
        # AI Pokemon HP is on row 6
        pokemon = battle.ai_team.get_current_pokemon()
        row = 6
    else:
        # Player Pokemon HP is on row 9
        pokemon = battle.player_team.get_current_pokemon()
        row = 9

    if not pokemon:
        return

    # Build the HP line
    hp_percent = pokemon.get_hp_percentage() * 100
    hp_bar_length = 20
    hp_filled = int(hp_bar_length * pokemon.get_hp_percentage())
    hp_bar = "█" * hp_filled + "░" * (hp_bar_length - hp_filled)

    if defender_owner == "ai":
        hp_line = f"  HP: {pokemon.current_hp}/{pokemon.max_hp} [{hp_bar}] {hp_percent:.0f}%"
        hp_line_with_padding = "│" + hp_line + " " * (58 - len(hp_line)) + "│"
    else:
        hp_line = f"HP: {pokemon.current_hp}/{pokemon.max_hp} [{hp_bar}] {hp_percent:.0f}%  "
        padding = " " * (58 - len(hp_line))
        hp_line_with_padding = "│" + padding + hp_line + "│"

    # Move cursor to the row and column 1, then print the updated line
    move_cursor(row, 1)
    print(hp_line_with_padding, end='')
    sys.stdout.flush()


def print_slowly(text: str, delay: float = 0.03, add_newline: bool = True):
    """
    Print text character by character like in Pokemon games.

    Args:
        text: Text to print
        delay: Delay between characters in seconds (default 0.03s = 30ms)
        add_newline: Whether to add newline at end (default True)
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    if add_newline:
        print()  # Newline at end


# Text Layout Helper Functions

def wrap_text(text: str, max_width: int = 56) -> list[str]:
    """
    Wrap text to fit within max_width, breaking at spaces.

    Args:
        text: Text to wrap
        max_width: Maximum width per line (default 56 for message box)

    Returns:
        List of wrapped lines
    """
    if len(text) <= max_width:
        return [text]

    lines = []
    current_line = ""

    words = text.split()
    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += (" " if current_line else "") + word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# Drawing Functions

def draw_pokemon_header(battle: 'Battle') -> list[str]:
    """
    Draw the Pokemon header section (lines 1-10).

    Args:
        battle: The Battle object

    Returns:
        List of 10 strings for the header
    """
    lines = []

    player_pokemon = battle.player_team.get_current_pokemon()
    ai_pokemon = battle.ai_team.get_current_pokemon()

    # Header
    lines.append("┌" + "─" * 58 + "┐")
    lines.append("│" + "POKEMON BATTLE SIMULATOR".center(58) + "│")
    lines.append("├" + "─" * 58 + "┤")

    # Opponent Pokemon area
    lines.append("│" + " " * 58 + "│")
    if ai_pokemon:
        types_str = "/".join([t.name.capitalize() for t in ai_pokemon.types])
        hp_percent = ai_pokemon.get_hp_percentage() * 100
        hp_bar_length = 20
        hp_filled = int(hp_bar_length * ai_pokemon.get_hp_percentage())
        hp_bar = "█" * hp_filled + "░" * (hp_bar_length - hp_filled)

        opponent_line = f"  OPPONENT: {ai_pokemon.name.upper()} ({types_str})"
        lines.append("│" + opponent_line + " " * (58 - len(opponent_line)) + "│")

        hp_line = f"  HP: {ai_pokemon.current_hp}/{ai_pokemon.max_hp} [{hp_bar}] {hp_percent:.0f}%"
        lines.append("│" + hp_line + " " * (58 - len(hp_line)) + "│")
    else:
        lines.append("│  OPPONENT: (None)" + " " * 40 + "│")
        lines.append("│" + " " * 58 + "│")

    lines.append("│" + " " * 58 + "│")

    # Player Pokemon area
    if player_pokemon:
        types_str = "/".join([t.name.capitalize() for t in player_pokemon.types])
        hp_percent = player_pokemon.get_hp_percentage() * 100
        hp_bar_length = 20
        hp_filled = int(hp_bar_length * player_pokemon.get_hp_percentage())
        hp_bar = "█" * hp_filled + "░" * (hp_bar_length - hp_filled)

        player_line = f"YOU: {player_pokemon.name.upper()} ({types_str})  "
        padding = " " * (58 - len(player_line))
        lines.append("│" + padding + player_line + "│")

        hp_line = f"HP: {player_pokemon.current_hp}/{player_pokemon.max_hp} [{hp_bar}] {hp_percent:.0f}%  "
        padding = " " * (58 - len(hp_line))
        lines.append("│" + padding + hp_line + "│")
    else:
        lines.append("│" + " " * 42 + "YOU: (None)  │")
        lines.append("│" + " " * 58 + "│")

    lines.append("│" + " " * 58 + "│")

    return lines


def draw_action_menu(pokemon_name: str, selected_action: int = 1) -> list[str]:
    """
    Draw the action menu (What will Pokemon do? + FIGHT/POKEMON).

    Args:
        pokemon_name: Name of the player's current Pokemon
        selected_action: 1=FIGHT (default), 2=POKEMON

    Returns:
        List of 9 strings for the action menu section
    """
    lines = []

    # Truncate long Pokemon names if necessary
    if len(f"What will {pokemon_name} do?") > 38:
        pokemon_name = pokemon_name[:20] + "..."

    lines.append("├" + "─" * 58 + "┤")
    lines.append("│" + " " * 40 + "│" + " " * 17 + "│")

    what_will = "  What will"
    # Dynamic selection indicator for FIGHT
    fight_text = "    > FIGHT <    " if selected_action == 1 else "      FIGHT      "
    lines.append("│" + what_will + " " * (40 - len(what_will)) + "│" + fight_text + "│")

    pokemon_do = f"  {pokemon_name} do?"
    lines.append("│" + pokemon_do + " " * (40 - len(pokemon_do)) + "│" + " " * 17 + "│")

    lines.append("│" + " " * 40 + "│" + " " * 17 + "│")
    # Dynamic selection indicator for POKEMON
    pokemon_text = "   > POKEMON <   " if selected_action == 2 else "     POKEMON     "
    lines.append("│" + " " * 40 + "│" + pokemon_text + "│")
    lines.append("│" + " " * 40 + "│" + " " * 17 + "│")
    lines.append("│" + " " * 40 + "│" + " " * 17 + "│")
    lines.append("└" + "─" * 58 + "┘")

    return lines


def draw_move_grid(pokemon: 'Pokemon', selected_move_index: int) -> list[str]:
    """
    Draw the 2x2 move grid with type/PP info.

    Args:
        pokemon: The Pokemon whose moves to display
        selected_move_index: Which move is selected (1-4)

    Returns:
        List of 9 strings for the move grid section
    """
    lines = []

    # Get all 4 moves
    moves = []
    for i in range(1, 5):
        move = pokemon.get_move(i)
        moves.append(move)

    # Get selected move info
    selected_move = moves[selected_move_index - 1] if selected_move_index in range(1, 5) else None

    # Helper function to center text in cell
    def center_in_cell(text: str, width: int = 19) -> str:
        if len(text) > width:
            text = text[:width - 3] + "..."
        padding = width - len(text)
        left_pad = padding // 2
        right_pad = padding - left_pad
        return " " * left_pad + text + " " * right_pad

    # Helper function to format move name
    def format_move(move: Optional['Move'], move_num: int) -> str:
        if move is None:
            return center_in_cell("---")

        move_name = move.name.upper()
        if move_num == selected_move_index:
            # Add selection markers
            marked = f"> {move_name} <"
            return center_in_cell(marked)
        else:
            return center_in_cell(move_name)

    # Build grid
    lines.append("├" + "─" * 58 + "┤")

    # Row 1: Top cells
    lines.append("│" + " " * 19 + "│" + " " * 19 + "│" + " " * 18 + "│")

    move1_text = format_move(moves[0], 1)
    move2_text = format_move(moves[1], 2)
    type_text = ""
    if selected_move:
        type_name = selected_move.move_type.name.upper()
        type_text = center_in_cell(type_name, 18)
    else:
        type_text = " " * 18

    lines.append("│" + move1_text + "│" + move2_text + "│" + type_text + "│")
    lines.append("│" + " " * 19 + "│" + " " * 19 + "│" + " " * 18 + "│")

    # Horizontal divider
    lines.append("│" + "─" * 19 + "│" + "─" * 19 + "│" + " " * 18 + "│")

    # Row 2: Bottom cells with PP on separate line above moves
    pp_text = ""
    if selected_move:
        pp_str = f"PP: {selected_move.current_pp}/{selected_move.pp}"
        pp_text = center_in_cell(pp_str, 18)
    else:
        pp_text = " " * 18

    lines.append("│" + " " * 19 + "│" + " " * 19 + "│" + pp_text + "│")

    move3_text = format_move(moves[2], 3)
    move4_text = format_move(moves[3], 4)

    lines.append("│" + move3_text + "│" + move4_text + "│" + " " * 18 + "│")
    lines.append("│" + " " * 19 + "│" + " " * 19 + "│" + " " * 18 + "│")
    lines.append("└" + "─" * 58 + "┘")

    return lines


def draw_message_area() -> list[str]:
    """
    Draw empty message area for battle readout.

    Returns:
        List of 9 strings for the message area
    """
    lines = []

    lines.append("├" + "─" * 58 + "┤")
    for _ in range(7):
        lines.append("│" + " " * 58 + "│")
    lines.append("└" + "─" * 58 + "┘")

    return lines


def draw_pokemon_select_grid(team: 'Team', selected_slot: int) -> list[str]:
    """
    Draw the Pokemon selection grid (2x3 grid + Cancel button).

    Grid layout:
        Slot 1  |  Slot 2
        Slot 3  |  Slot 4
        Slot 5  |  Slot 6
              Cancel

    Args:
        team: The player's team
        selected_slot: Which slot is selected (1-6 for Pokemon, 7 for Cancel)

    Returns:
        List of 16 strings for the Pokemon select screen
    """
    lines = []
    pokemon_list = team.pokemon_list

    # Helper function to format Pokemon name with selection indicator
    def format_pokemon_name(pokemon: 'Pokemon', slot_num: int, width: int = 28) -> str:
        name = pokemon.name.capitalize()
        if slot_num == selected_slot:
            # Add selection markers
            name_with_markers = f" > {name} <"
        else:
            name_with_markers = f"   {name}"

        # Pad to width
        if len(name_with_markers) > width:
            name_with_markers = name_with_markers[:width]
        return name_with_markers + " " * (width - len(name_with_markers))

    # Helper function to format type string
    def format_types(pokemon: 'Pokemon', width: int = 28) -> str:
        types_str = "/".join([t.name for t in pokemon.types])
        formatted = f"   ({types_str})"
        if len(formatted) > width:
            formatted = formatted[:width]
        return formatted + " " * (width - len(formatted))

    # Helper function to format HP/status
    def format_hp(pokemon: 'Pokemon', width: int = 28) -> str:
        if pokemon.is_fainted():
            status = "   FAINTED"
        else:
            status = f"   HP: {pokemon.current_hp}/{pokemon.max_hp}"
        if len(status) > width:
            status = status[:width]
        return status + " " * (width - len(status))

    # Header
    lines.append("┌" + "─" * 58 + "┐")
    lines.append("│" + "POKEMON BATTLE SIMULATOR".center(58) + "│")
    lines.append("├" + "─" * 58 + "┤")

    # Row 1: Slots 1 and 2
    pokemon1 = pokemon_list[0] if len(pokemon_list) > 0 else None
    pokemon2 = pokemon_list[1] if len(pokemon_list) > 1 else None

    if pokemon1:
        name1 = format_pokemon_name(pokemon1, 1)
        types1 = format_types(pokemon1)
        hp1 = format_hp(pokemon1)
    else:
        name1 = " " * 28
        types1 = " " * 28
        hp1 = " " * 28

    if pokemon2:
        name2 = format_pokemon_name(pokemon2, 2)
        types2 = format_types(pokemon2)
        hp2 = format_hp(pokemon2)
    else:
        name2 = " " * 28
        types2 = " " * 28
        hp2 = " " * 28

    lines.append("│" + name1 + "││" + name2 + "│")
    lines.append("│" + types1 + "││" + types2 + "│")
    lines.append("│" + hp1 + "││" + hp2 + "│")
    lines.append("├" + "─" * 28 + "┤├" + "─" * 28 + "┤")

    # Row 2: Slots 3 and 4
    pokemon3 = pokemon_list[2] if len(pokemon_list) > 2 else None
    pokemon4 = pokemon_list[3] if len(pokemon_list) > 3 else None

    if pokemon3:
        name3 = format_pokemon_name(pokemon3, 3)
        types3 = format_types(pokemon3)
        hp3 = format_hp(pokemon3)
    else:
        name3 = " " * 28
        types3 = " " * 28
        hp3 = " " * 28

    if pokemon4:
        name4 = format_pokemon_name(pokemon4, 4)
        types4 = format_types(pokemon4)
        hp4 = format_hp(pokemon4)
    else:
        name4 = " " * 28
        types4 = " " * 28
        hp4 = " " * 28

    lines.append("│" + name3 + "││" + name4 + "│")
    lines.append("│" + types3 + "││" + types4 + "│")
    lines.append("│" + hp3 + "││" + hp4 + "│")
    lines.append("├" + "─" * 28 + "┤├" + "─" * 28 + "┤")

    # Row 3: Slots 5 and 6
    pokemon5 = pokemon_list[4] if len(pokemon_list) > 4 else None
    pokemon6 = pokemon_list[5] if len(pokemon_list) > 5 else None

    if pokemon5:
        name5 = format_pokemon_name(pokemon5, 5)
        types5 = format_types(pokemon5)
        hp5 = format_hp(pokemon5)
    else:
        name5 = " " * 28
        types5 = " " * 28
        hp5 = " " * 28

    if pokemon6:
        name6 = format_pokemon_name(pokemon6, 6)
        types6 = format_types(pokemon6)
        hp6 = format_hp(pokemon6)
    else:
        name6 = " " * 28
        types6 = " " * 28
        hp6 = " " * 28

    lines.append("│" + name5 + "││" + name6 + "│")
    lines.append("│" + types5 + "││" + types6 + "│")
    lines.append("│" + hp5 + "││" + hp6 + "│")
    lines.append("├" + "─" * 58 + "┤")

    # Bottom section with Cancel button
    cancel_text = "   > CANCEL <    " if selected_slot == 7 else "     CANCEL      "
    lines.append("│" + " " * 40 + "│" + " " * 17 + "│")
    lines.append("│  Choose a Pokemon." + " " * 21 + "│" + cancel_text + "│")
    lines.append("│" + " " * 40 + "│" + " " * 17 + "│")
    lines.append("└" + "─" * 58 + "┘")

    return lines


# Message Printing Functions

def print_message_slowly_in_box(messages: list[str], start_row: int = 13):
    """
    Print messages character-by-character inside the message box using cursor positioning.

    Args:
        messages: List of messages to print
        start_row: Row number to start printing (default 13)
    """
    current_row = start_row

    for message in messages:
        if current_row > 18:  # Max row for messages
            break

        # Handle word wrapping
        wrapped_lines = wrap_text(message, max_width=56)

        for line in wrapped_lines:
            if current_row > 18:
                break

            # Position cursor at start of line (column 3 = 2 spaces from left border)
            move_cursor(current_row, 3)

            # Print character by character
            print_slowly(line, delay=0.03, add_newline=False)

            current_row += 1

        # Small delay between messages
        time.sleep(0.3)

    sys.stdout.flush()


def print_messages_in_box(messages: list[str], start_row: int = 13):
    """
    Print messages instantly inside the message box using cursor positioning.

    Args:
        messages: List of messages to print
        start_row: Row number to start printing (default 13)
    """
    current_row = start_row

    for message in messages:
        if current_row > 18:  # Max row for messages
            break

        # Handle word wrapping
        wrapped_lines = wrap_text(message, max_width=56)

        for line in wrapped_lines:
            if current_row > 18:
                break

            # Position cursor at start of line (column 3 = 2 spaces from left border)
            move_cursor(current_row, 3)

            # Print instantly
            print(line, end='')

            current_row += 1

    sys.stdout.flush()


# Screen Display Functions

def display_action_menu_screen(battle: 'Battle', selected_action: int = 1) -> None:
    """
    Display the action menu screen (What will Pokemon do? + FIGHT/POKEMON).

    Args:
        battle: The Battle object
        selected_action: 1=FIGHT (default), 2=POKEMON
    """
    clear_screen()
    player_pokemon = battle.player_team.get_current_pokemon()
    pokemon_name = player_pokemon.name.capitalize() if player_pokemon else "Pokemon"

    header = draw_pokemon_header(battle)
    menu = draw_action_menu(pokemon_name, selected_action)

    for line in header + menu:
        print(line)


def display_move_selection_screen(battle: 'Battle', selected_move_index: int) -> None:
    """
    Display the move selection screen with 2x2 grid.

    Args:
        battle: The Battle object
        selected_move_index: Which move is currently selected (1-4)
    """
    clear_screen()
    player_pokemon = battle.player_team.get_current_pokemon()

    header = draw_pokemon_header(battle)
    move_grid = draw_move_grid(player_pokemon, selected_move_index)

    for line in header + move_grid:
        print(line)


def display_battle_readout_screen(battle: 'Battle', messages: list[str]) -> None:
    """
    Display the battle readout screen with cursor-positioned messages.

    Args:
        battle: The Battle object
        messages: List of battle messages to display
    """
    clear_screen()
    header = draw_pokemon_header(battle)
    message_box = draw_message_area()

    for line in header + message_box:
        print(line)

    # Use cursor positioning to print messages slowly inside the box
    if ENABLE_TEXT_ANIMATION:
        print_message_slowly_in_box(messages, start_row=13)
    else:
        # Print instantly but still position in box
        print_messages_in_box(messages, start_row=13)


def display_pokemon_select_screen(team: 'Team', selected_slot: int) -> None:
    """
    Display the Pokemon selection screen with 2x3 grid + Cancel button.

    Args:
        team: The player's team
        selected_slot: Which slot is selected (1-6 for Pokemon, 7 for Cancel)
    """
    clear_screen()
    pokemon_select_grid = draw_pokemon_select_grid(team, selected_slot)

    for line in pokemon_select_grid:
        print(line)
