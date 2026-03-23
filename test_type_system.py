"""
Test Your Type System Implementation

Run this file to check if you've correctly implemented all 18 type classes.

Usage:
    python test_type_system.py
"""

def test_type_classes():
    """Test that all 18 type classes are implemented."""
    print("=" * 60)
    print("TESTING TYPE SYSTEM IMPLEMENTATION")
    print("=" * 60)
    print()

    # Try to import all type classes
    print("Step 1: Testing imports...")
    print("-" * 60)

    try:
        from type_system import (
            Type, FireType, WaterType, NormalType, ElectricType, GrassType,
            IceType, FightingType, PoisonType, GroundType, FlyingType,
            PsychicType, BugType, RockType, GhostType, DragonType,
            DarkType, SteelType, FairyType
        )
        print("✓ All type classes imported successfully!")
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        print("\nHINT: Make sure you've implemented all type classes in type_system.py")
        return False

    print()
    print("Step 2: Testing type class instantiation...")
    print("-" * 60)

    # Test creating instances of each type
    types_to_test = [
        ("NormalType", NormalType, "normal"),
        ("FireType", FireType, "fire"),
        ("WaterType", WaterType, "water"),
        ("ElectricType", ElectricType, "electric"),
        ("GrassType", GrassType, "grass"),
        ("IceType", IceType, "ice"),
        ("FightingType", FightingType, "fighting"),
        ("PoisonType", PoisonType, "poison"),
        ("GroundType", GroundType, "ground"),
        ("FlyingType", FlyingType, "flying"),
        ("PsychicType", PsychicType, "psychic"),
        ("BugType", BugType, "bug"),
        ("RockType", RockType, "rock"),
        ("GhostType", GhostType, "ghost"),
        ("DragonType", DragonType, "dragon"),
        ("DarkType", DarkType, "dark"),
        ("SteelType", SteelType, "steel"),
        ("FairyType", FairyType, "fairy"),
    ]

    all_passed = True
    for class_name, type_class, expected_name in types_to_test:
        try:
            type_obj = type_class()
            if type_obj.name == expected_name:
                print(f"✓ {class_name}: name='{type_obj.name}'")
            else:
                print(f"✗ {class_name}: Expected name='{expected_name}', got '{type_obj.name}'")
                all_passed = False
        except Exception as e:
            print(f"✗ {class_name}: {e}")
            all_passed = False

    if not all_passed:
        return False

    print()
    print("Step 3: Testing create_type_system() function...")
    print("-" * 60)

    try:
        from data_loader import create_type_system
        type_system = create_type_system()

        expected_types = [
            "normal", "fire", "water", "electric", "grass", "ice",
            "fighting", "poison", "ground", "flying", "psychic", "bug",
            "rock", "ghost", "dragon", "dark", "steel", "fairy"
        ]

        all_present = True
        for type_name in expected_types:
            if type_name in type_system:
                print(f"✓ '{type_name}' type found in type system")
            else:
                print(f"✗ '{type_name}' type MISSING from type system")
                all_present = False

        if not all_present:
            print("\nHINT: Make sure create_type_system() in data_loader.py returns all 18 types")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nHINT: Check create_type_system() in data_loader.py")
        return False

    print()
    print("Step 4: Testing type effectiveness...")
    print("-" * 60)

    # Test some key type matchups
    fire = type_system["fire"]
    water = type_system["water"]
    grass = type_system["grass"]
    electric = type_system["electric"]
    ground = type_system["ground"]
    flying = type_system["flying"]

    tests = [
        ("Fire vs Grass", fire, grass, 2.0, "super effective"),
        ("Water vs Fire", water, fire, 2.0, "super effective"),
        ("Fire vs Water", fire, water, 0.5, "not very effective"),
        ("Electric vs Ground", electric, ground, 0.0, "no effect"),
        ("Ground vs Flying", ground, flying, 0.0, "no effect"),
    ]

    for test_name, attacker, defender, expected, description in tests:
        effectiveness = attacker.get_effectiveness_against(defender)
        if effectiveness == expected:
            print(f"✓ {test_name}: {effectiveness}x ({description})")
        else:
            print(f"✗ {test_name}: Expected {expected}x, got {effectiveness}x")
            all_passed = False

    print()
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED! Your type system is complete!")
        print("=" * 60)
        print()
        print("Next step: Run 'python main.py' to play the game!")
        return True
    else:
        print("✗ SOME TESTS FAILED - Keep working on your implementation")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = test_type_classes()
    if not success:
        print()
        print("Review the errors above and fix your implementation.")
        print("Then run this test again!")
