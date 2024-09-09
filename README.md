# wagtail-custom-code-editor


A Wagtail Custom Field for your own in editor field.

This package adds a full-featured code editor that is perfect for coding tutorials, documentation containing code examples, or any other type of page that needs to display code.

This field uses the open-source Ace Editor library that you may found here [Ace Editor](https://ace.c9.io/)


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
class MyPage(Page):
    code = CustomCodeEditorField()
    ...
```

#### Panel
Then you must add `CustomCodeEditorPanel` like this:
```python
class MyPage(Page):
    code = CustomCodeEditorField()

    content_panels = Page.content_panels + [
        CustomCodeEditorPanel('code')
    ]
```

Then you'll see like this:
