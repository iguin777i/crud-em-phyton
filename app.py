from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://root:@localhost/estoque_pneus')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pneu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dimensoes = db.Column(db.String(20), nullable=False)
    indice_carga = db.Column(db.String(10), nullable=False)
    indice_velocidade = db.Column(db.String(2), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    condicoes_climaticas = db.Column(db.String(100))
    eficiencia = db.Column(db.String(1))
    ruido = db.Column(db.Integer)
    marca = db.Column(db.String(50), nullable=False)
    durabilidade = db.Column(db.String(50))
    quantidade = db.Column(db.Integer, default=0)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pneus', methods=['GET'])
def listar_pneus():
    pneus = Pneu.query.all()
    return jsonify([{
        'id': p.id,
        'dimensoes': p.dimensoes,
        'indice_carga': p.indice_carga,
        'indice_velocidade': p.indice_velocidade,
        'tipo': p.tipo,
        'condicoes_climaticas': p.condicoes_climaticas,
        'eficiencia': p.eficiencia,
        'ruido': p.ruido,
        'marca': p.marca,
        'durabilidade': p.durabilidade,
        'quantidade': p.quantidade
    } for p in pneus])

@app.route('/api/pneus', methods=['POST'])
def criar_pneu():
    data = request.json
    novo_pneu = Pneu(
        dimensoes=data['dimensoes'],
        indice_carga=data['indice_carga'],
        indice_velocidade=data['indice_velocidade'],
        tipo=data['tipo'],
        condicoes_climaticas=data['condicoes_climaticas'],
        eficiencia=data['eficiencia'],
        ruido=data['ruido'],
        marca=data['marca'],
        durabilidade=data['durabilidade'],
        quantidade=data['quantidade']
    )
    db.session.add(novo_pneu)
    db.session.commit()
    return jsonify({'message': 'Pneu criado com sucesso'}), 201

@app.route('/api/pneus/<int:id>', methods=['PUT'])
def atualizar_pneu(id):
    pneu = Pneu.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(pneu, key, value)
    db.session.commit()
    return jsonify({'message': 'Pneu atualizado com sucesso'})

@app.route('/api/pneus/<int:id>', methods=['DELETE'])
def deletar_pneu(id):
    pneu = Pneu.query.get_or_404(id)
    db.session.delete(pneu)
    db.session.commit()
    return jsonify({'message': 'Pneu deletado com sucesso'})

@app.route('/api/pneus/buscar', methods=['GET'])
def buscar_pneus():
    query = request.args.get('q', '')
    pneus = Pneu.query.filter(
        (Pneu.dimensoes.contains(query)) |
        (Pneu.marca.contains(query)) |
        (Pneu.tipo.contains(query))
    ).all()
    return jsonify([{
        'id': p.id,
        'dimensoes': p.dimensoes,
        'marca': p.marca,
        'tipo': p.tipo,
        'quantidade': p.quantidade
    } for p in pneus])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 