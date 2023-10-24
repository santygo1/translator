def arr_find(func, array):
    """
     Функция, проверяющая выполнение условия переданной функции на массиве
        @:var func - функция для проверки (True/False)
        @:var array - массив
        @:return True - если есть хотя бы один элемент удовлетворяющий функции, False - иначе
    """
    for i in array:
        if func(i):
            return True

    return False
