#!/usr/bin/env python3


class PlantError(Exception):
    def __init__(self, message="Unknown plant error"):
        super().__init__(message)


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def watering_loop(plants: list[str]) -> None:
    print("Opening watering system")
    try:
        for plant in plants:
            water_plant(plant)
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system\n")


def test_watering_system() -> None:
    valid_plants = ["Tomato", "Lettuce", "Carrots"]
    invalid_plants = ["Tomato", "lettuce", "Carrots"]
    print("Testing valid plants...")
    watering_loop(valid_plants)
    print("Testing invalid plants...")
    watering_loop(invalid_plants)


def main() -> None:
    print("=== Garden Watering System ===\n")
    test_watering_system()
    print("Cleanup always happens, even with errors!")


if __name__ == "__main__":
    main()
