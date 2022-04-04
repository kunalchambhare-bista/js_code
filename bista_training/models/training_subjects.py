# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class TrainingSubjects(models.Model):
    _name = "training.subjects"
    _description = "Subjects"
    _rec_name = "subject_name"

    subject_name = fields.Char(string='Subject Name', required=1)
    subject_description = fields.Text(string='Description')
    subject_topics = fields.One2many('training.topics', 'topic_subject_name', string='Topics', readonly=1)
    subject_trainer_ids = fields.Many2many('trainer.master', string='Trainers')


class TrainingTopics(models.Model):
    _name = "training.topics"  # creates a table in database named movie_library
    _description = "Topics"
    _rec_name = "display_name"

    topic_name = fields.Char(string='Topics', required=1)
    topic_subject_name = fields.Many2one('training.subjects', string='Subject Name', required=1)
    batch_id = fields.Many2one('training.batch', string='Batch')

    display_name = fields.Char(string='Topics Name', compuet='_get_display_name', readonly=1, store=True)

    @api.onchange('topic_name','topic_subject_name')
    def _get_display_name(self):
        for rec in self:
            if rec.topic_name and rec.topic_subject_name:
                rec.display_name = str(rec.topic_subject_name.subject_name) + "/" + str(rec.topic_name)



class TrainingStages(models.Model):
    _name = "training.stages"  # creates a table in database named movie_library
    _description = "Stages"
    _rec_name = "stage_name"

    STATUS = [
        ('draft', 'Draft'),
        ('progress', 'Progress'),
        ('done', 'Done')
    ]

    stage_name = fields.Char(string='Stage Name')
    available_on_batch = fields.Boolean(string='Available On Batch')
    available_on_training = fields.Boolean(string='Available On Training')
    status = fields.Selection(STATUS, string='Status')
    available_for_trainee = fields.Boolean('Available for Trainee')
