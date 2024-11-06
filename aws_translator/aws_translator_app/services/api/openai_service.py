# aws_translator_app/services/api/openai_service.py

"""
OpenAI Service Module
=====================

Este módulo fornece serviços para simplificar e, opcionalmente, resumir textos utilizando a API da OpenAI.
Ele gerencia a autenticação com a OpenAI, inicializa o cliente de tradução e executa a simplificação de textos
com base nos parâmetros fornecidos.

Classes:
    OpenAIService: Classe responsável pela interação com a API da OpenAI para simplificação de textos.

Dependências:
    - dotenv: biblioteca para carregar variáveis de ambiente a partir de um arquivo .env.
    - openai: biblioteca oficial da OpenAI para interagir com a API OpenAI.
    - os: biblioteca padrão para interagir com o sistema operacional.
    - time: biblioteca padrão para manipulação de tempo.
    - random: biblioteca padrão para geração de números aleatórios.
    - typing: biblioteca padrão para anotações de tipos.

Exemplo de Uso:
    >>> from translation_app.services.api.openai_service import OpenAIService
    >>> openai_service = OpenAIService()
    >>> texto_original = "This is a complex technical document."
    >>> texto_simplificado = openai_service.simplify_text(
    ...     text=texto_original,
    ...     area_tecnica="Computer Science",
    ...     estilo="informal",
    ...     summarize=True,
    ...     model="gpt-4"
    ... )
    >>> print(texto_simplificado)
    "This is a simplified version of the original technical document, making it easier to understand for non-experts."
"""

import os
import time
import random
from dotenv import load_dotenv
import openai
from typing import List, Optional


class OpenAIService:
    """
    Serviço para simplificar (e opcionalmente resumir) textos utilizando a API da OpenAI.

    Esta classe gerencia a autenticação com a OpenAI, inicializa o cliente de tradução
    e fornece métodos para simplificar textos de acordo com parâmetros específicos.

    Métodos:
        simplify_text(text: str, area_tecnica: str, estilo: str, summarize: bool, model: str) ⇾ str:
            Simplifica (e opcionalmente resume) o texto fornecido utilizando o modelo especificado da OpenAI.
    """

    def __init__(self):
        """
        Inicializa a instância do OpenAIService.

        Este metodo realiza os seguintes passos:
            1. Carrega as credenciais da OpenAI a partir do arquivo .env.
            2. Inicializa o cliente OpenAI com as credenciais carregadas.

        Exceções:
            - ValueError: se a chave da API OpenAI estiver faltando no arquivo .env.
            - ConnectionError: se houver falha ao inicializar o cliente OpenAI.
        """
        self.OPENAI_API_KEY = None  # Chave da API OpenAI
        self.client = None  # Instância do cliente OpenAI
        self.load_credentials()  # Carrega as credenciais OpenAI
        self.init_openai_client()  # Inicializa o cliente OpenAI

    def load_credentials(self) -> None:
        """
        Carrega as credenciais OpenAI do arquivo .env.

        Este metodo realiza os seguintes passos:
            1. Carrega as variáveis de ambiente a partir do arquivo .env.
            2. Obtém a chave da API OpenAI (`OPENAI_API_KEY`) das variáveis de ambiente.
            3. Verifica se a chave da API está presente; caso contrário, lança uma exceção.

        Exceções:
            - ValueError: se a chave da API OpenAI estiver faltando no arquivo .env.

        Teoria:
            - As credenciais da OpenAI são necessárias para autenticar e autorizar solicitações à API OpenAI.
            - É uma prática recomendada armazenar credenciais sensíveis em arquivos de ambiente (.env) para evitar exposição acidental.
        """
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

        if not self.OPENAI_API_KEY:
            raise ValueError("Chave da API OpenAI faltando. Por favor, verifique o arquivo .env.")

    def init_openai_client(self):
        """
        Inicializa o cliente OpenAI.

        Este metodo utiliza a chave da API carregada para configurar a biblioteca OpenAI,
        que será utilizada para realizar chamadas à API de simplificação de textos.

        Exceções:
            - ConnectionError: se houver falha ao inicializar o cliente OpenAI devido a credenciais inválidas
              ou problemas de conexão.

        Teoria:
            - A biblioteca OpenAI utiliza a chave da API para autenticar solicitações e garantir que o usuário
              tenha permissão para acessar os serviços da OpenAI.
        """
        try:
            openai.api_key = self.OPENAI_API_KEY
            self.client = openai
        except Exception as e:
            raise ConnectionError(f"Falha ao inicializar o cliente OpenAI: {str(e)}")

    def simplify_text(
            self,
            text: str,
            area_tecnica: str,
            estilo: str,
            summarize: bool,
            model: str,
            complexity_level: str = 'Intermediário',
            focus_aspects: Optional[List[str]] = None,
            temperature: float = 0.8,
            max_tokens: int = 4096,
            top_p: float = 1.0,
            frequency_penalty: float = 0.0,
            presence_penalty: float = 0.0
    ) -> str:
        """
        Simplifica (e opcionalmente resume) o texto fornecido usando a API da OpenAI.

        Este metodo realiza os seguintes passos:
            1. Define o prompt com base nos parâmetros fornecidos.
            2. Faz uma chamada à API OpenAI ChatCompletion para obter o texto simplificado.
            3. Implementa uma lógica de retry para lidar com possíveis falhas temporárias na API.

        Parâmetros:
            text (str): O texto a ser simplificado.
            area_tecnica (str): A área técnica do texto (e.g., "Computer Science", "Medicine").
            estilo (str): O estilo de escrita desejado (e.g., "informal", "formal", "casual").
            summarize (bool): Indica se o texto deve ser resumido além de ser simplificado.
            model (str): O modelo da OpenAI a ser utilizado (e.g., "gpt-4", "gpt-3.5-turbo").
            complexity_level (str): Nível de complexidade da simplificação (e.g., "Básico", "Intermediário", "Avançado").
            focus_aspects (List[str], optional): Aspectos a serem priorizados na simplificação (e.g., ["clareza", "concisão"]).
            temperature (float): Controla a aleatoriedade da resposta.
            max_tokens (int): Define o tamanho máximo da resposta.
            top_p (float): Controla a aleatoriedade via probabilidade cumulativa.
            frequency_penalty (float): Controla a repetição de palavras.
            presence_penalty (float): Controla a diversidade da resposta.

        Retorna:
            str: O texto simplificado (e opcionalmente resumido) retornado pela API da OpenAI.

        Exceções:
            - Exception: Se ocorrer um erro durante a comunicação com a API OpenAI após várias tentativas.

        Teoria:
            - A OpenAI utiliza modelos de linguagem avançados para gerar texto de forma contextualizada e adaptada às instruções fornecidas.
            - A simplificação de texto envolve reescrever o conteúdo de maneira mais acessível, mantendo a essência das informações.
            - A funcionalidade de sumarização reduz o texto mantendo os pontos-chave, facilitando a compreensão rápida do conteúdo.
        """
        # Construir a descrição do nível de complexidade
        complexity_description = ''
        if complexity_level == 'Básico':
            complexity_description = 'usando linguagem simples, adequada para iniciantes'
        elif complexity_level == 'Intermediário':
            complexity_description = 'usando linguagem moderadamente simplificada, adequada para o público em geral'
        elif complexity_level == 'Avançado':
            complexity_description = 'mantendo detalhes técnicos, adequado para público avançado'

        # Construir a descrição dos aspectos de foco
        focus_description = ''
        if focus_aspects:
            focus_description = 'focando em ' + ', '.join(focus_aspects)

        # Construir o conteúdo do usuário
        user_content = f"Por favor, reescreva o seguinte texto {complexity_description}"
        if focus_description:
            user_content += f", {focus_description}"
        user_content += f", utilizando um estilo {estilo}."
        if summarize:
            user_content += " Por favor, também resuma o texto, mantendo as informações essenciais."
        user_content += f"\n\nTexto:\n\"\"\"\n{text}\n\"\"\""

        messages = [
            {
                "role": "system",
                "content": (
                    f"Você é um(a) especialista em {area_tecnica}. Seu objetivo é tornar conceitos dessa área mais acessíveis a pessoas leigas."
                )
            },
            {
                "role": "user",
                "content": user_content
            }
        ]

        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.client.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Erro ao simplificar o texto após várias tentativas: {str(e)}")
                else:
                    wait_time = 2 ** attempt + random.uniform(0, 1)
                    time.sleep(wait_time)
