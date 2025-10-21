import json
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path(__file__).resolve().parents[1] / "data.json"

def _read_file() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _write_file(data: List[Dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def list_tasks() -> List[Dict]:
    return _read_file()

def add_task(task: Dict) -> Dict:
    data = _read_file()
    task_id = (max([t["id"] for t in data]) + 1) if data else 1
    task["id"] = task_id

    if "prioridade" not in task:
        task["prioridade"] = "Média"

    data.append(task)
    _write_file(data)
    return task

def get_task(task_id: int) -> Dict:
    data = _read_file()
    for t in data:
        if t["id"] == task_id:
            return t
    return None

def update_task(task_id: int, updates: Dict) -> Dict:
    data = _read_file()
    for i, t in enumerate(data):
        if t["id"] == task_id:
            data[i].update(updates)
            _write_file(data)
            return data[i]
    return None

def delete_task(task_id: int) -> bool:
    data = _read_file()
    new_data = [t for t in data if t["id"] != task_id]
    if len(new_data) == len(data):
        return False
    _write_file(new_data)
    return True
