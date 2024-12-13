# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DirectTransfer(models.Model):
    _name = 'stock.picking.transfer'
    _inherit ='stock.picking'
    
    company_id = fields.Many2one('res.company',string="Compania")
    location_dest_id = fields.Many2one('stock.location',string='Ubicación de destino')
    location_id = fields.Many2one('stock.location',string='Ubicación de origen')
    date = fields.Datetime('Hora')
    date_done = fields.Datetime('Hora')
    display_name = fields.Char('Nombre en pantalla')
    move_ids = fields.One2many('stock.move',string="Lineas de movimiento")
    scheduled_date = fields.Datetime('Fecha programada')
    user_id = fields.Many2one('res.users','Responsable')
    
    