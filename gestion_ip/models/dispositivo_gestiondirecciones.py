from odoo import models, fields
class dispositivo(models.Model):
    _name = 'dispositivo.gestiondirecciones'
    _descripcion = 'Dispositivos'

    name = fields.Char(string="Nombre de Dispositivo", required=True) #required=True
    modelo = fields.Char(string="Modelo", required=True) #required=True
    serie = fields.Char(string="Serie") 
    description = fields.Text(string="Descripción")
