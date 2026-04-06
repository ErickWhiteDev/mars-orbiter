# Mars Nano-Satellite Mission Design

This repository contains the code for the ASEN 5010 Spring 2026 semester project.

Each individual task is located in `tasks/`, with outputs going to the corresponding subdirectory in `output/` when run.
The tasks can be run from the root folder by executing `python3 -m tasks.task_NUMBER`.

Each task has an associated test for each output in `test/task_NUMBER`; these can all be run by executing `python3 -m unittest discover -s test`.

The `utils/` directory contains class and method definitions for all functionality in this repository and is meant to be highly modular for extension to other missions.