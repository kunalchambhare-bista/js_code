odoo.define('bista_training.color_widget_2', function (require) {

    var registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');

    var ColorSelector2 = AbstractField.extend({
        template: 'Fieldcolor_2',

        jsLibs: [
            '/bista_training/static/lib/pickr_addons/pickr.es5.min.js',
            '/bista_training/static/lib/pickr_addons/pickr.min.js',
        ],
        cssLibs: [
            '/bista_training/static/lib/pickr_addons/classic.min.css',
            '/bista_training/static/lib/pickr_addons/monolith.min.css',
            '/bista_training/static/lib/pickr_addons/nano.min.css',
        ],

        start: function () {

            const pickr = Pickr.create({
                el: this.$el.find('.color_input')[0],
                theme: "classic",
                components: {
                    preview: true,
                    opacity: true,
                    hue: true,
                    // Input / output Options
                    interaction: {
                        hex: true,
                        rgba: true,
                        hsla: true,
                        hsva: true,
                        cmyk: true,
                        input: true,
                        clear: true,
                        save: true
                    }
                }
            });

            pickr.on('save', (color, instance) => {
                this._setValue(color.toHEXA().toString())
            })


            return this._super(this, arguments);
        },

        _renderReadonly: function () {
            this.$el.text(this.value)
            this.$el.removeClass('o_field_empty')

        },
        isEmpty: function () {
            return false;
        }


    });

    registry.add('colorselector_2', ColorSelector2);
    return ColorSelector2;


});