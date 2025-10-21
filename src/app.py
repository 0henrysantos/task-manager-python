from flask import Flask, render_template, request, redirect, url_for, flash
from src import storage, forms
from pathlib import Path

# Corrige o caminho dos diretórios de templates e estáticos
BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)
app.secret_key = "chave-secreta-trocar-em-producao"

@app.route("/")
def index():
    tarefas = storage.list_tasks()
    return render_template("index.html", tarefas=tarefas)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        titulo = request.form.get("titulo", "")
        descricao = request.form.get("descricao", "")
        valid, msg = forms.validate_task_form({"titulo": titulo, "descricao": descricao})
        if not valid:
            flash(msg, "danger")
            return redirect(url_for("create"))
        prioridade = request.form.get("prioridade", "Média")
        tarefa = {"titulo": titulo, "descricao": descricao, "status": "A Fazer", "prioridade": prioridade}
        storage.add_task(tarefa)
        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    tarefa = storage.get_task(task_id)
    if not tarefa:
        flash("Tarefa não encontrada.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "")
        descricao = request.form.get("descricao", "")
        status = request.form.get("status", tarefa["status"])
        valid, msg = forms.validate_task_form({"titulo": titulo, "descricao": descricao})
        if not valid:
            flash(msg, "danger")
            return redirect(url_for("edit", task_id=task_id))
        prioridade = request.form.get("prioridade", tarefa.get("prioridade", "Média"))
        updates = {"titulo": titulo, "descricao": descricao, "status": status, "prioridade": prioridade}
        storage.update_task(task_id, updates)
        flash("Tarefa atualizada com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", tarefa=tarefa)

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    success = storage.delete_task(task_id)
    if success:
        flash("Tarefa removida!", "success")
    else:
        flash("Tarefa não encontrada.", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
