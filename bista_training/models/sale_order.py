# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SalesOrder(models.Model):
    _inherit = "sale.order"

    customer_name = fields.Char('Customer Name')
