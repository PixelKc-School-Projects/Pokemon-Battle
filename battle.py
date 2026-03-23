"""
Battle Class

This module implements the Battle class which manages a Pokemon battle between two teams.

The Battle class:
- Determines turn order based on Pokemon speed
- Executes moves in the correct order
- Tracks battle history
- Checks win/loss conditions
- Handles Pokemon switching

This demonstrates orchestration - bringing all the other classes together.
"""

from team import Team
from pokemon import Pokemon
from move import Move
from type_system import calculate_dual_type_effectiveness
from typing import Optional


class Battle:
    """
    Manages a battle between two teams.

    The Battle orchestrates:
    - Turn order (speed-based)
    - Move execution with damage calculation
    - Battle state tracking
    - Win/loss detection
    """

    def __init__(self, player_team: Team, ai_team: Team):
        """
        Initialize a battle between two teams.

        Args:
            player_team: The player's Team
            ai_team: The AI opponent's Team
        """
        self.player_team = player_team
        self.ai_team = ai_team
        self.battle_history: list[str] = []

    def determine_turn_order(self) -> tuple[tuple[str, Pokemon], tuple[str, Pokemon]]:
        """
        Determine which Pokemon goes first based on speed.

        Returns:
            tuple: ((owner, first_pokemon), (owner, second_pokemon))
                   where owner is "player" or "ai"
        """
        player_pokemon = self.player_team.get_current_pokemon()
        ai_pokemon = self.ai_team.get_current_pokemon()

        if player_pokemon is None or ai_pokemon is None:
            return (("player", player_pokemon), ("ai", ai_pokemon))

        player_speed = player_pokemon.get_stat("speed")
        ai_speed = ai_pokemon.get_stat("speed")

        # Player goes first if speed is greater than or equal to AI's speed
        if player_speed >= ai_speed:
            return (("player", player_pokemon), ("ai", ai_pokemon))
        else:
            return (("ai", ai_pokemon), ("player", player_pokemon))

    def execute_single_attack(self, attacker_owner: str, defender_owner: str,
                             attacker_move: Optional[Move]) -> dict:
        """
        Execute a single attack and return its results.

        Args:
            attacker_owner: "player" or "ai" (who is attacking)
            defender_owner: "player" or "ai" (who is defending)
            attacker_move: Move to execute

        Returns:
            dict with keys:
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
            attacker = self.player_team.get_current_pokemon()
            defender = self.ai_team.get_current_pokemon()
        else:
            attacker = self.ai_team.get_current_pokemon()
            defender = self.player_team.get_current_pokemon()

        if attacker is None or defender is None or attacker_move is None:
            return result

        # Check if move hits
        if attacker_move.check_hit():
            result["hit"] = True
            damage = attacker_move.calculate_damage(defender, attacker)

            # Add move usage message
            move_msg = f"{attacker.name} used {attacker_move.name}!"
            result["messages"].append(move_msg)
            self.add_to_history(move_msg)

            # Add type effectiveness message
            type_eff = calculate_dual_type_effectiveness(attacker_move.move_type, defender.types)
            if type_eff > 1.0:
                if type_eff >= 4.0:
                    eff_msg = "It's incredibly effective!"
                elif type_eff >= 2.0:
                    eff_msg = "It's super effective!"
                else:
                    eff_msg = "It's quite effective!"
                result["messages"].append(eff_msg)
                self.add_to_history(eff_msg)
            elif type_eff < 1.0 and type_eff > 0.0:
                if type_eff <= 0.25:
                    eff_msg = "It's barely effective..."
                else:
                    eff_msg = "It's not very effective..."
                result["messages"].append(eff_msg)
                self.add_to_history(eff_msg)
            elif type_eff == 0.0:
                no_eff_msg = "It has no effect!"
                result["messages"].append(no_eff_msg)
                self.add_to_history(no_eff_msg)

            # Store damage (but don't apply yet - UI will apply after displaying messages)
            result["damage"] = damage
            attacker_move.use()

            damage_msg = f"Dealt {damage} damage!"
            result["messages"].append(damage_msg)
            self.add_to_history(damage_msg)

            # Check if defender will faint (damage hasn't been applied yet)
            if damage >= defender.current_hp:
                result["defender_fainted"] = True
                faint_msg = f"{defender.name} fainted!"
                result["messages"].append(faint_msg)
                self.add_to_history(faint_msg)
        else:
            miss_msg = f"{attacker.name}'s {attacker_move.name} missed!"
            result["messages"].append(miss_msg)
            self.add_to_history(miss_msg)
            attacker_move.use()

        return result

    def execute_turn(self, player_move: Optional[Move], ai_move: Optional[Move]) -> dict:
        """
        Execute turn in speed order, returning results for sequential display.

        Args:
            player_move: Move chosen by player (or None if switching)
            ai_move: Move chosen by AI (or None if switching)

        Returns:
            dict with keys:
            - first_attack: dict (result from execute_single_attack)
            - second_attack: dict or None (None if first defender fainted)
            - turn_order: tuple ((owner1, pokemon1), (owner2, pokemon2))
        """
        player_pokemon = self.player_team.get_current_pokemon()
        ai_pokemon = self.ai_team.get_current_pokemon()

        # Determine turn order
        turn_order = self.determine_turn_order()
        first_owner, first_pokemon = turn_order[0]
        second_owner, second_pokemon = turn_order[1]

        # Determine which move goes first
        first_move = player_move if first_owner == "player" else ai_move
        first_defender_owner = "ai" if first_owner == "player" else "player"

        # Execute first attack
        first_attack = self.execute_single_attack(first_owner, first_defender_owner, first_move)

        # If first attack caused defender to faint, don't execute second attack
        if first_attack["defender_fainted"]:
            return {
                "first_attack": first_attack,
                "second_attack": None,
                "turn_order": turn_order
            }

        # Execute second attack
        second_move = player_move if second_owner == "player" else ai_move
        second_defender_owner = "ai" if second_owner == "player" else "player"

        second_attack = self.execute_single_attack(second_owner, second_defender_owner, second_move)

        return {
            "first_attack": first_attack,
            "second_attack": second_attack,
            "turn_order": turn_order
        }

    def check_battle_over(self) -> Optional[str]:
        """
        Check if the battle is over (one team has all Pokemon fainted).

        Returns:
            str | None: "player_wins" if AI team is defeated,
                        "ai_wins" if player team is defeated,
                        None if battle continues
        """
        if self.ai_team.all_fainted():
            return "player_wins"
        elif self.player_team.all_fainted():
            return "ai_wins"
        return None

    def switch_pokemon(self, team: Team, pokemon_index: int) -> bool:
        """
        Switch the active Pokemon for a team.

        Args:
            team: The Team to switch Pokemon for
            pokemon_index: Index of Pokemon to switch to

        Returns:
            bool: True if switch was successful, False otherwise
        """
        success = team.switch_pokemon(pokemon_index)
        if success:
            new_pokemon = team.get_current_pokemon()
            if new_pokemon:
                owner = "Player" if team == self.player_team else "AI"
                msg = f"{owner} switched to {new_pokemon.name}!"
                self.add_to_history(msg)
        return success

    def add_to_history(self, event: str) -> None:
        """
        Add an event to the battle history.

        Args:
            event: Event description string
        """
        self.battle_history.append(event)

    def get_battle_summary(self) -> str:
        """
        Get a formatted summary of the battle history.

        Returns:
            str: Battle history as a formatted string
        """
        if not self.battle_history:
            return "No battle history yet."

        summary = "Battle History:\n"
        summary += "=" * 50 + "\n"
        for i, event in enumerate(self.battle_history, 1):
            summary += f"{i}. {event}\n"
        return summary

    def __repr__(self) -> str:
        """Return a string representation of the battle."""
        return f"Battle(player_team vs ai_team, history_length={len(self.battle_history)})"
