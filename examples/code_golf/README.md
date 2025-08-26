## Google Code Golf 2025 Tasks

AlphaEvolve-Lite implementation for Google Code Golf 2025 pattern recognition and transformation problems.

### 📁 Directory Structure

* **`google-code-golf-2025/`** – Task JSON files (task001.json to task400.json) containing input/output examples
* **`initial_programs/`** – Starting point programs for each task (initial_program_task_X.py)
* **`best_solutions/`** – Human-optimized reference solutions for benchmarking
* **`task_template/`** – Template config.yml and evaluate.py files used to generate task-specific experiments
* **`taskXXX_vY/`** – Generated experiment directories containing customized configs and task data

### 🎯 Scoring System

**Final Score = Accuracy × (1 + Length Bonus)**

- **Accuracy**: Fraction of test cases passed (train + test + arc-gen examples)
- **Length Bonus**: max(0, (initial_length / generated_length) - 1)
- Incorrect programs score 0, shorter correct programs score higher

### 🚀 Running Experiments

**Single task:**
```bash
python run_batch.py 13 --version 1
```

**Multiple generations:**
```bash
python run_batch.py 13 --version 2 --max-generations 20
```

**With debugging:**
```bash
python run_batch.py 13 --version 3 --debug --workers 1
```

### 🧪 Testing Initial Programs

Test specific task:
```bash
python test_initial_programs.py 13
```

### 📊 Visualization

Generate plots for an experiment:
```bash
python scripts/visualize_experiment.py --db alphaevolve.db --experiment "code-golf-task013-v1"
```

With benchmark line:
```bash
python scripts/visualize_experiment.py --experiment code-golf-task013-v1 --benchmark-scores '{"task013": 3.827}'
```

### 📈 Benchmark Scores

Calculate reference score for a task:
```bash
python get_best_solution_score.py 13
```

This shows character counts and calculates the score using the best solution from `best_solutions/`.

### 🔧 Configuration

Tasks use the `custom` LLM provider by default. Set environment variables:
```bash
export CUSTOM_API_KEY="your-api-key"
export CUSTOM_BASE_URL="http://your-server:port/v1"
```

Or modify `task_template/config.yml` to use other providers (openai, gemini, openrouter).

### 📝 Task Format

Each task requires implementing a function `p(input_data)` that transforms 2D grids:
- Input: 2D list of integers (0-9 representing colors)
- Output: 2D list of same format
- Goal: Discover the pattern from train examples and apply to test examples
