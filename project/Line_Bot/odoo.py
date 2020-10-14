url = 'http://non-aspire-f5-573g:8069'
db = 'Leave'
username = 'odoo'
password = 'odoo'
import xmlrpc.client
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})


# print('---------------------------ค้นหาdepartment---------------------')
def Department():

    result = models.execute_kw(db, uid, password, 'hr.department', 'search_read', [[]],{'fields': ['name']})
    return result

def Department_id(name):
    dp_id=[]
    result = models.execute_kw(db, uid, password, 'hr.department', 'search_read', [[['name', '=', name]]],{'fields': ['id']})
    for data_dp in result:
        result = data_dp['id']
        dp_id.append(result)
    return result
# print('---------------------------ค้นหาข้อมูลพนักงานตามแผนกกกกกกกกกก---------------------')
def emp_dp(dp_id):
    emp_dp=[]
    result = models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [[['department_id', '=', dp_id]]])
    for data_emp in result:
        result = data_emp['name']
        emp_dp.append(result)
    return emp_dp


# print('---------------------------ค้นหาข้อมูลพนักงานตาม user_id_Line---------------------')
def dataEMP(user_id):
    x_line=user_id
    result = models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [[['x_line', '=', x_line]]])
    for l in result:
        if   l["x_line"]  == False :
             l["x_line"]="-"

    return result


# print('---------------------------ค้นหาข้อมูลพนักงาน---------------------')
def list_emp():
    result = models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [[]],{'fields': ['name']})
    emp_data=[]
    for data_emp in result:
        result = data_emp['name']
        emp_data.append(result)
    return emp_data
# print('---------------------------ค้นหาข้อมูลพนักงานตามชื่ออออออออ---------------------')
def emp_name(name):
    result = models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [[['name', '=', name]]], {'fields': [
        'id'
        ,'name'
        , 'work_email'
        , 'work_location'
        , 'mobile_phone'
        , 'birthday'
        , 'gender'
        , 'marital'
        , 'department_id'
        , 'job_id'

    ]})



    for l in result:
        if   l["work_email"]  == False :
             l["work_email"]="-"
        if l["work_location"] == False :
            l["work_location"]="-"
        if l["mobile_phone"] == False :
            l["mobile_phone"]="-"
        if l["birthday"] == False:
            l["birthday"] = "-"
        if l["gender"] == False :
            l["gender"]="-"
        if l["marital"] == False :
            l["marital"]="-"
        if l["job_id"] == False :
            l["job_id"]="ว่าง"

    return result

data = emp_name('oraya')
print(data)


# print('--------------------------เช็ควันลาของพนักงาน----------------------');
def dayleave(name):
    name = name
    leave=  models.execute_kw(db, uid, password,'hr.leave.allocation', 'search_read', [[['employee_id', '=', name],['state', '=', 'validate']]] ,{'fields': [
        'display_name'
        ,'employee_id'
        ,'holiday_status_id'
        ,'duration_display'
        ,'state'
        ,'name'
        , 'number_of_days'
        ]})


    for l in leave:
        if   l["display_name"]  == False :
             l["display_name"]="-"
        if l["employee_id"] == False :
            l["employee_id"]="-"
        if l["holiday_status_id"] == False :
            l["holiday_status_id"]="-"
        if l["duration_display"] == False:
            l["duration_display"] = "-"
        if l["state"] == False :
            l["state"]="-"
        if l["name"] == False :
            l["name"]="-"
        if l["number_of_days"] == False :
            l["number_of_days"]="-"

    return leave




# print('--------------------------เช็คขอวันลาาาาาาาาาาาาาาาาาาาาาาาาาาาา----------------------');
def dayleave_state(name):
    name = name
    leave=  models.execute_kw(db, uid, password,'hr.leave.allocation', 'search_read', [[['employee_id', '=', name]]] ,{'fields': [
        'display_name'
        ,'employee_id'
        ,'holiday_status_id'
        ,'duration_display'
        ,'state'
        ,'name'


        ]})
    for l in leave:
        if l["display_name"] == False:
            l["display_name"] = "-"
        if l["employee_id"] == False:
            l["employee_id"] = "-"
        if l["holiday_status_id"] == False:
            l["holiday_status_id"] = "-"
        if l["duration_display"] == False:
            l["duration_display"] = "-"
        if l["state"] == False:
            l["state"] = "-"
        if l["name"] == False:
            l["name"] = "-"



    return leave






# print('--------------------------เช็คขอวลางานนนนนนน---------------------');
def Leaves_Requests(name):
    name = name
    leave=  models.execute_kw(db, uid, password,'hr.leave', 'search_read',
                              [[['employee_id', '=', name]]] ,{'fields': [

        'employee_id'
        ,'holiday_status_id'
        ,'number_of_days'
        ,'state'
        ,'name'
        ,'request_date_from'
        ,'request_date_to'
        ,'number_of_days_display'
        ]})

    for l in leave:
        if l["employee_id"] == False:
            l["employee_id"] = "-"
        if l["holiday_status_id"] == False:
            l["holiday_status_id"] = "-"
        if l["number_of_days"] == False:
            l["number_of_days"] = "-"
        if l["state"] == False:
            l["state"] = "-"
        if l["name"] == False:
            l["name"] = "-"
        if l["request_date_from"] == False:
            l["request_date_from"] = "-"
        if l["request_date_to"] == False:
            l["request_date_to"] = "-"
        if l["number_of_days_display"] == False:
            l["number_of_days_display"] = "-"

    return  leave








