import heapq
import time
import networkx as nx
import matplotlib.pyplot as plt

class RoadNetwork:
    def __init__(self):
        self.graph = {}
        self.disabled_edges = set()

    def add_edge(self, u, v, weight=1.0):
        if u not in self.graph: self.graph[u] = {}
        if v not in self.graph: self.graph[v] = {}
        self.graph[u][v] = weight
        self.graph[v][u] = weight

    def load_from_mtx(self, filename):
        print(f"[*] Loading dataset: {filename}...")
        start_time = time.time()
        try:
            with open(filename, 'r') as f:
                count = 0
                for line in f:
                    if line.startswith('%'): continue
                    parts = list(map(int, line.split()))
                    if len(parts) >= 2:
                        self.add_edge(parts[0], parts[1])
                        count += 1
                        # İlk 50,000 əlaqəni yükləyirik ki, həm sürətli olsun, həm də vizual donmasın
                        if count > 50000: break 
            print(f"[+] Dataset loaded in {time.time() - start_time:.2f} seconds.")
        except FileNotFoundError:
            print("[-] Error: Dataset file not found! Make sure roadNet-PA.mtx is in the same folder.")

    def get_shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None, float('inf')

        queue = [(0, start, [])]
        visited = {start: 0}

        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node == end:
                return path + [node], cost

            for neighbor, weight in self.graph.get(node, {}).items():
                if (node, neighbor) in self.disabled_edges or (neighbor, node) in self.disabled_edges:
                    continue
                
                new_cost = cost + weight
                if neighbor not in visited or new_cost < visited[neighbor]:
                    visited[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor, path + [node]))
        return None, float('inf')

    def draw_graph(self, path=None):
        """Həqiqi qraf vizualizasiyası - Təkmilləşdirilmiş Versiya"""
        print("[*] Vizual xəritə hazırlanır, bir neçə saniyə gözləyin...")
        G = nx.Graph()
        
        # Vizualın donmaması üçün yalnız yolun və ətrafındakı vacib nöqtələri göstəririk
        if path:
            nodes_to_show = set(path)
            # Yolun ətrafındakı bəzi qonşuları da əlavə edək ki, xəritə real görünsün
            for node in path:
                if node in self.graph:
                    neighbors = list(self.graph[node].keys())[:3] # Hər nöqtədən max 3 qonşu
                    nodes_to_show.update(neighbors)
            
            for u in nodes_to_show:
                if u in self.graph:
                    for v in self.graph[u]:
                        if v in nodes_to_show:
                            if (u, v) not in self.disabled_edges:
                                G.add_edge(u, v)
        
        plt.figure(figsize=(10, 7))
        plt.clf() # Köhnə çertyojları təmizlə
        
        # Nöqtələrin ekrandakı düzülüş alqoritmi
        pos = nx.spring_layout(G, k=0.3, iterations=30)
        
        # 1. Bütün əlaqələri çək (Boz rəngdə)
        nx.draw(G, pos, node_size=40, node_color='lightgray', edge_color='silver', width=1, with_labels=True, font_size=7)
        
        # 2. Tapılan yolu çək (Qırmızı və qalın)
        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', node_size=100)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=4)
            
        plt.title("Pennsylvania Road Network - Shortest Path Result")
        print("[+] Xəritə pəncərəsi açılır...")
        plt.show()

def main():
    rn = RoadNetwork()
    rn.load_from_mtx("roadNet-PA.mtx")

    while True:
        print("\n--- Pennsylvania Navigation System ---")
        print("1. Find Shortest Path & Show Map")
        print("2. Block a Road (Dynamic Update)")
        print("3. Exit")
        choice = input("Select: ")

        if choice == '1':
            try:
                start = int(input("Enter start node: "))
                end = int(input("Enter destination node: "))
                path, cost = rn.get_shortest_path(start, end)
                if path:
                    print(f"\n[+] Path found! Total distance: {cost}")
                    print(f"Path: {' -> '.join(map(str, path))}")
                    rn.draw_graph(path)
                else:
                    print("[-] No path found between these nodes.")
            except ValueError:
                print("Please enter valid numbers.")

        elif choice == '2':
            try:
                u = int(input("Enter node 1 to block: "))
                v = int(input("Enter node 2 to block: "))
                rn.disabled_edges.add((u, v))
                print(f"[!] Road between {u} and {v} is now BLOCKED.")
            except ValueError:
                print("Invalid input.")

        elif choice == '3':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
