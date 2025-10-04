"""
Завдання 4. Візуалізація піраміди

Аналіз наданого коду та створення функції для візуалізації бінарної купи.

Наданий код виконує побудову бінарних дерев з використанням:
- Node клас з унікальними ідентифікаторами та кольорами
- Рекурсивна функція add_edges для додавання вузлів та ребер до NetworkX графа
- Функція draw_tree для візуалізації дерева з matplotlib

На основі цього коду створюємо візуалізацію бінарної купи.
"""

import uuid
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Optional
import random


class Node:
    """Клас для представлення вузла бінарної купи"""
    
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """
    Рекурсивна функція для додавання вузлів та ребер до графа
    
    Args:
        graph: NetworkX граф
        node: поточний вузол
        pos: словник позицій вузлів
        x, y: координати поточного вузла
        layer: поточний рівень дерева
    """
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title="Бінарне дерево"):
    """
    Візуалізує бінарне дерево
    
    Args:
        tree_root: корінь дерева
        title: заголовок графіка
    """
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, 
            node_color=colors, with_labels=True, font_size=12, font_weight='bold')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()


class BinaryHeap:
    """Реалізація бінарної купи (min-heap) з візуалізацією"""
    
    def __init__(self):
        self.heap = []
        self.root = None
    
    def insert(self, value: int) -> None:
        """
        Додає елемент до купи
        
        Args:
            value: значення для додавання
        """
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
        self._rebuild_tree()
    
    def extract_min(self) -> Optional[int]:
        """
        Видаляє та повертає мінімальний елемент
        
        Returns:
            Мінімальний елемент або None, якщо купа порожня
        """
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            min_val = self.heap.pop()
        else:
            min_val = self.heap[0]
            self.heap[0] = self.heap.pop()
            self._heapify_down(0)
        
        self._rebuild_tree()
        return min_val
    
    def _heapify_up(self, index: int) -> None:
        """Відновлює властивість купи вгору"""
        parent = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)
    
    def _heapify_down(self, index: int) -> None:
        """Відновлює властивість купи вниз"""
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)
    
    def _rebuild_tree(self) -> None:
        """Перебудовує дерево на основі масиву купи"""
        if not self.heap:
            self.root = None
            return
        
        # Створюємо вузли для всіх елементів
        nodes = [Node(val) for val in self.heap]
        
        # Встановлюємо зв'язки батько-дитина
        for i in range(len(nodes)):
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            
            if left_child < len(nodes):
                nodes[i].left = nodes[left_child]
            if right_child < len(nodes):
                nodes[i].right = nodes[right_child]
        
        self.root = nodes[0]
    
    def visualize(self, title: str = "Бінарна купа") -> None:
        """
        Візуалізує бінарну купу
        
        Args:
            title: заголовок графіка
        """
        if self.root is None:
            print("Купа порожня!")
            return
        
        # Встановлюємо кольори для різних рівнів
        self._set_colors_by_level()
        draw_tree(self.root, title)
    
    def _set_colors_by_level(self) -> None:
        """Встановлює кольори вузлів залежно від рівня"""
        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 
                 'lightpink', 'lightgray', 'lightsteelblue']
        
        def set_colors_recursive(node, level=0):
            if node:
                node.color = colors[level % len(colors)]
                set_colors_recursive(node.left, level + 1)
                set_colors_recursive(node.right, level + 1)
        
        set_colors_recursive(self.root)
    
    def visualize_operation(self, operation: str, value: Optional[int] = None, 
                          title: str = "Операція з купою") -> None:
        """
        Візуалізує купу після операції
        
        Args:
            operation: назва операції
            value: значення (якщо потрібно)
            title: заголовок графіка
        """
        full_title = f"{title}\n{operation}"
        if value is not None:
            full_title += f" (значення: {value})"
        full_title += f"\nКупа: {self.heap}"
        
        self.visualize(full_title)
    
    def is_empty(self) -> bool:
        """Перевіряє, чи купа порожня"""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """Повертає розмір купи"""
        return len(self.heap)
    
    def peek(self) -> Optional[int]:
        """Повертає мінімальний елемент без видалення"""
        return self.heap[0] if self.heap else None


def create_sample_heap() -> BinaryHeap:
    """Створює зразкову купу для демонстрації"""
    heap = BinaryHeap()
    values = [3, 1, 6, 5, 2, 4]
    
    print("Створення зразкової купи:")
    for value in values:
        print(f"Додаємо {value}")
        heap.insert(value)
        heap.visualize_operation(f"Додано {value}", value)
    
    return heap


def demo_heap_operations():
    """Демонстрація операцій з купою"""
    print("=== Демонстрація операцій з бінарною купою ===\n")
    
    # Створюємо купу
    heap = BinaryHeap()
    
    print("1. Додавання елементів до купи:")
    values = [15, 10, 20, 8, 12, 25, 5]
    
    for value in values:
        heap.insert(value)
        heap.visualize_operation(f"Додано {value}", value, "Побудова купи")
    
    print(f"\n2. Поточний стан купи: {heap.heap}")
    print(f"Мінімальний елемент: {heap.peek()}")
    
    print("\n3. Видалення мінімальних елементів:")
    for i in range(3):
        min_val = heap.extract_min()
        print(f"Видалено мінімальний елемент: {min_val}")
        heap.visualize_operation(f"Видалено {min_val}", min_val, "Видалення з купи")
    
    print(f"\n4. Фінальний стан купи: {heap.heap}")


def interactive_heap_demo():
    """Інтерактивна демонстрація роботи з купою"""
    print("=== Інтерактивна демонстрація бінарної купи ===\n")
    
    heap = BinaryHeap()
    
    while True:
        print("\nПоточний стан купи:", heap.heap)
        print("\nВиберіть операцію:")
        print("1. Додати елемент")
        print("2. Видалити мінімальний елемент")
        print("3. Показати мінімальний елемент")
        print("4. Візуалізувати купу")
        print("5. Заповнити випадковими числами")
        print("6. Очистити купу")
        print("7. Вихід")
        
        choice = input("\nВаш вибір (1-7): ").strip()
        
        try:
            if choice == '1':
                value = int(input("Введіть значення для додавання: "))
                heap.insert(value)
                heap.visualize_operation(f"Додано {value}", value)
                
            elif choice == '2':
                if heap.is_empty():
                    print("Купа порожня!")
                else:
                    min_val = heap.extract_min()
                    heap.visualize_operation(f"Видалено {min_val}", min_val)
                    
            elif choice == '3':
                min_val = heap.peek()
                if min_val is not None:
                    print(f"Мінімальний елемент: {min_val}")
                else:
                    print("Купа порожня!")
                    
            elif choice == '4':
                heap.visualize("Поточний стан купи")
                
            elif choice == '5':
                count = int(input("Скільки випадкових чисел додати (1-10): "))
                count = max(1, min(10, count))
                
                for i in range(count):
                    value = random.randint(1, 50)
                    heap.insert(value)
                    heap.visualize_operation(f"Додано {value}", value, "Заповнення купи")
                    
            elif choice == '6':
                heap = BinaryHeap()
                print("Купа очищена!")
                
            elif choice == '7':
                print("Дякуємо за використання програми!")
                break
                
            else:
                print("Будь ласка, виберіть опцію від 1 до 7!")
                
        except ValueError:
            print("Будь ласка, введіть правильне число!")
        except KeyboardInterrupt:
            print("\n\nПрограма перервана користувачем.")
            break
        except Exception as e:
            print(f"Виникла помилка: {e}")


def analyze_base_code():
    """Аналіз наданого коду для візуалізації бінарних дерев"""
    print("=== Аналіз наданого коду ===\n")
    
    print("1. Клас Node:")
    print("   - Зберігає значення вузла (val)")
    print("   - Має посилання на лівого та правого нащадків (left, right)")
    print("   - Містить унікальний ідентифікатор (id) для NetworkX")
    print("   - Підтримує колір для візуалізації (color)")
    
    print("\n2. Функція add_edges:")
    print("   - Рекурсивно обходить дерево")
    print("   - Додає вузли до NetworkX графа")
    print("   - Встановлює позиції вузлів для візуалізації")
    print("   - Створює ребра між батьківськими та дочірніми вузлами")
    
    print("\n3. Функція draw_tree:")
    print("   - Створює NetworkX DiGraph")
    print("   - Витягує кольори та мітки з вузлів")
    print("   - Візуалізує дерево з matplotlib")
    
    print("\n4. Переваги такого підходу:")
    print("   - Модульність: кожна функція має чітку відповідальність")
    print("   - Рекурсивність: природний спосіб обходу дерев")
    print("   - Гнучкість: легко змінювати кольори та стилі")
    print("   - Інтеграція: використання потужних бібліотек NetworkX та matplotlib")
    
    print("\n5. Застосування до бінарної купи:")
    print("   - Адаптуємо Node для зберігання елементів купи")
    print("   - Додаємо операції вставки та видалення")
    print("   - Зберігаємо властивості купи (heap property)")
    print("   - Візуалізуємо зміни після кожної операції")


def test_heap_properties():
    """Тестує властивості бінарної купи"""
    print("\n=== Тестування властивостей бінарної купи ===\n")
    
    heap = BinaryHeap()
    test_values = [10, 5, 15, 3, 7, 12, 18, 1, 8]
    
    print("1. Тестування вставки:")
    for value in test_values:
        heap.insert(value)
        # Перевіряємо властивість купи: батьківський елемент <= дочірніх
        for i in range(1, len(heap.heap)):
            parent = (i - 1) // 2
            assert heap.heap[parent] <= heap.heap[i], f"Порушена властивість купи: {heap.heap}"
    
    print("✓ Властивість купи збережена після всіх вставок")
    
    print("\n2. Тестування видалення:")
    prev_min = float('-inf')
    while not heap.is_empty():
        current_min = heap.extract_min()
        assert current_min >= prev_min, f"Елементи не відсортовані: {current_min} < {prev_min}"
        prev_min = current_min
    
    print("✓ Елементи видаляються в правильному порядку (за зростанням)")
    
    print("\n3. Тестування порожньої купи:")
    empty_heap = BinaryHeap()
    assert empty_heap.is_empty()
    assert empty_heap.extract_min() is None
    assert empty_heap.peek() is None
    
    print("✓ Порожня купа працює правильно")
    
    print("\nВсі тести пройдено успішно!")


def main():
    """Головна функція програми"""
    print("Програма для візуалізації бінарної купи")
    print("=" * 50)
    
    while True:
        print("\nВиберіть режим роботи:")
        print("1. Аналіз наданого коду")
        print("2. Демонстрація операцій з купою")
        print("3. Інтерактивна демонстрація")
        print("4. Тестування властивостей купи")
        print("5. Показати зразкове дерево (з наданого коду)")
        print("6. Вихід")
        
        choice = input("\nВаш вибір (1-6): ").strip()
        
        if choice == '1':
            analyze_base_code()
        elif choice == '2':
            demo_heap_operations()
        elif choice == '3':
            interactive_heap_demo()
        elif choice == '4':
            test_heap_properties()
        elif choice == '5':
            # Демонстрація оригінального коду
            root = Node(0)
            root.left = Node(4)
            root.left.left = Node(5)
            root.left.right = Node(10)
            root.right = Node(1)
            root.right.left = Node(3)
            
            draw_tree(root, "Зразкове бінарне дерево (з наданого коду)")
        elif choice == '6':
            print("Дякуємо за використання програми!")
            break
        else:
            print("Будь ласка, виберіть опцію від 1 до 6!")


if __name__ == "__main__":
    main()
