from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class DirectTransfer(models.Model):
    _name = 'stock.picking.transfer'
    _description = 'Direct Transfer of Stock Picking'

    # Secuencia automática para nuevos registros
    name = fields.Char(string='',readonly=True)
    sequence_used = fields.Char(String='Sequence',readonly=True)
    display_name = fields.Char(string='Número', compute='_compute_display_name')
    
    company_id = fields.Many2one(
        'res.company',
        string="Compañía",
        default=lambda self: self.env.user.company_id.id
    )
    location_dest_id = fields.Selection(
        selection='_get_all_locations',
        string='Ubicación de destino',
        store=True,
        required=True  # Opcional: asegura que siempre se establezca un valor
    )

    location_dest_id_new = fields.Many2one(
        'stock.location',
        string='Ubicación de destino',
        domain="[('usage', '=', 'internal')]",
        store=True
    )

    location_id = fields.Many2one(
        'stock.location',
        string='Ubicación de origen',
        domain="[('usage', '=', 'internal')]",
        store=True,
        required = True

    )
        
    date = fields.Datetime('Hora de salida',readonly=True)
    date_done = fields.Datetime('Hora de confirmación',readonly=True)
    scheduled_date = fields.Datetime(
        'Fecha programada',
        default=lambda self: fields.Datetime.now()
    )
    display_name = fields.Char('Nombre en pantalla')
    move_ids = fields.One2many(
        'stock.move.direct_transfer',
        'picking_transfer_id',
        string="Líneas de movimiento"
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.uid
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('assigned', 'Por confirmar'),
            ('done', 'Hecho'),
            ('cancel', 'Cancelado')
        ],
        string="Estado",
        default='draft',
        required=True
    )
    
    @api.model
    def _get_all_locations(self):
        """Busca todas las ubicaciones disponibles sin restricciones de compañía."""
        locations = self.env['stock.location'].sudo().search([('usage', '=', 'internal')])
        return [(loc.id, loc.display_name) for loc in locations]
    
    @api.depends('name')
    def _compute_display_name(self):
        _logger.info('Change display name')
        for transfer in self:
            _logger.info('Change display name')
            transfer.display_name = transfer.name if transfer.name else '/'
            
    @api.model
    def _get_default_sequence(self):
        """
        Genera un nombre secuencial automáticamente.
        """
        _logger.info('Get sequence')
        sequence = self.env['ir.sequence'].sudo().next_by_code('stock.picking.transfer') or 'Nuevo'
        return sequence

    def confirm(self):
        for transfer in self:
            """
            Genera los movimientos necesarios para la transferencia directa.
            """
            transport_location = self.env['stock.location'].search(
                [('usage', '=', 'transit'), ('company_id', '=', False)], limit=1
            )
            if not transport_location:
                raise UserError("No se ha configurado un inventario de transporte sin compañía asignada.")
            
            for picking in self:
                if not picking.move_ids:
                    raise UserError("No hay líneas de movimiento en esta transferencia.")
    
                for move in picking.move_ids:
                    if not move.product_id or move.quantity <= 0:
                        raise UserError(f"El producto {move.product_id.name} no tiene una cantidad válida para transferir.")
    
                    # Movimiento de salida
                    _logger.info(picking.location_id)
                    self.env['stock.move'].sudo().create({
                        'name': f"Salida de {move.product_id.name}",
                        'product_id': move.product_id.id,
                        'product_uom': move.product_uom.id,
                        'quantity': move.quantity,
                        'location_id': transfer.location_id.id,
                        'location_dest_id': transport_location.id,
                        'company_id': picking.company_id.id,
                        'direct_transfer_id': move.id,
                        'state': 'done'
                    })
                    # Movimiento de entrada
                    self.env['stock.move'].sudo().create({
                        'name': f"Entrada de {move.product_id.name}",
                        'product_id': move.product_id.id,
                        'product_uom': move.product_uom.id,
                        'quantity': move.quantity,
                        'location_id': transport_location.id,
                        'location_dest_id': transfer.location_dest_id_new.id,
                        'company_id': picking.company_id.id,
                        'direct_transfer_id': move.id,
                        'state': 'done'
                    })
            transfer.state = 'done'
            transfer.date_done = fields.Datetime.now()

    def send_products(self):
        self.date = fields.Datetime.now()
        if not self.name:
            self.name = self.env['ir.sequence'].next_by_code('stock.picking.transfer') or 'Nuevo'
            self.display_name = self.name
            self.sequence_used = self.name
        # Asegúrate de que los valores no se pierdan aquí
        self.write({
            'state': 'assigned',
            'location_dest_id_new': int(self.location_dest_id),
        })
        _logger.info('Movimientos generados y estado actualizado.')