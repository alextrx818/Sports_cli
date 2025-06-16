#!/usr/bin/env python3
"""
Example of using the module inspector on the standard library 'os' module.
Shows that you can inspect ANY module - built-in or custom.
"""

import inspect

# Inspect the os module from standard library
import os as target_module

def inspect_module(module):
    all_names = dir(module)
    
    functions = []
    classes = []
    modules = []
    variables = []
    
    for name in all_names:
        try:
            obj = getattr(module, name)
            
            if inspect.isfunction(obj):
                functions.append(name)
            elif inspect.isclass(obj):
                classes.append(name)
            elif inspect.ismodule(obj):
                modules.append(name)
            else:
                variables.append(name)
                
        except AttributeError:
            variables.append(name)
    
    return {
        'functions': sorted(functions),
        'classes': sorted(classes),
        'modules': sorted(modules),
        'variables': sorted(variables)
    }

if __name__ == "__main__":
    results = inspect_module(target_module)
    
    print(f"\n=== Module: {target_module.__name__} ===\n")
    
    # Show first 10 items in each category due to os module being large
    print(f"Functions (first 10 of {len(results['functions'])}): {results['functions'][:10]}")
    print(f"Classes   (first 10 of {len(results['classes'])}):   {results['classes'][:10]}")
    print(f"Modules   (first 10 of {len(results['modules'])}):   {results['modules'][:10]}")
    print(f"Variables (first 10 of {len(results['variables'])}): {results['variables'][:10]}")
    
    print(f"\nTotal counts:")
    print(f"  Functions: {len(results['functions'])}")
    print(f"  Classes:   {len(results['classes'])}")
    print(f"  Modules:   {len(results['modules'])}")
    print(f"  Variables: {len(results['variables'])}")
    print(f"  Total:     {sum(len(v) for v in results.values())}")
