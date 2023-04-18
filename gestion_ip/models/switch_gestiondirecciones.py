import string
from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
class switch(models.Model):
    _name = 'switch.gestiondirecciones'
    _descripcion = 'Switch'

    name = fields.Char(string="Número Switch", required=True) #required=True
    ip_switch = fields.Char(string="IP", default='10.0.0.', required=True) #required=True
    piso = fields.Char(string="Número de Piso", required=True) #required=True
    numero_puertos = fields.Char(string="Número de puertos", default='48', required=True) #required=True
    puert_disponibles = fields.Char(string="Puertos disponibles", compute="_compute_accomodation_count")
    num_serie = fields.Char(string="Número de serie")
    rack = fields.Selection([('1','1'), ('2','2')], string="Rack", required=True) #required=True
    stack = fields.Selection([('si','Si'), ('no','No')], string="Stack", required=True) #required=True
    modelo = fields.Char(String="Modelo")
    id_puerto= fields.One2many('puerto.gestiondirecciones', 'id_switch_2',  string="Puertos de Switch")

    #Función para contar los puertos libres por cada switch
    def _compute_accomodation_count(self):
        for rec in self:
            rec.puert_disponibles = self.env['puerto.gestiondirecciones'].search_count([('estado_puerto', '=', 'libre'),('id_switch_2', '=', rec.name)])
    
    # Función para retornar el piso en el que se encuentra un Switch, al momento de
    # querer ingresar un registro en el modelo "control.gestiondirecciones"
    def name_get(self):
        result = []
        for record in self:
            name = record.piso
            result.append((record.id, name))
        return result

    # Función para crear un registro en el modelo "puerto.gestiondirecciones" al momento 
    # de crear un registro en este modelo. "switch.gestiondirecciones"
    # En este caso creamos los puertos(48) automaticamente para no tener que ingresar manualmente
    # en el modelo "puerto.gestiondirecciones" y sea más comodo.
    @api.model_create_multi
    def create(self, vals):
        for i in vals:
            for y in range(1, 48+1): # 48 puertos
                datos = [
                    {'name':y, 'id_switch_2':i['name'], 'estado_puerto':'libre'} 
                ]
                self.env['puerto.gestiondirecciones'].create(datos)
        return super(switch, self).create(vals)

    # Función para no ingresar IP's repetidas
    @api.constrains('ip_switch')
    def _verificar_ip_switch(self):
        for record in self:
            if record.ip_switch:
                register = self.env['switch.gestiondirecciones'].search([['ip_switch', '=', record.ip_switch]])
                if register:
                    for r in register:
                        if r.id != record.id:
                            raise ValidationError('IP en uso, intente con otra!')

    # Función para no ingresar Número de Switch repetidos
    @api.constrains('name')
    def _verificar_numero_switch(self):
        for record in self:
            if record.name:
                register = self.env['switch.gestiondirecciones'].search([['name', '=', record.name]])
                if register:
                    for r in register:
                        if r.id != record.id:
                            raise ValidationError('Número de Switch en uso, intente con otra!')

    # CÓDIGO QUE PUEDE SER ÚTIL
    # @api.constrains('numero_puertos')
    # def _verificar_estado(self):
    #     for record in self:
    #         if record.numero_puertos:
    #             for i in range(1, int(record.numero_puertos)+1 ):
    #                 datos = [
    #                     {'name':i, 'id_switch_2':record.numero_puertos} 
    #                     ]
    #                 self.env['puerto.gestiondirecciones'].create(datos)

    # @api.model_create_multi
    # # @api.model
    # def create(self, vals):
    #     # for record in self:
    #     # if 'numero_puertos' in vals:
    #     #     ire = vals['numero_puertos']

    #     for i in range(2):
    #         datos = [
    #             {'name':i, 'id_switch':self.ip_switch} 
    #                 # {'name':'2', 'id_switch': '1'}, 
    #                 # {'name':'3', 'id_switch': '1'}
    #             ]
    #         self.env['puerto.gestiondirecciones'].create(datos)

    #     return super(switch, self).create(vals)

