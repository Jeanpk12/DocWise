import os
from groq import Groq

client = Groq(api_key="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")

def traduzir_texto(texto):
    prompt = f'Traduza o seguinte texto para português brasileiro de modo que as frases fiquem coerentes e sejam facilmente entendidas. Faça as adaptações necessárias: "{texto}"'
    
    stream = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Você é um tradutor de documentação de linguagem de programação. Sua tarefa é traduzir o texto para pt-br de forma que a linguagem fique acessível amigável, sempre presando pela acessibilidade do texto e clareza."
            },
            {
                "role": "user",
                "content": prompt + ' retorne apenas a tradução formatada em tags html (titulos em h1, subtitulos em h2, código encapsulados na tag <pre>, etc), sem nenhum comentário adicional'
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

    return "".join(traducao)

def explicar_conceito(traducao_html):
    prompt_explicacao = f'{traducao_html} Me explique esse conceito de forma didática, fornecendo exemplo e analogias.'

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

    return "".join(explicacao)
