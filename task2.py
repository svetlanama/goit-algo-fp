"""
Завдання 2. Рекурсія. Створення фрактала "дерево Піфагора" за допомогою рекурсії

Необхідно написати програму на Python, яка використовує рекурсію для створення 
фрактала "дерево Піфагора". Програма має візуалізувати фрактал "дерево Піфагора", 
і користувач повинен мати можливість вказати рівень рекурсії.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple


class PythagoreanTree:
    """Клас для створення фрактала дерево Піфагора"""
    
    def __init__(self):
        self.lines = []  # Зберігаємо координати ліній для візуалізації
        
    def draw_line(self, x1: float, y1: float, x2: float, y2: float) -> Tuple[float, float, float, float]:
        """
        Додає лінію до списку для візуалізації
        
        Args:
            x1, y1: координати початку лінії
            x2, y2: координати кінця лінії
        
        Returns:
            Координати лінії
        """
        line = (x1, y1, x2, y2)
        self.lines.append(line)
        return line
    
    def pythagorean_tree(self, x1: float, y1: float, x2: float, y2: float, 
                        level: int, max_level: int, angle: float = 0) -> None:
        """
        Рекурсивна функція для створення дерева Піфагора
        
        Args:
            x1, y1: координати початку лінії
            x2, y2: координати кінця лінії
            level: поточний рівень рекурсії
            max_level: максимальний рівень рекурсії
            angle: поточний кут повороту
        """
        # Базовий випадок рекурсії
        if level >= max_level:
            return
        
        # Малюємо поточну лінію
        self.draw_line(x1, y1, x2, y2)
        
        # Обчислюємо довжину та кут для наступних ліній
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        
        # Скорочуємо довжину для наступного рівня (коефіцієнт 0.7)
        new_length = length * 0.7
        
        # Кут повороту для дочірніх ліній (45 градусів)
        rotation_angle = np.pi / 4
        
        # Ліва дочірня лінія
        left_angle = angle - rotation_angle
        left_x2 = x2 + new_length * np.cos(left_angle)
        left_y2 = y2 + new_length * np.sin(left_angle)
        
        # Права дочірня лінія
        right_angle = angle + rotation_angle
        right_x2 = x2 + new_length * np.cos(right_angle)
        right_y2 = y2 + new_length * np.sin(right_angle)
        
        # Рекурсивно викликаємо для дочірніх ліній
        self.pythagorean_tree(x2, y2, left_x2, left_y2, level + 1, max_level, left_angle)
        self.pythagorean_tree(x2, y2, right_x2, right_y2, level + 1, max_level, right_angle)
    
    def create_tree(self, max_level: int = 5) -> None:
        """
        Створює дерево Піфагора з заданим рівнем рекурсії
        
        Args:
            max_level: максимальний рівень рекурсії
        """
        # Початкова лінія (ствол дерева)
        x1, y1 = 0, 0
        x2, y2 = 0, 2
        
        # Очищуємо попередні лінії
        self.lines = []
        
        # Починаємо рекурсію
        self.pythagorean_tree(x1, y1, x2, y2, 0, max_level, np.pi / 2)  # 90 градусів вгору
    
    def visualize(self, title: str = "Дерево Піфагора", 
                  figsize: Tuple[int, int] = (12, 8)) -> None:
        """
        Візуалізує дерево Піфагора
        
        Args:
            title: заголовок графіка
            figsize: розмір фігури
        """
        plt.figure(figsize=figsize)
        
        # Малюємо всі лінії
        for line in self.lines:
            x1, y1, x2, y2 = line
            plt.plot([x1, x2], [y1, y2], 'b-', linewidth=2)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('X', fontsize=12)
        plt.ylabel('Y', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


def get_user_input() -> int:
    """
    Отримує від користувача рівень рекурсії
    
    Returns:
        Рівень рекурсії
    """
    while True:
        try:
            level = int(input("Введіть рівень рекурсії (1-8, рекомендується 4-6): "))
            if 1 <= level <= 8:
                return level
            else:
                print("Рівень рекурсії повинен бути від 1 до 8!")
        except ValueError:
            print("Будь ласка, введіть ціле число!")


def demo_different_levels():
    """Демонструє дерево Піфагора з різними рівнями рекурсії"""
    print("=== Демонстрація дерева Піфагора з різними рівнями рекурсії ===\n")
    
    levels_to_demo = [2, 3, 4, 5]
    
    for level in levels_to_demo:
        print(f"Створюємо дерево Піфагора з рівнем рекурсії: {level}")
        
        tree = PythagoreanTree()
        tree.create_tree(level)
        
        title = f"Дерево Піфагора (рівень рекурсії: {level})"
        tree.visualize(title)
        
        print(f"Дерево з рівнем {level} створено. Кількість ліній: {len(tree.lines)}")
        print()


def interactive_mode():
    """Інтерактивний режим для користувача"""
    print("=== Інтерактивний режим створення дерева Піфагора ===\n")
    
    while True:
        try:
            level = get_user_input()
            
            print(f"\nСтворюємо дерево Піфагора з рівнем рекурсії: {level}")
            
            tree = PythagoreanTree()
            tree.create_tree(level)
            
            title = f"Ваше дерево Піфагора (рівень рекурсії: {level})"
            tree.visualize(title)
            
            print(f"Дерево створено! Кількість ліній: {len(tree.lines)}")
            
            continue_choice = input("\nХочете створити ще одне дерево? (y/n): ").lower()
            if continue_choice not in ['y', 'yes', 'так', 'т']:
                break
                
        except KeyboardInterrupt:
            print("\n\nПрограма перервана користувачем.")
            break
        except Exception as e:
            print(f"Виникла помилка: {e}")


def test_recursive_function():
    """Тестування рекурсивної функції"""
    print("=== Тестування рекурсивної функції ===\n")
    
    # Тест 1: Мінімальний рівень
    print("Тест 1: Рівень рекурсії = 1")
    tree1 = PythagoreanTree()
    tree1.create_tree(1)
    print(f"Кількість ліній: {len(tree1.lines)}")
    assert len(tree1.lines) == 1, "Для рівня 1 має бути 1 лінія"
    print("✓ Тест пройдено\n")
    
    # Тест 2: Середній рівень
    print("Тест 2: Рівень рекурсії = 3")
    tree2 = PythagoreanTree()
    tree2.create_tree(3)
    print(f"Кількість ліній: {len(tree2.lines)}")
    assert len(tree2.lines) == 7, "Для рівня 3 має бути 7 ліній"
    print("✓ Тест пройдено\n")
    
    # Тест 3: Перевірка формули кількості ліній
    print("Тест 3: Перевірка формули кількості ліній")
    for level in range(1, 6):
        tree = PythagoreanTree()
        tree.create_tree(level)
        expected_lines = 2**level - 1  # Формула для кількості ліній
        actual_lines = len(tree.lines)
        print(f"Рівень {level}: очікувано {expected_lines}, отримано {actual_lines}")
        assert actual_lines == expected_lines, f"Неспівпадіння для рівня {level}"
    print("✓ Всі тести пройдено\n")


def main():
    """Головна функція програми"""
    print("Програма для створення фрактала 'Дерево Піфагора'")
    print("=" * 50)
    
    while True:
        print("\nВиберіть режим роботи:")
        print("1. Інтерактивний режим (введіть свій рівень рекурсії)")
        print("2. Демонстрація з різними рівнями")
        print("3. Тестування функцій")
        print("4. Вихід")
        
        choice = input("\nВаш вибір (1-4): ").strip()
        
        if choice == '1':
            interactive_mode()
        elif choice == '2':
            demo_different_levels()
        elif choice == '3':
            test_recursive_function()
        elif choice == '4':
            print("Дякуємо за використання програми!")
            break
        else:
            print("Будь ласка, виберіть опцію від 1 до 4!")


if __name__ == "__main__":
    main()
