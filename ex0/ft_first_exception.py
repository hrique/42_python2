#!/usr/bin/env python3


def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    for value in ["25", "abc"]:
        print(f"\nInput data is '{value}'")
        try:
            x = input_temperature(value)
            print(f"Temperature is now {x}°C")
        except ValueError as e:
            print(f"Caught input_temperature error: {e}")


def main() -> None:
    print("=== Garden Temperature ===")
    test_temperature()
    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    main()
