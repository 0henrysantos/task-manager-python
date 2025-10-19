def validate_task_form(form_data: dict) -> (bool, str):
    titulo = form_data.get("titulo", "").strip()
    descricao = form_data.get("descricao", "").strip()

    if not titulo:
        return False, "O título é obrigatório."
    if len(titulo) > 200:
        return False, "O título é muito longo."

    return True, ""
