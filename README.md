# Dynamic-Road-Navigation-System
Shortest path navigation system for Pennsylvania road network using Dijkstra's algorithm.
# Dynamic Road Navigation System (Pennsylvania)

## Project Overview
This project implements a shortest-path navigation system using **Dijkstra's Algorithm** with **Min-Priority Queue** optimization. It processes the **roadNet-PA** dataset, which contains over 1 million nodes and 3 million edges.

## Key Features
- **Efficient Search:** O(E log V) time complexity.
- **Dynamic Updates:** Ability to block roads and find alternative routes in real-time.
- **Thread-Safety:** Implemented using `threading.RLock` to handle concurrent user requests.

## How to Run
1. Download the dataset from [SNAP](https://snap.stanford.edu/data/roadNet-PA.html).
2. Place the `roadNet-PA.mtx` file in the same directory as `main.py`.
3. Run: `python main.py`
