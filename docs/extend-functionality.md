# Extend Ace Editor Functionality (Javascript)
You can add more commands or even add ace editor functionality using Javascript event.

First, add `js` file in your static app folder. And add this event:
```js
// js/code-extend.js
window.addEventListener('customCodeEditor:afterInit', function(e) {
    // You can do anything you want with ace editor 
    // after the ace editor was initialized
    console.log("After Init:", e.detail.editor)
})

window.addEventListener('customCodeEditor:beforeInit', function(e) {
    // You can do anything you want with textarea or any DOM element 
    // before the ace editor is going to be initialized
    console.log("Before Init:", e.detail.textarea)
})
```

Then add the javascript file on admin global using wagtail hooks like this:
```python
from wagtail import hooks
from django.templatetags.static import static
from django.utils.safestring import mark_safe

@hooks.register("insert_global_admin_js")
def global_admin_js():
    """Add /static/css/custom.js to the admin."""
    return mark_safe(
        f'<script src="{static("/js/code-extend.js")}"></script>')
```

Then open your cms, navigate to the page where it has code editor setup and see console log!