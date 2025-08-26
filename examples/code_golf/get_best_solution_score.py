#!/usr/bin/env python3
"""
Simple script to get the best solution score for a code-golf task.
Usage: python get_best_solution_score_simple.py 363
"""

import sys
import os
import json
import copy

def get_best_solution_score(task_num):
    """Get the score for the best solution of a given task using direct file access."""
    
    # Determine if we're running from project root or code_golf directory
    if os.path.exists('examples/code_golf'):
        # Running from project root
        base_dir = 'examples/code_golf'
    else:
        # Running from code_golf directory
        base_dir = '.'
    
    # Check required files exist
    best_solution_path = f"{base_dir}/best_solutions/best_solution_task_{task_num}.py"
    initial_program_path = f"{base_dir}/initial_programs/initial_program_task_{task_num}.py"
    task_json_path = f"{base_dir}/google-code-golf-2025/task{task_num:03d}.json"
    
    if not os.path.exists(best_solution_path):
        print(f"Best solution not found: {best_solution_path}")
        return 0.0
    
    if not os.path.exists(initial_program_path):
        print(f"Initial program not found: {initial_program_path}")
        return 0.0
        
    if not os.path.exists(task_json_path):
        print(f"Task JSON not found: {task_json_path}")
        return 0.0
    
    try:
        # Load task data
        with open(task_json_path, 'r') as f:
            task_data = json.load(f)
        
        # Get initial program length
        with open(initial_program_path, 'r') as f:
            initial_length = len(f.read().strip())
        
        # Load and execute best solution
        with open(best_solution_path, 'r') as f:
            best_solution_code = f.read()
        
        # Create a temporary namespace and execute the code
        namespace = {}
        exec(best_solution_code, namespace)
        
        if 'p' not in namespace:
            print(f"Function 'p' not found in best solution")
            return 0.0
        
        p_func = namespace['p']
        
        # Test the function on all examples
        correct_examples = 0
        total_examples = 0
        
        # Test train examples
        for example in task_data.get('train', []):
            try:
                input_grid = copy.deepcopy(example['input'])
                expected_output = example['output']
                actual_output = p_func(input_grid)
                if actual_output == expected_output:
                    correct_examples += 1
                total_examples += 1
            except Exception:
                total_examples += 1
        
        # Test test examples  
        for example in task_data.get('test', []):
            try:
                input_grid = copy.deepcopy(example['input'])
                expected_output = example['output']
                actual_output = p_func(input_grid)
                if actual_output == expected_output:
                    correct_examples += 1
                total_examples += 1
            except Exception:
                total_examples += 1
        
        # Test arc-gen examples
        for example in task_data.get('arc-gen', []):
            try:
                input_grid = copy.deepcopy(example['input'])
                expected_output = example['output']
                actual_output = p_func(input_grid)
                if actual_output == expected_output:
                    correct_examples += 1
                total_examples += 1
            except Exception:
                total_examples += 1
        
        # Calculate score using the same formula as evaluate.py
        if total_examples == 0:
            return 0.0
            
        accuracy_ratio = correct_examples / total_examples
        
        # Get best solution length
        best_solution_length = len(best_solution_code.strip())
        
        # Calculate length bonus
        if best_solution_length > 0:
            length_ratio = initial_length / best_solution_length
            length_bonus = max(0, length_ratio - 1)
        else:
            length_bonus = 0
        
        # Final score calculation (same as evaluate.py)
        multiplier = 1 + length_bonus
        final_score = accuracy_ratio * multiplier
        
        # Print character counts to stderr so they don't interfere with score output
        print(f"Initial program length: {initial_length} characters", file=sys.stderr)
        print(f"Best solution length: {best_solution_length} characters", file=sys.stderr)
        print(f"Length ratio: {length_ratio:.3f} (bonus: {length_bonus:.3f})", file=sys.stderr)
        print(f"Accuracy: {correct_examples}/{total_examples} = {accuracy_ratio:.3f}", file=sys.stderr)
        
        return final_score
        
    except Exception as e:
        print(f"Error evaluating: {e}")
        import traceback
        traceback.print_exc()
        return 0.0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_best_solution_score_simple.py <task_number>")
        sys.exit(1)
    
    task_num = int(sys.argv[1])
    score = get_best_solution_score(task_num)
    print(f"{score:.4f}")
