from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class usuario(models.Model):
    _name = 'usuario.gestiondirecciones'
    _description = 'Usuarios'

    usuario = fields.Char(string="Usuario", required=True) #required=True
    apellidos_nombres = fields.Text(string="Apellidos y Nombres", required=True) #required=True
    name = fields.Char(string="Hostname", required=True) #required=True
    cedula = fields.Char(string="Cédula", required=True) #required=True
    ext_telefonica = fields.Char(string="Extención telefónica", required=True) #required=True
    email_trabajo = fields.Text(string="Email de Trabajo", required=True) #required=True
    permiso_navegacion = fields.Char(string="Permiso de Navegación")
    direccion = fields.Char(string="Dirección")
    estructura_salarial = fields.Char(string="Estructura Salarial", required=True) #required=True
    oficina = fields.Char(string="Oficina", required=True) #required=True
    estado_user = fields.Selection([('activo','Activo'), ('inactivo','Inactivo')], string="Estado", default='activo')
    descripcion = fields.Char(string="Descripción")

    # CÓDIGO QUE PUEDE SER ÚTIL
    # @api.constrains('usuario')
    # def _verificar_usuario(self):
    #     for record in self:
    #         if record.usuario:
    #             register = self.env['usuario.gestiondirecciones'].search([['usuario', '=', record.usuario]])
    #             if register:
    #                 for r in register:
    #                     if r.id != record.id:
    #                         raise ValidationError('Usuario ya existente, intente con otro!')