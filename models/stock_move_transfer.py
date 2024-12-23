from odoo import models,fields,api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger('')
class StockMove(models.Model):
    _name = 'stock.move.direct_transfer'
    
    sequence = fields.Integer(
    string="Sequence",
    default=10,
    help="Gives the sequence order when displaying a list of stock moves."
)
    name = fields.Char('Nombre')
    date = fields.Datetime(
        'Date Scheduled', default=fields.Datetime.now, index=True, required=True,
        help="Scheduled date until move is done, then date of actual move processing")
    date_deadline = fields.Datetime(
        "Deadline", readonly=True, copy=False,
        help="Date Promise to the customer on the top level document (SO/PO)")
    move_ids = fields.One2many('stock.move', 'direct_transfer_id')
    picking_transfer_id = fields.Many2one(
        'stock.picking.transfer', 
        string="Transferencia Directa"
    )
    product_id = fields.Many2one(
        'product.product', 'Product',
        domain="[('type', 'in', ['product', 'consu'])]", index=True, required=True)
    product_uom = fields.Many2one(
    'uom.uom', "UoM", required=True,
    compute='_compute_product_uom',
    readonly=False,)
    quantity = fields.Float(
    'Quantity', digits='Product Unit of Measure',store=True)
    availability = fields.Float(
        'Forecasted Quantity',
        readonly=True, help='Quantity in stock that can still be reserved for this move')
    company_id = fields.Many2one('res.company',string="Compania")
    location_dest_id = fields.Many2one('stock.location',string='Ubicación de destino',domain="[]")
    location_id = fields.Many2one('stock.location',string='Ubicación de origen')
    state = fields.Selection([
        ('draft', 'New'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='Status',
        copy=False, default='draft', index=True, readonly=True,
        help="* New: The stock move is created but not confirmed.\n"
             "* Waiting Another Move: A linked stock move should be done before this one.\n"
             "* Waiting Availability: The stock move is confirmed but the product can't be reserved.\n"
             "* Available: The product of the stock move is reserved.\n"
             "* Done: The product has been transferred and the transfer has been confirmed.")



            
    @api.depends('product_id')
    def _compute_product_uom(self):
        for transfer in self:
            if transfer.product_id:
                transfer.product_uom = transfer.product_id.uom_id
            else:
                transfer.product_uom = False

    def action_confirm(self):
        self.state = 'done'
        return