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
    pokemon_pattern = r"^(\w+(?:-\w)*)$\s*\n((?:^\s*-\s*.+$\s*\n?)+)"

    matches = re.finditer(pokemon_pattern, text, re.MULTILINE)
    for match in matches:
        pokemon_name = match.group(1).lower().strip()
        moves_block = match.group(2).strip()
        print("-----")
        print(pokemon_name)
        print("*****")
        print(moves_block)
        print("#####")
    move_pattern = r"^\s*-\s*(.+)$"
    
    move_matches = re.finditer(move_pattern, moves_block, re.MULTILINE)
    moves = []
    for move_match in move_matches:
        move_name = move_match.group(1).strip()
        move = normalize_move_name(move_name)
        moves.append(move)

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
    return re.sub(r"[^a-z0-9-]", "", re.sub(r'\s+', "-", move_name.lower()))

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

    if not 1 <= len(team_data) <= 6:
        errors.append("Error: # of pokemon is not within range")

    for pokemon in team_data:
        if not pokemon in available_pokemon:
            errors.append("Error: Pokemon is not available")
        if not 1 <= len(pokemon["moves"]) <= 4:
            errors.append("Error: # of moves is not within range")
        for move in pokemon["moves"]:
            if move not in available_moves:
                errors.append("Error: Move not available")
    return len(errors) == 0, errors


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
