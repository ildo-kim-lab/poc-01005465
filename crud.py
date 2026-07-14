"""할 일(Todo) 레코드에 대한 CRUD 로직."""

from storage import load_state, save_state


def create_todo(title, description):
    state = load_state()
    new_id = state["next_id"]
    todo = {"id": new_id, "title": title, "description": description, "done": False}
    state["todos"].append(todo)
    state["next_id"] = new_id + 1
    save_state(state)
    return todo


def read_all():
    return load_state()["todos"]


def find_by_id(todo_id):
    return next((t for t in load_state()["todos"] if t["id"] == todo_id), None)


def search_by_keyword(keyword):
    keyword_lower = keyword.lower()
    return [
        t
        for t in load_state()["todos"]
        if keyword_lower in t["title"].lower() or keyword_lower in t["description"].lower()
    ]


def update_todo(todo_id, title=None, description=None, done=None):
    state = load_state()
    target = next((t for t in state["todos"] if t["id"] == todo_id), None)
    if target is None:
        return None

    if title is not None:
        target["title"] = title
    if description is not None:
        target["description"] = description
    if done is not None:
        target["done"] = done

    save_state(state)
    return target


def delete_todo(todo_id):
    state = load_state()
    target = next((t for t in state["todos"] if t["id"] == todo_id), None)
    if target is None:
        return False

    state["todos"].remove(target)
    save_state(state)
    return True
