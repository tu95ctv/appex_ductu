from odoo import models, fields, api, _, exceptions


class Category(models.Model):
    _name = 'eastlog_checklist.category'
    _description = 'Category'

    name = fields.Char('Category Name')
    checklist_ids = fields.One2many(
        comodel_name='eastlog_checklist.checklist', inverse_name='category', string='Checklists')


class Checklist(models.Model):
    _name = 'eastlog_checklist.checklist'
    _description = 'Checklist'

    name = fields.Char('Checklist Name')
    category = fields.Many2one(
        'eastlog_checklist.category', auto_join=True)
    # user_id = fields.Many2many(
    #     'res.users',
    #     string='Responsible',
    #     default=lambda self: self.env.user,
    #     auto_join=True,
    # )
    sub_checklist_ids = fields.One2many(
        comodel_name='eastlog_checklist.sub_checklist', inverse_name='checklist_id', string='Sub Checklists')


class ChecklistRecord(models.Model):
    _name = 'eastlog_checklist.checklist_record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Checklist Record'

    name = fields.Char(string='Checklist Record Name')
    checklist_id = fields.Many2one(
        comodel_name='eastlog_checklist.checklist', string='Checklist', required=True)
    category = fields.Many2one(
        string='Category', related='checklist_id.category', auto_join=True, store=True)
    date_submitted = fields.Date(string='Date Submitted', required=True)
    user_id = fields.Many2one(
        comodel_name='res.users', string='Submitted By', auto_join=True, default=lambda self: self.env.user)
    sub_checklist_record_ids = fields.One2many(
        comodel_name='eastlog_checklist.sub_checklist_record', inverse_name='checklist_record_id', string='Sub Checklist Record')
    is_done = fields.Boolean(
        string='Done?',
        readonly=True,
    )
    has_problem = fields.Boolean(
        string='Problem?',
        readonly=True,
    )

    @api.model
    def create(self, vals):
        # print('CREATE')
        vals = self._prepare_params_for_create(vals)
        checklist_record = super(ChecklistRecord, self).create(vals)
        self._schedule_new_activity(vals, checklist_record)
        return checklist_record

    @api.multi
    def write(self, vals):
        # print('WRITE')
        # print(vals)
        if 'message_follower_ids' in vals:
            return True

        for rec in self:
            # print('INSIDE FOR WRITE')
            # print(rec.id)
            vals = self._prepare_params_for_update(vals, rec)
            self._schedule_new_activity(vals, rec)
            # print('AFTER NOTIFY')
        return super(ChecklistRecord, self).write(vals)

    def _prepare_params_for_create(self, vals):
        checklist_record_is_done = True
        checklist_record_has_problem = False
        key = 'sub_checklist_record_ids'
        if key in vals:
            val = vals.pop(key)
            sub_checklist_record_ids = []
            for sub_checklist_record in val:
                # One2many: 1 is for update, 4 is adds an existing record
                # We only check "1"
                sub_checklist_record_is_done = True
                sub_checklist_record_has_problem = False

                if 'item_record_ids' in sub_checklist_record[2]:
                    for item_record in sub_checklist_record[2]['item_record_ids']:
                        if item_record[0] <= 1:
                            if 'is_done' in item_record[2]:
                                sub_checklist_record_is_done = \
                                    sub_checklist_record_is_done and item_record[2]['is_done']
                            if 'has_problem' in item_record[2]:
                                sub_checklist_record_has_problem = \
                                    sub_checklist_record_has_problem or item_record[2]['has_problem']

                sub_checklist_record[2]['is_done'] = sub_checklist_record_is_done
                sub_checklist_record[2]['has_problem'] = sub_checklist_record_has_problem
                sub_checklist_record_ids.append(sub_checklist_record)
                checklist_record_is_done = checklist_record_is_done and sub_checklist_record_is_done
                checklist_record_has_problem = checklist_record_has_problem or sub_checklist_record_has_problem
            vals[key] = sub_checklist_record_ids
        vals['is_done'] = checklist_record_is_done
        vals['has_problem'] = checklist_record_has_problem
        return vals

    def _prepare_params_for_update(self, vals, rec):

        checklist_record_data = self._build_structure_checklist_record(rec)
        key = 'sub_checklist_record_ids'
        if key in vals:
            val = vals.pop(key)
            sub_checklist_record_ids = []
            for sub_checklist_record in val:
                # One2many: 1 is for update, 4 is adds an existing record
                # We only check "1"
                if sub_checklist_record[0] == 1:
                    existing_sub_checklist_record = rec.sub_checklist_record_ids.search(
                        [('id', '=', sub_checklist_record[1])], limit=1)[0]

                    sub_checklist_record_data = self._build_structure_sub_checklist_record(
                        existing_sub_checklist_record)

                    if 'item_record_ids' in sub_checklist_record[2]:
                        for item_record in sub_checklist_record[2]['item_record_ids']:
                            if item_record[0] == 1:
                                if 'is_done' in item_record[2]:
                                    self._update_is_done_or_has_problem(
                                        sub_checklist_record_data, item_record[1], new_is_done=item_record[2]['is_done'])
                                    print(sub_checklist_record_data)
                                if 'has_problem' in item_record[2]:
                                    self._update_is_done_or_has_problem(
                                        sub_checklist_record_data, item_record[1], new_has_problem=item_record[2]['has_problem'])
                                    print(sub_checklist_record_data)
                            elif item_record[0] == 4:
                                continue
                            else:
                                raise exceptions.ValidationError(
                                    _('Cannot add new Sub Checklist Record!'))

                    sub_checklist_record[2]['is_done'] = self._get_is_done(
                        sub_checklist_record_data)
                    sub_checklist_record[2]['has_problem'] = self._get_has_problem(
                        sub_checklist_record_data)
                    sub_checklist_record_ids.append(sub_checklist_record)
                    self._update_is_done_or_has_problem(
                        checklist_record_data, sub_checklist_record[1], new_is_done=sub_checklist_record[2]['is_done'])
                    self._update_is_done_or_has_problem(
                        checklist_record_data, sub_checklist_record[1], new_has_problem=sub_checklist_record[2]['has_problem'])

                elif sub_checklist_record[0] == 4:
                    continue
                else:
                    raise exceptions.ValidationError(
                        _('Cannot add new Sub Checklist Record!'))

            vals[key] = sub_checklist_record_ids
        vals['is_done'] = self._get_is_done(checklist_record_data)
        vals['has_problem'] = self._get_has_problem(checklist_record_data)
        print(vals)
        return vals

    def _schedule_new_activity(self, vals, rec):
        if 'date_submitted' not in vals:
            vals['date_submitted'] = rec['date_submitted']
        activities = self.env['mail.activity']
        if vals['has_problem']:
            act_type_id = self.env['mail.activity.type'].search(
                [('name', 'ilike', 'Checklist Record Has Problems')], limit=1).id
            # rec.activity_schedule(
            #     act_type_id, user_id=rec.user_id.id, date_deadline=vals['date_submitted'])
            activities |= self.env['mail.activity'].create({
                'res_model_id': self.env.ref('eastlog_checklist.model_eastlog_checklist_checklist_record').id,
                'res_id': rec.id,
                'user_id': rec.user_id.id,
                'activity_type_id': act_type_id,
                'date_deadline': vals['date_submitted'],
            })
        return activities

    def _update_is_done_or_has_problem(self, arr, id, new_is_done=None, new_has_problem=None):
        # Array = [[id1, is_done, has_problem], [id2, is_done, has_problem], [id3, is_done, has_problem]]
        for index in range(len(arr)):
            if arr[index][0] == id:
                if new_is_done != None:
                    arr[index][1] = new_is_done
                if new_has_problem != None:
                    arr[index][2] = new_has_problem

    def _build_structure_checklist_record(self, rec):
        temp_arr = []
        for sub_checklist_record in rec.sub_checklist_record_ids:
            temp_arr.append(
                [sub_checklist_record.id, sub_checklist_record.is_done, sub_checklist_record.has_problem])
        return temp_arr

    def _build_structure_sub_checklist_record(self, sub_checklist_record):
        temp_arr = []
        for item_record in sub_checklist_record.item_record_ids:
            temp_arr.append(
                [item_record.id, item_record.is_done, item_record.has_problem])
        return temp_arr

    def _get_is_done(self, arr):
        total_is_done = arr[0][1]
        for index in range(1, len(arr)):
            total_is_done = total_is_done and arr[index][1]
        return total_is_done

    def _get_has_problem(self, arr):
        total_has_problem = arr[0][2]
        for index in range(len(arr)):
            total_has_problem = total_has_problem or arr[index][2]
        return total_has_problem
