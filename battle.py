"""
Battle Module

This module implements battle functionality using dictionaries and functions.

A Battle is represented as a dictionary with these keys:
    {
        "player_team": dict,         # Player's team dictionary
        "ai_team": dict,             # AI's team dictionary
        "battle_history": list[str]  # List of battle events
    }

The Battle manages:
- Turn order (speed-based)
- Move execution with damage calculation
- Battle state tracking
- Win/loss detection
- Pokemon switching
"""

from team import *
from pokemon import *
from move import *
from type_system import *


def create_battle(player_team, ai_team):
    """
    Create a new battle between two teams.

    Args:
        player_team: The player's team dictionary
        ai_team: The AI opponent's team dictionary

    Returns:
        dict: Battle dictionary
    """
    return {
        "player_team": player_team,
        "ai_team": ai_team,
        "battle_history": []
    }


def execute_single_attack(battle, attacker_owner, defender_owner):
    """
    Execute a single attack, applying damage and updating battle state.

    Args:
        battle: Battle dictionary
        attacker_owner: "player" or "ai" (who is attacking)
        defender_owner: "player" or "ai" (who is defending)

    Returns:
        dict: Attack result with keys:
            - attacker: str ("player" or "ai")
            - defender: str ("player" or "ai")
            - messages: list[str] (all messages for this attack)
            - damage: int
            - hit: bool
            - defender_fainted: bool
    """
    result = {
        "attacker": attacker_owner,
        "defender": defender_owner,
        "messages": [],
        "damage": 0,
        "hit": False,
        "defender_fainted": False
    }

    # Get Pokemon
    if attacker_owner == "player":
        attacker = get_current_pokemon(battle["player_team"])
        defender = get_current_pokemon(battle["ai_team"])
    else:
        attacker = get_current_pokemon(battle["ai_team"])
        defender = get_current_pokemon(battle["player_team"])

    if attacker is None or defender is None:
        return result

    # Get the attacker's move
    attacker_move = attacker["move"]
    if attacker_move is None:
        return result

    # Check if move hits
    if check_hit(attacker_move):
        result["hit"] = True
        # Note: Damage calculation will be implemented in Week 24
        damage = 10  # Placeholder damage

        # Add move usage message
        move_msg = f"{attacker['name']} used {attacker_move['name']}!"
        result["messages"].append(move_msg)
        battle["battle_history"].append(move_msg)

        # Store damage and apply it
        result["damage"] = damage
        take_damage(defender, damage)

        damage_msg = f"Dealt {damage} damage!"
        result["messages"].append(damage_msg)
        battle["battle_history"].append(damage_msg)

        # Check if defender fainted
        if is_fainted(defender):
            result["defender_fainted"] = True
            faint_msg = f"{defender['name']} fainted!"
            result["messages"].append(faint_msg)
            battle["battle_history"].append(faint_msg)
    else:
        miss_msg = f"{attacker['name']}'s {attacker_move['name']} missed!"
        result["messages"].append(miss_msg)
        battle["battle_history"].append(miss_msg)

    return result


def get_battle_summary(battle):
    """
    Get a formatted summary of the battle history.

    Args:
        battle: Battle dictionary

    Returns:
        str: Battle history as a formatted string
    """
    if not battle["battle_history"]:
        return "No battle history yet."

    summary = "Battle History:\n"
    summary += "=" * 50 + "\n"
    for i, event in enumerate(battle["battle_history"], 1):
        summary += f"{i}. {event}\n"
    return summary
