import re

from django.forms import ModelForm, ModelChoiceField, ImageField, FileField, ClearableFileInput, widgets

from instagram.models import Post

from django.forms.widgets import FileInput
from django.utils.translation import ugettext_lazy
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

# new code
class NotClearableFileInput(FileInput):
    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')

    template_with_initial = '%(initial_text)s: %(initial)s <br />%(input_text)s: %(input)s'

    url_markup_template = '<a href="{0}">{1}</a>'

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
        }
        template = '%(input)s'
        substitutions['input'] = super(NotClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = format_html(self.url_markup_template,
                                               value.url,
                                               force_text(value))

        return mark_safe(template % substitutions)

class PostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'] = FileField(widget=ClearableFileInput(attrs={'multiple': True}))

        # self.fields['images'] = FileField(widgets = {'field_name': NotClearableFileInput})
        # self.fields['images'] = ImageField(attrs={'multiple': True})

    class Meta:
        model = Post
        fields = [
            'message', 'car_number', 'fran_name', 'as_1', 'as_2', 'as_3'
        ]

    # 영어는 저장안됨!
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            message = re.sub(r'[a-zA-Z]+', '', message)
        return message

class PostNonImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = [
            'message', 'car_number', 'fran_name', 'as_1', 'as_2', 'as_3'
        ]