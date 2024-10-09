# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DirectTransfer(models.Model):
    _name = 'stock.picking.transfer'
    _inherit ='stock.picking'
    
    some_field = fields.Char('Some field')
    
class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'
    
    code = fields.Selection([('incoming', 'Receipt'), ('outgoing', 'Delivery'), ('internal', 'Internal Transfer'),('sucursale', 'Sucursales')], 'Type of Operation', required=True)
    
# class my_module(models.Model):
#     _name = 'my_module.my_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100