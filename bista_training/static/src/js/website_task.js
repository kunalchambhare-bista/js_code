odoo.define('bista_training.website_table', function (require) {
    'use strict';

    const {qweb} = require('web.core');
    const publicWidget = require('web.public.widget');

    publicWidget.registry.website_template = publicWidget.Widget.extend({
        selector: '.table_template',
        xmlDependencies: ['/bista_training/static/src/xml/table_template.xml'],

        events: {
            'click .btn': '_onClick',
        },
        start: async function () {

            return this._super(...arguments);
        },
        _onClick: async function () {
            this.$el.find('.o_data').remove();
            const partner_dict = await this._rpc({
                model: 'res.partner',
                method: 'search_read',
                args: [[]],
                kwargs: {
                    fields: ["id", "name"],
                },
            })

            if (partner_dict) {
                let tableHtml = qweb.render('website_template', {'partners': partner_dict});
                this.$el.append(tableHtml)
            }
        }
    })
});