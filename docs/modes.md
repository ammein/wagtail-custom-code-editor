# Change Modes

## Table of contents
- [Modes Config](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/modes.md#modes-config)
- [Save Highlight Switching Modes](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/modes.md#save-highlight-switching-modes)
- [Override / Extend Modes](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/modes.md#override--extend-modes)

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

### Override / Extend Modes
If you wish to **disable snippet** on default mode for html, you can easily override like this:
```python
from wagtail_custom_code_editor.panels import CustomCodeEditorPanel
from wagtail_custom_code_editor.fields import CustomCodeEditorField

class MyPage(Page):
    code = CustomCodeEditorField()

    content_panels = Page.content_panels + [
        CustomCodeEditorPanel('code', mode='c_cpp', theme='monokai', modes=[
            {
                "name": "html",
                "disableSnippet": True
            }
        ], enable_modes=True, dropdown_config={
            "position": {
                "bottom": '20px',
                "right": "20px"
            },
        })
    ]
```
> Make sure the `name` value is the same name as default modes. The override can only happen if `name` property is similar. The default modes can be found here: https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/settings.md#default-settings

You can also add additional modes to the default modes like this:
```python
from wagtail_custom_code_editor.panels import CustomCodeEditorPanel
from wagtail_custom_code_editor.fields import CustomCodeEditorField

class MyPage(Page):
    code = CustomCodeEditorField()

    content_panels = Page.content_panels + [
        CustomCodeEditorPanel('code', mode='c_cpp', theme='monokai', modes=[
            {
                "name": "glsl",
                "snippet": """
                #version 300
                
                uniform float time;
                
                void main() {
                    gl_FragColor = vec4(vec3(1.0), 1.);
                }
                """
            }
        ], enable_modes=True, dropdown_config={
            "position": {
                "bottom": '20px',
                "right": "20px"
            },
        })
    ]
```
> This only happens if `name` value is not similar to any default modes settings. Therefore, it adds...

### Save Highlight Switching Modes
You can save new specific codes when switching the modes instead of copying everthing from your initial code. Highlight the code you want, and hit this command while the editor is active before switching mode. Refer command below:

| Windows     | Mac            |
|-------------|----------------|
| Alt-Shift-S | Option-Shift-S |

![Save Modes](https://raw.githubusercontent.com/ammein/wagtail-custom-code-editor/refs/heads/main/docs/save_modes.gif)
