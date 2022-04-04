from odoo import models, fields, api
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

import datetime
import calendar


class ConvertToEmployee(models.TransientModel):
    _name = "attendance.report"
    _description = "Attendance Report"

    # ROLES = [
    #     ('developer', 'Developer'),
    #     ('tester', 'Tester'),
    #     ('analyst', 'Analyst'),
    #     ('trainer', 'Trainer')
    # ]

    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")
    trainee_id = fields.Many2many('trainee.master', string="Trainee")

    def get_header_values(self):
        from_date = self.from_date
        to_date = self.to_date
        result = []

        while from_date <= to_date:
            if from_date.isoweekday() not in (6, 7):
                result.append(from_date)
            from_date = from_date + relativedelta(days=1)

        return result

    def get_attendance(self, trainee):
        for rec in self:
            f_date = rec.from_date
            attendance = []
            while f_date <= rec.to_date:
                if f_date.isoweekday() not in (6, 7):

                    exist_trainee = self.env['training.attendance'].search([
                        ('trainee_id', '=', trainee.id),
                        ('date', '=', f_date),
                    ])
                    if len(exist_trainee) > 0:
                        attendance.append('P')
                    else:
                        attendance.append('A')

                f_date = f_date + timedelta(days=1)

        return attendance

    def print_report(self):
        report_act = self.env.ref('bista_training.attendance_report_print_action').report_action(self)
        return report_act

