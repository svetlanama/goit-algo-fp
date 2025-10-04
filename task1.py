"""
Завдання 1. Структури даних. Сортування. Робота з однозв'язним списком

Для реалізації однозв'язного списку необхідно:
1. написати функцію, яка реалізує реверсування однозв'язного списку, змінюючи посилання між вузлами
2. розробити алгоритм сортування для однозв'язного списку, наприклад, сортування вставками або злиттям
3. написати функцію, що об'єднує два відсортовані однозв'язні списки в один відсортований список
"""


class ListNode:
    """Клас для представлення вузла однозв'язного списку"""
    
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    """Клас для представлення однозв'язного списку"""
    
    def __init__(self):
        self.head = None
    
    def append(self, data):
        """Додає новий елемент в кінець списку"""
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def prepend(self, data):
        """Додає новий елемент на початок списку"""
        new_node = ListNode(data)
        new_node.next = self.head
        self.head = new_node
    
    def display(self):
        """Виводить всі елементи списку"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements) + " -> None"
    
    def to_list(self):
        """Конвертує список в Python list для зручності тестування"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    @classmethod
    def from_list(cls, data_list):
        """Створює список з Python list"""
        linked_list = cls()
        for item in data_list:
            linked_list.append(item)
        return linked_list


def reverse_linked_list(head):
    """
    Функція для реверсування однозв'язного списку
    
    Args:
        head: початок списку (ListNode)
    
    Returns:
        нова голова реверсованого списку
    """
    if not head or not head.next:
        return head
    
    prev = None
    current = head
    
    while current:
        next_temp = current.next  # зберігаємо посилання на наступний вузол
        current.next = prev       # змінюємо посилання на попередній вузол
        prev = current           # переміщуємо prev на поточний вузол
        current = next_temp      # переміщуємо current на наступний вузол
    
    return prev


def insertion_sort_linked_list(head):
    """
    Сортування вставками для однозв'язного списку
    
    Args:
        head: початок списку (ListNode)
    
    Returns:
        нова голова відсортованого списку
    """
    if not head or not head.next:
        return head
    
    # Створюємо dummy вузол для спрощення логіки
    dummy = ListNode(0)
    dummy.next = head
    current = head.next
    last_sorted = head
    
    while current:
        if current.data >= last_sorted.data:
            # Елемент вже в правильному місці
            last_sorted = current
            current = current.next
        else:
            # Потрібно вставити елемент в відсортовану частину
            # Видаляємо поточний вузол
            last_sorted.next = current.next
            
            # Знаходимо правильне місце для вставки
            prev = dummy
            while prev.next.data < current.data:
                prev = prev.next
            
            # Вставляємо вузол
            current.next = prev.next
            prev.next = current
            
            # Переміщуємо current на наступний елемент
            current = last_sorted.next
    
    return dummy.next


def merge_sorted_lists(head1, head2):
    """
    Об'єднує два відсортовані однозв'язні списки в один відсортований список
    
    Args:
        head1: голова першого відсортованого списку
        head2: голова другого відсортованого списку
    
    Returns:
        голова об'єднаного відсортованого списку
    """
    # Створюємо dummy вузол для спрощення логіки
    dummy = ListNode(0)
    tail = dummy
    
    # Порівнюємо елементи з обох списків і об'єднуємо їх
    while head1 and head2:
        if head1.data <= head2.data:
            tail.next = head1
            head1 = head1.next
        else:
            tail.next = head2
            head2 = head2.next
        tail = tail.next
    
    # Додаємо залишкові елементи з першого або другого списку
    if head1:
        tail.next = head1
    elif head2:
        tail.next = head2
    
    return dummy.next


def test_linked_list_functionality():
    """Тестування всіх функцій"""
    print("=== Тестування однозв'язного списку ===\n")
    
    # Тест 1: Створення списку та додавання елементів
    print("1. Створення списку та додавання елементів:")
    ll = LinkedList()
    ll.append(3)
    ll.append(1)
    ll.append(4)
    ll.append(2)
    ll.prepend(0)
    print(f"Список: {ll.display()}")
    print()
    
    # Тест 2: Реверсування списку
    print("2. Реверсування списку:")
    print(f"Оригінальний список: {ll.display()}")
    reversed_head = reverse_linked_list(ll.head)
    
    # Створюємо новий список для відображення реверсованого
    reversed_ll = LinkedList()
    reversed_ll.head = reversed_head
    print(f"Реверсований список: {reversed_ll.display()}")
    print()
    
    # Тест 3: Сортування вставками
    print("3. Сортування вставками:")
    ll2 = LinkedList.from_list([5, 2, 8, 1, 9, 3])
    print(f"До сортування: {ll2.display()}")
    sorted_head = insertion_sort_linked_list(ll2.head)
    
    sorted_ll = LinkedList()
    sorted_ll.head = sorted_head
    print(f"Після сортування: {sorted_ll.display()}")
    print()
    
    # Тест 4: Об'єднання двох відсортованих списків
    print("4. Об'єднання двох відсортованих списків:")
    list1 = LinkedList.from_list([1, 3, 5, 7])
    list2 = LinkedList.from_list([2, 4, 6, 8])
    print(f"Список 1: {list1.display()}")
    print(f"Список 2: {list2.display()}")
    
    merged_head = merge_sorted_lists(list1.head, list2.head)
    merged_ll = LinkedList()
    merged_ll.head = merged_head
    print(f"Об'єднаний список: {merged_ll.display()}")
    print()
    
    # Тест 5: Об'єднання списків різної довжини
    print("5. Об'єднання списків різної довжини:")
    list3 = LinkedList.from_list([1, 5, 9])
    list4 = LinkedList.from_list([2, 3, 6, 7, 10, 11])
    print(f"Список 3: {list3.display()}")
    print(f"Список 4: {list4.display()}")
    
    merged_head2 = merge_sorted_lists(list3.head, list4.head)
    merged_ll2 = LinkedList()
    merged_ll2.head = merged_head2
    print(f"Об'єднаний список: {merged_ll2.display()}")
    print()


if __name__ == "__main__":
    test_linked_list_functionality()
