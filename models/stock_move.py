from odoo import models,fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    picking_transfer_id = fields.Many2one(
        'stock.picking.transfer', 
        string="Transferencia Directa"
    )