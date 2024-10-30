from config import db
from Professor.Professor_model import Professor

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    professor = db.relationship('Professor', backref='turmas')

    def __init__(self, descricao, professor_id, ativo=True):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'professor_id': self.professor_id,
            'ativo': self.ativo
        }

class TurmaNaoEncontrada(Exception):
    pass

def turma_por_id(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    return turma.to_dict()

def listar_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def adicionar_turma(turma_data):
    # Validações manuais
    if 'descricao' not in turma_data or 'professor_id' not in turma_data:
        raise ValueError('Campos obrigatórios: descricao, professor_id')

    # Verificar se o professor existe
    professor = Professor.query.get(turma_data['professor_id'])
    if not professor:
        raise ValueError('Professor não encontrado')

    nova_turma = Turma(
        descricao=turma_data['descricao'],
        professor_id=turma_data['professor_id'],
        ativo=turma_data.get('ativo', True)  # Define o valor padrão como True
    )

    db.session.add(nova_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada

    # Atualizando dados com validação
    if 'descricao' in novos_dados:
        turma.descricao = novos_dados['descricao']

    if 'professor_id' in novos_dados:
        professor = Professor.query.get(novos_dados['professor_id'])
        if not professor:
            raise ValueError('Professor não encontrado')
        turma.professor_id = novos_dados['professor_id']

    turma.ativo = novos_dados.get('ativo', turma.ativo)  # Atualiza o campo 'ativo', se fornecido

    db.session.commit()

def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada

    db.session.delete(turma)
    db.session.commit()
