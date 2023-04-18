import string
from odoo import models, fields
class direccion(models.Model):
    _name = 'direccion.gestiondirecciones'
    _descripcion = 'Direcciones'

    piso = fields.Char(string="Piso", required=True) #required=True
    name = fields.Char(string="Dirección", required=True) #required=True
    siglas = fields.Char(string="Siglas")
    responsable = fields.Char(string="Responsable", required=True) #required=True
    
