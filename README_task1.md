# Завдання 1. Структури даних. Сортування. Робота з однозв'язним списком

## Опис завдання
У цьому завданні реалізовано базові операції з **однозв’язним списком**:
1. Реверсування списку (зміна напрямку посилань між вузлами).
2. Сортування однозв’язного списку (алгоритм сортування вставками).
3. Об’єднання двох відсортованих списків у один відсортований.

## Реалізовані класи та функції

### `class ListNode`
Представлення вузла однозв’язного списку.
- `data` – значення вузла.
- `next` – посилання на наступний вузол.

### `class LinkedList`
Реалізація самого списку.
- `append(data)` – додає елемент у кінець.
- `prepend(data)` – додає елемент на початок.
- `display()` – повертає список у вигляді рядка `a -> b -> c -> None`.
- `to_list()` – конвертує список у звичайний Python list.
- `from_list(data_list)` – створює однозв’язний список зі звичайного списку.

### Функції
- `reverse_linked_list(head)` – реверсує список.
- `insertion_sort_linked_list(head)` – сортує список методом вставок.
- `merge_sorted_lists(head1, head2)` – об’єднує два відсортовані списки.

## Приклади використання

### Створення списку та додавання елементів
```python
ll = LinkedList()
ll.append(3)
ll.append(1)
ll.append(4)
ll.append(2)
ll.prepend(0)
print(ll.display())
# Вивід: 0 -> 3 -> 1 -> 4 -> 2 -> None

### Реверсування списку
```
reversed_head = reverse_linked_list(ll.head)
reversed_ll = LinkedList()
reversed_ll.head = reversed_head
print(reversed_ll.display())
# Вивід: 2 -> 4 -> 1 -> 3 -> 0 -> None
```
### Сортування списку
```
ll2 = LinkedList.from_list([5, 2, 8, 1, 9, 3])
sorted_head = insertion_sort_linked_list(ll2.head)
sorted_ll = LinkedList()
sorted_ll.head = sorted_head
print(sorted_ll.display())
# Вивід: 1 -> 2 -> 3 -> 5 -> 8 -> 9 -> None
```
### Об’єднання двох відсортованих списків
```
list1 = LinkedList.from_list([1, 3, 5, 7])
list2 = LinkedList.from_list([2, 4, 6, 8])
merged_head = merge_sorted_lists(list1.head, list2.head)
merged_ll = LinkedList()
merged_ll.head = merged_head
print(merged_ll.display())
# Вивід: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> None
``````



