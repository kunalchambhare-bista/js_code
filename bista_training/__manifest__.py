# -*- coding: utf-8 -*-
{
    'name': "Bista Training",
    'summary': "Bista Training Module",
    'category': 'Uncategorized',
    'version': '14.0',
    'sequence': -10,

    'depends': ['base', 'web', 'website', 'sale_management', 'point_of_sale'],

    'description': """Bista Training Data""",

    'author': "Kunal Chambhare",
    'website': "http://www.bistassolutions.com",

    'data': [
        'views/training_batch_view.xml',
        'security/ir.model.access.csv',
        'views/employee_role_view.xml',
        'views/trainee_master_view.xml',
        'views/trainer_master_view.xml',
        'views/training_subjects_view.xml',
        'data/ir_sequence_data.xml',
        'views/training_record_view.xml',
        'wizard/convert_to_employee_wiz_view.xml',
        'security/bista_training_security.xml',
        'wizard/reject_reason_wiz_view.xml',
        'report/attendance_report.xml',
        'report/template_attendance_report.xml',
        'wizard/attendance_report_wiz_view.xml',
        'report/trainee_report.xml',
        'report/trainee_report_template.xml',
        'views/template.xml',
        'views/assets.xml',
    ],
    'qweb':
        [
            'static/src/xml/base.xml',

        ],
    'application': True,
}
