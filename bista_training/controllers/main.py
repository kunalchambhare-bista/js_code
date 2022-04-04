from odoo import http, fields, tools
from odoo.http import request


class Controller(http.Controller):

    @http.route('/testroute', type="http", auth="public", website=True)
    def view(self, **kwargs):
        values = {}
        print('Called')
        partner_id = request.env['res.partner'].sudo().search([])
        return request.render("bista_training.template_test", {'partner_id': partner_id})

    @http.route(['/test/partner', '/test/partner/<int:id>'], type="http", auth="public", website=True)
    def partner_view(self, id=1, **kwargs):
        print('Called!!!')
        print(id)

        partner_id = request.env['res.partner'].sudo().browse(id)

        print(partner_id)
        return request.render("bista_training.template_test_partner", {'partner': partner_id})
