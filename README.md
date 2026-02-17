# AI Pathfinder – Uninformed Search Visualizer

This project is a simple grid-based **AI Pathfinder** implemented in Python using Pygame. It visualizes how different **uninformed search algorithms** explore a grid from a Start node to a Target node while avoiding walls. 

Implemented algorithms:

- Breadth-First Search (BFS) 
- Depth-First Search (DFS) 
- Uniform-Cost Search (UCS) 
- Depth-Limited Search (DLS) 
- Iterative Deepening DFS (IDDFS) 
- Bidirectional Search (Bidirectional BFS) 

The GUI shows frontier / explored nodes and the final path step-by-step so you can see how each algorithm behaves. 

---

## Requirements

- Python 3.10+ (tested with 3.14)
- Pygame 2

On Fedora / Linux you may need SDL2 development libraries for Pygame to compile, such as `SDL2-devel`, `SDL2_image-devel`, `SDL2_mixer-devel`, `SDL2_ttf-devel`, and `freetype-devel`. 

---

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/<your-username>/ai_pathfinder.git
cd ai_pathfinder

python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
Install dependencies:

bash
pip install pygame
(If pip install pygame fails on Fedora, install the SDL2 and freetype development packages with dnf and retry.)

How to Run
From the project root, with the virtual environment activated:

bash
python main.py
This opens the main window which is the program.
