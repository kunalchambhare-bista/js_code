from odoo.addons.sale.controllers.portal import CustomerPortal

from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, _




class CustomerPortalOverride(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None, customer_name=None):
        res = super(CustomerPortalOverride, self).portal_quote_accept(order_id, access_token=None, name=None, signature=None, customer_name=None)
        return res

