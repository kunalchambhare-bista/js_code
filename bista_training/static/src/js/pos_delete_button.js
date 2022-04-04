odoo.define('bista_training.pos_test', function (require) {

    const Orderline = require('point_of_sale.Orderline');
    const {patch} = require('web.utils');

    patch(Orderline, 'bista_training.Orderline', {
        onRemoveLine() {
            this.trigger('remove-line', {orderline: this.props.line});
        }
    });
});

odoo.define('bista_training.OrderWidget', function (require) {
    'use strict';

    const OrderWidget = require('point_of_sale.OrderWidget');
    const {useListener} = require('web.custom_hooks');
    const {patch} = require('web.utils');

    patch(OrderWidget, 'bista_training.Orderline', {
        setup() {
            useListener('remove-line', this._removeLine);
        },

        _removeLine(event) {
            this.order.remove_orderline(event.detail.orderline);
        }
    });
});