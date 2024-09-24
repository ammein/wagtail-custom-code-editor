# wagtail-custom-code-editor
![Workflow](https://github.com/ammein/wagtail-custom-code-editor/actions/workflows/github-actions-check.yml/badge.svg)

A **Wagtail Custom Code Editor Field** for your own editor field.

This package adds a full-featured code editor that is perfect for coding tutorials, documentation containing code examples, or any other type of page that needs to display code.

This field uses the open-source Ace Editor library that you may found here [Ace Editor](https://ace.c9.io/)

![intro](https://raw.githubusercontent.com/ammein/wagtail-custom-code-editor/refs/heads/main/docs/intro.gif)

## Install

In your settings, add the package in `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    "wagtail_custom_code_editor",
    ...
]
```

### Usage

#### Field
You can easily add the `CustomCodeEditorField` to your model fields like this:
```python
from wagtail_custom_code_editor.fields import CustomCodeEditorField

class MyPage(Page):
    code = CustomCodeEditorField()
    ...
```

#### Panel
Then you add `CustomCodeEditorPanel` like this:

```python
from wagtail_custom_code_editor.panels import CustomCodeEditorPanel
from wagtail_custom_code_editor.fields import CustomCodeEditorField

class MyPage(Page):
    code = CustomCodeEditorField()

    content_panels = Page.content_panels + [
        CustomCodeEditorPanel('code')
    ]
```

## License

Wagtail-Geo-Widget is released under the [MIT License](http://www.opensource.org/licenses/MIT).