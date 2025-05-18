# ⚡ Power Grid Rerouting GUI

A Python-based Tkinter GUI application for simulating and visualizing power grid rerouting using Dijkstra's algorithm. It enables dynamic fault handling and real-time graph visualization with rerouting functionality.

---

## 🚀 Features

- Load power grid from a file (`data.txt`)
- Display the network of grids and connections
- Mark faulty grids (nodes)
- Suggest rerouting paths around faulty grids
- Compute shortest path using Dijkstra’s algorithm (avoids faulty nodes)
- Real-time graphical visualization using NetworkX and Matplotlib

---

## 🧠 Algorithms Used

- **Dijkstra’s Algorithm**: For shortest path calculation avoiding faulty nodes
- **Tkinter GUI**: For user interaction
- **NetworkX + Matplotlib**: For graph visualization

---

## 🗂️ File Structure

- `power_grid_rerouting.py` - Main GUI application
- - `mainCode.cpp - Main Code in cpp
- `data.txt` - Input graph data (sample provided)
- `README.md` - Project documentation

---

## 📝 Sample `data.txt`

13 15
0 1 15
0 2 20
1 3 25
2 3 30
2 4 22
3 5 35
4 5 18
5 6 40
6 7 28
6 8 33
7 9 27
8 10 38
9 11 24
10 12 45
11 12 41
4 8 6
7 12 12
12 9 2
3 7 23
3 6 9
1 9 3


The first line 13 15 means:
13: Total number of nodes (or grids) in the power grid (numbered from 0 to 12).
15: This is likely outdated or misleading — there are actually 22 edges in the file. The program doesn't strictly rely on this number; it just reads all edges from the subsequent lines.

Each subsequent line (e.g., 0 1 15) represents an undirected edge:
0: Source grid (node)
1: Destination grid (node)
15: Weight (e.g., cost, distance, power loss, or any metric relevant to grid connection)

So, 0 1 15 means:
Grid 0 is connected to Grid 1 with a weight of 15.


✅ STEP-BY-STEP WORKING

1. GUI Initialization (Tkinter)
When you run the script:
•	A Tkinter GUI window opens.
•	It displays:
      •   Buttons: Load Graph, Display Power Grid, Mark grid Faulty, Reroute Around Faulty Grid, Dijkstra's Rerouting, Exit
	  •   Entry boxes for:
           •   Source Grid
	       •   Destination Grid
	       •   Faulty Grids (comma-separated)



