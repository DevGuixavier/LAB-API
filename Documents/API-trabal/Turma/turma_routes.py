from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .turma_model import TurmaNaoEncontrada, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma

turmas_blueprint = Blueprint('turmas', __name__)

# Rota para obter todas as turmas (JSON)
@turmas_blueprint.route('/api/turmas', methods=['GET'])
def get_turmas_json():
    """Retorna a lista de todas as turmas em formato JSON."""
    return jsonify(listar_turmas())

# Rota para obter todas as turmas (HTML)
@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas_html():
    """Retorna a lista de todas as turmas em formato HTML."""
    turmas = listar_turmas()
    return render_template("turmas.html", turmas=turmas)

# Rota para obter os detalhes de uma turma específica (JSON)
@turmas_blueprint.route('/api/turmas/<int:id_turma>', methods=['GET'])
def get_turma_json(id_turma):
    """Retorna os detalhes de uma turma específica em formato JSON."""
    try:
        turma = turma_por_id(id_turma)
        return jsonify(turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404

# Rota para obter os detalhes de uma turma específica (HTML)
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma_html(id_turma):
    """Retorna os detalhes de uma turma específica em formato HTML."""
    try:
        turma = turma_por_id(id_turma)
        return render_template("turma_id.html", turma=turma)
    except TurmaNaoEncontrada:
        return render_template("turma_id.html", error="Turma não encontrada"), 404

# Rota para criar uma nova turma (JSON)
@turmas_blueprint.route('/api/turmas', methods=['POST'])
def create_turma_json():
    """Cria uma nova turma e retorna o resultado em formato JSON."""
    data = request.json
    if 'descricao' not in data or 'professor_id' not in data:
        return jsonify({'message': 'Campos obrigatórios: descricao, professor_id'}), 400
    try:
        adicionar_turma(data)
        return jsonify(data), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

# Rota para criar uma nova turma (HTML)
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma_html():
    """Cria uma nova turma e redireciona para a página de turmas."""
    try:
        descricao = request.form['descricao']
        professor_id = int(request.form['professor_id'])

        nova_turma = {
            'descricao': descricao,
            'professor_id': professor_id
        }

        adicionar_turma(nova_turma)
        return redirect(url_for('turmas.get_turmas_html'))
    except ValueError as e:
        return render_template("criar_Turmas.html", error=str(e))

# Outras rotas de atualização e exclusão podem seguir o mesmo padrão...
