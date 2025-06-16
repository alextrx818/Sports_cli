#!/usr/bin/env python3
"""
Test module to inspect any Python module and categorize its contents into:
- Functions
- Classes  
- Sub-modules
- Variables (everything else)

Usage: Change the import statement to point to any module you want to inspect.
"""

import inspect
import sys

# Change this import to inspect a different module
import step2 as target_module

def inspect_module(module):
    """
    Inspect a module and categorize all its members.
    
    Args:
        module: The module object to inspect
        
    Returns:
        A dictionary with keys 'functions', 'classes', 'modules', 'variables'
        containing lists of names in each category.
    """
    # Get all names in the module
    all_names = dir(module)
    
    # Initialize collections
    functions = []
    classes = []
    modules = []
    variables = []
    
    # Categorize each name
    for name in all_names:
        # Skip private/special attributes unless you want them
        # if name.startswith('_'):
        #     continue
            
        try:
            obj = getattr(module, name)
            
            # Categorize based on type
            if inspect.isfunction(obj):
                functions.append(name)
            elif inspect.isclass(obj):
                classes.append(name)
            elif inspect.ismodule(obj):
                modules.append(name)
            else:
                # Everything else is a variable
                variables.append(name)
                
        except AttributeError:
            # Handle cases where getattr fails
            variables.append(name)
    
    return {
        'functions': sorted(functions),
        'classes': sorted(classes),
        'modules': sorted(modules),
        'variables': sorted(variables)
    }

def print_module_contents(module_name, results):
    """Pretty print the categorized contents of a module."""
    print(f"\n=== Module: {module_name} ===\n")
    
    print(f"Functions: {results['functions']}")
    print(f"Classes:   {results['classes']}")
    print(f"Modules:   {results['modules']}")
    print(f"Variables: {results['variables']}")
    
    # Print counts
    print(f"\nSummary:")
    print(f"  Functions: {len(results['functions'])}")
    print(f"  Classes:   {len(results['classes'])}")
    print(f"  Modules:   {len(results['modules'])}")
    print(f"  Variables: {len(results['variables'])}")
    print(f"  Total:     {sum(len(v) for v in results.values())}")

def test_module_inspection():
    """Test function that can be run with pytest or unittest."""
    results = inspect_module(target_module)
    
    # Basic assertions to verify the inspection worked
    assert isinstance(results['functions'], list)
    assert isinstance(results['classes'], list)
    assert isinstance(results['modules'], list)
    assert isinstance(results['variables'], list)
    
    # Verify we found at least some content
    total_items = sum(len(v) for v in results.values())
    assert total_items > 0, "Module appears to be empty"
    
    print("✓ Module inspection test passed!")
    return results

if __name__ == "__main__":
    # Run the inspection
    results = inspect_module(target_module)
    
    # Print the results
    print_module_contents(target_module.__name__, results)
    
    # Optional: Print detailed info about specific categories
    if '--verbose' in sys.argv:
        print("\n=== Detailed Information ===")
        
        if results['functions']:
            print("\nFunction signatures:")
            for func_name in results['functions'][:10]:  # First 10 only
                func = getattr(target_module, func_name)
                sig = inspect.signature(func) if hasattr(func, '__code__') else '(?)'
                print(f"  {func_name}{sig}")
                
        if results['classes']:
            print("\nClass information:")
            for class_name in results['classes'][:10]:  # First 10 only
                cls = getattr(target_module, class_name)
                bases = [b.__name__ for b in cls.__bases__] if hasattr(cls, '__bases__') else []
                print(f"  {class_name}({', '.join(bases)})")
    
    # Run the test
    print("\n=== Running Test ===")
    test_module_inspection()
