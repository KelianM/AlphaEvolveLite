#!/usr/bin/env python3
"""
Batch runner for code-golf tasks.
Creates versioned task directories and runs evolution directly using EvolutionController.
"""

import os
import shutil
import json
import random
import sys
import yaml
import multiprocessing
from pathlib import Path
from alphaevolve.config import Config
from alphaevolve.controller import EvolutionController

multiprocessing.set_start_method("fork", force=True)


def format_grid(grid):
    """Format a 2D grid for display in the prompt."""
    return "[" + ",\n     ".join(str(row) for row in grid) + "]"


def format_examples_for_prompt(task_data):
    """Format task examples for inclusion in the system prompt."""
    examples_text = "Task Examples:\n\n"
    
    # Add train examples
    if "train" in task_data and task_data["train"]:
        examples_text += "Training Examples:\n"
        for i, example in enumerate(task_data["train"][:3]):  # Show first 3 train examples
            examples_text += f"Example {i+1}:\n"
            examples_text += f"Input:\n{format_grid(example['input'])}\n\n"
            examples_text += f"Output:\n{format_grid(example['output'])}\n\n"
    
    # Add test examples
    if "test" in task_data and task_data["test"]:
        examples_text += "Test Example:\n"
        example = task_data["test"][0]  # Show first test example
        examples_text += f"Input:\n{format_grid(example['input'])}\n\n"
        examples_text += f"Expected Output:\n{format_grid(example['output'])}\n\n"
    
    examples_text += "Your task is to find the pattern that transforms the input grids to the output grids."
    
    return examples_text


def setup_task_directory(task_num, version=1):
    """Set up a versioned task directory with necessary files."""
    import shutil  # Import at the top of function
    
    task_dir = f"examples/code_golf/task{task_num:03d}_v{version}"
    
    # Remove existing directory if it exists to ensure clean setup
    if os.path.exists(task_dir):
        shutil.rmtree(task_dir)
        print(f"🗑️  Removed existing directory: {task_dir}")
    
    # Create task directory
    os.makedirs(task_dir, exist_ok=True)
    
    # Load task data
    task_file = f"examples/code_golf/google-code-golf-2025/task{task_num:03d}.json"
    if not os.path.exists(task_file):
        raise FileNotFoundError(f"Task file not found: {task_file}")
    
    with open(task_file, 'r') as f:
        task_data = json.load(f)
    
    # Create a reduced task JSON with random samples
    reduced_task_data = {
        "train": task_data["train"], 
        "test": task_data["test"], 
        # "arc-gen": random.sample(task_data["arc-gen"], min(10, len(task_data["arc-gen"])))  # 10 random arc-gen
        "arc-gen": task_data["arc-gen"][:10]
    }
    
    # Save the reduced task data
    with open(f"{task_dir}/task{task_num:03d}.json", 'w') as f:
        json.dump(reduced_task_data, f, indent=2)
    
    # Copy and customize config.yml from template
    template_dir = "examples/code_golf/task_template"
    with open(f"{template_dir}/config.yml", 'r') as f:
        config = yaml.safe_load(f)
    
    # Customize config for this specific task
    config['experiment']['label'] = f"code-golf-task{task_num:03d}-v{version}"
    config['experiment']['notes'] = f"Evolve solutions for Google Code Golf 2025 task {task_num:03d}."
    
    # Update problem paths to be relative to project root
    config['problem']['entry_script'] = f"{task_dir}/initial_program.py"
    config['problem']['evaluator'] = f"{task_dir}/evaluate.py"
    
    # Add task-specific examples to the system prompt
    examples_text = format_examples_for_prompt(task_data)
    config['llm']['system_prompt'] = config['llm']['system_prompt'] + "\n\n" + examples_text
    
    # Save customized config
    with open(f"{task_dir}/config.yml", 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    # Copy and customize evaluate.py template
    with open(f"{template_dir}/evaluate.py", 'r') as f:
        evaluate_content = f.read()
    
    # Update evaluate.py to use the correct task JSON file path
    evaluate_content = evaluate_content.replace(
        'task_file_name = f"task{task_num}.json"',
        f'task_file_name = "task{task_num:03d}.json"'
    )
    
    # Template already works correctly - no need to replace the get_initial_program_length function
    # Each task directory gets its own copy of initial_program.py which the template finds correctly
    
    with open(f"{task_dir}/evaluate.py", 'w') as f:
        f.write(evaluate_content)
    
    # Copy initial program if it exists
    initial_program_path = f"examples/code_golf/initial_programs/initial_program_task_{task_num}.py"
    if os.path.exists(initial_program_path):
        shutil.copy2(initial_program_path, f"{task_dir}/initial_program.py")
    else:
        print(f"Warning: No initial program found for task {task_num}")
        # Create a placeholder initial program
        with open(f"{task_dir}/initial_program.py", 'w') as f:
            f.write(f"""# Initial program for task {task_num:03d}
# TODO: Implement solution

def p(input_data):
    '''
    Solve the code golf task (Google's 'p' function convention).
    
    Args:
        input_data: The input data for this task
        
    Returns:
        The expected output
    '''
    # Placeholder implementation
    return input_data
""")
    
    print(f"✅ Set up task directory: {task_dir}")
    return task_dir


def run_task(task_dir, max_generations=None, debug=False, resume=False, workers=None):
    """Run evolution for a single task using EvolutionController directly."""
    print(f"\n🚀 Running evolution for {task_dir}...")
    
    config_path = f"{task_dir}/config.yml"
    
    try:
        # Load config
        cfg = Config.load(config_path)
        
        # Override settings from command line
        if debug:
            cfg.debug = debug
        if max_generations:
            cfg.evolution.max_generations = max_generations
        if workers is not None:
            cfg.evolution.max_workers = workers
        
        # Run evolution directly using EvolutionController
        controller = EvolutionController(cfg, resume=resume)
        controller.run_evolution()
        
        print(f"✅ Task {task_dir} completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Task {task_dir} failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main batch runner."""
    # Parse arguments
    import argparse
    
    parser = argparse.ArgumentParser(description='Run AlphaEvolve evolution for multiple code-golf tasks')
    parser.add_argument('tasks', nargs='+', type=int, help='Task numbers to run (e.g., 1 8 13)')
    parser.add_argument('--version', type=int, default=1, help='Version number for task directories')
    parser.add_argument('--max-generations', type=int, default=None, help='Maximum generations per task')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--resume', action='store_true', help='Resume evolution from current generation')
    parser.add_argument('--workers', type=int, default=None, help='Number of workers (overrides config)')
    
    args = parser.parse_args()
    
    print(f"🎯 Running batch evolution for tasks: {args.tasks}")
    print(f"📋 Version: v{args.version}")
    if args.max_generations:
        print(f"🔢 Limited to {args.max_generations} generations per task")
    if args.debug:
        print("🐛 Debug mode enabled")
    if args.resume:
        print("🔄 Resume mode enabled")
    if args.workers:
        print(f"👥 Using {args.workers} workers")
    
    # Set up task directories
    task_dirs = []
    for task_num in args.tasks:
        try:
            task_dir = setup_task_directory(task_num, args.version)
            task_dirs.append(task_dir)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            continue
    
    if not task_dirs:
        print("❌ No valid tasks could be set up")
        sys.exit(1)
    
    # Run evolution for each task
    results = {}
    for task_dir in task_dirs:
        success = run_task(
            task_dir, 
            max_generations=args.max_generations,
            debug=args.debug,
            resume=args.resume,
            workers=args.workers
        )
        results[task_dir] = success
    
    # Summary
    print(f"\n📊 Batch Run Summary:")
    print(f"{'Task Directory':<25} {'Status':<10}")
    print("-" * 35)
    for task_dir, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"{task_dir:<25} {status:<10}")
    
    successful = sum(results.values())
    total = len(results)
    print(f"\n🎉 {successful}/{total} tasks completed successfully")


if __name__ == "__main__":
    main()
