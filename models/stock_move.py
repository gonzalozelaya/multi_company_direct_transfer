from odoo import models,fields

class StockMove(models.Model):
    _inherit = 'stock.move'

    direct_transfer_id = fields.Many2one('stock.move.direct_transfer','Direct transfer id')