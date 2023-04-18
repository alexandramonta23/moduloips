import string
from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from email.policy import default
from itertools import chain

class ip(models.Model):
    _name = 'ip.gestiondirecciones'
    _descripcion = 'Ips'

    cod_vlan = fields.Many2one('vlan.gestionvlan',string="Vlan", required=True) #required=True
    name = fields.Char(string="Dirección ip", readonly=False, compute="_compute_is_approval", required=True) #required=True
    disponible2 = fields.Selection([('disponible','Disponible'), ('asignada','Asignada'), ('inactivo','Inactivo')], string="Estado", default='disponible')
    vlan = fields.Char(string="Vlan", related='cod_vlan.name', tracking=True, readonly=False)

    # Estas variables se crean para guardar automaticamente lo que escriben en los campos 
    # de arriba, ya que si queremos utilizarlos directamente no se puede
    ip = fields.Char(string="IP (Campo automático)", readonly=False)
    vlan_otro = fields.Char(string="Vlan", readonly=False)

    # Función para guardar lo que contiene "name" en "ip"
    @api.onchange('name')
    def onchange_partner_id(self):
        for rec in self:
            rec.ip = rec.name

    # Función para guardar lo que contiene "vlan" en "vlan_otro"
    @api.onchange('cod_vlan')
    def onchange_vlan_id(self):
        for rec in self:
            rec.vlan_otro = rec.vlan

    # Función para guardar lo que contiene "vlan" en "name"
    @api.depends('vlan')
    def _compute_is_approval(self):
        for record in self:
            record.name = f"192.168.{record.vlan}."

    # Función para retornar la "ip" y "disponible2" al momento de
    # querer ingresar un registro en el modelo "control.gestiondirecciones"
    def name_get(self):
        result = []
        for record in self:
            name = record.ip + ' - Estado: ' + record.disponible2
            result.append((record.id, name))
        return result

    # Función para no ingresar IP's repetidas
    @api.constrains('ip')
    def _no_repeat(self):
        for record in self:
            if record.ip:
                register = self.env['ip.gestiondirecciones'].search([['ip', '=', record.ip]])
                if register:
                    for r in register:
                        if r.id != record.id:
                            raise ValidationError('La IP ya ha sido registrada, intente con otra!')

    # CÓDIGO QUE PUEDE SER ÚTIL
    # @api.constrains('cod_vlan')
    # def _verificar_estado(self):
    #     for record in self:
    #         if record.cod_vlan:
    #             for i in range(1, 5):
    #                 datos = [
    #                     {'ip':f"192.168.{self.name}.{i}", 'disponible2':'disponible', 'vlan_otro':self.name} 
    #                     ]
    #                 self.env['ip.gestiondirecciones'].create(datos)

    # @api.model_create_multi
    # @api.model
    # def create(self, vals):
        # datos = [{'ip':'1234'}, {'ip':'1'}, {'ip':'555'}]
        # dat_list = self.env['ip.gestiondirecciones'].create(datos)
        # self._cr.commit()
        # self.env['ip.gestiondirecciones'].create(datos)
        # vals['ip'] = 'as'
        # iterador = int(0, 10)
        # for i in range(10):
            # vals['ip'] = self.env['ip.gestiondirecciones'].create(datos)
        #     vals['ip'] = i
        # return super(ip, self).create(vals)

    # @api.model
    # def create(self, vals):
    #     return super(ip, self).create(vals)

    # Funcion para colocar la vlan en el tercer octeto de la IP
    # @api.depends('vlan')
    # def _compute_is_approval(self):
    #     for record in self:
    #         # if record.disp_switch == 'dispositivo':
    #         record.name = f"192.168.{record.vlan}."
            # else:
            #     record.name = f"10.0.0."
            
	# @api.constrains('name')
	# def _verificar_registro(self):
	# 	for record in self:
	# 		if record.ip:
	# 			register = self.env['control.gestiondirecciones'].search([['ip', '=', record.ip]])
	# 			if register:
	# 				for r in register:
	# 					if r.id != record.id:
	# 						raise ValidationError('La IP ya esta en uso!')

    # attendees_count = fields.Integer(
    #     string="Vlan count", compute='_get_attendees_count')
    # cont_ip = fields.Char(string='Número de ips utilizadas por Vlan',compute='cont_ip',required=False,default=0)
    # número de ips utilizadas por Vlan
    
    # @api.multi
    # def cont_ip():
    #     return "Probando..."

    # @api.depends('attendee_ids')
    # def _get_attendees_count(self):
    #     for r in self:
    #         r.attendees_count = len(r.attendee_ids)
 
    