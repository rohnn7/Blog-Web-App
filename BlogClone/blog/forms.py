from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author', 'title', 'content')
        #helps you style the form using connection to css
        widgets={
            #textinputclass and postcontent are the class we will make in css rest all the class is builtin to css
            'title': forms.TextInput(attrs={'class':'textinputclass'}),
            'content':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent', 'id':'editor1'})
        }

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author', 'content')
        #helps you style the form using connection to css
        widgets={
            #textinputclass are the class we will make in css rest all the class is builtin to css
            'author': forms.TextInput(attrs={'class':'textinputclass'}),
            'content':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
