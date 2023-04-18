from pkg_resources import require
from odoo import models, fields
class puerto(models.Model):
    _name = 'puerto.gestiondirecciones'
    _descripcion = 'Puerto de Switch'

    id_switch_2 = fields.Char(string="Switch", required=True) #required=True
    name = fields.Char(string="Número de puerto", required=True) #required=True
    estado_puerto = fields.Selection([('ocupado','Ocupado'), ('libre','Libre')], string="Puerto disponible", default='libre')

    id_switch = fields.Many2one('switch.gestiondirecciones',string="Switch")
    ip_switch = fields.Char(string="IP Switch", related='id_switch.ip_switch', tracking=True, readonly=True)
    hostname_del_usuario = fields.Char(string="Hostname")

    # Función para retornar el Número de puerto, al momento de
    # querer ingresar un registro en el modelo "control.gestiondirecciones"
    def name_get(self):
        result = []
        for record in self:
            name = 'Número de puerto: ' + record.name
            result.append((record.id, name))
        return result

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


