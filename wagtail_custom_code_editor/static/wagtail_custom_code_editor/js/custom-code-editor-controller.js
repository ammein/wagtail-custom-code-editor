// noinspection JSUnusedGlobalSymbols,JSUnresolvedReference

class CustomCodeEditorStimulus extends window.StimulusModule.Controller {
    static targets = ['container', 'editor', 'input', 'dropdown', 'modeDropdown', 'copy', 'undo', 'optionsButton', 'options', 'optionList', 'optionsContainer', 'modes', 'modeList', 'notification']

    static values = {
        theme: String,
        mode: String,
        modes: Array,
        options: Array,
        originalOptions: Object,
        dropdownConfig: {
            defaultValue: {},
            type: Object
        }
    };

    connect() {
        this.ace = {
            theme: this.themeValue,
            defaultMode: this.modeValue,
            modes: this.modesValue,
            options: this.optionsValue,
            saveValue: {}
        }

        this.getValue = JSON.parse(this.inputTarget.value)

        if(this.hasCopyTarget && ClipboardJS.isSupported()) {
            new ClipboardJS(this.copyTarget);
        } else if(this.hasCopyTarget && !ClipboardJS.isSupported()) {
            this.copyTarget.style.display = 'none'
            this.undoTarget.style.display = 'none'
        }

        this.#initEditor()
    }

    #setBubble(range, bubble) {
        const val = range.value;
        const min = range.min ? range.min : 0;
        const max = range.max ? range.max : 100;
        const newVal = Number(((val - min) * 100) / (max - min));

        // Sorta magic numbers based on size of the native UI thumb
        bubble.style.left = `calc(${newVal}% + (${(23/6) - newVal * 0.2}px - ${23/2}px))`;
    }

    checkboxOnChange(event) {
        if (event.target.checked) {
            this.editor.setOption(event.target.name, true)
        } else {
            this.editor.setOption(event.target.name, false)
        }
    }

    dropdownOnChange(event){
        this.editor.setOption(event.target.name, event.target.value)
    }

    dropdownObjectOnChange(event){
        let value = typeof event.target.value === 'string' ? JSON.parse(event.target.value) : event.target.value;
        this.editor.setOption(event.target.name, value)
    }

    sliderOnChange(event) {
        let output = event.target.nextElementSibling;
        event.target.setAttribute('value', event.target.value)
        this.#setBubble(event.target, output);
        output.innerText = event.target.value
        output.style.display = 'block'
        this.editor.setOption(event.target.name, event.target.value)
    }

    sliderOnFocusOut(event) {
        let output = event.target.nextElementSibling;
        output.style.display = 'none'
    }

    numberOnChange(event) {
        this.editor.setOption(event.target.name, event.target.value)
    }

    toggleOptions(event){
        event.preventDefault()
        if (this.optionsContainerTarget.style.display === 'none') {
            this.optionsContainerTarget.style.removeProperty('display')
        } else {
            this.optionsContainerTarget.style.display = 'none'
        }
    }

    toggleModes(_event) {
        if (this.modesTarget.style.display === 'none') {
            this.modesTarget.style.removeProperty('display')
        } else {
            this.modesTarget.style.display = 'none'
        }
    }

    searchMode(event){
        let search = event.target.value;

        Array.from(this.modeListTargets).forEach((mode) => {

            // Get name
            let name = mode.dataset.name.toUpperCase().indexOf(search.toUpperCase());

            // Channel to each conditions
            switch(true) {
                case mode.dataset.title && mode.dataset.title.toUpperCase().indexOf(search.toUpperCase()) > -1:
                    mode.style.removeProperty('display');
                    break;
                
                case !mode.dataset.title && name > -1:
                    mode.style.removeProperty('display');
                    break;

                default:
                    mode.style.display = 'none'
            }
        })
    }

    searchOptions(event) {
        let search = event.target.value;

        Array.from(this.optionListTargets).forEach((option) => {
            let name = CustomCodeEditor.camelCaseToWords(option.id);

            if(name.toUpperCase().indexOf(search.toUpperCase()) > -1){
                option.style.removeProperty('display');
            } else {
                option.style.display = 'none'
            }
        })
    }

    setMode(event) {
        this.editorMode(event.params.mode)
    }

    editorMode(name) {
        // Turn off onChange active for easy replace code from existing value
        this.editorClass.active = false;
        this.editor.session.setMode('ace/mode/' + name)
        let snippet = this.#getSnippet(name);
        let selected = null

        this.#setSnippet(snippet);

        // Find the template for replace the code area
        const find = this.editor.find('@code-here', {
            backwards: false,
            wrap: true,
            caseSensitive: true,
            wholeWord: true,
            regExp: false
        });

        // If changing mode got existing codes , replace the value
        if (this.editor.getSelectedText().length > 0) {
            selected = this.editor.replace(this.editor.getSelectedText());
        }

        // If found
        if (find && selected) {
            this.editor.replace(this.editorClass.originalValue.code);
        } else {
            this.editor.replace('');
        }

        // Turn it back on
        this.editorClass.active = true;
    }

    #getSnippet(name) {
        let valueMatch = this.modesValue.filter((val) => val.name === name)[0];
        return valueMatch && !CustomCodeEditor.has(valueMatch, 'disableSnippet') && CustomCodeEditor.has(valueMatch, 'snippet') ? valueMatch.snippet : ""
    }

    #setSnippet(snippet){
        let beautify = ace.require('ace/ext/beautify');
        this.editor.setValue(snippet);
        beautify.beautify(this.editor.session);
    }

    #checkOptions(selectors){
        selectors.forEach((dom) => {
            let value = null
            switch(true){
                case (/select/g).test(dom.type):
                    if (this.editor.getOptions().hasOwnProperty(dom.name)){
                        Array.from(dom.children).forEach((option) => {
                            let defaultVal = dom.dataset["defaultValue"]
                            // Option Value Cleaning
                            switch(option.value){
                                case "true":
                                    option.value = true;
                                    break;

                                case "false":
                                    option.value = false;
                                    break;
                            }
                            // Default Value Cleaning
                            switch (defaultVal){
                                case "true":
                                    defaultVal = true;
                                    break;

                                case "false":
                                    defaultVal = false;
                                    break
                            }
                            if (!dom.hasAttribute('data-default-value') && option.value === this.editor.getOptions()[dom.name].toString()) {
                                option.setAttribute('selected', true)
                                this.ace.saveValue[dom.name] = option.value.toString()
                            } else if(dom.hasAttribute('data-default-value')) {
                                dom.value = defaultVal;
                                this.ace.saveValue[dom.name] = defaultVal.toString();
                                this.editor.setOption(dom.name, defaultVal)
                            }
                        })
                    }
                    break;

                case (/range/g).test(dom.type):
                    value = (this.editor.getOptions().hasOwnProperty(dom.name)) ? this.editor.getOptions()[dom.name] : 0
                    if(!dom.hasAttribute('data-default-value')) {
                        dom.setAttribute('value', value);
                        this.ace.saveValue[dom.name] = Number(this.editor.getOptions()[dom.name]);
                    } else if(dom.hasAttribute('data-default-value')) {
                        dom.setAttribute('value', dom.dataset["defaultValue"]);
                        this.ace.saveValue[dom.name] = Number(dom.dataset["defaultValue"]);
                        this.editor.setOption(dom.name, Number(dom.dataset["defaultValue"]));
                    }
                    break;

                case (/number/g).test(dom.type):
                    value = (this.editor.getOptions().hasOwnProperty(dom.name)) ? this.editor.getOptions()[dom.name] : 0;
                    if (!dom.hasAttribute('data-default-value')) {
                        dom.setAttribute('value', value);
                        this.ace.saveValue[dom.name] = parseFloat(this.editor.getOptions()[dom.name]);
                    } else if(dom.hasAttribute('data-default-value')) {
                        dom.setAttribute('value', dom.dataset["defaultValue"]);
                        this.ace.saveValue[dom.name] = parseFloat(dom.dataset["defaultValue"]);
                        this.editor.setOption(dom.name, parseFloat(dom.dataset["defaultValue"]));
                    }
                    break;

                case (/checkbox/g).test(dom.type):
                    if (!dom.hasAttribute('data-default-value') && this.editor.getOptions().hasOwnProperty(dom.name) && Boolean(this.editor.getOptions()[dom.name])) {
                        dom.setAttribute('checked', Boolean(this.editor.getOptions()[dom.name]))
                        this.ace.saveValue[dom.name] = Boolean(this.editor.getOptions()[dom.name])
                        return;
                    } else if(dom.hasAttribute('data-default-value')) {
                        if(JSON.parse(dom.dataset["defaultValue"])){
                            dom.setAttribute('checked', JSON.parse(dom.dataset["defaultValue"]))
                        }
                        this.ace.saveValue[dom.name] = JSON.parse(dom.dataset["defaultValue"])
                        this.editor.setOption(dom.name, JSON.parse(dom.dataset["defaultValue"]))
                    } else {
                        this.ace.saveValue[dom.name] = Boolean(this.editor.getOptions()[dom.name])
                    }
                    break;
            }
        })
    }

    copyToClipboard(event) {
        event.preventDefault()
        let value = {}
        Array.from(this.optionsTargets).forEach((dom) => {
            switch(true) {
                case (/checkbox/g).test(dom.type):
                    if(JSON.parse(dom.checked) !== this.ace.saveValue[dom.name]) {
                        value[dom.name] = dom.checked
                    }
                    break;

                case (/range/g).test(dom.type):
                    if(parseFloat(dom.value) !== this.ace.saveValue[dom.name]) {
                        value[dom.name] = parseFloat(dom.value)
                    }
                    break;

                case (/select/g).test(dom.type):
                    let getValue = dom.options[dom.selectedIndex].value;
                    if(getValue !== this.ace.saveValue[dom.name]) {
                        value[dom.name] = getValue;
                    }
                    break;

                case (/number/g).test(dom.type):
                    if(parseFloat(dom.value) !== this.ace.saveValue[dom.name]) {
                        value[dom.name] = parseFloat(dom.value)
                    }
                    break;
            }
        })
        
        // Run Copy to clipboard if value is more than one
        if(Object.keys(value).length > 0) {
            if(Object.keys(this.originalOptionsValue).length > 0) {
                value = {
                    ...this.originalOptionsValue,
                    ...value
                }
            }
            this.copyTarget.dataset.clipboardText = JSON.stringify(JSON.stringify(value))
            this.copyTarget.click()
            this.#outputNotification(Object.keys(value).length + ` item${Object.keys(value).length > 0 ? 's' : ''} copied`);
        } else {
            this.#outputNotification('No changes');
        }
    }

    resetOptions(event){
        event.preventDefault()
        Array.from(this.optionsTargets).forEach((dom) => {
            switch(true) {
                case (/checkbox/g).test(dom.type):
                    if(JSON.parse(dom.checked) !== this.ace.saveValue[dom.name]) {
                        dom.checked = JSON.parse(this.ace.saveValue[dom.name])
                        this.editor.setOption(dom.name, dom.checked)
                    }
                    break;

                case (/range/g).test(dom.type):
                    if(parseFloat(dom.value) !== this.ace.saveValue[dom.name]) {
                        dom.value = this.ace.saveValue[dom.name]
                        this.editor.setOption(dom.name, dom.value)
                    }
                    break;

                case (/select/g).test(dom.type):
                    let getValue = dom.options[dom.selectedIndex].value;
                    if(getValue !== this.ace.saveValue[dom.name]) {
                        // Set Editor Option Value
                        switch (this.ace.saveValue[dom.name]){
                            case "true":
                                this.editor.setOption(dom.name, JSON.parse(this.ace.saveValue[dom.name]))
                                break;

                            case "false":
                                this.editor.setOption(dom.name, JSON.parse(this.ace.saveValue[dom.name]))
                                break;

                            default:
                                this.editor.setOption(dom.name, this.ace.saveValue[dom.name])
                        }
                        // Set default on select html
                        dom.selectedIndex = Array.from(dom.options).filter(val => val.value === this.ace.saveValue[dom.name]).reduce((val, next) => next, -1).index

                    }
                    break;

                case (/number/g).test(dom.type):
                    if(parseFloat(dom.value) !== this.ace.saveValue[dom.name]) {
                        dom.value = this.ace.saveValue[dom.name]
                        this.editor.setOption(dom.name, this.ace.saveValue[dom.name])
                    }
                    break;
            }
        })
    }

    #outputNotification(text) {
        this.notificationTarget.style.removeProperty('display');
        this.notificationTarget.innerText = text;
        let self = this;
        setTimeout(() => {
            self.notificationTarget.style.display = 'none';
        }, self.editorClass.notificationTimeout)
    }

    #dropdownConfig(){
        if (CustomCodeEditor.has(this.dropdownConfigValue, 'position.top')) {
            this.dropdownTarget.style.top = this.dropdownConfigValue.position.top
        }

        if (CustomCodeEditor.has(this.dropdownConfigValue, 'position.left')) {
            this.dropdownTarget.style.left = this.dropdownConfigValue.position.left
        }

        if (CustomCodeEditor.has(this.dropdownConfigValue, 'position.right')) {
            this.dropdownTarget.style.right = this.dropdownConfigValue.position.right
        }

        if (CustomCodeEditor.has(this.dropdownConfigValue, 'position.bottom')) {
            this.dropdownTarget.style.bottom = this.dropdownConfigValue.position.bottom
        }

        if (CustomCodeEditor.has(this.dropdownConfigValue, 'height')) {
            this.dropdownTarget.style.height = this.dropdownConfigValue.height
        }

        if (CustomCodeEditor.has(this.dropdownConfigValue, 'borderRadius')) {
            this.dropdownTarget.style.borderRadius = this.dropdownConfigValue.borderRadius
        }

        if (CustomCodeEditor.has(this.dropdownConfigValue, 'boxShadow')) {
            this.dropdownTarget.style.boxShadow = this.dropdownConfigValue.boxShadow
        }

        if (CustomCodeEditor.has(this.dropdownConfigValue, 'width')) {
            this.dropdownTarget.style.width = this.dropdownConfigValue.width
        }

        if (CustomCodeEditor.has(this.dropdownConfigValue, 'backgroundColor')) {
            this.dropdownTarget.style.backgroundColor = this.dropdownConfigValue.backgroundColor
        }

    }

    #initEditor(){
        // Init the element
        this.inputTarget.style.display = 'none';

        this.editorClass = new CustomCodeEditor(this.inputTarget, this.editorTarget, { 
            ...this.ace,
            originalValue: this.getValue,
        })

        this.editor = this.editorClass.getEditor;

        this.editorMode(this.ace.defaultMode);

        // Check Options Modes
        if (this.hasOptionsTarget){
            this.#checkOptions(this.optionsTargets);
        }

        if(this.hasDropdownTarget){
            this.#dropdownConfig()
        }
    }

    disconnect(){
        this.editorClass.disconnect()
        this.editorClass = null;
    }
    
}

window.wagtail.app.register('custom-code-editor', CustomCodeEditorStimulus)