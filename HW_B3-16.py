
from htmlgen import HTML, TopLevelTag, Tag

if __name__ == "__main__":
    # Всем привет
    # Я не хотел пользоваться способом контекстного менеджера из-за громоздкости
    # Мой способ не менее очевиден. Каждый новый тег появляется вызовом метода от родительского,
    # согласно вложенности
    # В каждом полученном объекте класса присутствует метод, который позволяет
    # получить принт HTML структуры начиная именно с этого тега
    # А получение полного принта - это просто частный случай принта от самого корневого тега
    # Классы и функционал вынесены в модуль htmlgen
    # Там же в коде и остальные коментарии

    html = HTML() #пишем сюда output_file="index.html" например, для вывода в файл
    head = html.add_toplevel_tag('head')
    title = head.add_tag('title', text="Hello")
    body = html.add_toplevel_tag('body')
    h1 = body.add_tag('h1', cls=("main-text",))
    h1.text = 'Test'
    div = body.add_tag('div', cls=("container", "container-fluid"), id="lead")
    paragraph = div.add_tag('p', text='Another test')
    img = div.add_tag('img', is_single=True, src='/icon.png', data_image="responsive")

    html.output_default()