from odoo.addons.component.core import Component

from odoo.addons.base_rest.components.service import to_int, to_bool


class ChecklistService(Component):
    _inherit = 'base.rest.service'
    _name = 'res_users_checklist_records.service'
    _usage = 'res_users_checklist_records'
    _collection = 'eastlog_checklist.private.services'
    _description = """
        Res Users Checklist Services
        Access to the res_users_checklist_records services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Get res_users_checklist_records's informations
        """

        return self._to_json(self._get(_id))

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env['res.users'].browse(_id)

    def _to_json(self, user):
        res = {
            'id': user.id,
            'name': user.name,
        }
        if user.checklist_record_ids and len(user.checklist_record_ids) > 0:
            checklist_records = []
            for checklist_record_id in user.checklist_record_ids:
                checklist_records.append({
                    'id': checklist_record_id.id,
                    'name': checklist_record_id.name,
                    'date_submitted': checklist_record_id.date_submitted,
                    'is_done': checklist_record_id.is_done,
                    'has_problem': checklist_record_id.has_problem,
                })
            res['checklist_records'] = checklist_records
        return res
