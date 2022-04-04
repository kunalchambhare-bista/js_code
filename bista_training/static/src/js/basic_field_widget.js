odoo.define('bista_training.slider_widget', function (require) {

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var FormController = require('web.FormController');


    var Fieldspinner = AbstractField.extend({
        template: 'FieldSpinner',

        jsLibs: [
            '/bista_training/static/lib/jquery-ui-1.13.1/jquery-ui.js',
        ],
        cssLibs: [
            '/bista_training/static/lib/jquery-ui-1.13.1/jquery-ui.css',
        ],

//          init: function (parent, name, record, options) {
//            this._super(this, arguments)
//          },

        start: function () {
            var spinner = this.$el.spinner();
            spinner.spinner("enable");


            return this._super(this, arguments);
        },

//          _render1: function () {
//                if (this.attrs.decorations) {
//                    this._applyDecorations();
//                }
//                if (this.mode === 'edit') {
//                    return this._renderEdit();
//                } else if (this.mode === 'readonly') {
//                    return this._renderReadonly();
//                }

//          _renderEdit: function () {
//                this.$el.text('EditMode');
//                    },

        _renderReadonly: function () {
            this.$el.text('ReadOnlyMode');
        },


    });

    registry.add('spinner', Fieldspinner);

    return Fieldspinner;


});


odoo.define('bista_training.progressbar_widget', function (require) {

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var FormController = require('web.FormController');


    var FieldProgressbar = AbstractField.extend({
        template: 'FieldProgressbar',

        jsLibs: [
            '/bista_training/static/lib/jquery-ui-1.13.1/jquery-ui.js',
        ],
        cssLibs: [
            '/bista_training/static/lib/jquery-ui-1.13.1/jquery-ui.css',
        ],

//          init: function (parent, name, record, options) {
//            this._super(this, arguments)
//          },

        start: function () {
            if (this.mode == 'edit') {
                this.$el.progressbar({
                    value: 37
                });

            }

            return this._super(this, arguments);
        },

//          _render1: function () {
//                if (this.attrs.decorations) {
//                    this._applyDecorations();
//                }
//                if (this.mode === 'edit') {
//                    return this._renderEdit();
//                } else if (this.mode === 'readonly') {
//                    return this._renderReadonly();
//                }

//          _renderEdit: function () {
//                this.$el.text('EditMode');
//                    },

        _renderReadonly: function () {
//                this.$el.text(this.$el.data('uiProgressbar').value());
            this.$el.text(this.value)
            this.$el.removeClass('o_field_empty')

        },
        isEmpty: function () {
            return false;
        }


    });

    registry.add('progressbar', FieldProgressbar);
    return FieldProgressbar;


});


