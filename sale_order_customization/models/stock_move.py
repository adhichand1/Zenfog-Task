from odoo import models, fields 
from odoo.tools import float_compare
from odoo.tools.misc import groupby

class StockMove(models.Model):
    _inherit ='stock.move'
    
    def _assign_picking(self):
        grouped_records = groupby(self, key=lambda move: move._key_assign_picking())
        for grouping_key, move_batches in grouped_records:
            move_batch = self.env['stock.move'].concat(*move_batches)
            is_new_picking = False
            existing_picking = move_batch[0]._search_picking_for_assignation()

            if existing_picking:
                update_vals = {}
                if any(existing_picking.partner_id.id != move.partner_id.id for move in move_batch):
                    update_vals['partner_id'] = False
                if any(existing_picking.origin != move.origin for move in move_batch):
                    update_vals['origin'] = False
                if update_vals:
                    existing_picking.write(update_vals)
                active_picking = existing_picking
            else:
                move_batch = move_batch.filtered(
                    lambda mv: float_compare(mv.product_uom_qty, 0.0, precision_rounding=mv.product_uom.rounding) >= 0
                )
                if not move_batch:
                    continue

                is_new_picking = True
                picking_vals = move_batch._get_new_picking_values()
                related_sale_order = self.env['sale.order'].search([
                    ('name', '=', picking_vals.get('origin'))
                ])

                if related_sale_order:
                    sorted_lines = sorted(move_batch, key=lambda m: m.product_id.id)
                    for product, product_moves in groupby(sorted_lines, key=lambda m: m.product_id):
                        combined_moves = self.env['stock.move'].concat(*product_moves)
                        active_picking = combined_moves._get_new_picking_values()
                        created_picking = self.env['stock.picking'].create(active_picking)
                        combined_moves.write({'picking_id': created_picking.id})
                        combined_moves._assign_picking_post_process(new=is_new_picking)
                else:
                    picking_data = move_batch._get_new_picking_values()
                    created_picking = self.env['stock.picking'].create(picking_data)
                    move_batch.write({
                        'picking_id': created_picking.id,
                        'partner_id': related_sale_order.partner_id.id if related_sale_order else False
                    })
                    move_batch._assign_picking_post_process(new=is_new_picking)

        return True
    
    
    