# aws_translator_app/services/language/readability_service.py

"""
Readability Service Module
==========================

Este módulo fornece serviços para calcular métricas de legibilidade de textos.
Suporta o cálculo das seguintes métricas:

- Índice de Flesch Reading Ease
- Grau de Flesch-Kincaid
- Índice SMOG
- Índice de Coleman-Liau
- Índice Automático de Legibilidade (ARI)
- Pontuação de Dale-Chall

Classes:
    ReadabilityService: Classe responsável pelo cálculo das métricas de legibilidade.

Dependências:
    - textstat: biblioteca para calcular métricas de legibilidade.
    - langdetect: biblioteca para detecção de idioma de textos.

Exemplo de Uso:
    >>> from translation_app.services.language.readability_service import ReadabilityService
    >>> texto = "Este é um texto de exemplo para avaliar a legibilidade."
    >>> metrics = ReadabilityService.calculate_readability(texto)
    >>> print(metrics)
    {
        'flesch_reading_ease': 60.00,
        'flesch_kincaid_grade': 8.00,
        'smog_index': 7.50,
        'coleman_liau_index': 10.20,
        'automated_readability_index': 9.30,
        'dale_chall_readability_score': 7.00
    }
"""

import textstat
from langdetect import detect
import os


class ReadabilityService:
    """
    Serviço para calcular métricas de legibilidade de textos.

    Este serviço utiliza a biblioteca `textstat` para calcular diversas métricas
    de legibilidade. A detecção de idioma é realizada com a biblioteca `langdetect`
    para ajustar as métricas conforme o idioma do texto fornecido.

    Métodos:
        calculate_readability(text: str) ⇒ dict:
            Calcula e retorna as métricas de legibilidade para o texto fornecido.
    """

    def __init__(self):
        """
        Inicializa a instância do ReadabilityService.

        Atualmente, não há atributos de instância a serem inicializados.
        """
        pass

    @staticmethod
    def load_easy_words(language_code: str) -> None:
        """
        Carrega a lista de palavras fáceis para o idioma especificado.

        Se o idioma for Português ('pt'), carrega as palavras do arquivo 'pt_easy_words.txt'.
        Caso contrário, utiliza a lista padrão para o idioma configurado em `textstat`.

        Args:
            language_code (str): Código do idioma (e.g., 'en', 'pt').
        """
        if language_code == 'pt':
            # Caminho para o arquivo de palavras fáceis em português
            easy_words_file = os.path.join(os.path.dirname(__file__), 'pt_easy_words.txt')
            try:
                with open(easy_words_file, 'r', encoding='utf-8') as file:
                    easy_words = set(word.strip().lower() for word in file if word.strip())
                textstat.easy_word_set = easy_words
            except FileNotFoundError:
                print(f"Arquivo {easy_words_file} não encontrado. Usando lista padrão de palavras fáceis em Inglês.")
                # Define inglês como padrão se o arquivo não for encontrado
                textstat.set_lang('en')
        else:
            # Para outros idiomas suportados, usa a configuração padrão do textstat
            pass

    @staticmethod
    def calculate_readability(text: str) -> dict:
        """
        Calcula métricas de legibilidade para o texto fornecido.

        Este metodo realiza os seguintes passos:
            1. Detecta o idioma do texto usando `langdetect`.
            2. Configura o idioma para a biblioteca `textstat` se suportado.
            3. Carrega a lista de palavras fáceis para o idioma.
            4. Calcula as métricas de legibilidade.
            5. Retorna as métricas em um dicionário.

        Parâmetros:
            text (str): O texto a ser analisado.

        Retorna:
            dict: um dicionário contendo as métricas de legibilidade calculadas.

        Exceções:
            - Nenhuma exceção explícita é lançada. Caso ocorra um erro na detecção do idioma,
              o idioma padrão será configurado como inglês ('en').
        """
        # Detecta o idioma do texto
        try:
            language_code = detect(text)
            # Lista de idiomas suportados pelo textstat
            supported_languages = ['en', 'es', 'de', 'fr', 'it', 'nl', 'pt', 'ru']
            if language_code in supported_languages:
                textstat.set_lang(language_code)
                ReadabilityService.load_easy_words(language_code)
            else:
                # Define inglês como padrão se o idioma não for suportado
                textstat.set_lang('en')
        except Exception:
            # Em caso de erro na detecção do idioma, define inglês como padrão
            textstat.set_lang('en')

        # Calcula as métricas de legibilidade
        metrics = {
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
            'smog_index': textstat.smog_index(text),
            'coleman_liau_index': textstat.coleman_liau_index(text),
            'automated_readability_index': textstat.automated_readability_index(text),
            'dale_chall_readability_score': textstat.dale_chall_readability_score(text)
        }

        return metrics
