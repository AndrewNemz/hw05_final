from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    help_texts = {
        'text': ('Поле для текста Вашей записи'),
        'group': (
            'Группа, к которой будет относиться'
            'Ваша запись'
        ),
        'image': ('Картинка к Вашему посту')
    }

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        data = self.cleaned_data['text']
        if data.isspace():
            raise forms.ValidationError(
                'Ошибка: пост не должен состоять только из пробелов'
            )
        return data


class CommentForm(forms.ModelForm):
    help_texts = {
        'text': 'Текст вашего комментария'
    }

    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):                                 # test_func
        data = self.cleaned_data['text']
        if data.isspace():
            raise forms.ValidationError(
                'Ошибка: комментарий не должен состоять только из пробелов'
            )
        return data
