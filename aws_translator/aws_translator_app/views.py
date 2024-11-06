# aws_translator_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .constants import LANGUAGES, SPECIALITIES, STYLES, COMPLEXITY_LEVELS, AVAILABLE_MODELS
from .serializers import (
    TranslateRequestSerializer,
    TranslateResponseSerializer,
    ImportDocumentSerializer,
    ExportDocumentSerializer
)
from .services.api.aws_translate_service import AwsTranslateService
from .services.api.openai_service import OpenAIService
from .services.document_service import DocumentService
from .services.language.readability_service import ReadabilityService
from .services.language.bleu_score_service import BleuScoreService


class LanguagesView(APIView):
    def get(self, request):
        return Response(LANGUAGES)


class SpecialitiesView(APIView):
    def get(self, request):
        return Response(SPECIALITIES)


class StylesView(APIView):
    def get(self, request):
        return Response(STYLES)


class ComplexityLevelsView(APIView):
    def get(self, request):
        return Response(COMPLEXITY_LEVELS)


class ModelsView(APIView):
    def get(self, request):
        return Response(AVAILABLE_MODELS)


class TranslateView(APIView):
    def post(self, request):
        serializer = TranslateRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            text = data['text']
            target_language = data['target_language']
            speciality = data['speciality']
            style = data['style']
            summarize = data['summarize']
            model = data['model']
            complexity_level = data['complexity_level']
            focus_aspects = data.get('focus_aspects', [])
            temperature = data['temperature']
            max_tokens = data['max_tokens']

            try:
                # Initialize services
                aws_service = AwsTranslateService()
                openai_service = OpenAIService()
                readability_service = ReadabilityService()
                bleu_service = BleuScoreService()

                # Simplify text using OpenAI
                simplified_text = openai_service.simplify_text(
                    text=text,
                    area_tecnica=speciality,
                    estilo=style,
                    summarize=summarize,
                    model=model,
                    complexity_level=complexity_level,
                    focus_aspects=focus_aspects,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                # Calculate readability metrics
                metrics_original = readability_service.calculate_readability(text)
                metrics_simplified = readability_service.calculate_readability(simplified_text)

                # Translate simplified text
                translated_text, source_language_code = aws_service.translate_text(
                    simplified_text, target_language
                )

                # Compute BLEU score
                bleu_score = bleu_service.compute_bleu_score(
                    simplified_text, translated_text, source_language_code
                )

                response_data = {
                    'translated_text': translated_text,
                    'metrics_original': metrics_original,
                    'metrics_simplified': metrics_simplified,
                    'bleu_score': bleu_score,
                    'source_language_code': source_language_code
                }

                response_serializer = TranslateResponseSerializer(response_data)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImportDocumentView(APIView):
    def post(self, request):
        serializer = ImportDocumentSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            doc_service = DocumentService()
            try:
                text = doc_service.import_document(file)
                return Response({'text': text}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExportDocumentView(APIView):
    def post(self, request):
        serializer = ExportDocumentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            text = data['text']
            metrics_original = data['metrics_original']
            metrics_simplified = data['metrics_simplified']
            format = data['format']
            doc_service = DocumentService()
            try:
                # Generate the document and get the file path
                file_path = doc_service.export_document(
                    text=text,
                    metrics_original=metrics_original,
                    metrics_simplified=metrics_simplified,
                    format=format
                )
                # Return the file as a response
                with open(file_path, 'rb') as f:
                    response = Response(f.read(), content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    return response
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
