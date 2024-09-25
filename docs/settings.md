# Settings

## Table of Contents
- [Override Modes](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/settings.md#override-modes)
  - [Modes Properties](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/settings.md#modes-properties)
- [Emmet URL](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/settings.md#emmet-url)
- [Ace Editor Options Settings](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/settings.md#ace-editor-options-settings)
- [Default Settings](https://github.com/ammein/wagtail-custom-code-editor/blob/main/docs/settings.md#default-settings)

### Override Modes
These modes are used when you set kwargs parameter in widget called `enable_modes=True`, and you can easily switch mode by clicking the dropdown button. You can override the whole modes using _List_ of _Dictionaries_ from key named `MODES` in settings:
```python
WAGTAIL_CUSTOM_CODE_EDITOR = {
    "MODES": [
        {
            "title": "Installed Apps Django",
            "name": "python",
            "snippet": """
            INSTALLED_APPS = [
                @code-here
            ]
            """
        },
        {
            "title": "XML",
            "name": "xml",
            "snippet": """
            <note>
                <script/>
                <to>Tove</to>
                <from>Jani</from>
                <heading>Reminder</heading>
                <body>@code-here</body>
            </note>
            """
        }
    ]
}
```
#### Modes Properties
- `title` - You can set any title name you want for specific mode
- `name` - (CASE SENSITIVE) You must set the name of the mode for Ace Editor to set appropriate mode. You can see list of latest [modes here](https://github.com/ajaxorg/ace/tree/master/src/mode)
- `snippet` - This is where your existing code will be replaced by this snippet value.
- `disableSnippet` - You can set this key using boolean value if you want to disable the snippet on specific mode's name.
- `@code-here` - If you notice this from example above, any existing code will be placed on `@code-here` placement anywhere in the snippet texts. Useful if you wish retain the same value when switching modes.

### Emmet URL
By default, the emmet used for `html` mode is for experienced programmers who build HTML faster using emmet shortcodes. This needs to be extended for Ace Editor usage, and you can provide any emmet extension here by replacing this value:
```python
WAGTAIL_CUSTOM_CODE_EDITOR = {
    "EMMET_URL": "https://custom-emmet-extensions/emmet.js"
}
```

If you wish to push your own emmet extensions or disable emmet extensions, you can simply set to `None` like this:
```python
WAGTAIL_CUSTOM_CODE_EDITOR = {
    "EMMET_URL": None
}
```

### Ace Editor Options Settings
These options settings are the inputs for you to configure ace options from the Code Editor Field in your admin. You will be able to see these options when you clicked _Cog_ icon on top right corner (Available when `enable_options` is set to `True`). If you wish to override options settings, you may configure it in settings like this:
```python
WAGTAIL_CUSTOM_CODE_EDITOR = {
    "OPTIONS_TYPES": [
        # For Select Input
        {
            "name": "<your-custom-ace-options-name>", # Ace options name
            "type": "string", # Type of input value
            "value": ["line", "text"], # Choices value
            "category": "editor", # Category for this options
        },
        # For Select Custom Title Input
        {
            "name": "<your-custom-ace-options-name>",
            "type": "string", # Type of input value
            "value": [
                {"title": "Always", "value": "always"},
                {"title": "Never", "value": False},
                {"title": "Timed", "value": True},
            ], # Choices value
            "category": "editor", # Category for this options
        },
        # For Number Input
        {
            "name": "<your-custom-ace-options-name>", # Ace options name
            "type": "number", # Type of input value
            "value": 10, # Default Value
            "category": "mouseHandler", # Category for this options
        },
        # For Slider Number Input
        {
            "name": "<your-custom-ace-options-name>",
            "type": "number",  # Type of input value
            "value": {"min": 0, "max": 100, "steps": 1}, # Default Slider Attribute Value
            "category": "renderer", # Category for this options
        },
    ]
}
```

### 

### Default Settings

```python
WAGTAIL_CUSTOM_CODE_EDITOR = {
    "EMMET_URL": "https://cloud9ide.github.io/emmet-core/emmet.js",
    # MODES
    "MODES": [
        {
            "title": "Bash",
            "name": "sh",
            "snippet": """
                #!/bin/bash
                # GNU bash, version 4.3.46
                @code-here
            """
        },
        {
            "title": "ActionScript",
            "name": "actionscript"
        },
        {
            "title": "C++",
            "name": "c_cpp",
            "snippet": """
                //Microsoft (R) C/C++ Optimizing Compiler Version 19.00.23506 for x64
                #include <iostream>
        
                int main()
                {
                   @code-here
                }
            """
        },
        {
            "title": "C#",
            "name": "csharp",
            "snippet": """
                //Rextester.Program.Main is the entry point for your code. Don't change it.
                //Compiler version 4.0.30319.17929 for Microsoft (R) .NET Framework 4.5
            
                using System;
                using System.Collections.Generic;
                using System.Linq;
                using System.Text.RegularExpressions;
            
                namespace Rextester
                {
                   public class Program
                   {
                      public static void Main(string[] args)
                      {
                            // code goes here
                            @code-here
                      }
                   }
                }
            """
        },
        {
            "name": "php",
            "snippet": """
                <html>
                <head>
                <title>PHP Test</title>
                </head>
                <body>
                <?php //code goes here
                   @code-here
                ?> 
                </body>
                </html>
            """
        },
        {
            "name": "html",
            "snippet": """
                <!DOCTYPE html>
                <html>
                <head>
                <title>
                    <!-- Title Here -->
                </title>
                </head>
                <body>
                    <!-- Code-here -->
                    @code-here
                </body>
                </html>
            """
        },
        {
            "name": "javascript",
            "snippet": """
                document.addEventListener("DOMContentLoaded" , function(){
                   @code-here
                });
            """
        }
    ],
    # Options
    "OPTIONS_TYPES": [
        {
            "name": "selectionStyle",
            "type": "string",
            "value": ["line", "text"],
            "category": "editor",
        },
        {
            "name": "highlightActiveLine",
            "type": "boolean",
            "value": None,
            "category": "editor",
        },
        {
            "name": "highlightSelectedWord",
            "type": "boolean",
            "value": None,
            "category": "editor",
        },
        {
            "name": "readOnly",
            "type": "boolean",
            "value": None,
            "category": "editor",
        },
        {
            "name": "cursorStyle",
            "type": "string",
            "value": ["ace", "slim", "smooth", "wide"],
            "category": "editor",
        },
        {
            "name": "mergeUndoDeltas",
            "type": "string",
            "value": [
                {"title": "Always", "value": "always"},
                {"title": "Never", "value": False},
                {"title": "Timed", "value": True},
            ],
            "category": "editor",
        },
        {
            "name": "behavioursEnabled",
            "type": "boolean",
            "value": None,
            "category": "editor",
        },
        {
            "name": "wrapBehavioursEnabled",
            "type": "boolean",
            "value": None,
            "category": "editor",
        },
        {
            "name": "autoScrollEditorIntoView",
            "type": "boolean",
            "value": None,
            "help": "This is needed if editor is inside scrollable page",
            "category": "editor",
        },
        {
            "name": "copyWithEmptySelection",
            "type": "boolean",
            "value": None,
            "help": "Copy/Cut the full line if selection is empty, "
                    "defaults to False",
            "category": "editor",
        },
        {
            "name": "useSoftTabs",
            "type": "boolean",
            "value": None,
            "category": "editor",
        },
        {
            "name": "navigateWithinSoftTabs",
            "type": "boolean",
            "value": None,
            "category": "editor",
        },
        {
            "name": "enableMultiSelect",
            "type": "boolean",
            "value": None,
            "category": "editor",
        },
        {
            "name": "hScrollBarAlwaysVisible",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "vScrollBarAlwaysVisible",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "highlightGutterLine",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "animatedScroll",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "showInvisibles",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "showPrintMargin",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "printMarginColumn",
            "type": "number",
            "value": {"min": 0, "max": 100, "steps": 1},
            "category": "renderer",
        },
        {
            "name": "printMargin",
            "type": "number",
            "value": {"min": 0, "max": 100, "steps": 1},
            "category": "renderer",
        },
        {
            "name": "fadeFoldWidgets",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "showFoldWidgets",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "showLineNumbers",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "showGutter",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "displayIndentGuides",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "scrollPastEnd",
            "type": ["number", "boolean"],
            "value": {"min": 0, "max": 1, "steps": 0.1},
            "help": "Number of page sizes to scroll after document end "
                    "(typical values are 0, 0.5, and 1)",
            "category": "renderer",
        },
        {
            "name": "fixedWidthGutter",
            "type": "boolean",
            "value": None,
            "category": "renderer",
        },
        {
            "name": "scrollSpeed",
            "type": "number",
            "value": {"min": 0, "max": 100, "steps": 1},
            "category": "mouseHandler",
        },
        {
            "name": "dragDelay",
            "type": "number",
            "value": {"min": 0, "max": 200, "steps": 1},
            "category": "mouseHandler",
        },
        {
            "name": "dragEnabled",
            "type": "boolean",
            "value": None,
            "category": "mouseHandler",
        },
        {
            "name": "focusTimeout",
            "type": "number",
            "value": None,
            "category": "mouseHandler",
        },
        {
            "name": "tooltipFollowsMouse",
            "type": "boolean",
            "value": None,
            "category": "mouseHandler",
        },
        {
            "name": "overwrite",
            "type": "boolean",
            "value": None,
            "category": "session",
        },
        {
            "name": "newLineMode",
            "type": "string",
            "value": ["auto", "unix", "windows"],
            "category": "session",
        },
        {
            "name": "tabSize",
            "type": "number",
            "value": {"min": 0, "max": 20, "steps": 1},
            "category": "session",
        },
        {
            "name": "wrap",
            "type": ["boolean", "number"],
            "value": None,
            "category": "session",
        },
        {
            "name": "foldStyle",
            "type": "string",
            "value": ["markbegin", "markbeginend", "manual"],
            "category": "session",
        },
        {
            "name": "enableBasicAutocompletion",
            "type": "boolean",
            "value": None,
            "category": "extension",
        },
        {
            "name": "enableLiveAutocompletion",
            "type": "boolean",
            "value": None,
            "category": "extension",
        },
        {
            "name": "enableEmmet",
            "type": "boolean",
            "value": None,
            "category": "extension",
        },
        {
            "name": "useElasticTabstops",
            "type": "boolean",
            "value": None,
            "category": "extension",
        },
    ]
}
```