"""할 일(Todo) 레코드에 대한 CRUD 로직."""

from storage import load_todos, save_todos


def create_todo(title, description):
    todos = load_todos()
    new_id = max((t["id"] for t in todos), default=0) + 1
    todo = {"id": new_id, "title": title, "description": description, "done": False}
    todos.append(todo)
    save_todos(todos)
    return todo


def read_all():
    return load_todos()


def find_by_id(todo_id):
    return next((t for t in load_todos() if t["id"] == todo_id), None)


def search_by_keyword(keyword):
    keyword_lower = keyword.lower()
    return [
        t
        for t in load_todos()
        if keyword_lower in t["title"].lower() or keyword_lower in t["description"].lower()
    ]


def update_todo(todo_id, title=None, description=None, done=None):
    todos = load_todos()
    target = next((t for t in todos if t["id"] == todo_id), None)
    if target is None:
        return None

    if title is not None:
        target["title"] = title
    if description is not None:
        target["description"] = description
    if done is not None:
        target["done"] = done

    save_todos(todos)
    return target


def delete_todo(todo_id):
    todos = load_todos()
    target = next((t for t in todos if t["id"] == todo_id), None)
    if target is None:
        return False

    todos.remove(target)
    save_todos(todos)
    return True
