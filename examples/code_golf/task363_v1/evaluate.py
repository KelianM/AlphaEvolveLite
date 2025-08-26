#!/usr/bin/env python3
"""
Evaluation script for code-golf tasks.
This template is copied to individual task directories during batch runs.
"""

import json
import os
import sys
import glob
import re
from pathlib import Path
import importlib.util
import traceback
import functools
import copy


def load_examples():
    """Load examples for the current task."""
    # Extract task number from script path
    script_path = os.path.abspath(__file__)
    
    # Try to extract task number from script path (e.g., task001_v1/evaluate.py)
    path_match = re.search(r'task(\d+)', script_path)
    if not path_match:
        raise FileNotFoundError("Could not determine task number from script path")
    
    task_num = path_match.group(1)
    
    # The task JSON file should be in the same directory as this script
    script_dir = os.path.dirname(script_path)
    task_file_name = "task363.json"
    task_file_path = os.path.join(script_dir, task_file_name)
    
    if os.path.exists(task_file_path):
        print(f"Loading examples from: {task_file_path}")
        with open(task_file_path, 'r') as f:
            return json.load(f)
    
    raise FileNotFoundError(f"Could not find task JSON file: {task_file_path}")


def test_program_with_timeout(program_func, input_data, timeout_seconds=5):
    """Test a single input (without multiprocessing to avoid macOS issues)."""
    try:
        # Use deepcopy for safety (like Google's implementation)
        input_copy = copy.deepcopy(input_data)
        result = program_func(input_copy)
        return True, result
    except Exception as e:
        return False, str(e)


def test_program(program_path):
    """Test the program against all examples."""
    # Load the task examples
    examples = load_examples()
    
    # Import the program
    spec = importlib.util.spec_from_file_location("program", program_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Find the main function - must be named 'p' (Google's convention)
    if not hasattr(module, 'p'):
        raise ValueError("Function 'p()' not found in program")
    
    program_func = module.p
    if not callable(program_func):
        raise ValueError("'p' is not callable")
    
    total_examples = 0
    correct_examples = 0
    
    # Test all example categories
    for category in ['train', 'test', 'arc-gen']:
        if category in examples:
            for i, example in enumerate(examples[category]):
                total_examples += 1
                try:
                    success, result = test_program_with_timeout(program_func, example['input'])
                    if success and result == example['output']:
                        correct_examples += 1
                    else:
                        print(f"{category}[{i}]: Expected {example['output']}, got {result}")
                except Exception as e:
                    print(f"{category}[{i}]: Error - {str(e)}")
    
    return correct_examples == total_examples, correct_examples, total_examples


def get_initial_program_length():
    """Get the character length of the initial program."""
    # The initial program should be in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    initial_program_path = os.path.join(script_dir, "initial_program.py")
    
    if os.path.exists(initial_program_path):
        with open(initial_program_path, 'r') as f:
            content = f.read().strip()
            return len(content)
    
    print("Warning: Could not find initial program, using default length of 1000")
    return 1000


def evaluate(program_path):
    """
    Main evaluation function.
    Returns score: accuracy_ratio * (1 + length_bonus)
    Where length_bonus = max(0, (initial_length / generated_length) - 1)
    This ensures incorrect programs get low scores regardless of length.
    """
    try:
        # Test the program
        success, correct_examples, total_examples = test_program(program_path)
        
        # Calculate accuracy ratio
        accuracy_ratio = correct_examples / total_examples if total_examples > 0 else 0
        
        # Get program lengths
        with open(program_path, 'r') as f:
            generated_content = f.read().strip()
            generated_length = len(generated_content)
        
        initial_length = get_initial_program_length()
        
        # Calculate length bonus (only for correct programs)
        if generated_length > 0:
            length_ratio = initial_length / generated_length
            length_bonus = max(0, length_ratio - 1)  # Only bonus if shorter than initial
        else:
            length_bonus = 0
        
        # Final score calculation
        multiplier = 1 + length_bonus
        final_score = accuracy_ratio * multiplier
        
        # Print detailed results
        print(f"Program: {program_path}")
        print(f"Examples: {correct_examples}/{total_examples} correct")
        print(f"Accuracy ratio: {accuracy_ratio:.3f}")
        print(f"Generated length: {generated_length} chars")
        print(f"Initial length: {initial_length} chars")
        print(f"Length ratio: {length_ratio:.3f}")
        print(f"Length bonus: {length_bonus:.3f}")
        print(f"Multiplier: {multiplier:.3f}")
        print(f"Final score: {final_score:.3f}")
        
        return final_score
        
    except Exception as e:
        print(f"Error evaluating program: {e}")
        traceback.print_exc()
        return 0.0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluate.py <program_path>")
        sys.exit(1)
    
    program_path = sys.argv[1]
    score = evaluate(program_path)
    print(f"\nFinal Score: {score}")
