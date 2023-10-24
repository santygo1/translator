def arr_find(func, array):
    """
     Функция, проверяющая выполнение условия переданной функции на массиве
        :var func - функция для проверки (True/False)
        :var array - массив
        :return True - если есть хотя бы один элемент удовлетворяющий функции, False - иначе
    """
    for i in array:
        if func(i):
            return True

    return False


def arr_part(arr, index_from, end_cond_func, skip_end_cond_func):
    """
    Функция, которая достает элементы массива с определенного индекса до тех пор пока не стретился элемент,
    который не удовлетворяет переделанному условию(не включая этот элемент) при этом если несколько раз выполнилось
    условие скипа добавляет +1 к нарушению условия остановки

    :param arr: массив
    :param index_from: индекс начала
    :param end_cond_func: условие окончания
    :param skip_end_cond_func: условие для скипа
    :return: часть массива которая удовлетворяет условию
    :raise Exception - если не произошла остановка
    """

    skip_count = 0
    i = index_from
    part = []
    while i < len(arr):
        cur_elem = arr[i]
        if skip_end_cond_func(cur_elem):
            skip_count += 1
        elif end_cond_func(cur_elem):
            if skip_count == 0:
                return part
            else:
                skip_count -= 1
        part.append(cur_elem)
        i += 1

    raise Exception('End of array isn\'t found')
