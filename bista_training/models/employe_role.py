# -*- coding: utf-8 -*-


from odoo import models, fields, api


class EmployeeList(models.Model):
    _name = "employee.list"  # creates a table in database named movie_library
    _description = "Employee List"
    _rec_name = "display_name"

    ROLES = [
        ('developer', 'Developer'),
        ('tester', 'Tester'),
        ('analyst', 'Analyst'),
        ('trainer', 'Trainer')
    ]

    employee_name = fields.Char(string='Employee Name')
    role = fields.Selection(ROLES, string='Role')
    employee_sequence = fields.Char(string='Sequence Number', defauld='NEW')

    display_name = fields.Char(compute='_compute_display_name')

    trainee_name_id = fields.One2many('trainee.master', 'employee_id')

    def _compute_display_name(self):
        for rec in self:
            if rec.employee_name and rec.employee_sequence:
                rec.display_name = str(rec.employee_name ) + " (" + str(rec.employee_sequence) + ")"
            else:
                rec.display_name = "None"


    @api.model
    def create(self, vals):
        vals['employee_sequence'] = self.env['ir.sequence'].next_by_code('employee.sequence')
        return super(EmployeeList, self).create(vals)

    def name_get(self):
        show_sequence_number = self._context.get('show_employee_sequence') or False
        if show_sequence_number:
            list_rec = []
            for rec in self:
                show_sequence_number = rec.employee_sequence
                list_rec.append((rec.id, show_sequence_number))
            return list_rec
        return super(EmployeeList, self).name_get()
