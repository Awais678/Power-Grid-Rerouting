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
- `mainCode.cpp` - Main Code in cpp
- `data.txt` - Input graph data (sample provided)
- `README.md` - Project documentation

---

## 📝 Sample `data.txt`
```
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
```


The first line 13 15 means:
```
13: Total number of nodes (or grids) in the power grid (numbered from 0 to 12).
```
```
15: This is likely outdated or misleading — there are actually 22 edges in the file. The program doesn't strictly rely on this number; it just reads all edges from the subsequent lines.
```

Each subsequent line (e.g., 0 1 15) represents an undirected edge:
```
0: Source grid (node)
```
```
1: Destination grid (node)
```
```
15: Weight (e.g., cost, distance, power loss, or any metric relevant to grid connection)
```
So, 0 1 15 means:
```
Grid 0 is connected to Grid 1 with a weight of 15.
```


## ✅ STEP-BY-STEP WORKING

1. GUI Initialization (Tkinter)

When you run the script:<br>

•	A Tkinter GUI window opens.

•	It displays:

      •   Buttons: Load Graph, Display Power Grid, Mark grid Faulty, Reroute Around Faulty Grid, Dijkstra's Rerouting, Exit.
      
	  •   Entry boxes for:
   
           •   Source Grid
	   
	       •   Destination Grid
	
	       •   Faulty Grids (comma-separated)

2. Loading the Graph

When you click "Load Graph from data.txt":
```
What Happens Internally:

i.	data.txt is opened and read.

ii.	First line 13 15 is read:

	•	Total nodes = 13 (0 to 12)

iii.	Each remaining line is treated as an edge:

	•	Example: 0 1 15 → Connects node 0 and node 1 with weight 15

iv.	A graph is drawn using matplotlib:

	•	Nodes are drawn as circles with labels

	•	Edges show weights
```

![Image](https://github.com/user-attachments/assets/1d2ed770-dec9-4917-87f7-ad10f9b05a6f)

3. Output Results

The application shows the following nodes marked as faulty:
```
•       Grid 2

•	Grid 4

•	Grid 7

These are represented as red nodes on the graph.
```

![Image](https://github.com/user-attachments/assets/2f8801f7-5754-4e78-b0ba-b55a3da98205)

The application has calculated a shortest path that avoids all faulty grid points
```
•	The path goes from grid point 3 → 1 → 9 → 12

•	This path is highlighted in green on the graph visualization

•	The total cost (sum of weights) for this path is 30
```

![Image](https://github.com/user-attachments/assets/ed2f6203-4874-4aaf-95f8-6d776179ffb1)

## ✅ Conclusion
```
This project helps you see how a power grid can handle faults in real time. When some parts (grids) fail, it finds a new, best
path to keep the power flowing using smart algorithms. The red circles show broken grids, and the app shows a safe, working
route around them. It’s easy to use and great for learning how smart power systems work.
```
