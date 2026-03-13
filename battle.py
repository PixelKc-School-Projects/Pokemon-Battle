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


def determine_turn_order(battle):
    """
    Determine which Pokemon goes first based on speed.

    Args:
        battle: Battle dictionary

    Returns:
        tuple: ((owner, first_pokemon), (owner, second_pokemon))
               where owner is "player" or "ai"
    """
    player_pokemon = get_current_pokemon(battle['player_team'])
    ai_pokemon = get_current_pokemon(battle['ai_team'])
    if player_pokemon is None or ai_pokemon is None:
        return (("player", player_pokemon), {"ai", ai_pokemon})
    player_speed = get_stat(player_pokemon, "speed")
    ai_speed = get_stat(ai_pokemon, "speed")

    return (("player", player_pokemon), ("ai", ai_pokemon)) if player_speed >= ai_speed else (("ai", ai_pokemon), ("player", player_pokemon))


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
        damage = calculate_damage(attacker_move, attacker, defender)

        # Add move usage message
        move_msg = f"{attacker['name']} used {attacker_move['name']}!"
        result["messages"].append(move_msg)
        add_to_history(battle, move_msg)

        # Add type effectiveness message
        type_eff = calculate_dual_type_effectiveness(attacker_move["type"], defender["types"])
        if type_eff > 1.0:
            if type_eff >= 4.0:
                eff_msg = "It's incredibly effective!"
            elif type_eff >= 2.0:
                eff_msg = "It's super effective!"
            else:
                eff_msg = "It's quite effective!"
            result["messages"].append(eff_msg)
            add_to_history(battle, eff_msg)
        elif type_eff < 1.0 and type_eff > 0.0:
            if type_eff <= 0.25:
                eff_msg = "It's barely effective..."
            else:
                eff_msg = "It's not very effective..."
            result["messages"].append(eff_msg)
            add_to_history(battle, eff_msg)
        elif type_eff == 0.0:
            no_eff_msg = "It has no effect!"
            result["messages"].append(no_eff_msg)
            add_to_history(battle, no_eff_msg)

        # Store damage and apply it
        result["damage"] = damage
        take_damage(defender, damage)

        damage_msg = f"Dealt {damage} damage!"
        result["messages"].append(damage_msg)
        add_to_history(battle, damage_msg)

        # Check if defender fainted
        if is_fainted(defender):
            result["defender_fainted"] = True
            faint_msg = f"{defender['name']} fainted!"
            result["messages"].append(faint_msg)
            add_to_history(battle, faint_msg)
    else:
        miss_msg = f"{attacker['name']}'s {attacker_move['name']} missed!"
        result["messages"].append(miss_msg)
        add_to_history(battle, miss_msg)

    return result


def execute_turn(battle):
    """
    Execute turn in speed order, applying damage and returning results for sequential display.

    Args:
        battle: Battle dictionary

    Returns:
        dict: Turn results with keys:
            - first_attack: dict (result from execute_single_attack)
            - second_attack: dict or None (None if first defender fainted)
            - turn_order: tuple ((owner1, pokemon1), (owner2, pokemon2))
    """
    turn_order = determine_turn_order(battle)
    first_owner, first_pokemon = turn_order[0]
    second_owner, second_pokemon = turn_order[1]

    first_attack = execute_single_attack(battle, first_owner, second_owner)
    if first_attack["defender_fainted"]:
        return {"first_attack": first_attack, "second_attack": None, "turn_order": turn_order}
    
    second_attack = execute_single_attack(battle, second_owner, first_owner)
    

    return {"first_attack": first_attack, "second_attack": second_attack, "turn_order": turn_order}


def check_battle_over(battle):
    """
    Check if the battle is over (one team has all Pokemon fainted).

    Args:
        battle: Battle dictionary

    Returns:
        str | None: "player_wins" if AI team is defeated,
                    "ai_wins" if player team is defeated,
                    None if battle continues
    """
    if all_fainted(battle["player_team"]):
        return "player_wins"
    elif all_fainted(battle["ai_team"]):
        return "ai_wins"
    else:
        return None


def switch_pokemon_in_battle(battle, owner, pokemon_index):
    """
    Switch the active Pokemon for a team in battle.

    Args:
        battle: Battle dictionary
        owner: "player" or "ai" (which team to switch)
        pokemon_index: Index of Pokemon to switch to

    Returns:
        bool: True if switch was successful, False otherwise
    """
    team = battle[f"{owner}_team"]
    pokemon_switch = switch_pokemon(team, pokemon_index)
    if pokemon_switch:
        new_pokemon = get_current_pokemon(team)
        add_to_history(battle, f"{owner} switched to {new_pokemon}!")
        return True
    return False


def add_to_history(battle, event):
    """
    Add an event to the battle history.

    Args:
        battle: Battle dictionary
        event: Event description string
    """
    battle["battle_history"].append(event)


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
