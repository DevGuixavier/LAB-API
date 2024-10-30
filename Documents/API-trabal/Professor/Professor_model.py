from config import db

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)

    def __init__(self, nome, idade, materia, observacoes=None):
        # Validações manuais
        if not nome or len(nome) > 100:
            raise ValueError("O nome deve ser preenchido e ter no máximo 100 caracteres.")
        if not isinstance(idade, int) or idade <= 0:
            raise ValueError("A idade deve ser um número inteiro positivo.")
        if not materia or len(materia) > 100:
            raise ValueError("A matéria deve ser preenchida e ter no máximo 100 caracteres.")
        
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes
        }

class ProfessorNaoEncontrado(Exception):
    pass

def professor_por_id(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado("Professor não encontrado.")
    return professor.to_dict()

def listar_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def adicionar_professor(professor_data):
    # Validações de dados antes de adicionar
    nome = professor_data.get('nome')
    idade = professor_data.get('idade')
    materia = professor_data.get('materia')

    if not nome or len(nome) > 100:
        raise ValueError("O nome deve ser preenchido e ter no máximo 100 caracteres.")
    if not isinstance(idade, int) or idade <= 0:
        raise ValueError("A idade deve ser um número inteiro positivo.")
    if not materia or len(materia) > 100:
        raise ValueError("A matéria deve ser preenchida e ter no máximo 100 caracteres.")

    novo_professor = Professor(
        nome=nome,
        idade=idade,
        materia=materia,
        observacoes=professor_data.get('observacoes')  # Observações é opcional
    )
    db.session.add(novo_professor)
    db.session.commit()

def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado("Professor não encontrado.")

    nome = novos_dados.get('nome')
    idade = novos_dados.get('idade')
    materia = novos_dados.get('materia')

    # Validações ao atualizar
    if nome and len(nome) > 100:
        raise ValueError("O nome deve ter no máximo 100 caracteres.")
    if idade and (not isinstance(idade, int) or idade <= 0):
        raise ValueError("A idade deve ser um número inteiro positivo.")
    if materia and len(materia) > 40:
        raise ValueError("A matéria deve ter no máximo 40 caracteres.")

    professor.nome = nome if nome else professor.nome
    professor.idade = idade if idade else professor.idade
    professor.materia = materia if materia else professor.materia
    professor.observacoes = novos_dados.get('observacoes', professor.observacoes)  # Observações é opcional
    db.session.commit()

def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado("Professor não encontrado.")
    db.session.delete(professor)
    db.session.commit()





