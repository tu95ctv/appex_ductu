# from odoo.addons.component.core import Component

# from odoo.addons.base_rest.components.service import to_int, to_bool


# class ChecklistService(Component):
#     _inherit = 'base.rest.service'
#     _name = 'res_users_checklist.service'
#     _usage = 'res_users_checklist'
#     _collection = 'eastlog_checklist.private.services'
#     _description = """
#         Res Users Checklist Services
#         Access to the res_users_checklist services is only allowed to authenticated users.
#         If you are not authenticated go to <a href='/web/login'>Login</a>
#     """

#     def get(self, _id):
#         """
#         Get res_users_checklist's informations
#         """

#         return self._to_json(self._get(_id))

#     # The following method are 'private' and should be never never NEVER call
#     # from the controller.

#     def _get(self, _id):
#         return self.env['res.users'].browse(_id)

#     def _to_json(self, user):
#         res = {
#             'id': user.id,
#             'name': user.name,
#         }
#         if user.checklist_ids and len(user.checklist_ids) > 0:
#             checklists = []
#             for checklist_id in user.checklist_ids:
#                 checklists.append({
#                     'id': checklist_id.id,
#                     'name': checklist_id.name,
#                 })
#             res['checklists'] = checklists
#         return res
