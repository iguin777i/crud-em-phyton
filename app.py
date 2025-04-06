from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pneu(db.Model):
    __tablename__ = 'pneus'
    id = db.Column(db.Integer, primary_key=True)
    dimensoes = db.Column(db.String(50), nullable=False)
    indice_carga = db.Column(db.String(20), nullable=False)
    indice_velocidade = db.Column(db.String(10), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    condicoes_climaticas = db.Column(db.String(200))
    eficiencia = db.Column(db.String(10))
    ruido = db.Column(db.Integer)
    marca = db.Column(db.String(100), nullable=False)
    durabilidade = db.Column(db.String(100))
    quantidade = db.Column(db.Integer, default=0)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pneus', methods=['GET'])
def listar_pneus():
    try:
        logger.debug("Tentando listar pneus")
        pneus = Pneu.query.all()
        logger.debug(f"Encontrados {len(pneus)} pneus")
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
    except Exception as e:
        logger.error(f"Erro ao listar pneus: {str(e)}")
        return jsonify({'error': 'Erro ao listar pneus'}), 500

@app.route('/api/pneus', methods=['POST'])
def criar_pneu():
    try:
        logger.debug("Tentando criar novo pneu")
        data = request.json
        logger.debug(f"Dados recebidos: {data}")
        
        # Converter valores numéricos
        data['ruido'] = int(data.get('ruido', 0))
        data['quantidade'] = int(data.get('quantidade', 0))
        
        novo_pneu = Pneu(
            dimensoes=data['dimensoes'],
            indice_carga=data['indice_carga'],
            indice_velocidade=data['indice_velocidade'],
            tipo=data['tipo'],
            condicoes_climaticas=data.get('condicoes_climaticas'),
            eficiencia=data.get('eficiencia'),
            ruido=data.get('ruido'),
            marca=data['marca'],
            durabilidade=data.get('durabilidade'),
            quantidade=data['quantidade']
        )
        
        db.session.add(novo_pneu)
        db.session.commit()
        logger.debug("Pneu criado com sucesso")
        return jsonify({'message': 'Pneu criado com sucesso'}), 201
    except Exception as e:
        logger.error(f"Erro ao criar pneu: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/pneus/<int:id>', methods=['PUT'])
def atualizar_pneu(id):
    try:
        logger.debug(f"Tentando atualizar pneu {id}")
        pneu = Pneu.query.get_or_404(id)
        data = request.json
        logger.debug(f"Dados recebidos: {data}")
        
        # Converter valores numéricos
        if 'ruido' in data:
            data['ruido'] = int(data['ruido'])
        if 'quantidade' in data:
            data['quantidade'] = int(data['quantidade'])
        
        for key, value in data.items():
            if hasattr(pneu, key):
                setattr(pneu, key, value)
        
        db.session.commit()
        logger.debug("Pneu atualizado com sucesso")
        return jsonify({'message': 'Pneu atualizado com sucesso'})
    except Exception as e:
        logger.error(f"Erro ao atualizar pneu: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/pneus/<int:id>', methods=['DELETE'])
def deletar_pneu(id):
    try:
        logger.debug(f"Tentando deletar pneu {id}")
        pneu = Pneu.query.get_or_404(id)
        db.session.delete(pneu)
        db.session.commit()
        logger.debug("Pneu deletado com sucesso")
        return jsonify({'message': 'Pneu deletado com sucesso'})
    except Exception as e:
        logger.error(f"Erro ao deletar pneu: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/pneus/buscar', methods=['GET'])
def buscar_pneus():
    try:
        query = request.args.get('q', '')
        logger.debug(f"Buscando pneus com query: {query}")
        
        pneus = Pneu.query.filter(
            (Pneu.dimensoes.ilike(f'%{query}%')) |
            (Pneu.marca.ilike(f'%{query}%')) |
            (Pneu.tipo.ilike(f'%{query}%'))
        ).all()
        
        logger.debug(f"Encontrados {len(pneus)} pneus na busca")
        return jsonify([{
            'id': p.id,
            'dimensoes': p.dimensoes,
            'marca': p.marca,
            'tipo': p.tipo,
            'quantidade': p.quantidade
        } for p in pneus])
    except Exception as e:
        logger.error(f"Erro ao buscar pneus: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            logger.debug("Criando tabelas do banco de dados")
            db.create_all()
            logger.debug("Tabelas criadas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {str(e)}")
    app.run(debug=True) 