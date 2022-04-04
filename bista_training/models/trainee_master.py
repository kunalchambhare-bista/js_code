# -*- coding: utf-8 -*-


from odoo import models, fields, api
from validate_email import validate_email

from odoo.exceptions import ValidationError
from datetime import date


class TraineeMaster(models.Model):
    _name = "trainee.master"
    _description = "Trainees of Bista Solutions"

    GENDER = [
        ('male', 'M'),
        ('female', 'F'),
        ('others', 'Others')
    ]

    STATUS = [
        ('new', 'NEW'),
        ('training', 'TRAINING'),
        ('rejected', 'REJECTED'),
        ('employed', 'EMPLOYED')
    ]

    name = fields.Char(string='Trainee Name', compute='_compute_full_name', store=True)
    trainee_age = fields.Char('Age')
    first_name = fields.Char(string='Name', required=1)
    last_name = fields.Char(string='Last Name')
    trainee_id = fields.Char(string='Trainee ID', readonly=1, default='New')
    trainee_email = fields.Char(string='Email', default=False)
    contact_number = fields.Char(string='Contact Number')

    # trainee_to_employee = fields.One2many('employee.list')
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

    @api.constrains('trainee_email')
    def email_validation(self):
        for rec in self:
            if rec.trainee_email:
                is_valid = validate_email(rec.trainee_email)
                if not is_valid:
                    raise ValidationError(('Enter a Valid Email'))

    linkedin_url = fields.Char(string='Linkedin')
    Gender = fields.Selection(GENDER, string='Gender', required=1, default='male')

    date_of_birth = fields.Date(string='DOB')
    date_of_joining = fields.Date(string='Joining Date')
    location = fields.Many2one('trainee.location', string='Location')
    profile_image = fields.Image(string='Profile Image')

    status = fields.Selection(STATUS, string='Status', required=1, default='new')
    training_stages_id = fields.Many2one('training.stages')
    designation = fields.Char(string='Designation', default='INTERN', compute='_compute_designation')

    # employeed_intern_designation = fields.Many2one(related='employee_id.role')

    trainee_batch_id = fields.Many2one('training.batch', string="Batch", domain="[('location','=', location)]")

    employee_id = fields.Many2one('employee.list', string='Employee ID', domain="[('employee_name','=', name)]")

    # , string = 'Employee ID', domain = "[('employee_name','=', name)]"
    # employee_id = fields.Char(related='employee_rec_link_id.display_name')
    # employee_id = fields.Char(string = 'Employee ID', compute='_compute_employee_id')

    # def _compute_employee_id(self):
    #     for rec in self:
    #         if rec.status == 'employed':
    #             rec.employee_id = str(rec.employee_rec_link_id.display_name)

    def reject_intern(self):
        return_val = {
            'name': ('Reject Intern'),
            'view_mode': 'form',
            'res_model': 'reject.reason',
            'view id': self.env.ref('bista_training.view_reject_reason_form').id,
            'type': 'ir.actions.act_window',
            'context': {'default_trainee_name': self.id},
            'target': 'new',
        }
        return return_val

    def convert_to_intern(self):
        for rec in self:
            rec.status = 'training'

    def convert_to_employee(self):
        return_val = {
            'name': ('Convert To Employee'),
            'view_mode': 'form',
            'res_model': 'covert.to.employee',
            'view id': self.env.ref('bista_training.view_convert_to_employee_form').id,
            'type': 'ir.actions.act_window',
            'context': {'default_trainee_name': self.id},
            'target': 'new',
        }
        return return_val

    def _compute_designation(self):
        for rec in self:
            if rec.status:
                if rec.status == 'employed':
                    rec.designation = rec.employee_id.role

                elif rec.status == 'rejected':

                    rec.designation = 'NOT APPLICABLE'

                else:
                    rec.designation = 'INTERN'

    _sql_constraints = [
        ('trainee_id_constraints', 'UNIQUE (trainee_id)', 'ID should be unique')

    ]

    @api.model
    def create(self, vals):
        vals['trainee_id'] = self.env['ir.sequence'].next_by_code('trainee.sequence')
        return super(TraineeMaster, self).create(vals)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            if rec.last_name:
                rec.name = rec.first_name + " " + rec.last_name
            else:
                rec.name = rec.first_name


class TraineeLocation(models.Model):
    _name = "trainee.location"  # creates a table in database named movie_library
    _description = "Trainee's Location"
    _rec_name = "location"

    location = fields.Char(string='Location', required=1)
    street_one = fields.Char(string='Street 1')
    street_two = fields.Char(string='Street 2')
    country_id = fields.Many2one('res.country', string='Country', required=1)
    state_id = fields.Many2one('res.country.state', string='State')
    city = fields.Char(string='City')

    @api.onchange('country_id')
    def _onchange_country_id_wrapper(self):
        res = {'domain': {'state_id': []}}

        if self.country_id:
            res['domain']['state_id'] = [('country_id', '=', self.country_id.id)]

        return res
