from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Configurando o cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def traduzir_texto(texto):
    # Construindo o prompt para a IA
    prompt = f'Traduza o seguinte texto para português brasileiro de modo que as frases fiquem coerentes e sejam facilmente entendidas. Faça as adaptações necessárias: "{texto}"'

    # Criando a requisição para o modelo Llama
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": "Você é um tradutor de documentação de linguagem de programação. Sua tarefa é traduzir o texto para pt-br de forma que a linguagem fique acessível amigável, sempre presando pela acessibilidade do texto e clareza."
            },
            {
                "role": "user", 
                "content": prompt + ' retorne apenas a trução formatada em tags html (titulos em h1, subtitulos em h2, código encapsulados na tag <pre>, etc), sem nenhum comentário adicional'
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.6,
        max_tokens=8000,
        top_p=1,
        stream=True,
    )

    traducao = []
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            traducao.append(content)

    traducao_texto = "".join(traducao)
    return traducao_texto

def explicar_conceito(traducao_html):
    # Construindo o prompt para a explicação
    prompt_explicacao = f'{traducao_html} Me explique esse conceito de forma didática, fornecendo exemplo e analogias.'

    # Criando a requisição para o modelo Llama
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": "Você é um assistente técnico especializado em explicar conceitos de programação de forma didática. Sua tarefa é, tendo por base o texto técnico, criar uma explicação didática e detalhada de forma amigável."
            },
            {
                "role": "user", 
                "content": prompt_explicacao + ' \n Retorne apenas a explicação formatada em tags html (titulos em h1, subtitulos em h2, código encapsulados na tag <pre>, etc), sem nenhum comentário adicional'
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=1,
        max_tokens=5000,
        top_p=1,
        stream=True,
    )

    explicacao = []
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            explicacao.append(content)

    explicacao_texto = "".join(explicacao)
    return explicacao_texto

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traduzir', methods=['POST'])
def traduzir():
    texto_original = request.json.get('texto')
    traducao_html = traduzir_texto(texto_original)
    return jsonify({'traducao': traducao_html})

@app.route('/explicar', methods=['POST'])
def explicar():
    traducao_html = request.json.get('traducao')
    explicacao_html = explicar_conceito(traducao_html)
    return jsonify({'explicacao': explicacao_html})

if __name__ == '__main__':
    app.run()
