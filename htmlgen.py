def print_tag(obj, indentlevel=0, indent='  '):
    result = []
    line = ''

    # Тут проведём некоторые проверки для внутреннего использования
    # И удобного чтения кода
    # Проверяем наличие вложенных тегов. Если их нет, то
    # тег займёт всего одну строку вместе с закрывающим
    # Учтём это в дальнейшем
    is_multiline = True if obj.children else False

    # Так же сразу проверим, есть ли закрывающий тег
    # Изначально считая, что есть
    is_single = False
    if hasattr(obj, 'is_single'):
        if obj.is_single:
            is_single = True

    # Теперь проверяем пришедшие атрибуты, формируем из них строку
    attrib_line = ''
    if hasattr(obj, 'attributes'):
        if 'cls' in obj.attributes:
            # У нас есть кортеж с классами, немного преобразим их в словаре
            classes = " ".join(list(obj.attributes['cls']))
            obj.attributes['class'] = classes
            del obj.attributes['cls']

        for atr in obj.attributes:
            attrib_line += ' '+atr+'=\"'+obj.attributes[atr]+'\"'
    # Продолжаем формировать строку
    line += indent*indentlevel + '<' + obj.tag_name.upper() + attrib_line +'>'

    if hasattr(obj, 'text'):
        line += obj.text

    if not is_single and not is_multiline:
        line += '</'+ obj.tag_name.upper()+'>'
    result.append(line)

    # Здесь, если нужно, рекурсивно уходим во вложенные теги
    # И отступ тоже прибавляем
    # Результат возвращаем в список, который копит результат

    for child in obj.children:
        result.append(print_tag(child, indentlevel=indentlevel+1))
  
    # Закрываем многострочный тег (если он такой)
    if is_multiline:
        result.append(indent*indentlevel + '</' + obj.tag_name.upper() + '>')
    # Собираем в итоге большой кусок текста из списка строк
    # через джоин по символу переноса строки
    # и отдаём
    return '\n'.join(result)


class Htmlgen:
    #Это "родительский" класс для остальных трёх.
    #В нём общие для всех свойства и методы

    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.children = []

    def add_tag(self, tag_name, is_single=False, text='', **kwargs):
        _ = Tag(tag_name)
        _.is_single = is_single
        if text:
            _.text = text
        # Через кварги пришли аттрибуты, добавим их в экземпляр
        _.attributes = kwargs
        self.children.append(_)
        return _
    
    def _print_tag(self):
        return print_tag(self)


class HTML(Htmlgen):
    # Класс для главного тэга.
    # В нём есть именованный аргумент output_file
    # Если он задан, то по умолчанию вывод будет осуществляться
    # в указанный файл
    # Собственно есть метод output_default
    # который и выводит либо принтом, либо в файл

    def __init__(self, tag_name='HTML', output_file=None):
        super().__init__(tag_name)
        self.output_file = output_file

    # Метод добавления верхнеуровневых тэгов
    def add_toplevel_tag(self, tag_name):
        _ = TopLevelTag(tag_name)
        self.children.append(_)
        return _

    def output_default(self):
        if not self.output_file:
            print(self._print_tag())
        else:
            with open (self.output_file, 'w') as file:
                file.write(self._print_tag())

    # Метод для отладки, в основном
    def __str__(self):
        line1 = 'HTML object with '+str(len(self.children))+' children tags'
        line2 = (', ouput set to file \"'+ self.output_file+'\"')\
        if self.output_file else ''
        return  line1 + line2

class TopLevelTag(Htmlgen):
    # Класс верхнеуровневых тегов (Head и Body)
    # Они не имеют текста внутри и всегда имеют закрывашку
    def __init__(self, tag_name):
        super().__init__(tag_name)

    # Метод для отладки, в основном
    def __str__(self):
        line1 = 'TopLevelTag object \"' + self.tag_name +\
        '\" with '+str(len(self.children))+' children tags'
        return  line1

class Tag(Htmlgen):
    # Класс обычных тегов
    # В них может быть текст и атрибуты (читай ниже)
    # Так же есть условие is_single
    # которое отвечает за наличие закрывающего тега
    # ВАЖНО!!!
    # Условимся, что атрибут class для HTML мы меняем на cls
    # для разрешения конфликтов имён
    def __init__(self, tag_name, is_single=False, text='', **kwargs):
        super().__init__(tag_name)
        self.is_single = is_single
        self.text = text

    # Метод для отладки, в основном
    def __str__(self):
        line1 = 'Tag object \"' + self.tag_name +'\" with '\
        +str(len(self.children))+' children tags'
        return  line1
