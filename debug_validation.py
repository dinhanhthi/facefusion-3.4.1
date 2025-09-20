#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

from facefusion.program import create_program
from argparse import _SubParsersAction

def debug_validate_actions(program, program_name="main"):
    print(f"\n=== Debugging {program_name} ===")

    for action in program._actions:
        if action.default and action.choices:
            print(f"Action: {action.dest}")
            print(f"  Default: {action.default} (type: {type(action.default)})")
            print(f"  Choices: {action.choices}")

            if isinstance(action.default, list):
                invalid_defaults = [default for default in action.default if default not in action.choices]
                if invalid_defaults:
                    print(f"  ❌ INVALID DEFAULTS: {invalid_defaults}")
                    return False
                else:
                    print(f"  ✅ All defaults valid")
            elif action.default not in action.choices:
                print(f"  ❌ INVALID DEFAULT: {action.default} not in choices")
                return False
            else:
                print(f"  ✅ Default valid")

    return True

def debug_validate_args(program, program_name="main"):
    print(f"\n=== Validating {program_name} ===")

    # First check main program actions
    if not debug_validate_actions(program, program_name):
        print(f"❌ {program_name} validation failed")
        return False

    # Then check subparsers
    for action in program._actions:
        if isinstance(action, _SubParsersAction):
            print(f"\nFound subparsers in {program_name}")
            for sub_name, sub_program in action._name_parser_map.items():
                if not debug_validate_args(sub_program, f"{program_name}.{sub_name}"):
                    print(f"❌ Subparser {sub_name} validation failed")
                    return False

    print(f"✅ {program_name} validation passed")
    return True

if __name__ == "__main__":
    try:
        print("Creating program...")
        program = create_program()
        print("Program created successfully")

        print("\nStarting validation debug...")
        result = debug_validate_args(program)

        print(f"\nFinal result: {result}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
