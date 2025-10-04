"""
Завдання 6. Жадібні алгоритми та динамічне програмування

Програма для розв'язання задачі вибору їжі з найбільшою сумарною калорійністю
в межах обмеженого бюджету, використовуючи два підходи:
1. Жадібний алгоритм (максимізація співвідношення калорій до вартості)
2. Динамічне програмування (оптимальне рішення)
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
import time
import random


# Дані про їжу: назва -> {вартість, калорійність}
ITEMS = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


class FoodSelection:
    """Клас для розв'язання задачі вибору їжі з максимальною калорійністю"""
    
    def __init__(self, items: Dict[str, Dict[str, int]] = None):
        """
        Ініціалізація з даними про їжу
        
        Args:
            items: словник з даними про їжу
        """
        self.items = items or ITEMS
        self.item_names = list(self.items.keys())
        self.costs = [self.items[name]["cost"] for name in self.item_names]
        self.calories = [self.items[name]["calories"] for name in self.item_names]
    
    def greedy_algorithm(self, budget: int, verbose: bool = True) -> Tuple[List[str], int, int]:
        """
        Жадібний алгоритм: вибирає страви з найвищим співвідношенням калорій до вартості
        
        Args:
            budget: доступний бюджет
            verbose: чи виводити детальну інформацію
            
        Returns:
            Tuple[список вибраних страв, загальна вартість, загальна калорійність]
        """
        if verbose:
            print("=== Жадібний алгоритм ===")
            print("Стратегія: максимізація співвідношення калорій/вартість")
            print(f"Бюджет: {budget}")
            print()
        
        # Обчислюємо співвідношення калорій до вартості для кожної страви
        ratios = []
        for name in self.item_names:
            cost = self.items[name]["cost"]
            calories = self.items[name]["calories"]
            ratio = calories / cost
            ratios.append((name, cost, calories, ratio))
        
        # Сортуємо за спаданням співвідношення
        ratios.sort(key=lambda x: x[3], reverse=True)
        
        if verbose:
            print("Співвідношення калорій/вартість (відсортовані):")
            for name, cost, calories, ratio in ratios:
                print(f"  {name}: {calories}/{cost} = {ratio:.2f}")
            print()
        
        selected_items = []
        total_cost = 0
        total_calories = 0
        
        if verbose:
            print("Процес вибору:")
        
        for name, cost, calories, ratio in ratios:
            if total_cost + cost <= budget:
                selected_items.append(name)
                total_cost += cost
                total_calories += calories
                
                if verbose:
                    print(f"  ✓ Додано {name}: вартість {cost}, калорії {calories}")
                    print(f"    Загальна вартість: {total_cost}, загальні калорії: {total_calories}")
            else:
                if verbose:
                    print(f"  ✗ Пропущено {name}: не вміщується в бюджет")
        
        if verbose:
            print(f"\nРезультат жадібного алгоритму:")
            print(f"  Вибрані страви: {selected_items}")
            print(f"  Загальна вартість: {total_cost}")
            print(f"  Загальна калорійність: {total_calories}")
            print(f"  Залишок бюджету: {budget - total_cost}")
        
        return selected_items, total_cost, total_calories
    
    def dynamic_programming(self, budget: int, verbose: bool = True) -> Tuple[List[str], int, int]:
        """
        Динамічне програмування: знаходить оптимальне рішення
        
        Args:
            budget: доступний бюджет
            verbose: чи виводити детальну інформацію
            
        Returns:
            Tuple[список вибраних страв, загальна вартість, загальна калорійність]
        """
        if verbose:
            print("=== Динамічне програмування ===")
            print("Стратегія: оптимальне рішення через повний перебір")
            print(f"Бюджет: {budget}")
            print()
        
        n = len(self.item_names)
        
        # dp[i][w] = максимальна калорійність для перших i страв з бюджетом w
        dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]
        
        # Заповнюємо таблицю DP
        for i in range(1, n + 1):
            item_name = self.item_names[i - 1]
            cost = self.items[item_name]["cost"]
            calories = self.items[item_name]["calories"]
            
            for w in range(budget + 1):
                # Не беремо поточну страву
                dp[i][w] = dp[i - 1][w]
                
                # Беремо поточну страву, якщо вона вміщується в бюджет
                if cost <= w:
                    dp[i][w] = max(dp[i][w], dp[i - 1][w - cost] + calories)
        
        if verbose:
            print("Таблиця динамічного програмування (фрагмент):")
            print("Бюджет: ", end="")
            for w in range(0, min(budget + 1, 21), 5):
                print(f"{w:5d}", end="")
            print()
            
            for i in range(min(n + 1, 6)):
                print(f"Страва {i}: ", end="")
                for w in range(0, min(budget + 1, 21), 5):
                    print(f"{dp[i][w]:5d}", end="")
                print()
            if n > 5:
                print("...")
            print()
        
        # Відновлюємо рішення
        selected_items = []
        w = budget
        total_cost = 0
        total_calories = 0
        
        for i in range(n, 0, -1):
            item_name = self.item_names[i - 1]
            cost = self.items[item_name]["cost"]
            calories = self.items[item_name]["calories"]
            
            if w >= cost and dp[i][w] == dp[i - 1][w - cost] + calories:
                selected_items.append(item_name)
                total_cost += cost
                total_calories += calories
                w -= cost
        
        selected_items.reverse()  # Відновлюємо правильний порядок
        
        if verbose:
            print("Відновлення рішення:")
            for item in selected_items:
                cost = self.items[item]["cost"]
                calories = self.items[item]["calories"]
                print(f"  ✓ {item}: вартість {cost}, калорії {calories}")
            print()
        
        if verbose:
            print(f"Результат динамічного програмування:")
            print(f"  Вибрані страви: {selected_items}")
            print(f"  Загальна вартість: {total_cost}")
            print(f"  Загальна калорійність: {total_calories}")
            print(f"  Залишок бюджету: {budget - total_cost}")
        
        return selected_items, total_cost, total_calories
    
    def compare_algorithms(self, budget: int) -> None:
        """
        Порівнює результати жадібного алгоритму та динамічного програмування
        
        Args:
            budget: доступний бюджет
        """
        print("=" * 60)
        print("ПОРІВНЯННЯ АЛГОРИТМІВ")
        print("=" * 60)
        
        # Запускаємо обидва алгоритми
        start_time = time.time()
        greedy_items, greedy_cost, greedy_calories = self.greedy_algorithm(budget, verbose=False)
        greedy_time = time.time() - start_time
        
        start_time = time.time()
        dp_items, dp_cost, dp_calories = self.dynamic_programming(budget, verbose=False)
        dp_time = time.time() - start_time
        
        # Виводимо порівняння
        print(f"Бюджет: {budget}")
        print()
        
        print("ЖАДІБНИЙ АЛГОРИТМ:")
        print(f"  Вибрані страви: {greedy_items}")
        print(f"  Загальна вартість: {greedy_cost}")
        print(f"  Загальна калорійність: {greedy_calories}")
        print(f"  Час виконання: {greedy_time:.6f} секунд")
        print()
        
        print("ДИНАМІЧНЕ ПРОГРАМУВАННЯ:")
        print(f"  Вибрані страви: {dp_items}")
        print(f"  Загальна вартість: {dp_cost}")
        print(f"  Загальна калорійність: {dp_calories}")
        print(f"  Час виконання: {dp_time:.6f} секунд")
        print()
        
        # Аналіз результатів
        print("АНАЛІЗ:")
        if dp_calories > greedy_calories:
            improvement = ((dp_calories - greedy_calories) / greedy_calories) * 100
            print(f"  ✓ Динамічне програмування краще на {improvement:.1f}% калорій")
        elif greedy_calories > dp_calories:
            print("  ⚠ Жадібний алгоритм дав кращий результат (неочікувано)")
        else:
            print("  = Обидва алгоритми дали однаковий результат")
        
        if dp_time > greedy_time:
            speedup = dp_time / greedy_time
            print(f"  ⏱ Жадібний алгоритм швидший у {speedup:.1f} разів")
        else:
            speedup = greedy_time / dp_time
            print(f"  ⏱ Динамічне програмування швидше у {speedup:.1f} разів")
        
        print()
    
    def visualize_comparison(self, budgets: List[int]) -> None:
        """
        Візуалізує порівняння алгоритмів для різних бюджетів
        
        Args:
            budgets: список бюджетів для тестування
        """
        greedy_calories = []
        dp_calories = []
        greedy_times = []
        dp_times = []
        
        print("Тестування на різних бюджетах...")
        
        for budget in budgets:
            # Жадібний алгоритм
            start_time = time.time()
            _, _, calories = self.greedy_algorithm(budget, verbose=False)
            greedy_time = time.time() - start_time
            
            greedy_calories.append(calories)
            greedy_times.append(greedy_time)
            
            # Динамічне програмування
            start_time = time.time()
            _, _, calories = self.dynamic_programming(budget, verbose=False)
            dp_time = time.time() - start_time
            
            dp_calories.append(calories)
            dp_times.append(dp_time)
        
        # Створюємо графіки
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Графік 1: Калорійність
        ax1.plot(budgets, greedy_calories, 'o-', label='Жадібний алгоритм', linewidth=2, markersize=6)
        ax1.plot(budgets, dp_calories, 's-', label='Динамічне програмування', linewidth=2, markersize=6)
        ax1.set_xlabel('Бюджет')
        ax1.set_ylabel('Калорійність')
        ax1.set_title('Порівняння калорійності')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Графік 2: Час виконання
        ax2.plot(budgets, greedy_times, 'o-', label='Жадібний алгоритм', linewidth=2, markersize=6)
        ax2.plot(budgets, dp_times, 's-', label='Динамічне програмування', linewidth=2, markersize=6)
        ax2.set_xlabel('Бюджет')
        ax2.set_ylabel('Час виконання (секунди)')
        ax2.set_title('Порівняння часу виконання')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Графік 3: Ефективність (калорії/час)
        greedy_efficiency = [c/t if t > 0 else 0 for c, t in zip(greedy_calories, greedy_times)]
        dp_efficiency = [c/t if t > 0 else 0 for c, t in zip(dp_calories, dp_times)]
        
        ax3.plot(budgets, greedy_efficiency, 'o-', label='Жадібний алгоритм', linewidth=2, markersize=6)
        ax3.plot(budgets, dp_efficiency, 's-', label='Динамічне програмування', linewidth=2, markersize=6)
        ax3.set_xlabel('Бюджет')
        ax3.set_ylabel('Ефективність (калорії/секунда)')
        ax3.set_title('Ефективність алгоритмів')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Графік 4: Різниця в калорійності
        difference = [dp - greedy for dp, greedy in zip(dp_calories, greedy_calories)]
        ax4.bar(budgets, difference, alpha=0.7, color='green' if max(difference) > 0 else 'red')
        ax4.set_xlabel('Бюджет')
        ax4.set_ylabel('Різниця в калорійності (DP - Greedy)')
        ax4.set_title('Перевага динамічного програмування')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def analyze_items(self) -> None:
        """Аналізує дані про страви"""
        print("=== АНАЛІЗ СТРАВ ===")
        print()
        
        # Сортуємо за різними критеріями
        by_cost = sorted(self.item_names, key=lambda x: self.items[x]["cost"])
        by_calories = sorted(self.item_names, key=lambda x: self.items[x]["calories"], reverse=True)
        by_ratio = sorted(self.item_names, key=lambda x: self.items[x]["calories"] / self.items[x]["cost"], reverse=True)
        
        print("Сортировка за вартістю (від дешевих до дорогих):")
        for name in by_cost:
            cost = self.items[name]["cost"]
            calories = self.items[name]["calories"]
            ratio = calories / cost
            print(f"  {name}: {cost} грн, {calories} кал, співвідношення {ratio:.2f}")
        print()
        
        print("Сортировка за калорійністю (від високих до низьких):")
        for name in by_calories:
            cost = self.items[name]["cost"]
            calories = self.items[name]["calories"]
            ratio = calories / cost
            print(f"  {name}: {calories} кал, {cost} грн, співвідношення {ratio:.2f}")
        print()
        
        print("Сортировка за співвідношенням калорії/вартість (оптимальні для жадібного алгоритму):")
        for name in by_ratio:
            cost = self.items[name]["cost"]
            calories = self.items[name]["calories"]
            ratio = calories / cost
            print(f"  {name}: {ratio:.2f} ({calories}/{cost})")
        print()
        
        # Статистика
        total_cost = sum(self.items[name]["cost"] for name in self.item_names)
        total_calories = sum(self.items[name]["calories"] for name in self.item_names)
        avg_ratio = total_calories / total_cost
        
        print("ЗАГАЛЬНА СТАТИСТИКА:")
        print(f"  Кількість страв: {len(self.item_names)}")
        print(f"  Загальна вартість всіх страв: {total_cost} грн")
        print(f"  Загальна калорійність всіх страв: {total_calories} кал")
        print(f"  Середнє співвідношення калорії/вартість: {avg_ratio:.2f}")
        print()


def create_custom_items() -> Dict[str, Dict[str, int]]:
    """Створює кастомний набір страв"""
    print("Створення кастомного набору страв:")
    print("Введіть дані про страви (порожній рядок для завершення):")
    
    items = {}
    while True:
        name = input("Назва страви: ").strip()
        if not name:
            break
        
        try:
            cost = int(input("Вартість: "))
            calories = int(input("Калорійність: "))
            items[name] = {"cost": cost, "calories": calories}
            print(f"Додано: {name} - {cost} грн, {calories} кал")
        except ValueError:
            print("Помилка: введіть правильні числа!")
    
    return items


def demo_algorithms():
    """Демонстрація роботи алгоритмів"""
    print("=== ДЕМОНСТРАЦІЯ АЛГОРИТМІВ ===")
    
    food_selection = FoodSelection()
    
    # Аналізуємо страви
    food_selection.analyze_items()
    
    # Тестуємо на різних бюджетах
    test_budgets = [30, 50, 80, 100, 150]
    
    for budget in test_budgets:
        print(f"\n{'='*50}")
        print(f"ТЕСТ З БЮДЖЕТОМ {budget}")
        print('='*50)
        food_selection.compare_algorithms(budget)
    
    # Візуалізація
    print("\nСтворення візуалізації...")
    food_selection.visualize_comparison(test_budgets)


def interactive_mode():
    """Інтерактивний режим роботи"""
    print("=== ІНТЕРАКТИВНИЙ РЕЖИМ ===")
    
    # Вибір набору страв
    print("\nВиберіть набір страв:")
    print("1. Стандартний набір")
    print("2. Кастомний набір")
    
    choice = input("Ваш вибір (1-2): ").strip()
    
    if choice == '2':
        items = create_custom_items()
        if not items:
            print("Створено порожній набір, використовуємо стандартний")
            items = ITEMS
    else:
        items = ITEMS
    
    food_selection = FoodSelection(items)
    
    while True:
        print(f"\n{'='*40}")
        print("МЕНЮ")
        print('='*40)
        print("1. Аналіз страв")
        print("2. Жадібний алгоритм")
        print("3. Динамічне програмування")
        print("4. Порівняння алгоритмів")
        print("5. Візуалізація для різних бюджетів")
        print("6. Змінити набір страв")
        print("7. Вихід")
        
        choice = input("\nВаш вибір (1-7): ").strip()
        
        try:
            if choice == '1':
                food_selection.analyze_items()
                
            elif choice == '2':
                budget = int(input("Введіть бюджет: "))
                food_selection.greedy_algorithm(budget)
                
            elif choice == '3':
                budget = int(input("Введіть бюджет: "))
                food_selection.dynamic_programming(budget)
                
            elif choice == '4':
                budget = int(input("Введіть бюджет: "))
                food_selection.compare_algorithms(budget)
                
            elif choice == '5':
                print("Введіть бюджети через пробіл (наприклад: 30 50 80 100):")
                budgets_input = input().strip()
                try:
                    budgets = [int(x) for x in budgets_input.split()]
                    if budgets:
                        food_selection.visualize_comparison(budgets)
                    else:
                        print("Не введено жодного бюджету!")
                except ValueError:
                    print("Помилка: введіть правильні числа!")
                    
            elif choice == '6':
                items = create_custom_items()
                if items:
                    food_selection = FoodSelection(items)
                    print("Набір страв змінено!")
                else:
                    print("Скасовано")
                    
            elif choice == '7':
                print("Дякуємо за використання програми!")
                break
                
            else:
                print("Будь ласка, виберіть опцію від 1 до 7!")
                
        except ValueError:
            print("Помилка: введіть правильне число!")
        except KeyboardInterrupt:
            print("\n\nПрограма перервана користувачем.")
            break
        except Exception as e:
            print(f"Виникла помилка: {e}")


def analyze_algorithm_complexity():
    """Аналіз складності алгоритмів"""
    print("=== АНАЛІЗ СКЛАДНОСТІ АЛГОРИТМІВ ===")
    print()
    
    print("ЖАДІБНИЙ АЛГОРИТМ:")
    print("  Часова складність: O(n log n)")
    print("    - Сортування страв за співвідношенням: O(n log n)")
    print("    - Прохід по відсортованому списку: O(n)")
    print("  Просторова складність: O(n)")
    print("    - Зберігання відсортованого списку: O(n)")
    print("  Переваги:")
    print("    - Швидкий виконання")
    print("    - Простий у реалізації")
    print("    - Ефективний для великих наборів даних")
    print("  Недоліки:")
    print("    - Не завжди дає оптимальне рішення")
    print("    - Може пропустити кращі комбінації")
    print()
    
    print("ДИНАМІЧНЕ ПРОГРАМУВАННЯ:")
    print("  Часова складність: O(n × W)")
    print("    - n: кількість страв")
    print("    - W: максимальний бюджет")
    print("  Просторова складність: O(n × W)")
    print("    - Таблиця DP розміром n × W")
    print("  Переваги:")
    print("    - Завжди дає оптимальне рішення")
    print("    - Гарантована правильність")
    print("    - Можна відновити точний набір страв")
    print("  Недоліки:")
    print("    - Більша складність реалізації")
    print("    - Вимагає більше пам'яті")
    print("    - Може бути повільним для великих бюджетів")
    print()
    
    print("ПОРІВНЯННЯ:")
    print("  Жадібний алгоритм кращий для:")
    print("    - Великих наборів страв")
    print("    - Обмеженої пам'яті")
    print("    - Швидкого отримання приблизного рішення")
    print("  Динамічне програмування краще для:")
    print("    - Невеликих бюджетів")
    print("    - Коли потрібне оптимальне рішення")
    print("    - Коли важлива точність")
    print()


def main():
    """Головна функція програми"""
    print("Програма для вибору їжі з максимальною калорійністю")
    print("Жадібні алгоритми vs Динамічне програмування")
    print("=" * 60)
    
    while True:
        print("\nВиберіть режим роботи:")
        print("1. Демонстрація алгоритмів")
        print("2. Інтерактивний режим")
        print("3. Аналіз складності алгоритмів")
        print("4. Швидкий тест зі стандартним набором")
        print("5. Вихід")
        
        choice = input("\nВаш вибір (1-5): ").strip()
        
        if choice == '1':
            demo_algorithms()
        elif choice == '2':
            interactive_mode()
        elif choice == '3':
            analyze_algorithm_complexity()
        elif choice == '4':
            print("\n=== ШВИДКИЙ ТЕСТ ===")
            food_selection = FoodSelection()
            budget = int(input("Введіть бюджет для тесту: "))
            food_selection.compare_algorithms(budget)
        elif choice == '5':
            print("Дякуємо за використання програми!")
            break
        else:
            print("Будь ласка, виберіть опцію від 1 до 5!")


if __name__ == "__main__":
    main()
