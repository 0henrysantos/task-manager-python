import os
import json
import tempfile
from pathlib import Path

from src import storage
from src.app import app

def setup_function():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    
    # Converte para Path para evitar erro com .exists()
    storage.DATA_FILE = Path(tmp.name)
    
    with open(storage.DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def teardown_function():
    try:
        os.remove(storage.DATA_FILE)
    except Exception:
        pass

def test_add_and_list_task():
    t = storage.add_task({"titulo": "Tarefa 1", "descricao": "Teste", "status": "A Fazer"})
    assert t["id"] == 1
    tasks = storage.list_tasks()
    assert len(tasks) == 1

def test_flask_client(monkeypatch, tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("[]", encoding="utf-8")

    # Aqui já está correto: tmp_path é um Path
    monkeypatch.setattr(storage, "DATA_FILE", data_file)

    client = app.test_client()

    resp = client.post("/create", data={"titulo": "Nova", "descricao": "Tarefa Web"})
    assert resp.status_code in (200, 302)

    resp = client.get("/")
    assert b"Nova" in resp.data
