# aws_translator_app/services/language/bleu_score_service.py

"""
BLEU Score Service Module
=========================

Este módulo fornece serviços para calcular o BLEU Score usando Back-Translation.
Ele utiliza o serviço AWS Translate para tradução e back-translation, e a biblioteca
sacrebleu para calcular o BLEU Score.

Classes:
    BleuScoreService: Classe responsável por calcular o BLEU Score.

Dependências:
    - sacrebleu: Biblioteca para calcular o BLEU Score.
    - services.api.aws_translate_service: Para realizar traduções.

Exemplo de Uso:
    >>> from translation_app.services.language.bleu_score_service import BleuScoreService
    >>> bleu_service = BleuScoreService()
    >>> original_text = "Este é um teste."
    >>> translated_text = "This is a test."
    >>> source_language_code = "pt"
    >>> bleu_score = bleu_service.compute_bleu_score(original_text, translated_text, source_language_code)
    >>> print(bleu_score)
    0.8521
"""

import sacrebleu
from aws_translator_app.services.api.aws_translate_service import AwsTranslateService


class BleuScoreService:
    """
    Serviço para calcular o BLEU Score usando Back-Translation.

    Métodos:
        compute_bleu_score(original_text: str, translated_text: str, source_language_code: str) -> float:
            Traduz o texto traduzido de volta para o idioma original e calcula o BLEU Score entre o texto original e o texto back-translated.
    """

    def __init__(self):
        """
        Inicializa a instância do BleuScoreService.
        """
        self.aws_translate_service = AwsTranslateService()

    def compute_bleu_score(self, original_text: str, translated_text: str, source_language_code: str) -> float:
        """
        Calcula o BLEU Score realizando back-translation do texto traduzido para o idioma de origem.

        Parâmetros:
            original_text (str): O texto original (no idioma de origem).
            translated_text (str): O texto traduzido (no idioma de destino).
            source_language_code (str): O código do idioma de origem.

        Retorna:
            float: O BLEU Score entre o texto original e o texto back-translated na escala de 0 a 1.

        Exceções:
            - Exception: Se ocorrer um erro durante a tradução de volta ou no cálculo do BLEU Score.
        """
        try:
            # Back-translation para o idioma de origem
            back_translated_text, _ = self.aws_translate_service.translate_text(translated_text, source_language_code)

            # Cálculo do BLEU Score para sentença única com suavização e normalização
            bleu = sacrebleu.sentence_bleu(
                back_translated_text,
                [original_text],
                smooth_method='exp',
                smooth_value=0.1,
                lowercase=True
            )

            # Normaliza o BLEU Score para a escala de 0 a 1
            normalized_bleu = bleu.score / 100
            return normalized_bleu

        except Exception as e:
            raise Exception(f"Erro ao calcular o BLEU Score: {str(e)}") from e
