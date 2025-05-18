import tkinter as tk
from tkinter import messagebox, simpledialog
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj = [[] for _ in range(vertices)]

    def add_edge(self, src, dest, weight):
        self.adj[src].append((dest, weight))
        self.adj[dest].append((src, weight))

    def display_graph(self):
        result = ""
        for v in range(self.V):
            edges = ", ".join(f"{nbr}(w={w})" for nbr, w in self.adj[v])
            result += f"Grid {v}: {edges}\n"
        return result

    def dijkstra(self, start, end, faulty_nodes):
        dist = [float('inf')] * self.V
        parent = [-1] * self.V
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if curr_dist > dist[u]:
                continue
            if u == end:
                break
            for v, w in self.adj[u]:
                if v in faulty_nodes:
                    continue
                new_dist = curr_dist + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (new_dist, v))

        if dist[end] == float('inf'):
            return None, None  # No path

        path = []
        cur = end
        while cur != -1:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path, dist[end]

    def reroute_around_fault(self, faulty_node):
        if faulty_node < 0 or faulty_node >= self.V:
            return "Invalid node"
        neighbors = [f"{nbr}(weight={w})" for nbr, w in self.adj[faulty_node]]
        if not neighbors:
            return f"No neighbors for node {faulty_node}"
        return f"Neighbors of faulty node {faulty_node}: " + ", ".join(neighbors)


class PowerGridApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Power Grid Rerouting")
        self.geometry("1200x700")
        self.configure(bg="#f0f0f0")

        self.graph = None
        self.faulty_nodes = set()

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.text_area = tk.Text(left_frame, height=15, width=40, font=("Courier", 12), bg="#ffffff")
        self.text_area.pack(pady=5)

        button_style = {
            "font": ("Arial", 12),
            "bg": "#4CAF50",
            "fg": "#ffffff",
            "relief": "raised",
            "activebackground": "#45a049",
            "activeforeground": "#ffffff",
            "padx": 10,
            "pady": 5,
        }

        btn_frame = tk.Frame(left_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Load Graph from data.txt", command=self.load_graph, **button_style).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Display Power Grid Text", command=self.display_graph, **button_style).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Mark Faulty Grid", command=self.mark_faulty, **button_style).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Reroute Around Faulty Grid", command=self.reroute_around_faulty, **button_style).grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Dijkstra Rerouting", command=self.dijkstra_rerouting, **button_style).grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(btn_frame, text="Exit", command=self.quit, **button_style).grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_graph(self):
        try:
            with open("data.txt") as f:
                lines = f.readlines()
            num_vertices, num_edges = map(int, lines[0].split())
            self.graph = Graph(num_vertices)
            self.faulty_nodes = set()
            for line in lines[1:]:
                u, v, w = map(int, line.split())
                self.graph.add_edge(u, v, w)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, f"Loaded graph of different grids with {num_vertices} grids and {num_edges} connections between them.\n")
            self.draw_graph()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph: {e}")

    def display_graph(self):
        if not self.graph:
            messagebox.showwarning("Warning", "Load the graph first!")
            return
        graph_text = self.graph.display_graph()
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, graph_text)

    def mark_faulty(self):
        if not self.graph:
            messagebox.showwarning("Warning", "Load the graph first!")
            return
        node = simpledialog.askinteger("Input", "Enter grid to mark as faulty:")
        if node is None:
            return
        if node < 0 or node >= self.graph.V:
            messagebox.showerror("Error", "Invalid grid number!")
            return
        self.faulty_nodes.add(node)
        self.text_area.insert(tk.END, f"Grid {node} marked as faulty.\n")
        self.draw_graph()

    def reroute_around_faulty(self):
        if not self.graph:
            messagebox.showwarning("Warning", "Load the graph first!")
            return
        node = simpledialog.askinteger("Input", "Enter faulty grid to reroute around:")
        if node is None:
            return
        reroute_info = self.graph.reroute_around_fault(node)
        self.text_area.insert(tk.END, reroute_info + "\n")

    def dijkstra_rerouting(self):
        if not self.graph:
            messagebox.showwarning("Warning", "Load the graph first!")
            return
        start = simpledialog.askinteger("Input", "Enter start grid:")
        if start is None:
            return
        end = simpledialog.askinteger("Input", "Enter end grid:")
        if end is None:
            return
        if start in self.faulty_nodes or end in self.faulty_nodes:
            messagebox.showwarning("Warning", "Start or end grid is faulty!")
            return
        path, cost = self.graph.dijkstra(start, end, self.faulty_nodes)
        if path is None:
            self.text_area.insert(tk.END, f"No path found from {start} to {end} avoiding faulty grids.\n")
        else:
            path_str = " -> ".join(map(str, path))
            self.text_area.insert(tk.END, f"Shortest path: {path_str}\n")
            self.text_area.insert(tk.END, f"Total cost: {cost}\n")
            self.draw_graph(path)

    def draw_graph(self, highlight_path=None):
        if not self.graph:
            return

        G = nx.Graph()
        for u in range(self.graph.V):
            for v, w in self.graph.adj[u]:
                if u < v:
                    G.add_edge(u, v, weight=w)

        self.ax.clear()
        pos = nx.spring_layout(G, seed=42)

        node_colors = ['red' if n in self.faulty_nodes else 'lightblue' for n in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=self.ax, node_size=500)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=10)
        nx.draw_networkx_edges(G, pos, ax=self.ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, font_size=8)

        if highlight_path and len(highlight_path) > 1:
            path_edges = list(zip(highlight_path, highlight_path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green', width=3, ax=self.ax)

        self.canvas.draw()


if __name__ == "__main__":
    app = PowerGridApp()
    app.mainloop()
