from odoo import models, fields, api, _
from datetime import datetime,timedelta, date,time
from odoo.tools.misc import xlwt
import io
import base64
from xlwt import easyxf
import datetime
from operator import itemgetter
import math
class LeaveSummaryReport(models.TransientModel):
    _name = "leave.summary.report"


    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    leave_summary_file = fields.Binary('Leave Summary Report')
    file_name = fields.Char('File Name')
    leave_report_printed = fields.Boolean('Leave Report Printed')
    department_id = fields.Many2one('hr.department'
                                    ,'Department'
                                  )
    employee_id= fields.Many2one('hr.employee'
                                    ,'Employee'
                                  )
    holiday_type = fields.Selection([
                                    ('validate', 'Approved'),
                                    ('refuse', 'Refuse'),
                                    ('both', 'Both Approved and Confirmed')
                                    ], string='Leave Type', required=True, default='both')



    @api.multi
    def action_print_leave_summary(self):
        workbook = xlwt.Workbook()
        amount_tot = 0
        hr_holiday_objs_list = []
        column_heading_style = easyxf('font:height 180;font:bold True;align: horiz center;')
        column_heading_style1 = easyxf('font:height 300;font:bold True;align: horiz left;')
        column_heading_style2 = easyxf('font:height 300;font:bold True;align: horiz right;')
        worksheet = workbook.add_sheet('รายงานข้อมูลการลางาน')

        # worksheet.write(3, 2, self.from_date.strftime('%d-%m-%Y'),easyxf('font:height 180;font:bold True;align: horiz center;'))
        # worksheet.write(3, 3, 'ถึง',easyxf('font:height 180;font:bold True;align: horiz center;'))
        # worksheet.write(3, 4, self.to_date.strftime('%d-%m-%Y'),easyxf('font:height 180;font:bold True;align: horiz center;'))

        date_time = self.from_date.strftime('%d-%m-%Y')+'  ถึง  '+self.to_date.strftime('%d-%m-%Y')
        worksheet.write_merge(1, 1, 0, 7, 'Software company in Bangkok',
                              easyxf('font:height 220; align: horiz center;font:bold True;'))
        worksheet.write_merge(2, 2, 0, 7, 'รายงานข้อมูลการลางาน',
                              easyxf('font:height 220; align: horiz center;font:bold True;'))

        worksheet.write_merge(3, 3, 0, 7, date_time,
                              easyxf('font:height 220; align: horiz center;font:bold True;'))

        worksheet.write(5, 0, _('ชื่อ'), column_heading_style)
        worksheet.write(5, 1, _('แผนก'), column_heading_style)
        worksheet.write(5, 2, _('ประเภท'), column_heading_style)
        worksheet.write(5, 3, _('เรื่อง'), column_heading_style)
        worksheet.write(5, 4, _('จำนวน(วัน)'), column_heading_style)
        worksheet.write(5, 5, _('ตั้งแต่'), column_heading_style)
        worksheet.write(5, 6, _('ถึงวันที่'), column_heading_style)
        worksheet.write(5, 7, _('สถานะ'), column_heading_style)
        
        worksheet.col(0).width = 6000
        worksheet.col(1).width = 3000
        worksheet.col(2).width = 2500
        worksheet.col(3).width = 3300
        worksheet.col(4).width = 2500
        worksheet.col(5).width = 2500
        worksheet.col(6).width = 2500
        worksheet.col(7).width = 2000

        String = self.from_date.strftime('%d-%m-%Y') + ' ' + '  ถึง  ' + ' ' + self.to_date.strftime('%d-%m-%Y')
        worksheet2 = workbook.add_sheet('สรุปจำนวนวันลางานของพนักงาน')
        worksheet2.write_merge(2, 2, 0, 1, String, easyxf('font:height 300; align: horiz center;font:bold True;'))
        worksheet2.write(4, 0, _('ชื่อ                     '), column_heading_style2)
        worksheet2.write(4, 1, _('               จำนวน(วัน)'), column_heading_style1)
        worksheet2.col(0).width = 12300
        worksheet2.col(1).width = 12000
        row = 6
        employee_row = 5
        
        
        dict = {}
            
        for wizard in self:

            employee_leave_data = {}

            heading =  'Trinity Roots Co.,Ltd.'
            worksheet.write_merge(0, 0, 0, 7, heading, easyxf('font:height 220; align: horiz center;font:bold True;'))

            heading = 'Trinity Roots Co.,Ltd'
            worksheet2.write_merge(0, 0, 0, 1, heading, easyxf('font:height 300; align: horiz center;font:bold True;'))

            heading =  'สรุปจำนวนวันลางานของพนักงาน'
            worksheet2.write_merge(1, 1, 0, 1, heading, easyxf('font:height 300; align: horiz center;font:bold True;'))

            if wizard.department_id:

                if wizard.holiday_type=='':
                    wizard.holiday_type='both'

                if wizard.holiday_type !='both': #ถ้าstateยืนยันหรือปฎิเสธ

                    if wizard.employee_id.id: #ถ้าเลือกพนักงาน
                        print(wizard.holiday_type)
                        hr_holiday_objs = self.env['hr.leave'].search([('request_date_from', '>=', wizard.from_date),
                                                                       ('request_date_to', '<=', wizard.to_date),
                                                                       ('department_id', '=', wizard.department_id.id),
                                                                       ('employee_id', '=', wizard.employee_id.id),
                                                                       ('state', '=', wizard.holiday_type)
                                                                       ])
                    else:# ไม่เลือกพนักงาน
                        print(wizard.holiday_type)
                        hr_holiday_objs = self.env['hr.leave'].search([('request_date_from', '>=', wizard.from_date),
                                                                       ('request_date_to', '<=', wizard.to_date),
                                                                       ('department_id', '=', wizard.department_id.id),
                                                                       ('state', '=', wizard.holiday_type)
                                                                       ])



                else: #ถ้าstateเลือกทั้งหมด
                    if wizard.employee_id.id:  # ถ้าเลือกพนักงาน
                        hr_holiday_objs = self.env['hr.leave'].search([('request_date_from', '>=', wizard.from_date),
                                                                       ('request_date_to', '<=', wizard.to_date),
                                                                       ('department_id', '=', wizard.department_id.id),
                                                                       ('employee_id', '=', wizard.employee_id.id)
                                                                       ])
                    else:  # ไม่เลือกพนักงาน
                        hr_holiday_objs = self.env['hr.leave'].search([('request_date_from', '>=', wizard.from_date),
                                                                       ('request_date_to', '<=', wizard.to_date),
                                                                       ('department_id', '=', wizard.department_id.id),
                                                                       ])
            else:
                # ไม่เลือกประเภท
                if wizard.holiday_type != 'both':
                    print(wizard.holiday_type)
                    hr_holiday_objs = self.env['hr.leave'].search([('request_date_from', '>=', wizard.from_date),
                                                                   ('request_date_to', '<=', wizard.to_date),
                                                                   ('state', '=', wizard.holiday_type)])
                else:
                    print(wizard.holiday_type)
                    hr_holiday_objs = self.env['hr.leave'].search([('request_date_from', '>=', wizard.from_date),
                                                                   ('request_date_to', '<=', wizard.to_date)])

            for obj in hr_holiday_objs:

                date_from = datetime.datetime.strptime(obj.request_date_from.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                hr_holiday_objs_list.append({'id':obj,'date':date_from,'emp':obj.employee_id.name})
            hr_holiday_objs_list = sorted(hr_holiday_objs_list, key=itemgetter('emp'))
            hr_holiday_objs_list = sorted(hr_holiday_objs_list, key=itemgetter('date'),reverse=True)
            print(hr_holiday_objs_list)
            for dict  in hr_holiday_objs_list:
                for id in dict['id']:
                    print(id)
                    if id.state =='validate':
                        state = 'อนุมัติ'
                    else:
                        state = 'ปฎิเสธ'
                    leave_date_from = datetime.datetime.strptime(id.request_date_from.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                    leave_date_to = datetime.datetime.strptime(id.request_date_to.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')
                    worksheet.write(row, 0, id.employee_id.name,easyxf('font:height 150;align: horiz left;'))
                    worksheet.write(row, 1, id.department_id.name or '',easyxf('font:height 150;align: horiz center;'))
                    worksheet.write(row, 2, id.holiday_status_id.name,easyxf('font:height 150;align: horiz center;'))
                    worksheet.write(row, 3, id.name or '',easyxf('font:height 150;align: horiz center;'))
                    worksheet.write(row, 4, id.number_of_days,easyxf('font:height 150;align: horiz center;'))
                    worksheet.write(row, 5, leave_date_from,easyxf('font:height 150;align: horiz center;'))
                    worksheet.write(row, 6, leave_date_to,easyxf('font:height 150;align: horiz center;'))
                    worksheet.write(row, 7, state, easyxf('font:height 150;align: horiz center;'))
                    if id.employee_id.name not in employee_leave_data:
                       employee_leave_data.update({id.employee_id.name: id.number_of_days})
                    else:
                        leave_data = employee_leave_data[id.employee_id.name] + id.number_of_days
                        employee_leave_data.update({id.employee_id.name: leave_data})
                    row += 1
                    time_now= row +1
             
            for employee in sorted(employee_leave_data):
                name_emp ='        '+employee
                data ='                          '+str(math.ceil(employee_leave_data[employee]))
                worksheet2.write(employee_row, 0, name_emp,easyxf('font:height 300;align: horiz center;'))
                worksheet2.write(employee_row, 1,data,easyxf('font:height 300;align: horiz left;'))
                employee_row += 1


        print(time_now)
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        worksheet.write(time_now,7,today , easyxf('font:height 150;align: horiz center;'))

        print(employee_row)
        worksheet2.write(employee_row, 1, today,easyxf('font:height 180;align: horiz right;'))
            
        fp = io.BytesIO()
        workbook.save(fp)
        excel_file = base64.encodestring(fp.getvalue())
        wizard.leave_summary_file = excel_file

        wizard.file_name = 'รายงานสรุปการลาวันที่ '+today +'.xls'
        wizard.leave_report_printed = True
        fp.close()
        return {
                'view_mode': 'form',
                'res_id': wizard.id,
                'res_model': 'leave.summary.report',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'context': self.env.context,
                'target': 'new',
                       }  
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
 # vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
