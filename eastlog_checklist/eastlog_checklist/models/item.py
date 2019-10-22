from odoo import api, fields, models


class Item(models.Model):
    _name = 'eastlog_checklist.item'
    _description = 'Item'

    name = fields.Char(string='Item Name')
    sub_checklist_id = fields.Many2one(
        comodel_name='eastlog_checklist.sub_checklist', string='Sub Checklist', auto_join=True)


class ItemRecord(models.Model):
    _name = 'eastlog_checklist.item_record'
    _description = 'Item Record'

    name = fields.Char(string='Item Record Name')
    item_id = fields.Many2one(
        comodel_name='eastlog_checklist.item', string='Item', auto_join=True)
    user_id = fields.Many2one(
        comodel_name='res.users', string='Submitted By', auto_join=True, default=lambda self: self.env.user)
    has_problem = fields.Boolean(string='Problem?')
    comment = fields.Text(string='Comment')
    media_url = fields.Char(string='Media URL')
    media_type = fields.Char(string='Media type')

    sub_checklist_record_id = fields.Many2one(
        comodel_name='eastlog_checklist.sub_checklist_record', string='Sub Checklist Record')
    is_done = fields.Boolean(string='Done?', auto_join=True)
