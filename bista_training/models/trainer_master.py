# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class TrainerMaster(models.Model):
    _name = "trainer.master"  # creates a table in database named movie_library
    _description = "Trainers of Bista Solutions"

    name = fields.Char(string='Trainer Name', compute='_compute_full_name')
    abc = fields.Integer(string='ABC')
    first_name = fields.Char(string='First Name', required=1)
    last_name = fields.Char(string='Last Name')
    profile_image = fields.Image(string='Profile Image')
    subject = fields.One2many('training.subjects', 'subject_trainer_ids', readonly=1, string="Subjects")
    trainer_batch_id = fields.Many2many('training.batch', string="Batch")
    contact_number = fields.Char(string='Contact Number')

    @api.onchange('contact_number')
    def _phone_validation(self):
        contact = self.contact_number
        if self.contact_number:
            if len(contact) != 10:
                raise ValidationError(('Enter a valid Contact number'))
                # or not self.phone.isnumeric():
            elif not self.contact_number.isnumeric():
                raise ValidationError(('Enter a valid Contact number'))
            else:
                a = contact[:3]
                b = contact[3:6]
                c = contact[6:]
                self.contact_number = a + '-' + b + '-' + c


    def _compute_full_name(self):
        for rec in self:
            if rec.last_name:
                rec.name = rec.first_name + " " + rec.last_name
            else:
                rec.name = rec.first_name

    @api.model
    def create(self, vals):
        value_of_logs = {
            'employee_name': vals.get('first_name') + " " + vals.get('last_name'),
            'role': 'trainer'
        }
        self.env['employee.list'].create(value_of_logs)
        return super(TrainerMaster, self).create(vals)
