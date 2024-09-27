# Widget Options

## Default Options

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
> Set default theme.
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
> CSS Config for Dropdown Config.
- `readOnlyConfig` : `<Dict[str, str] or None>`
> CSS Config for Read Only Container Config
- `saveCommandConfig` : `<Dict[str, str] or None>`
> Save Command Keys for mac & windows when use switch mode.
- `options` : `<Dict[str, Any] or None>`
> Set Ace Editor Options using key and value. Ex: `options=dict(readOnly=True, cursorStyle="smooth", printMarginColumn=100, showFoldWidgets=True,
                             printMargin=50)`
- `modes` : `<List[Dict[str, str]] or None>`
> Set Ace Editor Modes for switching modes feature. Ex `modes=List({
                "title": "GLSL",
                "name": "glsl",
                "snippet": "@code-here"
            })`
- `attrs` : `<Dict[str, Any] or None>`
> You can set any html value here for the editor container. https://docs.djangoproject.com/en/5.1/ref/forms/widgets/#django.forms.Widget.attrs