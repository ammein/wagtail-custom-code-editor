// noinspection JSUnresolvedReference

(function(){
    function CustomCodeEditorWidget(html, id, ace) {
        this.html = html;
        this.id = id;
        this.ace = ace;
    }

    CustomCodeEditorWidget.prototype.render = function(placeholder, name, id, initialState){
        // eslint-disable-next-line no-param-reassign
        placeholder.innerHTML = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        // eslint-disable-next-line no-undef
        const codeEditor = new CustomCodeEditor(placeholder.querySelector('div.editor-' + id));
        // Hacky way to insert default original value
        if(codeEditor.originalValue.code){
            placeholder.querySelector('textarea#' + id).innerHTML = JSON.stringify({
                "mode": codeEditor.originalValue.mode,
                "code": codeEditor.originalValue.code
            })
        } else {
            codeEditor.setState(JSON.parse(initialState));
        }

        return codeEditor;
    };

    window.telepath.register('wagtail_custom_code_editor.widgets.CustomCodeEditor', CustomCodeEditorWidget);
})()