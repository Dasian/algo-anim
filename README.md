# Algo Anim
Animate common algorithms on randomly generated data structures using [manim](https://github.com/ManimCommunity/manim)

## Features
- Animate BFS and DFS on randomly generated trees

## Installation
Follow the [manim installation instructions](https://docs.manim.community/en/stable/installation.html)
for your operating system. It's useful to install LaTeX as well.

### Python Virtual Environment (optional)
Isolates packages from the rest of your system. The environment needs to be activated before you can run the scripts.
> First command creates a venv, second command activates it.
#### Windows
```cmd
python -m venv .algo-anim
call .algo-anime/scripts/activate.bat
```
#### Linux
```bash
python3 -m venv .algo-anim  
source .algo-anime/bin/activate
```
### Install Python Libraries
```bash
pip3 install -r requirements.txt
```

## Usage
> Has only been tested on Linux
```
python3 algo-anim.py --help

usage: algo-anim.py [-h] [-a {BFS,DFS,bfs,dfs}] [--size SIZE] [--inf | --no-inf | --infinite | --no-infinite]
                    [--num-animations NUM_ANIMATIONS] [-r | --random | --no-random] [-ds {graph}] [-rt RUNTIME]

Generate an algorithm animation with manim

options:
  -h, --help            show this help message and exit
  -a {BFS,DFS,bfs,dfs}, --algo {BFS,DFS,bfs,dfs}
                        Algorithm to display
  --size SIZE           Size of the generated data structure
  --inf, --no-inf, --infinite, --no-infinite
                        Generate animations indefinitely
  --num-animations NUM_ANIMATIONS
                        Number of animations to generate
  -r, --random, --no-random
                        Generate a random animation
  -ds {graph}, --data-structure {graph}
                        Data structure to generate animations on
  -rt RUNTIME, --runtime RUNTIME
                        Maximum runtime of the program in seconds
```

## TODO
- [X] bring driver to a working state
- [X] command line flags
- [X] implement DFS
- [ ] create sorting animations
- [ ] update/clean up code and design
- [ ] work on windows
