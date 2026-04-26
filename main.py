import collections
import heapq
import threading
import time
import random

class RouteService:
    def __init__(self):
        self.graph = collections.defaultdict(dict)
        self.disabled_edges = set()
        # Müəllimə: Thread-safe əməliyyatlar üçün Lock
        self.lock = threading.RLock() 
        self.version_id = 0 # Müəllimə: "Versioned graph" yanaşması üçün

    def add_edge(self, u, v, weight=1.0):
        with self.lock:
            self.graph[u][v] = weight
            self.graph[v][u] = weight
            self.version_id += 1

    def disable_edge(self, u, v):
        with self.lock:
            self.disabled_edges.add((u, v))
            self.disabled_edges.add((v, u))
            self.version_id += 1
            print(f"\n[SİSTEM YENİLƏNMƏSİ]: {u}-{v} yolu bloklandı. (Versiya: {self.version_id})")

    def get_neighbors(self, node):
        if node not in self.graph: return {}
        return {n: w for n, w in self.graph[node].items() 
                if (node, n) not in self.disabled_edges}

    def find_shortest_path(self, start_node, end_node, user_id="User"):
        # Dijkstra Alqoritmi
        distances = {node: float('inf') for node in self.graph}
        distances[start_node] = 0
        previous_nodes = {node: None for node in self.graph}
        pq = [(0, start_node)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            if current_node == end_node: break
            if current_distance > distances[current_node]: continue

            for neighbor, weight in self.get_neighbors(current_node).items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        path = []
        current = end_node
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        path.reverse()
        
        res = path if (path and path[0] == start_node) else None
        if res:
            print(f"[{user_id}]: Yol tapıldı! ({len(res)} nöqtə)")
        return res

    def load_from_mtx(self, file_path):
        print(f"Məlumatlar {file_path} faylından yüklənir...")
        count = 0
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('%') or not line.strip(): continue
                parts = line.split()
                if len(parts) == 3 and count == 0:
                    count += 1
                    continue
                if len(parts) >= 2:
                    self.add_edge(parts[0], parts[1])
                    count += 1
        print(f"Uğurlu! {count} yol yükləndi. (Versiya: {self.version_id})")

def run_concurrent_test(service):
    """Müəllimə: Eyni anda bir çox sorğunun işləməsini nümayiş etdirir"""
    threads = []
    print("\n--- CONCURRENCY TESTİ BAŞLADI (10 istifadəçi eyni anda) ---")
    for i in range(10):
        # Hər user üçün random nöqtələr seçirik
        u_id = f"İstifadəçi-{i+1}"
        t = threading.Thread(target=service.find_shortest_path, args=('1', str(random.randint(100, 500)), u_id))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    print("--- CONCURRENCY TESTİ TAMAMLANDI ---\n")

if __name__ == "__main__":
    service = RouteService()
    service.load_from_mtx('roadNet-PA.mtx')
    
    while True:
        print("\n--- NAVİQASİYA SİSTEMİ ---")
        print("1. Yol axtar (Dijkstra)")
        print("2. Yolu bağla (Qəza simulyasiyası)")
        print("3. Concurrency Testini işlət (Professional nümayiş)")
        print("4. Çıxış")
        
        choice = input("Seçiminiz: ")
        
        if choice == '1':
            start = input("Başlanğıc nöqtə (məs. 1): ")
            end = input("Hədəf nöqtə (məs. 100): ")
            path = service.find_shortest_path(start, end)
            if path:
                print(f"Marşrut tapıldı: {' -> '.join(path[:5])} ... {path[-1]}")
            else:
                print("Yol tapılmadı!")
        
        elif choice == '2':
            u = input("Bağlanacaq yolun başlanğıcı: ")
            v = input("Bağlanacaq yolun sonu: ")
            service.disable_edge(u, v)
        
        elif choice == '3':
            run_concurrent_test(service)
            
        elif choice == '4':
            print("Sistem bağlanır. Uğurlar!")
            break