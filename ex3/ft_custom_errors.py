#!/usr/bin/env python3


class GardenError(Exception):
    def __init__(self, message="Unknown garden error"):
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message="Unknown plant error"):
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message="Unknown water error"):
        super().__init__(message)


def check_plant(is_wilting: bool) -> None:
    if is_wilting:
        raise PlantError("The tomato plant is wilting!")


def check_water(no_water: bool) -> None:
    if no_water:
        raise WaterError("Not enough water in the tank!")


def ft_custom_errors() -> None:
    print("Testing PlantError...")
    try:
        check_plant(True)
    except PlantError as e:
        print(f"Caught PlantError: {e}\n")

    print("Testing WaterError...")
    try:
        check_water(True)
    except WaterError as e:
        print(f"Caught WaterError: {e}\n")

    print("Testing catching all garden errors...")
    try:
        check_plant(True)
    except GardenError as e:
        print(f"Caught GardenError: {e}")
    try:
        check_water(True)
    except GardenError as e:
        print(f"Caught GardenError: {e}\n")


def main() -> None:
    print("=== Custom Garden Errors Demo ===\n")
    ft_custom_errors()
    print("All custom error types work correctly!")


if __name__ == "__main__":
    main()
