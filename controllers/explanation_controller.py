from flask import Blueprint, request, jsonify
from models.groq_model import explicar_conceito

explanation_controller = Blueprint('explanation_controller', __name__)

@explanation_controller.route('/explicar', methods=['POST'])
def explicar():
    traducao_html = request.json.get('traducao')
    explicacao_html = explicar_conceito(traducao_html)
    return jsonify({'explicacao': explicacao_html})
