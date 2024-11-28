from flask import Blueprint, request, jsonify
from models.groq_model import traduzir_texto

translation_controller = Blueprint('translation_controller', __name__)

@translation_controller.route('/traduzir', methods=['POST'])
def traduzir():
    texto_original = request.json.get('texto')
    traducao_html = traduzir_texto(texto_original)
    return jsonify({'traducao': traducao_html})
