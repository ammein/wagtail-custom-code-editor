# Django Admin
You can also use this widget in your `django-admin` setup. Say your app has this code in your `models.py` like this for your wagtail snippet:
```python
from django.db import models
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin
)
from wagtail.snippets.models import register_snippet
from wagtail_custom_code_editor.panels import CustomCodeEditorPanel
from wagtail_custom_code_editor.fields import CustomCodeEditorField

@register_snippet
class CodeModel(DraftStateMixin, RevisionMixin, TranslatableMixin, PreviewableMixin, models.Model):
    first_code = CustomCodeEditorField()
    second_code = CustomCodeEditorField()

    panels = [
        CustomCodeEditorPanel('first_code', theme='monokai', mode='html', dropdown_config={
            "position": {
                "bottom": "30px",
                "right": "30px"
            }
        }),
        CustomCodeEditorPanel('second_code', theme='github', mode='javascript', dropdown_config={
            "position": {
                "bottom": "30px",
                "right": "30px"
            }
        })
    ]
```

Then you must add forms in `forms.py` in your app for it to work on Django admin:
```python
from django import forms
from wagtail_custom_code_editor.widgets import CustomCodeEditorWidget

from .models import CodeModel


class CodeModelForm(forms.ModelForm):
    class Meta:
        model = CodeModel
        fields = '__all__'
        widgets = {
            'first_code': CustomCodeEditorWidget(mode='html', theme='monokai', django_admin=True, enable_options=False),
            'second_code': CustomCodeEditorWidget(mode='javascript', theme='monokai', django_admin=True, enable_options=False),
        }
```
> You must set `django_admin` to true for it to be able to use in Django Admin forms.

Then register the form in `admin.py` for it to display in admin UI
```python
from django.contrib import admin

from .models import CodeModel
from .forms import CodeModelForm


class CodeModelFormAdmin(admin.ModelAdmin):
    form = CodeModelForm


# Register your models here.
admin.site.register(CodeModel, CodeModelFormAdmin)
```

Voilà! You can see that the Custom Code Editor Widget display in your `django-admin` url! Navigate to that Model in Django Admin, and see for yourself!