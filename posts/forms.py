from .models import Post
from django.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["group", "text"]
        labels = {'text': 'Текст поста', 'group': 'Группа'}
        help_texts = {'text': 'Введите текст поста', 'group': 'Укажите группу'}
