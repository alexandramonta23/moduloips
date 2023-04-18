import string
from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class vlan(models.Model):
    _name = 'vlan.gestionvlan'
    _description = 'Vlan'

    name = fields.Char(string="Vlan", required=True) #required=True
    direccion_departamental = fields.Many2one('direccion.gestiondirecciones',string="Direccion Departamental", required=True) #required=True
    siglas = fields.Char(string="Siglas", related='direccion_departamental.siglas', tracking=True, readonly=True)
    responsable = fields.Char(string="Responsable", related='direccion_departamental.responsable', tracking=True, readonly=True)

    # no eliminar esta variable
    cod_ip = fields.One2many('ip.gestiondirecciones', 'cod_vlan', string="Ips de Vlan")

    # Función para evitar ingresar Vlan's repetidas
    @api.constrains('name')
    def _verificar_vlan(self):
        for record in self:
            register = self.env['vlan.gestionvlan'].search([['name', '=', record.name]])
            if register:
                for r in register:
                    if r.id != record.id:
                        raise ValidationError('Vlan ya registrada, intente con otra!')

    # Función para crear un registro en el modelo "ip.gestiondirecciones" al momento 
    # de crear un registro en este modelo. "vlan.gestionvlan"
    # En este caso creamos las IP's automaticamente para no tener que ingresar manualmente
    # en el modelo "ip.gestiondirecciones" y sea más comodo.
    @api.model_create_multi
    def create(self, vals):
        for i in vals:
            for y in range(1, 253+1):
                datos = [
                    {'ip':f"192.168.{i['name']}.{y}", 'disponible2':'disponible', 'vlan_otro':i['name']} 
                ]
                self.env['ip.gestiondirecciones'].create(datos)

        return super(vlan, self).create(vals)

    # CÓDIGO QUE PUEDE SER ÚTIL
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         # name = record.piso
    #         name = record.name + ' - ' + record.responsable
    #         result.append((record.id, name))
    #     return result

    # @api.constrains('name')
    # def _verificar_estado(self):
    #     for record in self:
    #         if record.name:
    #             for i in range(1, 5):
    #                 datos = [
    #                     {'ip':f"192.168.{self.name}.{i}", 'disponible2':'disponible', 'vlan_otro':self.name} 
    #                     ]
    #                 self.env['ip.gestiondirecciones'].create(datos)   

