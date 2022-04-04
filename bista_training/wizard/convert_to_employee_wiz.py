from odoo import models, fields, api


class ConvertToEmployee(models.TransientModel):
    _name = "covert.to.employee"
    _description = "Employee List"

    ROLES = [
        ('developer', 'Developer'),
        ('tester', 'Tester'),
        ('analyst', 'Analyst'),
        ('trainer', 'Trainer')
    ]

    trainee_name = fields.Many2one('trainee.master', string="Trainee")
    role = fields.Selection(ROLES, string='Role to Convert')

    def convert_to_employee(self):
        trainee_name = self.trainee_name
        trainee_name.status = 'employed'

    @api.model
    def create(self, vals):
        # import pdb
        # pdb.set_trace()
        value_of_logs = {
            'employee_name': self.env['trainee.master'].browse(vals.get('trainee_name')).name,
            'role': vals.get('role')
        }

        self.env['employee.list'].create(value_of_logs)

        return super(ConvertToEmployee, self).create(vals)
