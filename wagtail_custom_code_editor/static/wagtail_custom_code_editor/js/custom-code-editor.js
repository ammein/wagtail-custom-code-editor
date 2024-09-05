// noinspection JSUnusedGlobalSymbols

class CustomCodeEditor {
    originalValue;
    notificationTimeout = 1500;
    active = true;

    constructor(textarea, editor, aceValue){
        this.beforeInit(textarea, editor, aceValue);
        this.editor = ace.edit(editor);
        this.textarea = textarea
        this.ace = aceValue

        let self = this;
        this.originalValue = {
            get code(){
                let value = JSON.parse(self.textarea.value)

                return value.code
            },

            get mode(){
                let value = JSON.parse(self.textarea.value)

                return value.mode
            },

            set code(val){
                return val;
            },

            set mode(val){
                if (/[\\/]\w+$/g.test(val)) {
                    return val.match(/(?!([\/\\]))\w*$/g)[0]
                }
                return val;
            }
        }

        // Hacky way to put default value of a textarea
        if (aceValue.hasOwnProperty('originalValue')){
            this.textarea.innerHTML = this.stringifyJSON({
                mode: aceValue.originalValue.mode,
                code: aceValue.originalValue.code
            })
        }

        this.setValue(this.originalValue.mode, this.originalValue.code)

        this.allEvents();
        this.commands();

        // Set Theme
        this.setTheme(this.ace.theme)

        // Set After Init
        this.afterInit();
    }

    beforeInit(textarea, editor, aceValue){

    }

    afterInit(){

    }

    setMode(mode){
        this.editor.session.setMode('ace/mode/' + mode);
    }

    setTheme(name) {
        this.editor.setTheme('ace/theme/' + name);
    }

    setValue(mode, code){
        this.editor.setValue(code || '')
        this.setMode(mode)
        this.textarea.value = this.stringifyJSON({
            mode,
            code: code || ''
        })
    }

    get getEditor(){
        return this.editor
    }

    commands() {
        // Save new value when press save command
        const _this = this;
        this.editor.commands.addCommand({
            name: 'saveNewCode',
            bindKey: {
                win: (CustomCodeEditor.has(this.ace, 'config.saveCommand.win')) ? this.ace.config["saveCommand"].win : 'Alt-Shift-S',
                mac: (CustomCodeEditor.has(this.ace, 'config.saveCommand.mac')) ? this.ace.config["saveCommand"].mac : 'Option-Shift-S'
            },
            exec: function (editor) {
                _this.originalValue = {
                    mode: _this.originalValue.mode,
                    code: editor.getSelectedText()
                };
            },
            readOnly: false
        });
    }
    
    allEvents(){
        // Apply value on change in textarea
        const _this = this;
        this.editor.getSession().on('change', function () {
            let value = _this.getValue()

            if(value && _this.active){
                _this.textarea.value = _this.stringifyJSON({
                    mode: value.mode,
                    code: value.code
                })
            }
        })
    }

    getValue(){
        let mode = this.editor.session.getMode().$id.match(/(?!([\/\\]))\w*$/g)[0]
        if(this.editor.getValue().length > 0) {
            return {
                mode: mode,
                code: this.editor.getValue()
            }
        }

        return null;
    }

    trim(str) {
        return str.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '');
    };

    stringifyJSON({mode, code}){
        return JSON.stringify({
            mode,
            code: code ? this.trim(code) : code,
        })
    }

    static camelCaseToWords(str) {
        const result = str.replace(/([A-Z])/g, ' $1');
        return result.charAt(0).toUpperCase() + result.slice(1);
    }

    static cloneDeep(obj) {
        return JSON.parse(JSON.stringify(obj));
    }

    static isArray(item) {
        if (!item) {
            return false;
        }
        // check if got object in it
        for (let i = 0; i < item.length; i++) {
            if (item[i].constructor === Object) {
                return false
            }
        }
        return item && typeof item === 'object' && item.constructor === Array;
    }

    static isObject(item) {
        if (!item) {
            return false;
        }
        return item && typeof item === 'object' && item.constructor === Object;
    }

    static isString(item) {
        if (!item) {
            return false;
        }
        return typeof item === 'string' && typeof item.length === 'number'
    }

    static isArrayOfObject(item) {
        if (!item) {
            return false;
        }

        // check if got object in it
        for (let i = 0; i < item.length; i++) {
            if (item[i].constructor !== Object) {
                return false
            }
        }

        // Also check if the item is not a string
        return !this.isString(item);
    }

    static has(object, path) {
        let curObj = object;
        let pathArr = path.match(/([^.[\]]+)/g);
        for (let p in pathArr) {
            if (curObj === undefined || curObj === null) return curObj; // should probably test for object/array instead
            curObj = curObj[pathArr[p]];
        }
        return curObj;
    }

    static capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    // Widget Adapter Functions
    setState(value) {
        this.setValue(value.mode, value.code)
    }

    getState() {
        return this.getValue();
    }

    focus() {
        this.editor.focus();
    }

    disconnect() {
        this.editor.destroy();
    }
}