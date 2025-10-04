"""
Завдання 7. Використання методу Монте-Карло

Програма для симуляції кидків кубиків з використанням методу Монте-Карло.
Обчислює ймовірності різних сум при киданні двох кубиків та порівнює
експериментальні результати з теоретичними.
"""

import random
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple
import time
from collections import Counter
import pandas as pd


class DiceSimulation:
    """Клас для симуляції кидків кубиків методом Монте-Карло"""
    
    def __init__(self, num_dice: int = 2, sides: int = 6):
        """
        Ініціалізація симуляції
        
        Args:
            num_dice: кількість кубиків
            sides: кількість граней на кубику
        """
        self.num_dice = num_dice
        self.sides = sides
        self.min_sum = num_dice
        self.max_sum = num_dice * sides
        self.possible_sums = list(range(self.min_sum, self.max_sum + 1))
        
        # Теоретичні ймовірності для двох кубиків
        self.theoretical_probabilities = self._calculate_theoretical_probabilities()
    
    def _calculate_theoretical_probabilities(self) -> Dict[int, float]:
        """Обчислює теоретичні ймовірності для всіх можливих сум"""
        if self.num_dice == 2 and self.sides == 6:
            # Для двох кубиків з 6 гранями
            theoretical = {
                2: 1/36,   # (1,1)
                3: 2/36,   # (1,2), (2,1)
                4: 3/36,   # (1,3), (2,2), (3,1)
                5: 4/36,   # (1,4), (2,3), (3,2), (4,1)
                6: 5/36,   # (1,5), (2,4), (3,3), (4,2), (5,1)
                7: 6/36,   # (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
                8: 5/36,   # (2,6), (3,5), (4,4), (5,3), (6,2)
                9: 4/36,   # (3,6), (4,5), (5,4), (6,3)
                10: 3/36,  # (4,6), (5,5), (6,4)
                11: 2/36,  # (5,6), (6,5)
                12: 1/36   # (6,6)
            }
        else:
            # Загальний випадок (менш ефективний, але універсальний)
            theoretical = {}
            total_combinations = self.sides ** self.num_dice
            
            for target_sum in self.possible_sums:
                count = self._count_combinations(target_sum)
                theoretical[target_sum] = count / total_combinations
        
        return theoretical
    
    def _count_combinations(self, target_sum: int) -> int:
        """Рекурсивно підраховує кількість комбінацій для заданої суми"""
        def count_recursive(remaining_dice: int, remaining_sum: int) -> int:
            if remaining_dice == 0:
                return 1 if remaining_sum == 0 else 0
            
            if remaining_sum < remaining_dice or remaining_sum > remaining_dice * self.sides:
                return 0
            
            total = 0
            for face_value in range(1, self.sides + 1):
                total += count_recursive(remaining_dice - 1, remaining_sum - face_value)
            
            return total
        
        return count_recursive(self.num_dice, target_sum)
    
    def roll_dice(self) -> int:
        """Симулює кидок кубиків та повертає суму"""
        return sum(random.randint(1, self.sides) for _ in range(self.num_dice))
    
    def simulate(self, num_rolls: int, verbose: bool = True) -> Dict[int, float]:
        """
        Проводить симуляцію Монте-Карло
        
        Args:
            num_rolls: кількість кидків для симуляції
            verbose: чи виводити детальну інформацію
            
        Returns:
            Словник з експериментальними ймовірностями
        """
        if verbose:
            print(f"=== СИМУЛЯЦІЯ МОНТЕ-КАРЛО ===")
            print(f"Кількість кубиків: {self.num_dice}")
            print(f"Граней на кубику: {self.sides}")
            print(f"Кількість кидків: {num_rolls:,}")
            print(f"Можливі суми: {self.min_sum} - {self.max_sum}")
            print()
        
        # Симуляція кидків
        start_time = time.time()
        sums = []
        
        if verbose:
            print("Проведення симуляції...")
            progress_interval = max(1, num_rolls // 10)
        
        for i in range(num_rolls):
            sums.append(self.roll_dice())
            
            if verbose and (i + 1) % progress_interval == 0:
                progress = (i + 1) / num_rolls * 100
                print(f"Прогрес: {progress:.1f}% ({i + 1:,}/{num_rolls:,})")
        
        simulation_time = time.time() - start_time
        
        # Підрахунок частоти кожної суми
        sum_counts = Counter(sums)
        
        # Обчислення експериментальних ймовірностей
        experimental_probabilities = {}
        for sum_value in self.possible_sums:
            count = sum_counts.get(sum_value, 0)
            probability = count / num_rolls
            experimental_probabilities[sum_value] = probability
        
        if verbose:
            print(f"\nСимуляція завершена за {simulation_time:.3f} секунд")
            print(f"Середня швидкість: {num_rolls/simulation_time:,.0f} кидків/сек")
            print()
        
        return experimental_probabilities
    
    def compare_probabilities(self, experimental: Dict[int, float], 
                            num_rolls: int, verbose: bool = True) -> None:
        """
        Порівнює експериментальні та теоретичні ймовірності
        
        Args:
            experimental: експериментальні ймовірності
            num_rolls: кількість кидків (для обчислення похибки)
            verbose: чи виводити детальну інформацію
        """
        if verbose:
            print("=== ПОРІВНЯННЯ ЙМОВІРНОСТЕЙ ===")
            print()
        
        # Створюємо таблицю порівняння
        comparison_data = []
        total_error = 0
        
        for sum_value in self.possible_sums:
            theoretical = self.theoretical_probabilities[sum_value]
            experimental_prob = experimental[sum_value]
            
            # Обчислюємо абсолютну та відносну похибку
            absolute_error = abs(experimental_prob - theoretical)
            relative_error = (absolute_error / theoretical * 100) if theoretical > 0 else 0
            
            # Стандартна похибка (для нормального розподілу)
            standard_error = np.sqrt(theoretical * (1 - theoretical) / num_rolls)
            z_score = absolute_error / standard_error if standard_error > 0 else 0
            
            total_error += absolute_error
            
            comparison_data.append({
                'Сума': sum_value,
                'Теоретична': theoretical,
                'Експериментальна': experimental_prob,
                'Абс. похибка': absolute_error,
                'Відн. похибка (%)': relative_error,
                'Z-статистика': z_score
            })
        
        if verbose:
            # Виводимо таблицю
            df = pd.DataFrame(comparison_data)
            print(df.to_string(index=False, float_format='%.4f'))
            print()
            
            # Статистика
            avg_error = total_error / len(self.possible_sums)
            max_error = max(row['Абс. похибка'] for row in comparison_data)
            max_relative_error = max(row['Відн. похибка (%)'] for row in comparison_data)
            
            print("СТАТИСТИКА ПОХИБОК:")
            print(f"  Середня абсолютна похибка: {avg_error:.6f}")
            print(f"  Максимальна абсолютна похибка: {max_error:.6f}")
            print(f"  Максимальна відносна похибка: {max_relative_error:.2f}%")
            print(f"  Загальна абсолютна похибка: {total_error:.6f}")
            
            # Оцінка якості симуляції
            if avg_error < 0.01:
                quality = "Відмінна"
            elif avg_error < 0.05:
                quality = "Добра"
            elif avg_error < 0.1:
                quality = "Задовільна"
            else:
                quality = "Погана"
            
            print(f"  Якість симуляції: {quality}")
            print()
    
    def visualize_results(self, experimental: Dict[int, float], 
                         num_rolls: int, save_plot: bool = False) -> None:
        """
        Створює візуалізацію результатів симуляції
        
        Args:
            experimental: експериментальні ймовірності
            num_rolls: кількість кидків
            save_plot: чи зберегти графік у файл
        """
        sums = list(self.possible_sums)
        theoretical_probs = [self.theoretical_probabilities[s] for s in sums]
        experimental_probs = [experimental[s] for s in sums]
        
        # Створюємо графік з двома підграфіками
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Графік 1: Порівняння ймовірностей
        x = np.arange(len(sums))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, theoretical_probs, width, 
                       label='Теоретична', alpha=0.8, color='skyblue')
        bars2 = ax1.bar(x + width/2, experimental_probs, width, 
                       label='Експериментальна', alpha=0.8, color='lightcoral')
        
        ax1.set_xlabel('Сума кубиків')
        ax1.set_ylabel('Ймовірність')
        ax1.set_title(f'Порівняння ймовірностей (n={num_rolls:,})')
        ax1.set_xticks(x)
        ax1.set_xticklabels(sums)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Додаємо значення на стовпці
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=8)
        
        for bar in bars2:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=8)
        
        # Графік 2: Похибка
        errors = [abs(exp - theo) for exp, theo in zip(experimental_probs, theoretical_probs)]
        ax2.bar(sums, errors, alpha=0.7, color='red')
        ax2.set_xlabel('Сума кубиків')
        ax2.set_ylabel('Абсолютна похибка')
        ax2.set_title('Похибка експериментальних результатів')
        ax2.grid(True, alpha=0.3)
        
        # Додаємо значення похибки на стовпці
        for i, error in enumerate(errors):
            ax2.text(sums[i], error + 0.0001, f'{error:.4f}', 
                    ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        if save_plot:
            filename = f'dice_simulation_{num_rolls}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Графік збережено як {filename}")
        
        plt.show()
    
    def convergence_analysis(self, max_rolls: int = 100000, 
                           step: int = 10000) -> None:
        """
        Аналізує збіжність експериментальних результатів до теоретичних
        
        Args:
            max_rolls: максимальна кількість кидків
            step: крок для аналізу збіжності
        """
        print("=== АНАЛІЗ ЗБІЖНОСТІ ===")
        print(f"Максимальна кількість кидків: {max_rolls:,}")
        print(f"Крок аналізу: {step:,}")
        print()
        
        roll_counts = list(range(step, max_rolls + 1, step))
        convergence_data = []
        
        print("Проведення аналізу збіжності...")
        
        for num_rolls in roll_counts:
            # Проводимо симуляцію
            experimental = self.simulate(num_rolls, verbose=False)
            
            # Обчислюємо середню абсолютну похибку
            total_error = 0
            for sum_value in self.possible_sums:
                theoretical = self.theoretical_probabilities[sum_value]
                experimental_prob = experimental[sum_value]
                total_error += abs(experimental_prob - theoretical)
            
            avg_error = total_error / len(self.possible_sums)
            convergence_data.append((num_rolls, avg_error))
            
            print(f"Кидків: {num_rolls:,}, Середня похибка: {avg_error:.6f}")
        
        # Візуалізуємо збіжність
        rolls, errors = zip(*convergence_data)
        
        plt.figure(figsize=(12, 6))
        plt.plot(rolls, errors, 'o-', linewidth=2, markersize=4)
        plt.xlabel('Кількість кидків')
        plt.ylabel('Середня абсолютна похибка')
        plt.title('Збіжність експериментальних результатів до теоретичних')
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.xscale('log')
        
        # Додаємо теоретичну лінію збіжності (1/sqrt(n))
        theoretical_convergence = [1/np.sqrt(n) for n in rolls]
        plt.plot(rolls, theoretical_convergence, 'r--', 
                label='Теоретична збіжність (1/√n)', alpha=0.7)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
        print("\nАналіз збіжності завершено!")
    
    def statistical_tests(self, experimental: Dict[int, float], 
                         num_rolls: int) -> None:
        """
        Проводить статистичні тести для перевірки якості симуляції
        
        Args:
            experimental: експериментальні ймовірності
            num_rolls: кількість кидків
        """
        print("=== СТАТИСТИЧНІ ТЕСТИ ===")
        print()
        
        # Тест хі-квадрат
        chi_square_stat = 0
        degrees_of_freedom = len(self.possible_sums) - 1
        
        print("Тест хі-квадрат:")
        for sum_value in self.possible_sums:
            theoretical = self.theoretical_probabilities[sum_value]
            experimental_prob = experimental[sum_value]
            expected_count = theoretical * num_rolls
            observed_count = experimental_prob * num_rolls
            
            if expected_count > 0:
                chi_square_stat += (observed_count - expected_count) ** 2 / expected_count
        
        print(f"  Статистика хі-квадрат: {chi_square_stat:.4f}")
        print(f"  Ступені свободи: {degrees_of_freedom}")
        
        # Критичні значення для різних рівнів значущості
        critical_values = {
            0.05: 19.68,  # α = 0.05
            0.01: 24.72,  # α = 0.01
            0.001: 31.26  # α = 0.001
        }
        
        print("  Критичні значення:")
        for alpha, critical in critical_values.items():
            result = "✓ Приймається" if chi_square_stat < critical else "✗ Відхиляється"
            print(f"    α = {alpha}: {critical:.2f} ({result})")
        
        # Тест Колмогорова-Смирнова (спрощена версія)
        print("\nТест Колмогорова-Смирнова:")
        
        # Сортуємо суми
        sorted_sums = sorted(self.possible_sums)
        theoretical_cdf = []
        experimental_cdf = []
        
        cumulative_theoretical = 0
        cumulative_experimental = 0
        
        for sum_value in sorted_sums:
            cumulative_theoretical += self.theoretical_probabilities[sum_value]
            cumulative_experimental += experimental[sum_value]
            theoretical_cdf.append(cumulative_theoretical)
            experimental_cdf.append(cumulative_experimental)
        
        ks_statistic = max(abs(exp - theo) for exp, theo in 
                          zip(experimental_cdf, theoretical_cdf))
        
        print(f"  Статистика KS: {ks_statistic:.6f}")
        
        # Критичні значення для KS тесту
        ks_critical = 1.36 / np.sqrt(num_rolls)  # Приблизно для α = 0.05
        print(f"  Критичне значення (α=0.05): {ks_critical:.6f}")
        
        if ks_statistic < ks_critical:
            print("  ✓ Розподіл відповідає теоретичному")
        else:
            print("  ✗ Розподіл не відповідає теоретичному")
        
        print()


def demo_basic_simulation():
    """Демонстрація базової симуляції"""
    print("=== ДЕМОНСТРАЦІЯ БАЗОВОЇ СИМУЛЯЦІЇ ===")
    
    # Створюємо симуляцію
    simulation = DiceSimulation()
    
    # Різні кількості кидків для порівняння
    test_rolls = [1000, 10000, 100000]
    
    for num_rolls in test_rolls:
        print(f"\n{'='*50}")
        print(f"СИМУЛЯЦІЯ З {num_rolls:,} КИДКАМИ")
        print('='*50)
        
        # Проводимо симуляцію
        experimental = simulation.simulate(num_rolls)
        
        # Порівнюємо з теоретичними значеннями
        simulation.compare_probabilities(experimental, num_rolls)
        
        # Візуалізуємо результати
        simulation.visualize_results(experimental, num_rolls)


def demo_convergence():
    """Демонстрація аналізу збіжності"""
    print("=== ДЕМОНСТРАЦІЯ АНАЛІЗУ ЗБІЖНОСТІ ===")
    
    simulation = DiceSimulation()
    simulation.convergence_analysis(max_rolls=50000, step=5000)


def demo_statistical_tests():
    """Демонстрація статистичних тестів"""
    print("=== ДЕМОНСТРАЦІЯ СТАТИСТИЧНИХ ТЕСТІВ ===")
    
    simulation = DiceSimulation()
    
    # Проводимо симуляцію
    num_rolls = 10000
    experimental = simulation.simulate(num_rolls)
    
    # Порівнюємо результати
    simulation.compare_probabilities(experimental, num_rolls)
    
    # Проводимо статистичні тести
    simulation.statistical_tests(experimental, num_rolls)


def interactive_mode():
    """Інтерактивний режим роботи"""
    print("=== ІНТЕРАКТИВНИЙ РЕЖИМ ===")
    
    while True:
        print("\n" + "="*40)
        print("МЕНЮ")
        print("="*40)
        print("1. Базова симуляція")
        print("2. Аналіз збіжності")
        print("3. Статистичні тести")
        print("4. Кастомна симуляція")
        print("5. Порівняння різних кількостей кидків")
        print("6. Вихід")
        
        choice = input("\nВаш вибір (1-6): ").strip()
        
        try:
            if choice == '1':
                demo_basic_simulation()
                
            elif choice == '2':
                demo_convergence()
                
            elif choice == '3':
                demo_statistical_tests()
                
            elif choice == '4':
                num_rolls = int(input("Введіть кількість кидків: "))
                simulation = DiceSimulation()
                experimental = simulation.simulate(num_rolls)
                simulation.compare_probabilities(experimental, num_rolls)
                simulation.visualize_results(experimental, num_rolls)
                
            elif choice == '5':
                print("Введіть кількості кидків через пробіл (наприклад: 1000 10000 100000):")
                rolls_input = input().strip()
                try:
                    rolls_list = [int(x) for x in rolls_input.split()]
                    if rolls_list:
                        simulation = DiceSimulation()
                        
                        for num_rolls in rolls_list:
                            print(f"\n{'='*50}")
                            print(f"СИМУЛЯЦІЯ З {num_rolls:,} КИДКАМИ")
                            print('='*50)
                            
                            experimental = simulation.simulate(num_rolls, verbose=False)
                            simulation.compare_probabilities(experimental, num_rolls, verbose=False)
                            simulation.visualize_results(experimental, num_rolls)
                    else:
                        print("Не введено жодної кількості кидків!")
                except ValueError:
                    print("Помилка: введіть правильні числа!")
                    
            elif choice == '6':
                print("Дякуємо за використання програми!")
                break
                
            else:
                print("Будь ласка, виберіть опцію від 1 до 6!")
                
        except ValueError:
            print("Помилка: введіть правильне число!")
        except KeyboardInterrupt:
            print("\n\nПрограма перервана користувачем.")
            break
        except Exception as e:
            print(f"Виникла помилка: {e}")


def analyze_theoretical_probabilities():
    """Аналіз теоретичних ймовірностей"""
    print("=== АНАЛІЗ ТЕОРЕТИЧНИХ ЙМОВІРНОСТЕЙ ===")
    
    simulation = DiceSimulation()
    
    print("Теоретичні ймовірності для двох кубиків:")
    print()
    
    # Створюємо таблицю
    data = []
    for sum_value in simulation.possible_sums:
        prob = simulation.theoretical_probabilities[sum_value]
        percentage = prob * 100
        combinations = int(prob * 36)  # Для двох кубиків
        
        data.append({
            'Сума': sum_value,
            'Ймовірність': f"{prob:.4f}",
            'Відсоток': f"{percentage:.2f}%",
            'Комбінації': f"{combinations}/36"
        })
    
    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    print()
    
    # Статистика
    total_prob = sum(simulation.theoretical_probabilities.values())
    print(f"Сума всіх ймовірностей: {total_prob:.6f}")
    print(f"Найбільш ймовірна сума: {max(simulation.possible_sums, key=lambda x: simulation.theoretical_probabilities[x])}")
    print(f"Найменш ймовірна сума: {min(simulation.possible_sums, key=lambda x: simulation.theoretical_probabilities[x])}")
    print()


def main():
    """Головна функція програми"""
    print("Програма симуляції кидків кубиків методом Монте-Карло")
    print("=" * 60)
    
    while True:
        print("\nВиберіть режим роботи:")
        print("1. Демонстрація базової симуляції")
        print("2. Аналіз збіжності")
        print("3. Статистичні тести")
        print("4. Аналіз теоретичних ймовірностей")
        print("5. Інтерактивний режим")
        print("6. Швидкий тест")
        print("7. Вихід")
        
        choice = input("\nВаш вибір (1-7): ").strip()
        
        if choice == '1':
            demo_basic_simulation()
        elif choice == '2':
            demo_convergence()
        elif choice == '3':
            demo_statistical_tests()
        elif choice == '4':
            analyze_theoretical_probabilities()
        elif choice == '5':
            interactive_mode()
        elif choice == '6':
            print("\n=== ШВИДКИЙ ТЕСТ ===")
            simulation = DiceSimulation()
            num_rolls = int(input("Введіть кількість кидків: "))
            experimental = simulation.simulate(num_rolls)
            simulation.compare_probabilities(experimental, num_rolls)
            simulation.visualize_results(experimental, num_rolls)
        elif choice == '7':
            print("Дякуємо за використання програми!")
            break
        else:
            print("Будь ласка, виберіть опцію від 1 до 7!")


if __name__ == "__main__":
    main()
