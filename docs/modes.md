# Change Modes

## Table of contents
- [Modes Config](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/options.md#modes-config)
- [Save Highlight Switching Modes](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/options.md#save-highlight-switching-modes)

### Modes Config
You must set `enable_modes` to `True` to use change modes feature like this:
```python
from wagtail_custom_code_editor.panels import CustomCodeEditorPanel
from wagtail_custom_code_editor.fields import CustomCodeEditorField

class MyPage(Page):
    code = CustomCodeEditorField()

    content_panels = Page.content_panels + [
        CustomCodeEditorPanel('code', mode='c_cpp', theme='monokai', enable_modes=True)
    ]
```

Then you can switch modes as you wish like this:

![Enable Modes](https://raw.githubusercontent.com/ammein/wagtail-custom-code-editor/refs/heads/main/docs/enable_modes.gif)

> If you wish to confirm the selected modes and the snippet value, click the "Read Only Mode" button below to confirm, and you may start editing on it as you wish.

You noticed that the dropdown placement is somewhat off. You can customize the dropdown position  by insert value on `dropdown_config` like this:
```python
from wagtail_custom_code_editor.panels import CustomCodeEditorPanel
from wagtail_custom_code_editor.fields import CustomCodeEditorField

class MyPage(Page):
    code = CustomCodeEditorField()

    content_panels = Page.content_panels + [
        CustomCodeEditorPanel('code', mode='c_cpp', theme='monokai', enable_modes=True, dropdown_config={
            "position": {
                "bottom": '20px',
                "right": "20px"
            },
        })
    ]
```
> This also applies the same for `read_only_config` kwargs. You can refer the [value properties here](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/options.md#default-options).

### Save Highlight Switching Modes
You can save new specific codes when switching the modes instead of copying everthing from your initial code. Highlight the code you want, and hit this command while the editor is active before switching mode. Refer command below:

| Windows     | Mac            |
|-------------|----------------|
| Alt-Shift-S | Option-Shift-S |

![Save Modes](https://raw.githubusercontent.com/ammein/wagtail-custom-code-editor/refs/heads/main/docs/save_modes.gif)
