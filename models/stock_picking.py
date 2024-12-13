from odoo import fields,models

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'
    
    code = fields.Selection([('incoming', 'Receipt'), ('outgoing', 'Delivery'), ('internal', 'Internal Transfer'),('multicompany', 'Multicompania')], 'Type of Operation', required=True)
    
