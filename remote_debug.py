#!/usr/bin/env python3
"""
Remote server debug script for FaceFusion validation issues.
Copy this script to your remote server and run it to identify validation problems.
"""

import sys
sys.path.insert(0, '.')

from facefusion.program import create_program
from facefusion.program_helper import validate_args, validate_actions
from argparse import _SubParsersAction

def check_config_file():
    """Check if facefusion.ini has invalid values"""
    try:
        from facefusion import config, state_manager
        print("=== Checking Configuration File ===")
        
        # Check if config file exists and is readable
        config_path = state_manager.get_item('config_path') or 'facefusion.ini'
        print(f"Config path: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                content = f.read()
                print(f"Config file exists and readable ({len(content)} chars)")
        except Exception as e:
            print(f"❌ Config file error: {e}")
            return False
            
        # Test config parsing
        try:
            config.clear_config_parser()
            parser = config.get_config_parser()
            print(f"✅ Config parsed successfully, {len(parser.sections())} sections")
            
            # Check for common problematic values
            for section in parser.sections():
                print(f"Section [{section}]:")
                for option in parser.options(section):
                    value = parser.get(section, option)
                    if value.strip():  # Only show non-empty values
                        print(f"  {option} = {value}")
                        
        except Exception as e:
            print(f"❌ Config parsing error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Config check failed: {e}")
        return False
    
    return True

def detailed_validation_debug():
    """Detailed validation debugging"""
    print("\n=== Starting Detailed Validation Debug ===")
    
    try:
        print("Creating program...")
        program = create_program()
        print("✅ Program created")
        
        print("\nTesting main program validation...")
        main_valid = validate_actions(program)
        print(f"Main program valid: {main_valid}")
        
        if not main_valid:
            print("❌ Main program validation failed - checking arguments...")
            for action in program._actions:
                if action.default and action.choices:
                    if isinstance(action.default, list):
                        invalid = [d for d in action.default if d not in action.choices]
                        if invalid:
                            print(f"❌ INVALID: {action.dest} = {action.default}, invalid items: {invalid}")
                    elif action.default not in action.choices:
                        print(f"❌ INVALID: {action.dest} = {action.default} not in {action.choices}")
            return False
        
        print("Checking subparsers...")
        for action in program._actions:
            if isinstance(action, _SubParsersAction):
                for sub_name, sub_program in action._name_parser_map.items():
                    sub_valid = validate_args(sub_program)
                    print(f"Subparser {sub_name}: {sub_valid}")
                    if not sub_valid:
                        print(f"❌ Subparser {sub_name} failed")
                        return False
        
        print("✅ All validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Validation debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("FaceFusion Remote Debug Script")
    print("=" * 50)
    
    # Check Python environment
    print(f"Python version: {sys.version}")
    print(f"Working directory: {sys.path[0]}")
    
    # Check config file
    config_ok = check_config_file()
    
    # Run detailed validation
    validation_ok = detailed_validation_debug()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Config file: {'✅ OK' if config_ok else '❌ FAILED'}")
    print(f"Validation: {'✅ OK' if validation_ok else '❌ FAILED'}")
    
    if not validation_ok:
        print("\n🔧 POTENTIAL FIXES:")
        print("1. Check your facefusion.ini file for invalid values")
        print("2. Try renaming facefusion.ini to facefusion.ini.backup")
        print("3. Check execution_providers setting (should be 'cpu' on most servers)")
        print("4. Ensure all paths in config are valid for your server")

if __name__ == "__main__":
    main()
