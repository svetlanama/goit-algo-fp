"""
Завдання 3. Дерева, алгоритм Дейкстри

Розробіть алгоритм Дейкстри для знаходження найкоротших шляхів у зваженому графі, 
використовуючи бінарну купу. Завдання включає створення графа, використання піраміди 
для оптимізації вибору вершин та обчислення найкоротших шляхів від початкової вершини 
до всіх інших.
"""

import heapq
import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
import math


class BinaryHeap:
    """Реалізація бінарної купи (min-heap) для алгоритму Дейкстри"""
    
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def push(self, item: Tuple[float, int, int]) -> None:
        """
        Додає елемент до купи
        
        Args:
            item: кортеж (відстань, вершина, попередник)
        """
        heapq.heappush(self.heap, item)
        self.size += 1
    
    def pop(self) -> Tuple[float, int, int]:
        """
        Видаляє та повертає мінімальний елемент з купи
        
        Returns:
            Кортеж (відстань, вершина, попередник)
        """
        if self.size == 0:
            raise IndexError("Купа порожня")
        self.size -= 1
        return heapq.heappop(self.heap)
    
    def is_empty(self) -> bool:
        """Перевіряє, чи купа порожня"""
        return self.size == 0
    
    def __len__(self) -> int:
        return self.size


class WeightedGraph:
    """Клас для представлення зваженого графа"""
    
    def __init__(self):
        self.vertices: Set[int] = set()
        self.edges: Dict[int, Dict[int, float]] = defaultdict(dict)
        self.vertex_positions: Dict[int, Tuple[float, float]] = {}
    
    def add_vertex(self, vertex: int, x: float = 0, y: float = 0) -> None:
        """
        Додає вершину до графа
        
        Args:
            vertex: номер вершини
            x, y: координати для візуалізації
        """
        self.vertices.add(vertex)
        self.vertex_positions[vertex] = (x, y)
    
    def add_edge(self, vertex1: int, vertex2: int, weight: float) -> None:
        """
        Додає ребро між двома вершинами
        
        Args:
            vertex1: перша вершина
            vertex2: друга вершина
            weight: вага ребра
        """
        if vertex1 not in self.vertices:
            self.add_vertex(vertex1)
        if vertex2 not in self.vertices:
            self.add_vertex(vertex2)
        
        # Додаємо ребро в обох напрямках для неорієнтованого графа
        self.edges[vertex1][vertex2] = weight
        self.edges[vertex2][vertex1] = weight
    
    def get_neighbors(self, vertex: int) -> Dict[int, float]:
        """
        Повертає сусідів вершини з вагами
        
        Args:
            vertex: номер вершини
            
        Returns:
            Словник {сусід: вага_ребра}
        """
        return self.edges.get(vertex, {})
    
    def get_all_edges(self) -> List[Tuple[int, int, float]]:
        """
        Повертає всі ребра графа
        
        Returns:
            Список кортежів (вершина1, вершина2, вага)
        """
        edges = []
        visited = set()
        for vertex1 in self.edges:
            for vertex2, weight in self.edges[vertex1].items():
                if (vertex2, vertex1) not in visited:
                    edges.append((vertex1, vertex2, weight))
                    visited.add((vertex1, vertex2))
        return edges


class DijkstraAlgorithm:
    """Реалізація алгоритму Дейкстри з використанням бінарної купи"""
    
    def __init__(self, graph: WeightedGraph):
        self.graph = graph
        self.distances: Dict[int, float] = {}
        self.predecessors: Dict[int, Optional[int]] = {}
        self.visited: Set[int] = set()
    
    def dijkstra(self, start_vertex: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Знаходить найкоротші шляхи від початкової вершини до всіх інших
        
        Args:
            start_vertex: початкова вершина
            
        Returns:
            Кортеж (відстані, попередники)
        """
        # Ініціалізація
        self.distances = {vertex: float('infinity') for vertex in self.graph.vertices}
        self.predecessors = {vertex: None for vertex in self.graph.vertices}
        self.visited = set()
        
        self.distances[start_vertex] = 0
        
        # Створюємо бінарну купу
        heap = BinaryHeap()
        heap.push((0, start_vertex, start_vertex))
        
        while not heap.is_empty():
            current_distance, current_vertex, predecessor = heap.pop()
            
            # Якщо вершина вже відвідана, пропускаємо
            if current_vertex in self.visited:
                continue
            
            # Позначаємо вершину як відвідану
            self.visited.add(current_vertex)
            self.predecessors[current_vertex] = predecessor
            
            # Перевіряємо всіх сусідів
            for neighbor, weight in self.graph.get_neighbors(current_vertex).items():
                if neighbor not in self.visited:
                    new_distance = current_distance + weight
                    
                    # Якщо знайшли коротший шлях
                    if new_distance < self.distances[neighbor]:
                        self.distances[neighbor] = new_distance
                        heap.push((new_distance, neighbor, current_vertex))
        
        return self.distances, self.predecessors
    
    def get_shortest_path(self, start_vertex: int, end_vertex: int) -> Tuple[List[int], float]:
        """
        Знаходить найкоротший шлях між двома вершинами
        
        Args:
            start_vertex: початкова вершина
            end_vertex: кінцева вершина
            
        Returns:
            Кортеж (шлях, відстань)
        """
        # Спочатку запускаємо алгоритм Дейкстри
        self.dijkstra(start_vertex)
        
        # Відновлюємо шлях
        path = []
        current = end_vertex
        
        while current is not None:
            path.append(current)
            current = self.predecessors[current]
        
        path.reverse()
        
        # Якщо шлях не існує
        if path[0] != start_vertex:
            return [], float('infinity')
        
        return path, self.distances[end_vertex]
    
    def get_all_shortest_paths(self, start_vertex: int) -> Dict[int, Tuple[List[int], float]]:
        """
        Знаходить найкоротші шляхи від початкової вершини до всіх інших
        
        Args:
            start_vertex: початкова вершина
            
        Returns:
            Словник {вершина: (шлях, відстань)}
        """
        self.dijkstra(start_vertex)
        
        paths = {}
        for vertex in self.graph.vertices:
            if vertex != start_vertex and self.distances[vertex] != float('infinity'):
                path = []
                current = vertex
                
                while current is not None:
                    path.append(current)
                    current = self.predecessors[current]
                
                path.reverse()
                paths[vertex] = (path, self.distances[vertex])
        
        return paths


class GraphVisualizer:
    """Клас для візуалізації графа та результатів алгоритму Дейкстри"""
    
    def __init__(self, graph: WeightedGraph):
        self.graph = graph
        self.nx_graph = nx.Graph()
        
        # Додаємо вершини та ребра до NetworkX графа
        for vertex in graph.vertices:
            self.nx_graph.add_node(vertex)
        
        for vertex1, neighbors in graph.edges.items():
            for vertex2, weight in neighbors.items():
                if vertex1 < vertex2:  # Щоб не дублювати ребра
                    self.nx_graph.add_edge(vertex1, vertex2, weight=weight)
    
    def visualize_graph(self, title: str = "Граф", figsize: Tuple[int, int] = (12, 8)):
        """
        Візуалізує граф
        
        Args:
            title: заголовок графіка
            figsize: розмір фігури
        """
        plt.figure(figsize=figsize)
        
        # Використовуємо позиції вершин з графа або генеруємо автоматично
        if self.graph.vertex_positions:
            pos = self.graph.vertex_positions
        else:
            pos = nx.spring_layout(self.nx_graph, k=3, iterations=50)
        
        # Малюємо граф
        nx.draw(self.nx_graph, pos, with_labels=True, node_color='lightblue',
                node_size=1000, font_size=12, font_weight='bold', 
                edge_color='gray', width=2)
        
        # Додаємо ваги ребер
        edge_labels = nx.get_edge_attributes(self.nx_graph, 'weight')
        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels, font_size=10)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def visualize_shortest_paths(self, start_vertex: int, dijkstra_result: DijkstraAlgorithm,
                                title: str = "Найкоротші шляхи", figsize: Tuple[int, int] = (15, 10)):
        """
        Візуалізує граф з виділеними найкоротшими шляхами
        
        Args:
            start_vertex: початкова вершина
            dijkstra_result: результат роботи алгоритму Дейкстри
            title: заголовок графіка
            figsize: розмір фігури
        """
        plt.figure(figsize=figsize)
        
        # Використовуємо позиції вершин з графа або генеруємо автоматично
        if self.graph.vertex_positions:
            pos = self.graph.vertex_positions
        else:
            pos = nx.spring_layout(self.nx_graph, k=3, iterations=50)
        
        # Малюємо граф
        nx.draw(self.nx_graph, pos, with_labels=True, node_color='lightblue',
                node_size=1000, font_size=12, font_weight='bold', 
                edge_color='gray', width=1, alpha=0.6)
        
        # Виділяємо найкоротші шляхи
        for vertex in dijkstra_result.visited:
            if vertex != start_vertex and dijkstra_result.predecessors[vertex] is not None:
                pred = dijkstra_result.predecessors[vertex]
                if pred in pos and vertex in pos:
                    plt.plot([pos[pred][0], pos[vertex][0]], 
                            [pos[pred][1], pos[vertex][1]], 
                            'r-', linewidth=3, alpha=0.8)
        
        # Виділяємо початкову вершину
        if start_vertex in pos:
            plt.scatter([pos[start_vertex][0]], [pos[start_vertex][1]], 
                       c='green', s=1500, marker='o', edgecolors='black', linewidth=3)
        
        # Додаємо відстані як підписи
        for vertex, (x, y) in pos.items():
            distance = dijkstra_result.distances[vertex]
            if distance != float('infinity'):
                plt.text(x, y + 0.2, f'd={distance:.1f}', 
                        ha='center', va='bottom', fontsize=10, 
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()


def create_sample_graph() -> WeightedGraph:
    """Створює зразковий граф для демонстрації"""
    graph = WeightedGraph()
    
    # Додаємо вершини з координатами для візуалізації
    graph.add_vertex(1, 0, 0)
    graph.add_vertex(2, 2, 0)
    graph.add_vertex(3, 4, 0)
    graph.add_vertex(4, 1, 2)
    graph.add_vertex(5, 3, 2)
    graph.add_vertex(6, 2, 4)
    
    # Додаємо ребра
    graph.add_edge(1, 2, 4)
    graph.add_edge(1, 4, 2)
    graph.add_edge(2, 3, 1)
    graph.add_edge(2, 4, 3)
    graph.add_edge(2, 5, 2)
    graph.add_edge(3, 5, 1)
    graph.add_edge(4, 5, 2)
    graph.add_edge(4, 6, 3)
    graph.add_edge(5, 6, 1)
    
    return graph


def create_complex_graph() -> WeightedGraph:
    """Створює складніший граф для тестування"""
    graph = WeightedGraph()
    
    # Додаємо вершини
    for i in range(1, 8):
        angle = 2 * math.pi * (i - 1) / 7
        x = 3 * math.cos(angle)
        y = 3 * math.sin(angle)
        graph.add_vertex(i, x, y)
    
    # Додаємо ребра
    graph.add_edge(1, 2, 2)
    graph.add_edge(1, 3, 4)
    graph.add_edge(1, 7, 3)
    graph.add_edge(2, 3, 1)
    graph.add_edge(2, 4, 2)
    graph.add_edge(3, 4, 3)
    graph.add_edge(3, 5, 1)
    graph.add_edge(4, 5, 2)
    graph.add_edge(4, 6, 1)
    graph.add_edge(5, 6, 3)
    graph.add_edge(5, 7, 2)
    graph.add_edge(6, 7, 1)
    
    return graph


def demo_dijkstra_algorithm():
    """Демонстрація роботи алгоритму Дейкстри"""
    print("=== Демонстрація алгоритму Дейкстри ===\n")
    
    # Створюємо граф
    graph = create_sample_graph()
    visualizer = GraphVisualizer(graph)
    
    print("1. Візуалізація початкового графа:")
    visualizer.visualize_graph("Початковий граф")
    
    # Запускаємо алгоритм Дейкстри
    dijkstra = DijkstraAlgorithm(graph)
    start_vertex = 1
    
    print(f"\n2. Запуск алгоритму Дейкстри з початкової вершини {start_vertex}:")
    distances, predecessors = dijkstra.dijkstra(start_vertex)
    
    print(f"Результати для початкової вершини {start_vertex}:")
    for vertex in sorted(graph.vertices):
        if vertex != start_vertex:
            distance = distances[vertex]
            if distance != float('infinity'):
                path = []
                current = vertex
                while current is not None:
                    path.append(current)
                    current = predecessors[current]
                path.reverse()
                print(f"  До вершини {vertex}: відстань = {distance:.1f}, шлях = {' -> '.join(map(str, path))}")
            else:
                print(f"  До вершини {vertex}: недосяжна")
    
    print(f"\n3. Візуалізація найкоротших шляхів:")
    visualizer.visualize_shortest_paths(start_vertex, dijkstra, 
                                       f"Найкоротші шляхи від вершини {start_vertex}")
    
    # Тестуємо знаходження конкретного шляху
    print(f"\n4. Пошук найкоротшого шляху між вершинами {start_vertex} та 6:")
    path, distance = dijkstra.get_shortest_path(start_vertex, 6)
    if path:
        print(f"  Шлях: {' -> '.join(map(str, path))}")
        print(f"  Відстань: {distance:.1f}")
    else:
        print("  Шлях не знайдено")


def interactive_mode():
    """Інтерактивний режим для користувача"""
    print("=== Інтерактивний режим алгоритму Дейкстри ===\n")
    
    while True:
        try:
            print("Виберіть граф:")
            print("1. Простий граф (6 вершин)")
            print("2. Складний граф (7 вершин)")
            print("3. Створити власний граф")
            print("4. Вихід")
            
            choice = input("Ваш вибір (1-4): ").strip()
            
            if choice == '1':
                graph = create_sample_graph()
                print("Створено простий граф з 6 вершинами")
            elif choice == '2':
                graph = create_complex_graph()
                print("Створено складний граф з 7 вершинами")
            elif choice == '3':
                graph = create_custom_graph()
                if not graph:
                    continue
            elif choice == '4':
                print("Дякуємо за використання програми!")
                break
            else:
                print("Будь ласка, виберіть опцію від 1 до 4!")
                continue
            
            # Візуалізуємо граф
            visualizer = GraphVisualizer(graph)
            visualizer.visualize_graph("Ваш граф")
            
            # Запускаємо алгоритм Дейкстри
            start_vertex = int(input(f"Введіть початкову вершину (1-{max(graph.vertices)}): "))
            
            if start_vertex not in graph.vertices:
                print(f"Вершина {start_vertex} не існує в графі!")
                continue
            
            dijkstra = DijkstraAlgorithm(graph)
            distances, predecessors = dijkstra.dijkstra(start_vertex)
            
            print(f"\nНайкоротші шляхи від вершини {start_vertex}:")
            for vertex in sorted(graph.vertices):
                if vertex != start_vertex:
                    distance = distances[vertex]
                    if distance != float('infinity'):
                        print(f"  До вершини {vertex}: {distance:.1f}")
                    else:
                        print(f"  До вершини {vertex}: недосяжна")
            
            # Візуалізуємо результати
            visualizer.visualize_shortest_paths(start_vertex, dijkstra, 
                                               f"Найкоротші шляхи від вершини {start_vertex}")
            
            continue_choice = input("\nХочете спробувати ще раз? (y/n): ").lower()
            if continue_choice not in ['y', 'yes', 'так', 'т']:
                break
                
        except ValueError:
            print("Будь ласка, введіть правильне число!")
        except KeyboardInterrupt:
            print("\n\nПрограма перервана користувачем.")
            break
        except Exception as e:
            print(f"Виникла помилка: {e}")


def create_custom_graph() -> Optional[WeightedGraph]:
    """Дозволяє користувачу створити власний граф"""
    try:
        graph = WeightedGraph()
        
        num_vertices = int(input("Введіть кількість вершин: "))
        if num_vertices < 1:
            print("Кількість вершин має бути більше 0!")
            return None
        
        # Додаємо вершини
        for i in range(1, num_vertices + 1):
            print(f"Вершина {i}: координати (x, y) або Enter для автоматичного розміщення")
            coords = input().strip()
            if coords:
                x, y = map(float, coords.split(','))
                graph.add_vertex(i, x, y)
            else:
                graph.add_vertex(i)
        
        print(f"\nДодавання ребер (введіть 'done' коли закінчите):")
        print("Формат: вершина1 вершина2 вага")
        
        while True:
            edge_input = input("Ребро: ").strip()
            if edge_input.lower() == 'done':
                break
            
            try:
                vertex1, vertex2, weight = edge_input.split()
                vertex1, vertex2 = int(vertex1), int(vertex2)
                weight = float(weight)
                
                if vertex1 not in range(1, num_vertices + 1) or vertex2 not in range(1, num_vertices + 1):
                    print("Номер вершини поза діапазоном!")
                    continue
                
                graph.add_edge(vertex1, vertex2, weight)
                print(f"Додано ребро {vertex1}-{vertex2} з вагою {weight}")
                
            except ValueError:
                print("Неправильний формат! Використовуйте: вершина1 вершина2 вага")
        
        return graph
        
    except Exception as e:
        print(f"Помилка створення графа: {e}")
        return None


def test_dijkstra_algorithm():
    """Тестування алгоритму Дейкстри"""
    print("=== Тестування алгоритму Дейкстри ===\n")
    
    # Тест 1: Простий граф
    print("Тест 1: Простий граф")
    graph = create_sample_graph()
    dijkstra = DijkstraAlgorithm(graph)
    
    # Тестуємо від вершини 1
    distances, predecessors = dijkstra.dijkstra(1)
    
    # Перевіряємо відстані
    expected_distances = {1: 0, 2: 4, 3: 5, 4: 2, 5: 4, 6: 5}
    for vertex, expected_dist in expected_distances.items():
        actual_dist = distances[vertex]
        assert abs(actual_dist - expected_dist) < 0.001, f"Неспівпадіння для вершини {vertex}: очікувано {expected_dist}, отримано {actual_dist}"
    
    print("✓ Всі відстані правильні")
    
    # Тест 2: Перевірка шляху
    print("\nТест 2: Перевірка шляху")
    path, distance = dijkstra.get_shortest_path(1, 6)
    expected_path = [1, 4, 6]
    assert path == expected_path, f"Неспівпадіння шляху: очікувано {expected_path}, отримано {path}"
    assert abs(distance - 5) < 0.001, f"Неспівпадіння відстані: очікувано 5, отримано {distance}"
    
    print("✓ Шлях правильний")
    
    # Тест 3: Бінарна купа
    print("\nТест 3: Бінарна купа")
    heap = BinaryHeap()
    heap.push((3.5, 1, 0))
    heap.push((1.2, 2, 0))
    heap.push((4.1, 3, 0))
    
    assert not heap.is_empty()
    assert len(heap) == 3
    
    min_item = heap.pop()
    assert min_item == (1.2, 2, 0), f"Очікувано (1.2, 2, 0), отримано {min_item}"
    
    print("✓ Бінарна купа працює правильно")
    
    print("\nВсі тести пройдено успішно!")


def main():
    """Головна функція програми"""
    print("Програма для алгоритму Дейкстри з бінарною купою")
    print("=" * 50)
    
    while True:
        print("\nВиберіть режим роботи:")
        print("1. Демонстрація алгоритму")
        print("2. Інтерактивний режим")
        print("3. Тестування")
        print("4. Вихід")
        
        choice = input("\nВаш вибір (1-4): ").strip()
        
        if choice == '1':
            demo_dijkstra_algorithm()
        elif choice == '2':
            interactive_mode()
        elif choice == '3':
            test_dijkstra_algorithm()
        elif choice == '4':
            print("Дякуємо за використання програми!")
            break
        else:
            print("Будь ласка, виберіть опцію від 1 до 4!")


if __name__ == "__main__":
    main()
