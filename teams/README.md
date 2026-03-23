# Pokemon Team Files

This folder contains team files for the Pokemon Battle Simulator.

## Team File Format

Team files use a simple text format inspired by Pokemon Showdown:

```
Pokemon Name
- Move 1
- Move 2
- Move 3
- Move 4

Next Pokemon Name
- Move 1
- Move 2
- Move 3
- Move 4
```

### Rules

1. **Pokemon Name**: One word per line, lowercase or capitalized (e.g., `Charizard` or `charizard`)
2. **Moves**: Lines starting with `- ` followed by the move name
3. **Move Count**: Each Pokemon must have 1-4 moves
4. **Team Size**: Teams must have 1-6 Pokemon
5. **Blank Lines**: Separate Pokemon with blank lines (optional but improves readability)

### Example

```
Pikachu
- Thunderbolt
- Quick Attack
- Iron Tail
- Thunder

Charizard
- Flamethrower
- Dragon Claw
- Air Slash
- Heat Wave
```

## Available Team Files

- **team_fire.txt** - Fire-type themed team (6 Pokemon)
- **team_water.txt** - Water-type themed team (6 Pokemon)
- **team_classic.txt** - Classic Gen 1 favorites (6 Pokemon)
- **team_mini.txt** - Small team for quick battles (3 Pokemon)

## Creating Your Own Team

1. Create a new `.txt` file in this folder
2. Follow the format above
3. Use Pokemon names from `data/pokemon/` (any of the 151 Gen 1 Pokemon)
4. Use move names from `data/moves/` (282 damaging moves available)
5. Load your custom team from the "Custom Team Battle" menu!

### Tips

- Move names with spaces: `"Thunder Bolt"` or `"Thunderbolt"` both work (converted to `thunder-bolt`)
- Check available Pokemon: Look in `data/pokemon/` folder
- Check available moves: Look in `data/moves/` folder
- You can give any Pokemon any move (as long as the move exists)!

## Advanced: Creating Custom Moves (Bonus Enhancement)

Want to create your own custom move?

1. Create a new JSON file in `data/moves/` (e.g., `super-blast.json`)
2. Use this format:
```json
{
  "id": 999,
  "name": "super-blast",
  "type": "normal",
  "power": 100,
  "accuracy": 95,
  "pp": 10
}
```
3. Reference the move in your team file!

**Note**: Only damaging moves work in the battle system.
