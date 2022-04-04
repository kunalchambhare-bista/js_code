from odoo import models, fields, api


class ConvertToEmployee(models.TransientModel):
    _name = "reject.reason"
    _description = "Intern Rejection Reason"

    # ROLES = [
    #     ('developer', 'Developer'),
    #     ('tester', 'Tester'),
    #     ('analyst', 'Analyst'),
    #     ('trainer', 'Trainer')
    # ]

    trainee_name = fields.Many2one('trainee.master', string="Trainee")
    reject_reason = fields.Char(string='Enter the reason for rejection', required=1)

    def reject_intern(self):
        trainee_name = self.trainee_name
        trainee_name.status = 'rejected'

    # @api.model
    # def create(self, vals):
    #     # import pdb
    #     # pdb.set_trace()
    #     value_of_logs = {
    #         'employee_name': self.env['trainee.master'].browse(vals.get('trainee_name')).name,
    #         'role': vals.get('role')
    #     }
    #     self.env['employee.list'].create(value_of_logs)
    #     return super(ConvertToEmployee, self).create(vals)
