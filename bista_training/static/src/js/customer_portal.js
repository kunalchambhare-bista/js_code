odoo.define('bista_training.customer_portal_customer_field', function (require) {


    var core = require('web.core');
    var config = require('web.config');
    var utils = require('web.utils');
    var customer_portal = require('web.name_and_signature').NameAndSignature;
    var qweb = core.qweb;

    var _t = core._t;
    console.log("----NameAndSignature---->")

    customer_portal.include({

        xmlDependencies: (customer_portal.prototype.xmlDependencies || []).concat(
            ['/bista_training/static/src/xml/customer_portal.xml']
        ),

        // events: {
        //     // name
        //     'input .o_web_customer_name_input': '_onInputCustomerName'
        // },

        // events: _.extend({}, customer_portal.prototype.events, {
        //     'input .o_web_customer_name_input': '_onInputCustomerName',
        // }),

        start: function () {
            this.$customernameInput = this.$('.o_web_customer_name_input');
            return this._super(this, arguments);
        },

        getCustomerName: function () {
            return this.$customernameInput.val();
        },


    });
});

odoo.define('bista_training.portal_signature_customer_field', function (require) {
    var SignatureForm = require('portal.signature_form').SignatureForm;


    SignatureForm.include({

        _onClickSignSubmit: function (ev) {
            var self = this;
            ev.preventDefault();

            if (!this.nameAndSignature.validateSignature()) {
                return;
            }

            var name = this.nameAndSignature.getName();
            var customer_name = this.nameAndSignature.getCustomerName();
            var signature = this.nameAndSignature.getSignatureImage()[1];

            return this._rpc({
                route: this.callUrl,
                params: _.extend(this.rpcParams, {
                    'name': name,
                    'signature': signature,
                    'customer_name': customer_name,
                }),
            }).then(function (data) {
                if (data.error) {
                    self.$('.o_portal_sign_error_msg').remove();
                    self.$controls.prepend(qweb.render('portal.portal_signature_error', {widget: data}));
                } else if (data.success) {
                    var $success = qweb.render('portal.portal_signature_success', {widget: data});
                    self.$el.empty().append($success);
                }
                if (data.force_refresh) {
                    if (data.redirect_url) {
                        window.location = data.redirect_url;
                    } else {
                        window.location.reload();
                    }
                    // no resolve if we reload the page
                    return new Promise(function () {
                    });
                }
            });
        },
    });
});