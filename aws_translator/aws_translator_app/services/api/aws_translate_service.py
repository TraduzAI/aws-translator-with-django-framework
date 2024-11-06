# aws_translator_app/services/api/aws_translate_service.py

"""
AWS Translate Service Module
============================

Este módulo fornece serviços para traduzir textos utilizando a API AWS Translate.
Ele gerencia a autenticação com a AWS, inicializa o cliente de tradução e executa
a tradução de textos para o idioma de destino especificado.

Classes:
    AwsTranslateService: Classe responsável pela tradução de textos usando AWS Translate.

Dependências:
    - boto3: biblioteca da AWS para interagir com os serviços da AWS.
    - dotenv: biblioteca para carregar variáveis de ambiente a partir de um arquivo .env.
    - os: biblioteca padrão para interagir com o sistema operacional.
    - typing: para anotações de tipagem.
"""

import boto3
import os
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
from typing import Tuple


class AwsTranslateService:
    """
    Serviço para traduzir textos utilizando a API AWS Translate.

    Esta classe gerencia a autenticação com a AWS, inicializa o cliente de tradução
    e fornece métodos para traduzir textos para diferentes idiomas de destino.

    Métodos:
        translate_text(text: str, target_language_code: str) ⇾ Tuple[str, str]:
            Traduz o texto fornecido para o idioma de destino especificado e retorna o texto traduzido com o código do idioma de origem detectado.
    """

    def __init__(self):
        """
        Inicializa a instância do AwsTranslateService.

        Este metodo realiza os seguintes passos:
            1. Carrega as credenciais da AWS a partir do arquivo .env.
            2. Inicializa o cliente AWS Translate usando as credenciais carregadas.

        Exceções:
            - ValueError: Se alguma das credenciais da AWS estiver faltando no arquivo .env.
            - ConnectionError: Se houver falha ao inicializar o cliente AWS Translate.
        """
        self.translate_client = None
        self.ACCESS_KEY = None
        self.SECRET_KEY = None
        self.REGION = None

        # Carrega as credenciais AWS
        self.load_credentials()

        # Inicializa o cliente AWS Translate
        self.init_translate_client()

    def load_credentials(self) -> None:
        """
        Carrega as credenciais AWS do arquivo .env.

        Este metodo realiza os seguintes passos:
            1. Carrega as variáveis de ambiente a partir do arquivo .env.
            2. Obtém as credenciais AWS (ACCESS_KEY_ID, SECRET_ACCESS_KEY, REGION) das variáveis de ambiente.
            3. Verifica se todas as credenciais estão presentes; caso contrário, lança uma exceção.

        Exceções:
            - ValueError: se alguma das credenciais da AWS estiver faltando no arquivo .env.
        """
        load_dotenv()
        self.ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', '')
        self.SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        self.REGION = os.getenv('AWS_REGION', '')

        # Verifica se todas as credenciais estão presentes
        if not all([self.ACCESS_KEY, self.SECRET_KEY, self.REGION]):
            raise ValueError("Credenciais AWS faltando. Por favor, verifique o arquivo .env.")

    def init_translate_client(self):
        """
        Inicializa o cliente AWS Translate.

        Este metodo utiliza as credenciais carregadas para criar um cliente AWS Translate
        que será utilizado para realizar as traduções de textos.

        Exceções:
            - ConnectionError: se houver falha ao inicializar o cliente AWS Translate devido a credenciais inválidas
              ou problemas de rede.
        """
        try:
            session = boto3.Session(
                aws_access_key_id=self.ACCESS_KEY,
                aws_secret_access_key=self.SECRET_KEY,
                region_name=self.REGION
            )
            self.translate_client = session.client('translate')
        except (BotoCoreError, ClientError) as e:
            raise ConnectionError(f"Falha ao inicializar o cliente AWS Translate: {str(e)}") from e

    def translate_text(self, text: str, target_language_code: str) -> Tuple[str, str]:
        """
        Traduz o texto fornecido para o idioma de destino especificado e retorna o código do idioma de origem detectado.

        Parâmetros:
            text (str): O texto a ser traduzido.
            target_language_code (str): Código do idioma de destino.

        Retorna:
            Tuple[str, str]: Uma tupla contendo o texto traduzido e o código do idioma de origem detectado.

        Exceções:
            - Exception: Se ocorrer um erro durante a tradução.
        """
        try:
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode='auto',  # Detecta automaticamente o idioma do texto de origem
                TargetLanguageCode=target_language_code
            )
            return response['TranslatedText'], response['SourceLanguageCode']
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Erro na tradução: {str(e)}") from e
