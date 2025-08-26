# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module containing utilities for the 2025 Google Code Golf Championship."""

import copy
import importlib.util
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np


code_golf_dir = "/kaggle/input/google-code-golf-2025/"
libraries = ["collections", "itertools", "math", "operator", "re", "string",
             "struct"]
colors = [
    (0, 0, 0),
    (30, 147, 255),
    (250, 61, 49),
    (78, 204, 48),
    (255, 221, 0),
    (153, 153, 153),
    (229, 59, 163),
    (255, 133, 28),
    (136, 216, 241),
    (147, 17, 49),
]
task_zero = {
    "train": [{
        "input": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
        "output": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 5, 0, 0, 0, 0, 0, 0, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
    }],
    "test": [{
        "input": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 5, 5, 5],
            [5, 5, 4, 5, 5, 5, 4, 5, 5, 5],
            [5, 5, 4, 5, 5, 5, 4, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
        "output": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 0, 5],
            [5, 5, 5, 0, 0, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 5, 5, 5],
            [5, 5, 4, 0, 0, 0, 4, 0, 5, 5],
            [5, 5, 4, 0, 5, 5, 4, 0, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 0, 5, 5],
            [5, 5, 5, 0, 0, 0, 0, 0, 5, 5],
        ],
    }],
    "arc-gen": [{
        "input": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 2, 2, 2, 2, 2, 2, 5, 5],
            [5, 5, 2, 5, 5, 5, 5, 2, 5, 5],
            [5, 5, 2, 5, 5, 5, 5, 2, 5, 5],
            [5, 5, 2, 5, 5, 5, 5, 2, 5, 5],
            [5, 5, 2, 5, 5, 5, 5, 2, 5, 5],
            [5, 5, 2, 2, 2, 2, 2, 2, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
        "output": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 2, 2, 2, 2, 2, 2, 5, 5],
            [5, 5, 2, 0, 0, 0, 0, 2, 0, 5],
            [5, 5, 2, 0, 5, 5, 5, 2, 0, 5],
            [5, 5, 2, 0, 5, 5, 5, 2, 0, 5],
            [5, 5, 2, 0, 5, 5, 5, 2, 0, 5],
            [5, 5, 2, 2, 2, 2, 2, 2, 0, 5],
            [5, 5, 5, 0, 0, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
    }],
}


def load_examples(task_num):
  """Loads relevant data from ARC-AGI and ARC-GEN."""
  if not task_num:
    return task_zero
  with open(code_golf_dir + f"task{task_num:03d}.json") as f:
    examples = json.load(f)
  return examples


def show_legend():
  image = [[(255, 255, 255) for _ in range(21)] for _ in range(3)]
  for idx, color in enumerate(colors):
    image[1][2 * idx + 1] = color
  fig = plt.figure(figsize=(10, 5))
  ax = fig.add_axes([0, 0, 1, 1])
  ax.imshow(np.array(image))
  for idx, _ in enumerate(colors):
    color = "white" if idx in [0, 9] else "black"
    ax.text(2 * idx + 0.9, 1.1, str(idx), color=color)
  ax.set_xticks([])
  ax.set_yticks([])


def show_examples(examples, bgcolor=(255, 255, 255)):
  # Determine the dimensions of the image to be rendered.
  width, height, offset = 0, 0, 1
  for example in examples:
    grid, output = example["input"], example["output"]
    width += len(grid[0]) + 1 + len(output[0]) + 4
    height = max(height, max(len(grid), len(output)) + 4)
  # Determine the contents of the image.
  image = [[bgcolor for _ in range(width)] for _ in range(height)]
  for example in examples:
    grid, output = example["input"], example["output"]
    grid_width, output_width = len(grid[0]), len(output[0])
    for r, row in enumerate(grid):
      for c, cell in enumerate(row):
        image[r + 2][offset + c + 1] = colors[cell]
    offset += grid_width + 1
    for r, row in enumerate(output):
      for c, cell in enumerate(row):
        image[r + 2][offset + c + 1] = colors[cell]
    offset += output_width + 4
  # Draw the image.
  fig = plt.figure(figsize=(10, 5))
  ax = fig.add_axes([0, 0, 1, 1])
  ax.imshow(np.array(image))
  # Draw the horizontal and vertical lines.
  offset = 1
  for example in examples:
    grid, output = example["input"], example["output"]
    grid_width, grid_height = len(grid[0]), len(grid)
    output_width, output_height = len(output[0]), len(output)
    ax.hlines([r + 1.5 for r in range(grid_height+1)],
              xmin=offset+0.5, xmax=offset+grid_width+0.5, color="black")
    ax.vlines([offset + c + 0.5 for c in range(grid_width+1)],
              ymin=1.5, ymax=grid_height+1.5, color="black")
    offset += grid_width + 1
    ax.hlines([r + 1.5 for r in range(output_height+1)],
              xmin=offset+0.5, xmax=offset+output_width+0.5, color="black")
    ax.vlines([offset + c + 0.5 for c in range(output_width+1)],
              ymin=1.5, ymax=output_height+1.5, color="black")
    offset += output_width + 2
    ax.vlines([offset+0.5], ymin=-0.5, ymax=height-0.5, color="black")
    offset += 2
  ax.set_xticks([])
  ax.set_yticks([])


def verify_program(task_num, examples):
  task_name, task_path = "task_with_imports", "/kaggle/working/task.py"
  spec = importlib.util.spec_from_file_location(task_name, task_path)
  if spec is None:
    print("Error: Unable to import task.py.")
    return
  module = sys.modules[task_name] = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  if not hasattr(module, "p"):
    print("Error: Unable to locate function p() in task.py.")
    return
  program = getattr(module, "p")
  if not callable(program):
    print("Error: Function p() in task.py is not callable.")
    return
  print()
  def verify(example_subset):
    right, wrong, expected = 0, 0, None
    for example in example_subset:
      example_copy = copy.deepcopy(example)
      try:
        if program(example_copy["input"]) == example_copy["output"]:
          right += 1
        else:
          expected = copy.deepcopy(example)
          wrong += 1
      except:
        wrong += 1
    return right, wrong, expected
  arc_agi_right, arc_agi_wrong, arc_agi_expected = verify(examples["train"] + examples["test"])
  arc_gen_right, arc_gen_wrong, arc_gen_expected = verify(examples["arc-gen"])
  print(f"Results on ARC-AGI examples: {arc_agi_right} pass, {arc_agi_wrong} fail")
  print(f"Results on ARC-GEN examples: {arc_gen_right} pass, {arc_gen_wrong} fail")
  print()
  if arc_agi_wrong + arc_gen_wrong == 0:
    task_length = os.path.getsize(task_path)
    print("Your code IS READY for submission!")
    print("Its length appears to be " + str(task_length) + " bytes.")
    print("Next steps:")
    print(" * Copy it into a file named task{:03d}.py on your local machine.".format(task_num))
    print(" * Create a zip file containing that program along with all others.")
    print(" * Submit that zip file to the Kaggle competition so that it can be officially scored.")
  else:
    print("Your code IS NOT ready for submission.")
    expected = arc_agi_expected if arc_agi_expected else arc_gen_expected
    if not expected: return
    actual = {}
    actual["input"] = expected["input"]
    actual["output"] = program(copy.deepcopy(expected["input"]))
    print("The expected result is shown in green; your actual result is shown in red.")
    show_examples([expected], bgcolor=(200, 255, 200))
    show_examples([actual], bgcolor=(255, 200, 200))
