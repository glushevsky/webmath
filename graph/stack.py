# coding: utf-8


# реализация стэка
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        # добавление элемента
        self.items.append(item)

    def pop(self):
        # извлечение из стэка
        return self.items.pop()

    def peek(self):
        # просмотр верхнего элемента стэка
        return self.items[len(self.items) - 1]

    def size(self):
        # размер стэка
        return len(self.items)
