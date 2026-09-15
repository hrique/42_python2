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


def print_error () -> None:
    try:
        raise GardenError()
    except GardenError as e:
        print(f"Caught GardenError: {e}")
    
    try:
        raise GardenError("O jardim está pegando fogo")
    except GardenError as e:
        print(f"Caught GardenError: {e}")


if __name__ == "__main__":
    print_error()