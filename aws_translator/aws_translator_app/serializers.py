# aws_translator_app/serializers.py

from rest_framework import serializers


class TranslateRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    target_language = serializers.CharField()
    speciality = serializers.CharField()
    style = serializers.CharField()
    complexity_level = serializers.CharField()
    summarize = serializers.BooleanField(default=False)
    model = serializers.CharField()
    focus_aspects = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    temperature = serializers.FloatField(default=0.8)
    max_tokens = serializers.IntegerField(default=1500)


class TranslateResponseSerializer(serializers.Serializer):
    translated_text = serializers.CharField()
    metrics_original = serializers.DictField()
    metrics_simplified = serializers.DictField()
    bleu_score = serializers.FloatField()
    source_language_code = serializers.CharField()


class ImportDocumentSerializer(serializers.Serializer):
    file = serializers.FileField()


class ExportDocumentSerializer(serializers.Serializer):
    text = serializers.CharField()
    metrics_original = serializers.DictField()
    metrics_simplified = serializers.DictField()
    format = serializers.ChoiceField(choices=['pdf', 'docx', 'txt'])
