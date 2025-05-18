#include <iostream>
#include <fstream>
#include <vector>
#include <list>
#include <queue>
#include <limits>
#include <stdexcept>
#include<algorithm>

class Graph {
private:
    int numVertices;
    // adjacency list now stores pairs (neighbor, weight)
    std::vector<std::list<std::pair<int, int>>> adjLists;

public:
    Graph(int vertices);
    void addEdge(int src, int dest, int weight);
    void printGraph() const;
    const std::list<std::pair<int, int>> &getAdjList(int vertex) const;
    void BFS(int startVertex, std::vector<bool> &visited) const;
    std::vector<int> dijkstra(int start, int end) const;  // Returns shortest path from start to end
};

Graph::Graph(int vertices) {
    if (vertices <= 0 || vertices > 1000) {
        throw std::invalid_argument("Invalid number of vertices");
    }
    numVertices = vertices;
    adjLists.resize(numVertices);
}

void Graph::addEdge(int src, int dest, int weight) {
    if (src >= 0 && src < numVertices && dest >= 0 && dest < numVertices) {
        adjLists[src].push_back({dest, weight});
        adjLists[dest].push_back({src, weight}); // Undirected graph
    }
}

const std::list<std::pair<int, int>> &Graph::getAdjList(int vertex) const {
    if (vertex >= 0 && vertex < numVertices)
        return adjLists[vertex];
    else
        throw std::out_of_range("Vertex out of range in getAdjList");
}

void Graph::printGraph() const {
    for (int v = 0; v < numVertices; ++v) {
        std::cout << "\nVertex " << v << ":";
        for (auto &[adj, weight] : adjLists[v])
            std::cout << " -> " << adj << "(weight " << weight << ")";
    }
}

void Graph::BFS(int startVertex, std::vector<bool> &visited) const {
    std::list<int> queue;
    visited[startVertex] = true;
    queue.push_back(startVertex);

    while (!queue.empty()) {
        int currVertex = queue.front();
        queue.pop_front();

        for (auto &[adjVertex, weight] : adjLists[currVertex]) {
            if (!visited[adjVertex]) {
                visited[adjVertex] = true;
                queue.push_back(adjVertex);
            }
        }
    }
}

std::vector<int> Graph::dijkstra(int start, int end) const {
    std::vector<int> dist(numVertices, std::numeric_limits<int>::max());
    std::vector<int> parent(numVertices, -1);
    dist[start] = 0;

    // Min-heap priority queue (distance, vertex)
    using pii = std::pair<int, int>;
    std::priority_queue<pii, std::vector<pii>, std::greater<pii>> pq;
    pq.push({0, start});

    while (!pq.empty()) {
        int currDist = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (currDist > dist[u])
            continue;

        if (u == end)
            break;

        for (auto &[v, weight] : adjLists[u]) {
            int newDist = dist[u] + weight;
            if (newDist < dist[v]) {
                dist[v] = newDist;
                parent[v] = u;
                pq.push({newDist, v});
            }
        }
    }

    // Reconstruct path
    std::vector<int> path;
    if (dist[end] == std::numeric_limits<int>::max()) {
        // No path found
        return path;
    }
    for (int v = end; v != -1; v = parent[v])
        path.push_back(v);

    std::reverse(path.begin(), path.end());
    return path;
}

class FaultDetector {
private:
    Graph *graph;
    int numVertices;
    std::vector<bool> isFaulty;

public:
    FaultDetector(Graph *g, int vertices);
    void markFaultyNode(int node);
    void detectDisconnectedComponents() const;
    void suggestRerouteAroundFault(int faultyNode) const;
    void suggestRerouteShortestPath(int startNode, int endNode) const;
};

FaultDetector::FaultDetector(Graph *g, int vertices) : graph(g), numVertices(vertices), isFaulty(vertices, false) {}

void FaultDetector::markFaultyNode(int node) {
    if (node >= 0 && node < numVertices)
        isFaulty[node] = true;
    else
        std::cout << "Invalid node number.\n";
}

void FaultDetector::detectDisconnectedComponents() const {
    std::vector<bool> visited(numVertices, false);

    for (int i = 0; i < numVertices; i++) {
        if (!visited[i] && !isFaulty[i]) {
            std::cout << "\nComponent starting at node " << i << ": ";
            graph->BFS(i, visited);
            // Print all visited nodes in this component (optional)
            for (int j = 0; j < numVertices; ++j) {
                if (visited[j]) {
                    std::cout << j << " ";
                }
            }
        }
    }
    std::cout << std::endl;
}

void FaultDetector::suggestRerouteAroundFault(int faultyNode) const {
    std::cout << "\nSuggesting rerouting around faulty node " << faultyNode << "...\n";
    try {
        const auto &adjList = graph->getAdjList(faultyNode);

        for (auto &[neighbor, weight] : adjList) {
            if (!isFaulty[neighbor])
                std::cout << "Use path from node " << neighbor << " (edge weight " << weight << ")\n";
        }
    } catch (const std::out_of_range &e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
}

void FaultDetector::suggestRerouteShortestPath(int startNode, int endNode) const {
    std::cout << "\nSuggesting shortest path from " << startNode << " to " << endNode << " avoiding faulty nodes...\n";

    std::vector<int> path = graph->dijkstra(startNode, endNode);

    if (path.empty()) {
        std::cout << "No path found from " << startNode << " to " << endNode << ".\n";
    } else {
        std::cout << "Shortest path: ";
        for (size_t i = 0; i < path.size(); ++i) {
            std::cout << path[i];
            if (i != path.size() - 1)
                std::cout << " -> ";
        }
        std::cout << std::endl;
    }
}

int main() {
    std::ifstream fin("data.txt");
    if (!fin) {
        std::cerr << "Error opening data.txt\n";
        return 1;
    }

    int numVertices, edges;
    if (!(fin >> numVertices >> edges)) {
        std::cerr << "Error reading number of vertices or edges.\n";
        return 1;
    }

    if (numVertices <= 0 || numVertices > 1000) {
        std::cerr << "Invalid number of vertices: " << numVertices << "\n";
        return 1;
    }

    Graph graph(numVertices);
    FaultDetector detector(&graph, numVertices);

    for (int i = 0; i < edges; i++) {
        int u, v, w;
        if (!(fin >> u >> v >> w)) {
            std::cerr << "Error reading edge " << i << ".\n";
            continue;
        }
        graph.addEdge(u, v, w);
    }

    int choice;
    do {
        std::cout << "\n\n--- Power Grid Menu ---\n";
        std::cout << "1. Display Power Grid\n";
        std::cout << "2. Mark Grid as Faulty\n";
        std::cout << "3. Suggest Rerouting Around Faulty Grid\n";
        std::cout << "4. Suggest Rerouting (Dijkstra's Shortest Path)\n";
        std::cout << "5. Exit\n";
        std::cout << "Enter your choice: ";
        std::cin >> choice;

        switch (choice) {
            case 1:
                graph.printGraph();
                break;
            case 2: {
                int node;
                std::cout << "Enter node to mark as faulty: ";
                std::cin >> node;
                detector.markFaultyNode(node);
                break;
            }
            case 3: {
                int node;
                std::cout << "Enter faulty node to reroute around: ";
                std::cin >> node;
                detector.suggestRerouteAroundFault(node);
                break;
            }
            case 4: {
                int startNode, endNode;
                std::cout << "Enter start node: ";
                std::cin >> startNode;
                std::cout << "Enter end node: ";
                std::cin >> endNode;
                detector.suggestRerouteShortestPath(startNode, endNode);
                break;
            }
            case 5:
                std::cout << "Exiting...\n";
                break;
            default:
                std::cout << "Invalid choice.\n";
        }
    } while (choice != 5);

    return 0;
}
