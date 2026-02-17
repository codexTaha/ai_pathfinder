# AI Pathfinder – Uninformed Search Visualizer

This project is a simple grid-based **AI Pathfinder** implemented in Python using Pygame. It visualizes how different **uninformed search algorithms** explore a grid from a Start node to a Target node while avoiding walls. [web:15][web:24]

Implemented algorithms:

- Breadth-First Search (BFS) [web:10][web:97]
- Depth-First Search (DFS) [web:10][web:97]
- Uniform-Cost Search (UCS) [web:10][web:102]
- Depth-Limited Search (DLS) [web:11][web:128]
- Iterative Deepening DFS (IDDFS) [web:106][web:130]
- Bidirectional Search (Bidirectional BFS) [web:10][web:97]

The GUI shows frontier / explored nodes and the final path step-by-step so you can see how each algorithm behaves. [web:15][web:24]

---

## Requirements

- Python 3.10+ (tested with 3.14)
- Pygame 2.x [web:69]

On Fedora / Linux you may need SDL2 development libraries for Pygame to compile, such as `SDL2-devel`, `SDL2_image-devel`, `SDL2_mixer-devel`, `SDL2_ttf-devel`, and `freetype-devel`. [web:60][web:64]

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
