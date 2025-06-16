#!/usr/bin/env python3
"""
Tool to identify and fix module-level code that should be inside functions.
This helps prevent import-time execution errors.
"""

import ast
import sys
import os

class ModuleLevelCodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.module_level_code = []
        self.main_block_line = None
        self.issues = []
        
    def visit_Module(self, node):
        """Analyze module-level statements"""
        for i, stmt in enumerate(node.body):
            # Skip imports, function/class definitions, and constants
            if isinstance(stmt, (ast.Import, ast.ImportFrom, ast.FunctionDef, 
                                ast.ClassDef, ast.Assign)):
                if isinstance(stmt, ast.Assign):
                    # Check if it's a simple constant assignment
                    if not self._is_simple_assignment(stmt):
                        self.module_level_code.append((stmt.lineno, ast.unparse(stmt)))
            # Check for if __name__ == "__main__"
            elif isinstance(stmt, ast.If):
                if self._is_main_check(stmt):
                    self.main_block_line = stmt.lineno
                else:
                    self.module_level_code.append((stmt.lineno, ast.unparse(stmt)))
            # Any other statement at module level is suspicious
            elif not isinstance(stmt, ast.Expr) or not self._is_docstring(stmt):
                self.module_level_code.append((stmt.lineno, ast.unparse(stmt)))
                
        self.generic_visit(node)
        
    def _is_simple_assignment(self, node):
        """Check if assignment is a simple constant"""
        if len(node.targets) != 1:
            return False
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            return False
        # Check if the value is a constant or simple expression
        return isinstance(node.value, (ast.Constant, ast.Name, ast.Attribute, 
                                     ast.Call, ast.List, ast.Dict, ast.Tuple))
    
    def _is_main_check(self, node):
        """Check if this is if __name__ == "__main__" """
        if not isinstance(node.test, ast.Compare):
            return False
        if not isinstance(node.test.left, ast.Name) or node.test.left.id != "__name__":
            return False
        if not node.test.comparators or not isinstance(node.test.comparators[0], ast.Constant):
            return False
        return node.test.comparators[0].value == "__main__"
    
    def _is_docstring(self, node):
        """Check if expression is a docstring"""
        return isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)

def analyze_file(filepath):
    """Analyze a Python file for module-level code issues"""
    print(f"\n=== Analyzing {filepath} ===\n")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the AST
        tree = ast.parse(content, filepath)
        analyzer = ModuleLevelCodeAnalyzer()
        analyzer.visit(tree)
        
        # Report findings
        if analyzer.module_level_code:
            print("⚠️  Found module-level code that executes at import time:")
            for lineno, code in analyzer.module_level_code:
                print(f"  Line {lineno}: {code[:60]}...")
                
        if analyzer.main_block_line:
            print(f"\n✓ Found if __name__ == '__main__': block at line {analyzer.main_block_line}")
            
        # Check for code after main block
        lines = content.split('\n')
        if analyzer.main_block_line:
            code_after_main = []
            for i in range(analyzer.main_block_line + 2, len(lines)):  # +2 to skip main() call
                line = lines[i].strip()
                if line and not line.startswith('#'):
                    code_after_main.append((i + 1, line))
                    
            if code_after_main:
                print("\n❌ CRITICAL: Found code AFTER if __name__ == '__main__' block:")
                for lineno, line in code_after_main[:10]:  # Show first 10 lines
                    print(f"  Line {lineno}: {line}")
                print("\n  This code runs at import time and should be removed!")
                
        return analyzer
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return None

def fix_file(filepath, backup=True):
    """Remove code after if __name__ == '__main__' block"""
    print(f"\n=== Fixing {filepath} ===\n")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Find the main block
        main_block_line = None
        for i, line in enumerate(lines):
            if 'if __name__ == "__main__":' in line:
                main_block_line = i
                break
                
        if main_block_line is None:
            print("No if __name__ == '__main__': block found")
            return False
            
        # Find where the main block ends (usually main() call)
        end_line = main_block_line + 1
        while end_line < len(lines):
            if lines[end_line].strip() and not lines[end_line].startswith(' '):
                break
            end_line += 1
            
        # Check if there's code after
        has_code_after = False
        for i in range(end_line, len(lines)):
            if lines[i].strip() and not lines[i].strip().startswith('#'):
                has_code_after = True
                break
                
        if not has_code_after:
            print("✓ No problematic code found after main block")
            return True
            
        # Backup original file
        if backup:
            backup_path = filepath + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Created backup: {backup_path}")
            
        # Write fixed file (remove everything after main block)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines[:end_line])
            
        print(f"✓ Removed {len(lines) - end_line} lines after main block")
        return True
        
    except Exception as e:
        print(f"Error fixing file: {e}")
        return False

if __name__ == "__main__":
    # Analyze step2.py
    filepath = "/root/6-4-2025/step2.py"
    
    print("Python Module-Level Code Analyzer")
    print("=" * 50)
    
    # First analyze the file
    analyzer = analyze_file(filepath)
    
    # Ask user if they want to fix it
    if analyzer:
        print("\nOptions:")
        print("1. Fix the file (remove code after main block)")
        print("2. Just analyze (no changes)")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            if fix_file(filepath):
                print("\n✓ File fixed successfully!")
                print("Re-analyzing to confirm...")
                analyze_file(filepath)
            else:
                print("\n❌ Failed to fix file")
        elif choice == "2":
            print("\nAnalysis complete. No changes made.")
        else:
            print("\nExiting.")
