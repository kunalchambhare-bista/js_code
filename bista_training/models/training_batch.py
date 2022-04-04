# -*- coding: utf-8 -*-


from odoo import models, fields, api
from datetime import timedelta


class TrainingBatch(models.Model):
    _name = "training.batch"
    _description = "Batches"
    _rec_name = "batch_name"

    BATCH_STAGE = [
        ('draft', 'NEW'),
        ('ongoing', 'ON GOING'),
        ('done', 'DONE')
    ]

    batch_name = fields.Char(string='Batch Name', required=1)
    start_date = fields.Date(string='From', required=1)
    end_date = fields.Date(string='To', compute='_get_end_date')
    location = fields.Many2one('trainee.location', string='Location')
    trainees_id = fields.One2many('trainee.master', 'trainee_batch_id', string='Trainees', readonly=1)
    trainer_id = fields.One2many('trainer.master', 'trainer_batch_id', string='Trainers', readonly=1)
    stages = fields.Selection(BATCH_STAGE, default='draft')
    training_topics = fields.One2many('training.topics', 'batch_id', string='Topics', readonly=1)
    progress = fields.Integer(string='Batch Progress')
    progress_bar = fields.Integer(string='Batch Progress Bar')

    def _get_end_date(self):
        for rec in self:
            if rec.start_date:
                rec.end_date = rec.start_date + timedelta(days=90)
            else:
                rec.end_date = False

