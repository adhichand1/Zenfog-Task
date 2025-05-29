from odoo import models, fields 


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_order_limit = fields.Float(string='Sale Order Limit',                                 
        config_parameter='sale_order_customization.sale_order_limit',
        help='Sale order limit restricts high-value sales; only Sale Admin can confirm them.')