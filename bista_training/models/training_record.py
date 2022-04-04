# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from datetime import datetime
from datetime import timedelta

from datetime import timedelta


class TrainingBatch(models.Model):
    _name = "training.record"
    _description = "Bista Training Record"

    name = fields.Char(string='Record Name', compute='_compute_record_name')
    rec_date = fields.Date(string='Date', default=lambda self: self._get_todays_date())

    batch_id = fields.Many2one('training.batch', string="Batches")

    trainee_inverse_id = fields.One2many('training.record.line', 'training_record_id',
                                         string="Training Record Inverse Var", readonly=1)
    attendance_inverse_id = fields.One2many('training.attendance', 'training_record_id',
                                            string="Training Attendance Inverse Var", readonly=1)

    topic_inverse_id = fields.One2many('training.topics.line', 'training_record_id',
                                       string="Training Attendance Inverse Var", readonly=1)

    score_inverse_id = fields.One2many('training.score', 'training_record_id',
                                       string="Training Attendance Inverse Var")

    score_total = fields.Integer(string='Score Total', compute='calculate_count')

    # record_count = fields.Integer('Record Count', default=0)

    @api.depends('score_inverse_id')
    def calculate_count(self):
        score = 0
        for rec in self.score_inverse_id:
            score += rec.score
        self.score_total = score


    # @api.onchange('score_inverse_id')
    # def _compute_total_score(self, score_inverse_id):
    #     inverse_ids = []
    #     inverse_ids.append(score_inverse_id.score)

    # @api.onchange('score_inverse_id')
    # def _compute_total_score(self, score_inverse_id):
    #     for rec in self:
    #
    #         total = score_inverse_id.score
    #         rec.score_total = rec.score_total + total

    def _get_todays_date(self):
        return fields.Date.today()

    def _compute_record_name(self):
        for rec in self:
            if rec.rec_date:
                rec.name = "Record For the Date: " + str(rec.rec_date)


class TrainingRecordLine(models.Model):
    _name = "training.record.line"
    _rec_name = "trainee_name_id"

    ATTENDANCE = [
        ('present', 'P'),
        ('absent', 'A'),
    ]

    training_record_id = fields.Many2one('training.record', string="Date of Record")

    trainee_name_id = fields.Many2one('trainee.master', string="Trainees Name")
    trainee_id = fields.Char(related="trainee_name_id.trainee_id", string="Trainee ID")
    report_trainee_name = fields.Char(related="trainee_name_id.name", store=True)

    rec_date = fields.Date(related="training_record_id.rec_date", store=True)

    remarks = fields.Text(string="Remarks")
    attendance = fields.Selection(ATTENDANCE, string='Attendance', default='absent')
    attendance_status = fields.Many2one('training.attendance', string='Attendance',
                                        domain="[('trainee_id','=', trainee_name_id)]")

    # def make_trainee_name_array(self):
    #     for rec in self:
    #         trainee_list = []
    #         trainee_list.append(rec.trainee_name_id)

    # report_wiz_ids = fields.Many2one('attendance.report')
    #
    # from_date = fields.Date(related='report_wiz_ids.')

    # def get_header_values(self):
    #     result = ['A', 'B']
    #     return result

    @api.onchange('training_record_id', 'trainee_name_id')
    def _attendance_compute(self):
        for rec in self:
            if rec.trainee_name_id and rec.training_record_id:
                exist_tranee = self.env['training.attendance'].search([
                    ('trainee_id.id', '=', rec.trainee_name_id.id),
                    ('date', '=', rec.rec_date),
                ])
                if len(exist_tranee) > 0:
                    rec.attendance = 'present'
                else:
                    rec.attendance = 'absent'
                # if rec.training_record_id.trainee_id == rec.trainee_name_id:

            # check_trainee_record = self.env['training.attendance'].search([
            #     '&amp;', '|',
            #     ('date', '=', rec.rec_date),
            #     ('trainee_id', '=', rec.trainee_id)
            # ])
            # if check_trainee_record:
            #     rec.attendance = 'present'
            # else:
            #     rec.attendance = 'absent'


class TrainingAttendance(models.Model):
    _name = "training.attendance"

    training_record_id = fields.Many2one('training.record', string="Record Linking Var")
    name = fields.Char(compute='_get_the_date')
    date = fields.Date(related="training_record_id.rec_date", store=True)
    # import pdb
    # pdb.set_trace()

    trainee_id = fields.Many2one('trainee.master', string="Name of the Trainee")
    login_time = fields.Datetime(string='Login Time')
    logout_time = fields.Datetime(string='Logout Time')
    hours = fields.Float('Hours Studied', compute='_compute_hours')

    def print_report(self):
        return_val = {
            'name': ('Attendance Report'),
            'view_mode': 'form',
            'res_model': 'attendance.report',
            'view id': self.env.ref('bista_training.view_attendance_report_wiz_form').id,
            'type': 'ir.actions.act_window',
            'context': {},
            'target': 'new',
        }
        return return_val

    @api.depends('login_time', 'logout_time')
    def _compute_hours(self):
        for rec in self:
            if rec.login_time and rec.logout_time:
                t1 = datetime.strptime(str(rec.login_time), DEFAULT_SERVER_DATETIME_FORMAT)
                t2 = datetime.strptime(str(rec.logout_time), DEFAULT_SERVER_DATETIME_FORMAT)
                t3 = t2 - t1

                rec.hours = float(t3.days) * 24 + (float(t3.seconds) / 3600)
            else:
                rec.hours = 0

    @api.depends('date')
    def _get_the_date(self):
        for rec in self:
            if rec.date:
                rec.login_time = rec.date
                rec.name = "Attendance for Date: " + str(rec.date)
            else:
                rec.name = "Attendance for Date: "


class TrainingTopicsLine(models.Model):
    _name = "training.topics.line"

    topics_id = fields.Many2one('training.topics', string="Topics Covered")
    # name = fields.Char(compute='_get_the_date')
    remark = fields.Text('Remarks')
    training_record_id = fields.Many2one('training.record', string="Record Linking Var")


class TrainingScore(models.Model):
    _name = "training.score"

    trainee_name_id = fields.Many2one('trainee.master', string="Trainees Name")
    date_of_evaluation = fields.Date(string='Date Of Evaluation')
    score = fields.Integer('Score')
    training_record_id = fields.Many2one('training.record', string="Record Linking Var",
                                         domain="[('rec_date','=', date_of_evaluation)]")
