"""
Team Parser Module

This module handles parsing Pokemon team files in Pokemon Showdown format.
Uses advanced regex to extract Pokemon names and their moves from text files.

Team File Format:
    Pokemon Name
    - Move 1
    - Move 2
    - Move 3
    - Move 4

    Next Pokemon Name
    - Move 1
    ...

This demonstrates advanced regex skills:
- Multi-line pattern matching
- Capture groups for extracting data
- Handling optional whitespace
- Pattern validation
"""

import re
from typing import List, Dict, Tuple


def parse_team_file(file_path: str) -> List[Dict[str, any]]:
    """
    Parse a team file and return a list of Pokemon with their moves.

    Args:
        file_path: Path to the team file

    Returns:
        List of dictionaries with format:
        [
            {
                "pokemon": "charizard",
                "moves": ["flamethrower", "dragon-claw", "air-slash", "heat-wave"]
            },
            ...
        ]

    Raises:
        FileNotFoundError: If team file doesn't exist
        ValueError: If team file format is invalid
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Team file not found: {file_path}")

    # Parse the team file
    team_data = parse_team_text(content)

    if not team_data:
        raise ValueError("No valid Pokemon found in team file")

    return team_data


def parse_team_text(text: str) -> List[Dict[str, any]]:
    """
    Parse team text content and extract Pokemon with their moves.

    Uses advanced regex with multi-line matching to extract Pokemon blocks.

    Pattern explanation:
    - Matches Pokemon name on its own line
    - Followed by 1-4 move lines starting with "- "
    - Handles optional whitespace and blank lines

    Args:
        text: Text content of team file

    Returns:
        List of Pokemon dictionaries with names and moves
    """
    team = []

    # Pattern to match a Pokemon block:
    # ^(\w+(?:-\w+)*)$     - Pokemon name (allows hyphens like "mr-mime")
    #                        ^ = start of line, $ = end of line
    #                        \w+ = one or more word characters
    #                        (?:-\w+)* = optional groups of "-word" (for hyphenated names)
    # \s*\n                - Optional whitespace and newline
    # ((?:^\s*-\s*.+$\s*\n?)+) - One or more move lines
    #                        (?:...) = non-capturing group
    #                        ^\s*-\s* = line starting with optional space, dash, space
    #                        .+ = move name (one or more characters)
    #                        \s*\n? = optional whitespace and newline
    #                        + = one or more move lines
    pokemon_pattern = r'^(\w+(?:-\w+)*)$\s*\n((?:^\s*-\s*.+$\s*\n?)+)'

    # re.MULTILINE makes ^ and $ match line boundaries, not just string start/end
    matches = re.finditer(pokemon_pattern, text, re.MULTILINE)

    for match in matches:
        pokemon_name = match.group(1).lower().strip()
        moves_block = match.group(2)

        # Extract individual moves from the moves block
        # Pattern: ^\s*-\s*(.+)$
        #          ^\s* = start of line with optional whitespace
        #          - = literal dash
        #          \s* = optional whitespace
        #          (.+) = capture group for move name (one or more characters)
        #          $ = end of line
        move_pattern = r'^\s*-\s*(.+)$'
        move_matches = re.finditer(move_pattern, moves_block, re.MULTILINE)

        moves = []
        for move_match in move_matches:
            move_name = move_match.group(1).strip()
            # Convert "Thunder Bolt" or "Thunderbolt" to "thunder-bolt"
            move_name = normalize_move_name(move_name)
            moves.append(move_name)

        # Only add Pokemon if they have 1-4 moves
        if 1 <= len(moves) <= 4:
            team.append({
                "pokemon": pokemon_name,
                "moves": moves
            })

    return team


def normalize_move_name(move_name: str) -> str:
    """
    Normalize a move name to match our JSON file format.

    Converts:
    - "Thunder Bolt" -> "thunder-bolt"
    - "Flamethrower" -> "flamethrower"
    - "Dragon Claw" -> "dragon-claw"
    - "Ice Beam" -> "ice-beam"

    Pattern explanation:
    - Convert to lowercase
    - Replace spaces with hyphens using \s+ (one or more whitespace)
    - Remove any non-alphanumeric characters except hyphens

    Args:
        move_name: Move name from team file (may have spaces or be one word)

    Returns:
        Normalized move name (lowercase with hyphens)
    """
    # Convert to lowercase
    normalized = move_name.lower()

    # Replace one or more whitespace characters with a single hyphen
    # \s+ matches spaces, tabs, newlines, etc.
    normalized = re.sub(r'\s+', '-', normalized)

    # Remove any characters that aren't letters, numbers, or hyphens
    # [^a-z0-9-] means "anything that is NOT a-z, 0-9, or hyphen"
    normalized = re.sub(r'[^a-z0-9-]', '', normalized)

    return normalized


def validate_team_data(team_data: List[Dict[str, any]],
                       available_pokemon: List[str],
                       available_moves: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that all Pokemon and moves in the team actually exist.

    Checks:
    - All Pokemon names exist in the Pokemon database
    - All move names exist in the moves database
    - Each Pokemon has at least 1 move and at most 4 moves
    - Team has between 1-6 Pokemon

    Args:
        team_data: Parsed team data
        available_pokemon: List of available Pokemon names (from data/pokemon/)
        available_moves: List of available move names (from data/moves/)

    Returns:
        Tuple of (is_valid, list_of_errors)
        - is_valid: True if team is valid, False otherwise
        - list_of_errors: List of error messages (empty if valid)
    """
    errors = []

    # Check team size (1-6 Pokemon)
    if len(team_data) < 1:
        errors.append("Team must have at least 1 Pokemon")
    elif len(team_data) > 6:
        errors.append(f"Team has {len(team_data)} Pokemon (maximum is 6)")

    for entry in team_data:
        pokemon_name = entry["pokemon"]
        moves = entry["moves"]

        # Check if Pokemon exists
        if pokemon_name not in available_pokemon:
            errors.append(f"Pokemon '{pokemon_name}' not found in database")

        # Check move count
        if len(moves) < 1:
            errors.append(f"Pokemon '{pokemon_name}' has no moves")
        elif len(moves) > 4:
            errors.append(f"Pokemon '{pokemon_name}' has {len(moves)} moves (maximum is 4)")

        # Check if all moves exist
        for move in moves:
            if move not in available_moves:
                errors.append(f"Move '{move}' not found in database (for {pokemon_name})")

    is_valid = len(errors) == 0
    return is_valid, errors


def get_team_summary(team_data: List[Dict[str, any]]) -> str:
    """
    Get a human-readable summary of the team.

    Args:
        team_data: Parsed team data

    Returns:
        String summary of the team with Pokemon names and moves
    """
    if not team_data:
        return "Empty team"

    lines = [f"Team ({len(team_data)} Pokemon):"]
    lines.append("-" * 50)

    for i, entry in enumerate(team_data, 1):
        pokemon_name = entry["pokemon"].capitalize()
        moves = entry["moves"]
        lines.append(f"{i}. {pokemon_name}")
        for move in moves:
            # Convert back to readable format: "thunder-bolt" -> "Thunder Bolt"
            move_display = move.replace('-', ' ').title()
            lines.append(f"   - {move_display}")
        lines.append("")

    return "\n".join(lines)


# Example usage and testing
if __name__ == "__main__":
    # Test parsing with sample team text
    sample_text = """
Charizard
- Flamethrower
- Dragon Claw
- Air Slash
- Heat Wave

Pikachu
- Thunder
- Quick Attack
- Iron Tail
- Thunderbolt

Blastoise
- Hydro Pump
- Ice Beam
- Skull Bash
- Water Gun
"""

    print("Testing team parser...")
    print("=" * 50)

    team = parse_team_text(sample_text)
    print(get_team_summary(team))

    print("\nParsed data structure:")
    print(team)
