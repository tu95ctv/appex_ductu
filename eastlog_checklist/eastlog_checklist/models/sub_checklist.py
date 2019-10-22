from odoo import models, fields, api


class SubChecklist(models.Model):
    _name = 'eastlog_checklist.sub_checklist'
    _description = 'Sub Checklist'

    name = fields.Char(string='Sub Checklist Name')
    checklist_id = fields.Many2one(
        comodel_name='eastlog_checklist.checklist', string='Checklist', auto_join=True)
    item_ids = fields.One2many(
        comodel_name='eastlog_checklist.item', inverse_name='sub_checklist_id', string='List of Item')


class SubChecklistRecord(models.Model):
    _name = 'eastlog_checklist.sub_checklist_record'
    _description = 'Sub Checklist Record'

    name = fields.Char(string='Sub Checklist Record Name')
    checklist_record_id = fields.Many2one(
        comodel_name='eastlog_checklist.checklist_record', string='Checklist Record', auto_join=True)
    item_record_ids = fields.One2many(
        comodel_name='eastlog_checklist.item_record', inverse_name='sub_checklist_record_id', string='List of Item')
    sub_checklist_id = fields.Many2one(
        comodel_name='eastlog_checklist.sub_checklist', string='Sub Checklist', auto_join=True)
    is_done = fields.Boolean(
        string='Done?',
        readonly=True,
    )

    has_problem = fields.Boolean(
        string='Problem?',
        readonly=True,
    )

    # @api.depends('item_record_ids', 'item_record_ids.is_done')
    # def _compute_item_record_is_done(self):
    #     for sub_checklist_record in self:
    #         for item_record in sub_checklist_record.item_record_ids:
    #             if item_record.is_done == False:
    #                 sub_checklist_record.is_done = False
    #                 return False
    #         sub_checklist_record.is_done = True
    #         return True

    # @api.depends('item_record_ids', 'item_record_ids.has_problem')
    # def _check_item_record_problem(self):
    #     for sub_checklist_record in self:
    #         for item_record in sub_checklist_record.item_record_ids:
    #             if item_record.has_problem:
    #                 sub_checklist_record.has_problem = True
    #                 return True
    #         sub_checklist_record.has_problem = False
    #         return False

    # @api.model
    # def create(self, vals):

    #     sub_checklist_record = super(
    #         SubChecklistRecord, self.sudo()).create(vals)
    #     sub_checklist_record.write({})
    #     return sub_checklist_record

    # @api.multi
    # def write(self, vals):
    #     super(SubChecklistRecord, self).write(vals)
    #     update_vals = self._check_is_done_and_has_problem()
    #     return super(SubChecklistRecord, self).write(update_vals)

    # def _check_is_done_and_has_problem(self):
    #     update_vals = {}
    #     for sub_checklist_record in self:
    #         for item_record in sub_checklist_record.item_record_ids:
    #             if item_record.is_done == False:
    #                 update_vals['is_done'] = False
    #                 break
    #             else:
    #                 update_vals['is_done'] = True
    #         for item_record in sub_checklist_record.item_record_ids:
    #             if item_record.has_problem:
    #                 update_vals['has_problem'] = True
    #                 break
    #             else:
    #                 update_vals['has_problem'] = False
    #     return update_vals
