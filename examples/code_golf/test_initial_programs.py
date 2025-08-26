#!/usr/bin/env python3
"""
Test initial programs for code-golf tasks to verify they work correctly.
"""

import json
import os
import sys
import importlib.util
import traceback
import multiprocessing
import queue
import copy
from pathlib import Path


def load_task_json(task_num):
    """Load the task JSON file for a specific task number."""
    # Look for the task JSON file in the google-code-golf-2025 directory
    task_file = f"examples/code_golf/google-code-golf-2025/task{task_num:03d}.json"
    
    if os.path.exists(task_file):
        with open(task_file, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"Could not find {task_file}")


def test_program_with_timeout(program_func, input_data, timeout_seconds=5):
    """Test a single input with timeout using multiprocessing."""
    def target(q, func, inp):
        try:
            # Use deepcopy for safety (like Google's implementation)
            input_copy = copy.deepcopy(inp)
            result = func(input_copy)
            q.put(('success', result))
        except Exception as e:
            q.put(('error', str(e)))
    
    q = multiprocessing.Queue()
    process = multiprocessing.Process(target=target, args=(q, program_func, input_data))
    process.start()
    process.join(timeout=timeout_seconds)
    
    if process.is_alive():
        process.terminate()
        process.join()
        return False, "Timeout"
    
    if process.exitcode != 0:
        return False, "Process crashed"
    
    try:
        result_type, result_value = q.get_nowait()
        if result_type == 'success':
            return True, result_value
        else:
            return False, result_value
    except:
        return False, "No result"


def test_program_against_examples(program_func, examples, task_num):
    """Test program against a set of examples."""
    failed_count = 0
    total_examples = len(examples)
    
    for i, example in enumerate(examples):
        try:
            # Use direct call instead of multiprocessing for now
            input_copy = copy.deepcopy(example['input'])
            result = program_func(input_copy)
            if result != example['output']:
                failed_count += 1
        except Exception as e:
            failed_count += 1
    
    passed = failed_count == 0
    return passed, failed_count, total_examples


def test_single_task(task_num, verbose=False):
    """Test a single task's initial program."""
    results = []
    
    try:
        # Load task data
        task_data = load_task_json(task_num)
        results.append(f"Task {task_num}: Loaded task data")
        
        # Load initial program
        program_path = f"examples/code_golf/initial_programs/initial_program_task_{task_num}.py"
        if not os.path.exists(program_path):
            results.append(f"Task {task_num}: 💥 ERROR - Initial program not found: {program_path}")
            return False, results
        
        # Import the program
        spec = importlib.util.spec_from_file_location("program", program_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find the main function - must be named 'p' (Google's convention)
        if not hasattr(module, 'p'):
            results.append(f"Task {task_num}: 💥 ERROR - Function 'p()' not found in program")
            return False, results
        
        program_func = module.p
        if not callable(program_func):
            results.append(f"Task {task_num}: 💥 ERROR - 'p' is not callable")
            return False, results
        
        # Test against all example categories
        train_examples = task_data.get('train', [])
        test_examples = task_data.get('test', [])
        arc_gen_examples = task_data.get('arc-gen', [])
        
        train_passed = test_passed = arc_gen_passed = True
        train_failed_count = test_failed_count = arc_gen_failed_count = 0
        train_total = test_total = arc_gen_total = 0
        
        if train_examples:
            train_passed, train_failed_count, train_total = test_program_against_examples(program_func, train_examples, task_num)
            results.append(f"Train examples: {'✅ PASSED' if train_passed else '❌ FAILED'} ({train_failed_count}/{train_total} failed)")
        
        if test_examples:
            test_passed, test_failed_count, test_total = test_program_against_examples(program_func, test_examples, task_num)
            results.append(f"Test examples: {'✅ PASSED' if test_passed else '❌ FAILED'} ({test_failed_count}/{test_total} failed)")
        
        if arc_gen_examples:
            arc_gen_passed, arc_gen_failed_count, arc_gen_total = test_program_against_examples(program_func, arc_gen_examples, task_num)
            results.append(f"Arc-gen examples: {'✅ PASSED' if arc_gen_passed else '❌ FAILED'} ({arc_gen_failed_count}/{arc_gen_total} failed)")
        
        # Overall result
        overall_passed = train_passed and test_passed and arc_gen_passed
        total_failed = train_failed_count + test_failed_count + arc_gen_failed_count
        total_examples = train_total + test_total + arc_gen_total
        
        results.append(f"Overall: {'✅ PASSED' if overall_passed else '❌ FAILED'} ({total_failed}/{total_examples} total failed)")
        
        return overall_passed, results
        
    except Exception as e:
        results.append(f"Task {task_num}: 💥 ERROR - {str(e)}")
        if verbose:
            results.append(f"Traceback: {traceback.format_exc()}")
        return False, results


def main():
    """Main function to test initial programs."""
    if len(sys.argv) < 2:
        print("Usage: python test_initial_programs.py <task_numbers...> [--verbose]")
        print("Example: python test_initial_programs.py 1 8 13")
        print("Example: python test_initial_programs.py 1 8 13 --verbose")
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    verbose = "--verbose" in args
    if verbose:
        args.remove("--verbose")
    
    task_numbers = [int(x) for x in args]
    
    print(f"🧪 Testing initial programs for tasks: {task_numbers}")
    print(f"📁 Looking for programs in: initial_programs/")
    print(f"📊 Looking for task data in: google-code-golf-2025/")
    print()
    
    # Test each task
    overall_results = {}
    for task_num in task_numbers:
        print(f"Testing task {task_num}...")
        passed, results = test_single_task(task_num, verbose)
        overall_results[task_num] = passed
        
        for result in results:
            print(f"  {result}")
        print()
    
    # Summary
    print("📋 Summary:")
    print("=" * 40)
    passed_count = 0
    for task_num, passed in overall_results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"Task {task_num:3d}: {status}")
        if passed:
            passed_count += 1
    
    total_tasks = len(overall_results)
    print(f"\n🎯 Overall: {passed_count}/{total_tasks} tasks passed")
    
    if passed_count == total_tasks:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
