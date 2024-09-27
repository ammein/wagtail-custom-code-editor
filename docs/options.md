# Widget Options

## Table of contents
- [Default Options](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/options.md#default-options)
- [Copy & Paste Options](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/options.md#copy-%26-paste-options)
- [Reset Options](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/options.md#reset-options)

### Default Options

```python
mode="html",
theme="chrome",
width="100%",
height="500px",
font_size=None,
keybinding=None,
useworker=True,
extensions=None,
enable_options=True,
enable_modes=False,
dropdown_config=None,
read_only_config=None,
save_command_config=None,
options=None,
modes=None,
attrs=None
```

- `mode` : `<str>`
> Set default mode when code editor appear.
- `theme` : `<str>` 
> Set default theme. See [list of themes](https://github.com/ajaxorg/ace-builds/blob/master/src/ext-themelist.js#L9).
- `width` : `<str>` 
> Width of Ace Editor
- `height` : `<str>` 
> Height of Ace Editor
- `font_size` : `<str or None>`
> Font size of ace editor
- `keybinding` : `<str or None>`
> Type of keybinding option for Ace Editor
- `useworker` : `<bool>` 
> Turn On/Off for Ace Editor either to use Worker or not (Worker only works on certain mode. Check here).
- `extensions` : `<List[str] or str or None>` 
> Ace Editor extensions to use (All extensions is used by default). You must insert the value without `ext-` and `.js` . Ex: `extensions=["hardwrap", "keybinding_menu", "linking"]`. Check [list of extensions](https://github.com/ajaxorg/ace/tree/master/src/ext).
- `enable_options` : `<bool>` 
> Turn On/Off for Ace Editor Options Configurations that appear as a drawer on the right container.
- `enable_modes` : `<bool>` 
> Turn On/Off for Ace Editor change mode feature when clicking the dropdown.
- `dropdownConfig` : `<Dict[str, str] or None>`
> CSS Config for Dropdown.
```python
dropdown_config={
    "position": {
        "top": "<string>",
        "left": "<string>",
        "right": "<string>",
        "bottom": "<string>"
    },
    "height": "<string>",
    "borderRadius": "<string>",
    "boxShadow": "<string>",
    "width": "<string>",
    "backgroundColor": "<string>"
}
```
- `readOnlyConfig` : `<Dict[str, str] or None>`
> CSS Config for Read Only container.
```python
read_only_config={
    "position": {
        "top": "<string>",
        "left": "<string>",
        "right": "<string>",
        "bottom": "<string>"
    },
    "height": "<string>",
    "borderRadius": "<string>",
    "boxShadow": "<string>",
    "width": "<string>",
    "backgroundColor": "<string>"
}
```
- `saveCommandConfig` : `<Dict[str, str] or None>`
> Save Command Keys for mac & windows when use switch mode. All ace editor [keyboard shortcuts here](https://github.com/ajaxorg/ace/wiki/Default-Keyboard-Shortcuts)
- `options` : `<Dict[str, Any] or str or None>`
> Override existing Ace Editor Options using key and value. Ex: `options=dict(readOnly=True, cursorStyle="smooth", printMarginColumn=100, showFoldWidgets=True, printMargin=50)`
- `modes` : `<List[Dict[str, str]] or None>`
> Override/extend Ace Editor Modes for switching modes feature. Refer [mode's properties](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/settings.md#modes-properties). Ex: `modes=list({ "title": "GLSL", "name": "glsl", "snippet": "@code-here" })`. Check [list of modes](https://github.com/ajaxorg/ace-builds/blob/master/src/ext-modelist.js#L36).
- `attrs` : `<Dict[str, Any] or None>`
> You can set any html value here for the editor container. https://docs.djangoproject.com/en/5.1/ref/forms/widgets/#django.forms.Widget.attrs

### Copy & Paste Options
The best thing about this custom code editor is that you can test out your options in your code editor, copy it and paste the options in your widget/block.

![Copy & Paste Options](https://raw.githubusercontent.com/ammein/wagtail-custom-code-editor/refs/heads/main/docs/options.gif)

Then you can paste the copied options into the `options` kwargs like this:
```python
from wagtail_custom_code_editor.blocks import CustomCodeEditorBlock
from wagtail.blocks import (
    StructBlock,
)

class CodeBlock(StructBlock):
    code = CustomCodeEditorBlock(
                mode='c_cpp', 
                theme='chrome', 
                options="{\"highlightActiveLine\":false,\"showLineNumbers\":false}"
            )
```

> You can also use `Dict` in `options` kwargs like this: `options=dict(highlightActiveLine=False, showLineNumbers=False)`

### Reset Options
Reset options is as easy as press the second button near to copy button like this:

![Reset Options](https://raw.githubusercontent.com/ammein/wagtail-custom-code-editor/refs/heads/main/docs/reset.gif)