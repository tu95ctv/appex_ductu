from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # checklist_ids = fields.One2many(
    #     comodel_name='eastlog_checklist.checklist', inverse_name='user_id', string='Checklists')
    checklist_record_ids = fields.One2many(
        comodel_name='eastlog_checklist.checklist_record', inverse_name='user_id', string='ChecklistRecords')
