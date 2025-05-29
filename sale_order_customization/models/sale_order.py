from odoo import models, fields, api, _ 
from odoo.exceptions import UserError
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def _get_default_check_is_sale_manager(self):
        if self.user_has_groups('sale_order_customization.sale_admin_security'):
            return True
        else:
            return False
    
    manager_reference = fields.Char(string = 'Manager Reference')
    is_sale_manager = fields.Boolean(string ='Is Sale Manager', default =_get_default_check_is_sale_manager)
    allow_auto_work_flow = fields.Boolean(string="Allow Auto Workflow")



    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            sale_order_limit = self.env['res.config.settings'].sudo().search([],limit=1).sale_order_limit
            if rec.amount_total > sale_order_limit and not self.env.user.has_group('sale_order_customization.sale_admin_security'):
                raise UserError(_('Only Sales Admins are authorized to confirm orders that surpass the set limit.'))
            if rec.allow_auto_work_flow == True:
                invoice_created = rec._create_invoices()
                invoice_created.action_post()
                for line in rec.order_line:
                    if line.product_id.type == 'product' and line.product_uom_qty > line.product_id.free_qty:
                        return res 
                    for picking in  rec.picking_ids:
                        if picking.state == 'assigned': 
                            picking.button_validate()
                context = {
                    "active_model": "account.move", 
                    "active_ids": [invoice_created.id]
                    }
                payments = self.env['account.payment.register'].with_context(**context).create(
                    {
                        'payment_date': date.today(),
                    }
                )
                payments.action_create_payments()
        return res
