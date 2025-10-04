"""
Завдання 5. Візуалізація обходу бінарного дерева

Програма для візуалізації обходів бінарного дерева (у глибину та в ширину)
з кольоровим кодуванням вузлів залежно від послідовності обходу.
"""

import uuid
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Optional, Tuple
import time
import random
from collections import deque


class Node:
    """Клас для представлення вузла бінарного дерева"""
    
    def __init__(self, key, color="lightgray"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


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


def draw_tree(tree_root, title="Бінарне дерево", step_info=""):
    """
    Візуалізує бінарне дерево з кольоровим кодуванням
    
    Args:
        tree_root: корінь дерева
        title: заголовок графіка
        step_info: додаткова інформація про крок
    """
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(12, 8))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=3000, 
            node_color=colors, with_labels=True, font_size=14, font_weight='bold',
            edge_color='gray', width=2)
    
    full_title = title
    if step_info:
        full_title += f"\n{step_info}"
    
    plt.title(full_title, fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()


def generate_color_gradient(n_colors: int) -> List[str]:
    """
    Генерує градієнт кольорів від темних до світлих відтінків
    
    Args:
        n_colors: кількість кольорів для генерації
        
    Returns:
        Список hex-кольорів у форматі #RRGGBB
    """
    colors = []
    
    # Базові кольори для градієнта (від темного до світлого)
    base_colors = [
        (18, 150, 240),   # Темно-синій (#1296F0)
        (30, 144, 255),   # Синій
        (100, 149, 237),  # Світло-синій
        (135, 206, 250),  # Небесно-блакитний
        (173, 216, 230),  # Світло-блакитний
        (176, 224, 230),  # Пороховий блакитний
        (224, 255, 255),  # Світло-блакитний
        (240, 248, 255)   # М'ятний крем
    ]
    
    if n_colors <= len(base_colors):
        # Якщо потрібно менше кольорів, ніж у базовому списку
        for i in range(n_colors):
            r, g, b = base_colors[i]
            colors.append(f"#{r:02x}{g:02x}{b:02x}")
    else:
        # Інтерполяція між базовими кольорами
        for i in range(n_colors):
            # Нормалізуємо індекс до діапазону [0, 1]
            t = i / (n_colors - 1) if n_colors > 1 else 0
            
            # Знаходимо індекси базових кольорів для інтерполяції
            color_index = t * (len(base_colors) - 1)
            color_index_low = int(color_index)
            color_index_high = min(color_index_low + 1, len(base_colors) - 1)
            
            # Коефіцієнт інтерполяції
            t_local = color_index - color_index_low
            
            # Інтерполюємо кольори
            r1, g1, b1 = base_colors[color_index_low]
            r2, g2, b2 = base_colors[color_index_high]
            
            r = int(r1 + t_local * (r2 - r1))
            g = int(g1 + t_local * (g2 - g1))
            b = int(b1 + t_local * (b2 - b1))
            
            colors.append(f"#{r:02x}{g:02x}{b:02x}")
    
    return colors


def reset_tree_colors(root: Node) -> None:
    """Скидає кольори всіх вузлів дерева до стандартного"""
    if root:
        root.color = "lightgray"
        reset_tree_colors(root.left)
        reset_tree_colors(root.right)


def count_nodes(root: Node) -> int:
    """Підраховує кількість вузлів у дереві"""
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


class BinaryTreeTraversal:
    """Клас для візуалізації обходів бінарного дерева"""
    
    def __init__(self, root: Node):
        self.root = root
        self.total_nodes = count_nodes(root)
        self.colors = generate_color_gradient(self.total_nodes)
    
    def depth_first_preorder(self, show_steps: bool = True) -> List[int]:
        """
        Обхід у глибину (preorder): корінь -> лівий -> правий
        
        Args:
            show_steps: чи показувати кожен крок візуально
            
        Returns:
            Список значень вузлів у порядку обходу
        """
        print("=== Обхід у глибину (Preorder) ===")
        print("Порядок: Корінь -> Лівий піддерево -> Правий піддерево")
        
        reset_tree_colors(self.root)
        result = []
        step = 0
        
        def preorder_helper(node: Node):
            nonlocal step
            if node:
                # Відвідуємо корінь
                node.color = self.colors[step]
                result.append(node.val)
                step += 1
                
                if show_steps:
                    print(f"Крок {step}: Відвідуємо вузол {node.val}")
                    draw_tree(self.root, "Обхід у глибину (Preorder)", 
                            f"Крок {step}: Відвідуємо {node.val}")
                    time.sleep(1)
                
                # Рекурсивно обходимо ліве піддерево
                preorder_helper(node.left)
                # Рекурсивно обходимо праве піддерево
                preorder_helper(node.right)
        
        preorder_helper(self.root)
        print(f"Результат обходу: {result}")
        return result
    
    def depth_first_inorder(self, show_steps: bool = True) -> List[int]:
        """
        Обхід у глибину (inorder): лівий -> корінь -> правий
        
        Args:
            show_steps: чи показувати кожен крок візуально
            
        Returns:
            Список значень вузлів у порядку обходу
        """
        print("=== Обхід у глибину (Inorder) ===")
        print("Порядок: Лівий піддерево -> Корінь -> Правий піддерево")
        
        reset_tree_colors(self.root)
        result = []
        step = 0
        
        def inorder_helper(node: Node):
            nonlocal step
            if node:
                # Рекурсивно обходимо ліве піддерево
                inorder_helper(node.left)
                
                # Відвідуємо корінь
                node.color = self.colors[step]
                result.append(node.val)
                step += 1
                
                if show_steps:
                    print(f"Крок {step}: Відвідуємо вузол {node.val}")
                    draw_tree(self.root, "Обхід у глибину (Inorder)", 
                            f"Крок {step}: Відвідуємо {node.val}")
                    time.sleep(1)
                
                # Рекурсивно обходимо праве піддерево
                inorder_helper(node.right)
        
        inorder_helper(self.root)
        print(f"Результат обходу: {result}")
        return result
    
    def depth_first_postorder(self, show_steps: bool = True) -> List[int]:
        """
        Обхід у глибину (postorder): лівий -> правий -> корінь
        
        Args:
            show_steps: чи показувати кожен крок візуально
            
        Returns:
            Список значень вузлів у порядку обходу
        """
        print("=== Обхід у глибину (Postorder) ===")
        print("Порядок: Лівий піддерево -> Правий піддерево -> Корінь")
        
        reset_tree_colors(self.root)
        result = []
        step = 0
        
        def postorder_helper(node: Node):
            nonlocal step
            if node:
                # Рекурсивно обходимо ліве піддерево
                postorder_helper(node.left)
                # Рекурсивно обходимо праве піддерево
                postorder_helper(node.right)
                
                # Відвідуємо корінь
                node.color = self.colors[step]
                result.append(node.val)
                step += 1
                
                if show_steps:
                    print(f"Крок {step}: Відвідуємо вузол {node.val}")
                    draw_tree(self.root, "Обхід у глибину (Postorder)", 
                            f"Крок {step}: Відвідуємо {node.val}")
                    time.sleep(1)
        
        postorder_helper(self.root)
        print(f"Результат обходу: {result}")
        return result
    
    def breadth_first(self, show_steps: bool = True) -> List[int]:
        """
        Обхід у ширину (BFS): рівень за рівнем
        
        Args:
            show_steps: чи показувати кожен крок візуально
            
        Returns:
            Список значень вузлів у порядку обходу
        """
        print("=== Обхід у ширину (BFS) ===")
        print("Порядок: Рівень за рівнем, зліва направо")
        
        reset_tree_colors(self.root)
        result = []
        step = 0
        
        if not self.root:
            return result
        
        queue = deque([self.root])
        
        while queue:
            node = queue.popleft()
            
            # Відвідуємо поточний вузол
            node.color = self.colors[step]
            result.append(node.val)
            step += 1
            
            if show_steps:
                print(f"Крок {step}: Відвідуємо вузол {node.val}")
                draw_tree(self.root, "Обхід у ширину (BFS)", 
                        f"Крок {step}: Відвідуємо {node.val}")
                time.sleep(1)
            
            # Додаємо дочірні вузли до черги
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        print(f"Результат обходу: {result}")
        return result
    
    def show_final_result(self, traversal_type: str, result: List[int]) -> None:
        """Показує фінальний результат обходу з усіма кольорами"""
        print(f"\n=== Фінальний результат {traversal_type} ===")
        print(f"Послідовність відвідування: {result}")
        print("Кольори вузлів відповідають порядку відвідування (від темного до світлого)")
        
        draw_tree(self.root, f"Фінальний результат: {traversal_type}", 
                 f"Послідовність: {' -> '.join(map(str, result))}")


def create_sample_tree() -> Node:
    """Створює зразкове бінарне дерево для демонстрації"""
    # Створюємо дерево:
    #       1
    #      / \
    #     2   3
    #    / \   \
    #   4   5   6
    #  /     \
    # 7       8
    
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.right = Node(6)
    root.left.left.left = Node(7)
    root.left.right.right = Node(8)
    
    return root


def create_random_tree(size: int) -> Node:
    """Створює випадкове бінарне дерево заданого розміру"""
    if size <= 0:
        return None
    
    values = list(range(1, size + 1))
    random.shuffle(values)
    
    root = Node(values[0])
    
    for value in values[1:]:
        insert_random(root, value)
    
    return root


def insert_random(root: Node, value: int) -> None:
    """Вставляє значення у випадкове місце в дереві"""
    if not root:
        return
    
    # Випадково вибираємо лівий або правий нащадок
    if random.choice([True, False]):
        if root.left is None:
            root.left = Node(value)
        else:
            insert_random(root.left, value)
    else:
        if root.right is None:
            root.right = Node(value)
        else:
            insert_random(root.right, value)


def demo_all_traversals():
    """Демонстрація всіх типів обходів"""
    print("=== Демонстрація всіх типів обходів бінарного дерева ===\n")
    
    # Створюємо зразкове дерево
    root = create_sample_tree()
    traversal = BinaryTreeTraversal(root)
    
    print("Створено зразкове дерево:")
    draw_tree(root, "Зразкове бінарне дерево", "Вузли без кольорового кодування")
    
    # Демонструємо всі типи обходів
    traversals = [
        ("Preorder", traversal.depth_first_preorder),
        ("Inorder", traversal.depth_first_inorder),
        ("Postorder", traversal.depth_first_postorder),
        ("BFS", traversal.breadth_first)
    ]
    
    for name, method in traversals:
        print(f"\n{'='*50}")
        result = method(show_steps=True)
        traversal.show_final_result(name, result)
        input("\nНатисніть Enter для продовження...")


def interactive_traversal_demo():
    """Інтерактивна демонстрація обходів"""
    print("=== Інтерактивна демонстрація обходів бінарного дерева ===\n")
    
    root = None
    traversal = None
    
    while True:
        print("\nПоточне меню:")
        print("1. Створити зразкове дерево")
        print("2. Створити випадкове дерево")
        print("3. Показати поточне дерево")
        print("4. Preorder обхід (з кроками)")
        print("5. Inorder обхід (з кроками)")
        print("6. Postorder обхід (з кроками)")
        print("7. BFS обхід (з кроками)")
        print("8. Швидкий обхід (без кроків)")
        print("9. Порівняння всіх обходів")
        print("10. Вихід")
        
        choice = input("\nВаш вибір (1-10): ").strip()
        
        try:
            if choice == '1':
                root = create_sample_tree()
                traversal = BinaryTreeTraversal(root)
                print("Створено зразкове дерево!")
                draw_tree(root, "Зразкове бінарне дерево")
                
            elif choice == '2':
                size = int(input("Введіть розмір дерева (3-15): "))
                size = max(3, min(15, size))
                root = create_random_tree(size)
                traversal = BinaryTreeTraversal(root)
                print(f"Створено випадкове дерево розміром {size}!")
                draw_tree(root, f"Випадкове бінарне дерево (розмір {size})")
                
            elif choice == '3':
                if root:
                    draw_tree(root, "Поточне бінарне дерево")
                else:
                    print("Спочатку створіть дерево!")
                    
            elif choice in ['4', '5', '6', '7']:
                if not root:
                    print("Спочатку створіть дерево!")
                    continue
                
                methods = {
                    '4': ("Preorder", traversal.depth_first_preorder),
                    '5': ("Inorder", traversal.depth_first_inorder),
                    '6': ("Postorder", traversal.depth_first_postorder),
                    '7': ("BFS", traversal.breadth_first)
                }
                
                name, method = methods[choice]
                result = method(show_steps=True)
                traversal.show_final_result(name, result)
                
            elif choice == '8':
                if not root:
                    print("Спочатку створіть дерево!")
                    continue
                
                print("\nШвидкий обхід (без показу кроків):")
                print("1. Preorder")
                print("2. Inorder") 
                print("3. Postorder")
                print("4. BFS")
                
                sub_choice = input("Виберіть тип обходу (1-4): ").strip()
                
                methods = {
                    '1': ("Preorder", traversal.depth_first_preorder),
                    '2': ("Inorder", traversal.depth_first_inorder),
                    '3': ("Postorder", traversal.depth_first_postorder),
                    '4': ("BFS", traversal.breadth_first)
                }
                
                if sub_choice in methods:
                    name, method = methods[sub_choice]
                    result = method(show_steps=False)
                    traversal.show_final_result(name, result)
                else:
                    print("Невірний вибір!")
                    
            elif choice == '9':
                if not root:
                    print("Спочатку створіть дерево!")
                    continue
                
                print("\n=== Порівняння всіх обходів ===")
                
                methods = [
                    ("Preorder", traversal.depth_first_preorder),
                    ("Inorder", traversal.depth_first_inorder),
                    ("Postorder", traversal.depth_first_postorder),
                    ("BFS", traversal.breadth_first)
                ]
                
                results = {}
                for name, method in methods:
                    result = method(show_steps=False)
                    results[name] = result
                    print(f"{name}: {result}")
                
                # Показуємо фінальний результат з кольорами
                print("\nФінальний стан дерева (BFS кольори):")
                traversal.breadth_first(show_steps=False)
                traversal.show_final_result("BFS", results["BFS"])
                
            elif choice == '10':
                print("Дякуємо за використання програми!")
                break
                
            else:
                print("Будь ласка, виберіть опцію від 1 до 10!")
                
        except ValueError:
            print("Будь ласка, введіть правильне число!")
        except KeyboardInterrupt:
            print("\n\nПрограма перервана користувачем.")
            break
        except Exception as e:
            print(f"Виникла помилка: {e}")


def analyze_traversal_algorithms():
    """Аналіз алгоритмів обходу дерев"""
    print("=== Аналіз алгоритмів обходу бінарних дерев ===\n")
    
    print("1. Обходи у глибину (Depth-First Search - DFS):")
    print("   - Preorder (NLR): Корінь -> Лівий -> Правий")
    print("   - Inorder (LNR): Лівий -> Корінь -> Правий")
    print("   - Postorder (LRN): Лівий -> Правий -> Корінь")
    print("   - Складність: O(n) часу, O(h) простору (h - висота дерева)")
    print("   - Застосування: копіювання дерев, обчислення виразів, серіалізація")
    
    print("\n2. Обхід у ширину (Breadth-First Search - BFS):")
    print("   - Рівень за рівнем, зліва направо")
    print("   - Складність: O(n) часу, O(w) простору (w - максимальна ширина)")
    print("   - Застосування: пошук найкоротшого шляху, обробка рівнями")
    
    print("\n3. Кольорове кодування:")
    print("   - Використовуємо 16-систему RGB (формат #RRGGBB)")
    print("   - Градієнт від темних до світлих відтінків")
    print("   - Кожен вузол отримує унікальний колір залежно від порядку відвідування")
    print("   - Візуально показує послідовність обходу")
    
    print("\n4. Переваги візуалізації:")
    print("   - Наочне розуміння алгоритмів")
    print("   - Порівняння різних типів обходів")
    print("   - Демонстрація різниці між DFS та BFS")
    print("   - Навчання та налагодження алгоритмів")


def main():
    """Головна функція програми"""
    print("Програма для візуалізації обходів бінарного дерева")
    print("=" * 60)
    
    while True:
        print("\nВиберіть режим роботи:")
        print("1. Демонстрація всіх обходів")
        print("2. Інтерактивна демонстрація")
        print("3. Аналіз алгоритмів обходу")
        print("4. Швидкий тест з зразковим деревом")
        print("5. Вихід")
        
        choice = input("\nВаш вибір (1-5): ").strip()
        
        if choice == '1':
            demo_all_traversals()
        elif choice == '2':
            interactive_traversal_demo()
        elif choice == '3':
            analyze_traversal_algorithms()
        elif choice == '4':
            print("\n=== Швидкий тест ===")
            root = create_sample_tree()
            traversal = BinaryTreeTraversal(root)
            
            print("Зразкове дерево:")
            draw_tree(root, "Зразкове дерево")
            
            print("\nШвидкий обхід (без кроків):")
            traversal.depth_first_preorder(show_steps=False)
            traversal.show_final_result("Preorder", traversal.depth_first_preorder(show_steps=False))
            
        elif choice == '5':
            print("Дякуємо за використання програми!")
            break
        else:
            print("Будь ласка, виберіть опцію від 1 до 5!")


if __name__ == "__main__":
    main()
