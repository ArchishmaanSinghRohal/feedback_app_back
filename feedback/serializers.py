from rest_framework import serializers
from feedback.models import Videos, Form_feedback
from django.contrib.auth.models import User
from rest_framework import permissions
class SnippetSerializer(serializers.ModelSerializer):
    uploader_id = serializers.ReadOnlyField(source='uploader_id.username')
    class Meta:
        model = Videos
        fields = ['uploader_id', 'video_url','school_name']

class FormSerializer(serializers.ModelSerializer):
    filled_by = serializers.ReadOnlyField(source='filled_by.username')
    class Meta:
        model = Form_feedback
        fields = ['filled_by','school_name','q1','q2','q3','q4','q5','q6','q7','q8','q9','q10']

class UserSerializer(serializers.ModelSerializer):
    videos = serializers.PrimaryKeyRelatedField(many=True, queryset=Videos.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'videos']