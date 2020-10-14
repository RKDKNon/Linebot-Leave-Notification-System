import math
from flask import *
from flask import flash
import psycopg2
import requests
import json
from odoo import *
try:

    con = psycopg2.connect(database="Leave", user="odoo",password="odoo", host="non-aspire-f5-573g", port="5432")
    con.set_client_encoding('UTF8')
    print("Database opened successfully")
    cur = con.cursor()
except(con) as error:
    print("Database opened error")
Channel_secret = "aa7a35b08380992ee06312f1209a9d6e"
Channel_access_token = "r4ClYhA/byseGzn02jnFV6WIlB73p8UmbCE7iSQ6aHzlwcoaFRFheLWG9NWJJ2GK6Tx55j41syQPPxF1rGWUDQ/3wFdRDmK2onrL29Ck/pTBSoJi1bH9k2aKUE83OMBU9WnaDUTr9b6U+gwSlaYajAdB04t89/1O/w1cDnyilFU="
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/')
def hello():
    return 'hello world book', 200
@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("index.html")
@app.route('/result_data', methods=['POST', 'GET'])
def result_data():
    if request.method == 'POST':
        email = request.form['email']
        email= str(email)
        passuser = request.form['password']
        passuser = str(passuser)
        userId = request.form['userId']
        displayName = request.form['displayName']
        conn = None
        if userId != '':
            if displayName != '':
                # -------------------------------------------------------------------------------

                try:
                    cur.execute(
                        "SELECT id, name, user_id from hr_employee where x_pin = ('%s')" % (passuser))
                    PW = cur.fetchall()
                except psycopg2.DatabaseError as error:
                        print('error')
                        PW = []


                # -------------------------------------------------------------------------------

                try:
                    cur.execute(
                        "SELECT id ,login from res_users where login = ('%s')" % (email))
                    Login = cur.fetchall()
                except psycopg2.DatabaseError as error:
                        print('error')
                        Login=[]

                # -------------------------------------------------------------------------------

                if not Login:
                    print('ไม่มีlogin')
                    flash("ไม่พบข้อมูลผู้ใช้งาน")
                    return render_template("index.html")
                else:
                    if not PW:
                        print('ไม่มีpass')
                        flash("ไม่พบข้อมูลผู้ใช้งาน")
                        return render_template("index.html")
                    else:
                        print('มี')
                        for row in PW:
                            print(row)
                            print(row[2])
                            if row[2] != '':
                                for row2 in Login:
                                    print(row2)
                                    print(row2[0])
                                    if row[2] == row2[0]:
                                        id = row[0]
                                        print('รหัสพนักงาน =', id)
                                        print('ชื่อพนักงาน', row[1])
                                        print('user_id_line =', userId)
                                        print('ชื่อไลน์', displayName)
                                        cur.execute(
                                            " UPDATE hr_employee SET x_line = ('%s') WHERE id = ('%s')" % (userId, id))
                                        con.commit()
                                        return render_template("show_emp.html", name=row[1])
                                
                            else:
                                flash("user หรือ PIN ไม่ถูกต้อง")
                                return render_template("index.html")

    elif request.method == 'GET':
        return 'result_data GET!!!', 200

    else:
        abort(400)
def leave(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8', "imageUrl": "https://img.icons8.com/cute-clipart/128/000000/connection-status-off.png",
        'Authorization': Authorization
    }
    data = {
        "replyToken": Reply_token,
        "messages": [{
            "type": "text",
            "text": TextMessage,
            "quickReply": {
                "items": [
                    {
                        "type": "action",
                        "imageUrl": "https://img.icons8.com/plasticine/400/000000/bookmark.png",
                        "action": {
                            "type": "message",
                            "label": "เช็คข้อมูลขอลางาน",
                            "text": "ข้อมูลขอลางาน"
                        }
                    }

                ]
            }
        }]
    }
    print(data)
    data = json.dumps(data)  # dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200
def check_data(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    data = {
        "replyToken": Reply_token,
        "messages": [{
            "type": "text",
            "text": TextMessage,
            "quickReply": {
                "items": [
                    {
                        "type": "action",
                        "imageUrl": "https://img.icons8.com/office/80/000000/employee-card.png",
                        "action": {
                            "type": "message",
                            "style": "primary",
                            "label": "ข้อมูลพนักงาน",
                            "text": "ข้อมูลพนักงาน"
                        }
                    }, {
                        "type": "action",
                        "imageUrl": "https://img.icons8.com/dusk/512/000000/bookmark.png",
                        "action": {
                            "type": "message",
                            "style": "primary",
                            "label": "เช็คข้อมูลวันลา",
                            "text": "ข้อมูลวันลา"
                        }
                    }, {
                        "type": "action",
                        "imageUrl": "https://img.icons8.com/wired/512/000000/bookmark.png",
                        "action": {
                            "type": "message",
                            "label": "ข้อมูลขอวันลาเพิ่ม",
                            "text": "ข้อมูลขอวันลาเพิ่ม"
                        }
                    }
                ]
            }
        }]
    }
    data = json.dumps(data)  # dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200
def set_emp(Reply_token, TextMessage, result, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    print(result)
    if result:
        for emp in result:
            emp_name = emp['name']
            work_email = emp['work_email']
            work_location = emp['work_location']
            mobile_phone = emp['mobile_phone']
            birthday = emp['birthday']
            gender = emp['gender']
            if gender == "male":
                gender = "ชาย"
            elif gender == "Female":
                gender = "หญิง"
            else:
                gender = "อื่่นๆ"

            marital = emp['marital']
            if marital == "single":
                marital = "โสด"
            elif marital == "married":
                marital = "แต่งงานแล้ว"
            else:
                marital = "เหตุผลส่วนตัว"
            department_id = emp['department_id'][1]
            job = emp['job_id'][1]

        data = {
            "replyToken": Reply_token,
            "messages": [{
                "type": "flex",
                "altText": "ข้อมูลพนักงาน",
                "contents":{
  "type": "bubble",
   "size": "giga",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": TextMessage,
            "color": "#ffffff",
            "size": "xl",
            "flex": 4,
            "weight": "bold"
          }
        ]
      }
    ],
    "paddingAll": "20px",
    "backgroundColor": "#e4afaf",
    "spacing": "md",
    "height": "70px",
    "paddingTop": "22px"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
        {
        "type": "text",
        "text": "ชื่อ-สกุล",
        "color": "#000000",
        "size": "md",
        "decoration": "underline",
        "weight": "bold",
      },
        {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "filler"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  }
                ],
                "cornerRadius": "30px",
                "width": "12px",
                "height": "12px",
                "borderWidth": "2px",
                "borderColor": "#e36464"
              },
              {
                "type": "filler"
              }
            ],
            "flex": 0
          },
          {
            "type": "text",
            "text": TextMessage,
            "gravity": "center",
            "flex": 4,
            "size": "sm"
          }
        ],
        "spacing": "lg",
        "cornerRadius": "30px",
        "height": "40px"
      },
        {
            "type": "text",
            "text": "แผนก",
            "color": "#000000",
            "size": "md",
            "decoration": "underline",
            "weight": "bold",
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "cornerRadius": "30px",
                            "width": "12px",
                            "height": "12px",
                            "borderWidth": "2px",
                            "borderColor": "#e36464"
                        },
                        {
                            "type": "filler"
                        }
                    ],
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": department_id,
                    "gravity": "center",
                    "flex": 4,
                    "size": "sm"
                }
            ],
            "spacing": "lg",
            "cornerRadius": "30px",
            "height": "40px"
        },
        {
            "type": "text",
            "text": "ตำแหน่ง",
            "color": "#000000",
            "size": "md",
            "decoration": "underline",
            "weight": "bold",
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "cornerRadius": "30px",
                            "width": "12px",
                            "height": "12px",
                            "borderWidth": "2px",
                            "borderColor": "#e36464"
                        },
                        {
                            "type": "filler"
                        }
                    ],
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": job,
                    "gravity": "center",
                    "flex": 4,
                    "size": "sm"
                }
            ],
            "spacing": "lg",
            "cornerRadius": "30px",
            "height": "40px"
        },
       
        {
            "type": "text",
            "text": "เบอร์โทร",
            "color": "#000000",
            "size": "md",
            "decoration": "underline",
            "weight": "bold",
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "cornerRadius": "30px",
                            "width": "12px",
                            "height": "12px",
                            "borderWidth": "2px",
                            "borderColor": "#e36464"
                        },
                        {
                            "type": "filler"
                        }
                    ],
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": mobile_phone,
                    "gravity": "center",
                    "flex": 4,
                    "size": "sm"
                }
            ],
            "spacing": "lg",
            "cornerRadius": "30px",
            "height": "40px"
        },
        {
            "type": "text",
            "text": "อีเมล",
            "color": "#000000",
            "size": "md",
            "decoration": "underline",
            "weight": "bold",
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "cornerRadius": "30px",
                            "width": "12px",
                            "height": "12px",
                            "borderWidth": "2px",
                            "borderColor": "#e36464"
                        },
                        {
                            "type": "filler"
                        }
                    ],
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": work_email,
                    "gravity": "center",
                    "flex": 4,
                    "size": "sm"
                }
            ],
            "spacing": "lg",
            "cornerRadius": "30px",
            "height": "40px"
        },
        {
            "type": "text",
            "text": "ที่อยู่",
            "color": "#000000",
            "size": "md",
            "decoration": "underline",
            "weight": "bold",
        },
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "filler"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "cornerRadius": "30px",
                            "width": "12px",
                            "height": "12px",
                            "borderWidth": "2px",
                            "borderColor": "#e36464"
                        },
                        {
                            "type": "filler"
                        }
                    ],
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": work_location,
                    "gravity": "center",
                    "flex": 4,
                    "size": "sm"
                }
            ],
            "spacing": "lg",
            "cornerRadius": "30px",
            "height": "40px"
        },

    ]
  }
}


            }
            
            ]}
        data = json.dumps(data)

        requests.post(LINE_API, headers=headers, data=data)
        return 200
    else:
        not_data(Reply_token, TextMessage, Channel_access_token)
def more(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    data = {
        "replyToken": Reply_token,
        "messages": [{
            "type": "text",
            "text": TextMessage,
            "quickReply": {
                "items": [
                    {
                        "type": "action",
                        "action": {
                            "type": "cameraRoll",
                            "label": "Camera Roll"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type": "camera",
                            "label": "Camera"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type": "location",
                            "label": "Location"
                        }
                    },
                    {
                        "type": "action",
                        "imageUrl": "https://icla.org/wp-content/uploads/2018/02/blue-calendar-icon.png",
                        "action": {
                            "type": "datetimepicker",
                            "label": "Datetime Picker",
                            "data": "storeId=12345",
                            "mode": "datetime",
                            "initial": "2018-08-10t00:00",
                            "max": "2018-12-31t23:59",
                            "min": "2018-08-01t00:00"
                        }
                    }


                ]
            }
        }]
    }
    data = json.dumps(data)  # dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200
def day_data(Reply_token, TextMessage, days, Leaves_days, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    if Leaves_days:
        if days:
            sum_day = []
            for day in days:
                data_sum = 0
                total = 0
                list = []
                d2 = day['holiday_status_id'][1]
                d3 = day['duration_display']
                d3 = " จำนวนท้้งหมด " + d3
                d5 = day['employee_id'][1]
                d6 = day['number_of_days']
                name1 = {"type": "box",
                         "layout": "horizontal",
                         "contents": [
                             {
                                 "type": "text",
                                 "text": d2,
                                 "size": "md",
                                 "decoration": "underline",
                                 "weight": "bold",
                                 "color": "#000000",
                                 "flex": 0}
                         ]
                         }
                sum_day.append(name1)
                name2 = {"type": "box",
                         "layout": "horizontal",
                         "contents": [
                             {
                                 "type": "text",
                                 "text": d3,
                                 "size": "sm",
                                 "color": "#000000",
                                 "align": "end",
                                 "style": "italic",

                             }

                         ]
                         }
                sum_day.append(name2)
                i = 1
                for num in Leaves_days:
                    dd2 = num['number_of_days_display']
                    if dd2 == '-':
                        dd2 = 1
                    dd3 = num['holiday_status_id'][1]
                    state = num['state']
                    dd5 = num['name']
                    dd5 = "เนื่องด้วย " + dd5
                    if d2 == dd3:
                        if state != "refuse":
                            list.append(dd2)
                            if state == 'confirm':
                                state = "สถานะ: รอการตรวจสอบ"
                                color = "#fbff00"
                            elif state == 'refuse':
                                state = "สถานะ: ถูกปฎิเสธ"
                                color = "#fbff00"
                            else:
                                state = "สถานะ: อนุมัติ"
                                color = "#33CC00"
                            print('dd2',dd2)


                            data_sum = math.ceil(dd2)
                            count = str(data_sum)
                            count = "ใช้ไป " + count + " days "
                            name11 = {"type": "box",
                                      "layout": "horizontal",
                                      "contents": [
                                          {
                                              "type": "text",
                                              "text": dd5,
                                              "size": "sm",
                                              "color": "#000000",
                                              "flex": 0}
                                      ]
                                      }
                            sum_day.append(name11)
                            name12 = {"type": "box",
                                      "layout": "horizontal",
                                      "contents": [
                                          {
                                              "type": "text",
                                              "text": count,
                                              "size": "sm",
                                              "color": "#000000",
                                              "flex": 0}, {
                                              "type": "text",
                                              "text": state,
                                              "size": "sm",
                                              "color": color,
                                              "align": "end"
                                          }

                                      ]
                                      }
                            sum_day.append(name12)
                            name111 = {"type": "separator", "margin": "xxl"}
                            sum_day.append(name111)
                print(list)
                for l in list:
                    total = total + l

                print(total)
                balance = d6 - total
                print(balance)
                balance = math.ceil(balance)
                balance = str(balance)
                balance = str(balance).lstrip('-')
                balance = "คงเหลือ  " + balance + " days"
                name10 = {"type": "box",
                          "layout": "horizontal",
                          "contents": [
                              {
                                  "type": "text",
                                  "text": balance,
                                  "size": "sm",
                                  "color": "#000000",
                                  "align": "end",
                                  "style": "italic",

                              }
                          ]
                          }
                sum_day.append(name10)
                name = {"type": "separator", "margin": "xxl"}
                sum_day.append(name)
            data = {
                "replyToken": Reply_token,
                "messages": [{
                    "type": "flex",
                    "altText": "ข้อมูลวันลา",
                    "contents": {
                        "type": "bubble",
                        "size": "giga",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "backgroundColor": "#ffffff",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": TextMessage,
                                    "weight": "bold",
                                    "color": "#11222c",
                                    "size": "xxl",
                                    "margin": "md"
                                },
                                {
                                    "type": "text",
                                    "text": d5,
                                    "size": "md",
                                    "color": "#000000",
                                    "wrap": True
                                },
                                {
                                    "type": "separator",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "margin": "xxl",
                                    "spacing": "sm",
                                    "contents": sum_day
                                }

                            ]
                        },
                        "styles": {
                            "footer": {
                                "separator": True
                            }
                        },
                        "styles": {
                            "footer": {
                                "separator": True
                            }
                        }
                    }

                }
                ]

            }
            data = json.dumps(data)
            requests.post(LINE_API, headers=headers, data=data)
            return 200
        else:
            not_data(Reply_token, TextMessage, Channel_access_token)
    else:
        not_data(Reply_token, TextMessage, Channel_access_token)
def Allocation(Reply_token, TextMessage, Allocations, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    if Allocations:
        sum_day = []
        for day in Allocations:
            d2 = day['holiday_status_id'][1]
            d3 = day['duration_display']
            d3 = "ขอวันลาเพิ่มจำนวน " + d3
            d4 = day['state']
            if d4 == 'confirm':
                d4 = "สถานะ: รอการตรวจสอบ"
                color = "#fbff00"
            elif d4 == 'refuse':
                d4 = "สถานะ: ถูกปฎิเสธ"
                color = "#ff0000"
            else:
                d4 = "สถานะ: อนุมัติ"
                color = "#33CC00"
            d5 = day['employee_id'][1]
            name0 = {
                "type": "separator",
                "margin": "xxl"

            }
            sum_day.append(name0)
            name1 = {"type": "box",
                     "layout": "horizontal",
                     "contents": [
                         {
                             "type": "text",
                             "text": d2,
                             "size": "md",
                             "decoration": "underline",
                             "weight": "bold",
                             "color": "#000000",
                             "flex": 0}

                     ]
                     }
            sum_day.append(name1)
            name2 = {"type": "box",
                     "layout": "horizontal",
                     "contents": [
                         {
                             "type": "text",
                             "text": d3,
                             "size": "sm",
                             "color": "#000000",
                         }, {
                             "type": "text",
                             "text": d4,
                             "size": "sm",
                             "weight": "bold",
                             "color": color,
                             "align": "end"

                         }
                     ]
                     }
            sum_day.append(name2)
        data = {
            "replyToken": Reply_token,
            "messages": [{
                "type": "flex",
                "altText": "ข้อมูลวันลา",
                "contents": {
                    "type": "bubble",
                    "size": "giga",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#ffffff",
                        "contents": [
                            {
                                "type": "text",
                                "text": TextMessage,
                                "weight": "bold",
                                "color": "#11222c",
                                "size": "xxl",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": d5,
                                "size": "md",
                                "color": "#000000",
                                "wrap": True
                            },
                            {
                                "type": "separator",
                                "margin": "xxl"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "xxl",
                                "spacing": "sm",
                                "contents": sum_day
                            },
                            {
                                "type": "separator",
                                "margin": "xxl"
                            }
                        ]
                    },
                    "styles": {
                        "footer": {
                            "separator": True
                        }
                    }
                }

            }
            ]

        }
        data = json.dumps(data)
        requests.post(LINE_API, headers=headers, data=data)
        return 200
    else:
        not_data(Reply_token,TextMessage, Channel_access_token)
def LeavesRe(Reply_token, TextMessage, result, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    if result:
        sum_day = []
        print(result)
        for day in result:
            d1 = day['name']
            d1 = "เนื่องใน " + d1
            d2 = day['holiday_status_id'][1]
            d3 = day['number_of_days']
            if d3 == '-':
                d3 = 1
            n11 = math.ceil(d3)
            d3 = str(n11)
            d3 = "จำนวน: " + d3 + " วัน"
            d4 = day['state']
            if d4 == 'confirm':
                d4 = "สถานะ: รอการตรวจสอบ"
                color = "#fbff00"
            elif d4 == 'refuse':
                d4 = "สถานะ: ถูกปฎิเสธ"
                color = "#ff0000"
            else:
                d4 = "สถานะ: อนุมัติ"
                color = "#33CC00"

            d5 = day['employee_id'][1]
            d6 = day['request_date_from']
            d6 = "ตั้งแต่ " + d6
            d7 = day['request_date_to']
            d7 = " ถึง " + d7

            name0 = {
                "type": "separator",
                "margin": "xxl"

            }
            sum_day.append(name0)
            name5 = {"type": "box",
                     "layout": "horizontal",
                     "contents": [
                         {
                             "type": "text",
                             "text": d2,
                             "size": "md",
                             "decoration": "underline",
                             "weight": "bold",
                             "color": "#000000",
                             "flex": 0}

                     ]
                     }
            sum_day.append(name5)
            name1 = {"type": "box",
                     "layout": "horizontal",
                     "contents": [
                         {
                             "type": "text",
                             "text": d1,
                             "size": "sm",
                             "color": "#000000",
                             "flex": 0}

                     ]
                     }
            sum_day.append(name1)
            name2 = {"type": "box",
                     "layout": "horizontal",
                     "contents": [
                         {
                             "type": "text",
                             "text": d6,
                             "size": "sm",
                             "color": "#000000",
                             "flex": 0
                         },
                         {
                             "type": "text",
                             "text": d7,
                             "size": "sm",
                             "color": "#000000",
                             "flex": 0
                         }

                     ]
                     }
            sum_day.append(name2)

            name3 = {"type": "box",
                     "layout": "horizontal",
                     "contents": [
                         {
                             "type": "text",
                             "text": d3,
                             "size": "sm",
                             "color": "#000000"
                         }

                     ]
                     }
            sum_day.append(name3)
            name4 = {"type": "box",
                     "layout": "horizontal",
                     "contents": [
                         {
                             "type": "text",
                             "text": d4,
                             "size": "sm",
                             "weight": "bold",
                             "color": color,

                         }
                     ]
                     }
            sum_day.append(name4)

        print(sum_day)

        data = {
            "replyToken": Reply_token,
            "messages": [{
                "type": "flex",
                "altText": "ข้อมูลวันลา",
                "contents": {
                    "type": "bubble",
                    "size": "giga",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": "#ffffff",
                        "contents": [
                            {
                                "type": "text",
                                "text": TextMessage,
                                "weight": "bold",
                                "color": "#11222c",
                                "size": "xxl",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": d5,
                                "size": "md",
                                "color": "#000000",
                                "wrap": True
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "margin": "xxl",
                                "spacing": "sm",
                                "contents": sum_day
                            },
                            {
                                "type": "separator",
                                "margin": "xxl"
                            }
                        ]
                    },
                    "styles": {
                        "footer": {
                            "separator": True
                        }
                    }
                }

            }
            ]

        }
        data = json.dumps(data)
        requests.post(LINE_API, headers=headers, data=data)

        return 200
    else:

        not_data(Reply_token,TextMessage, Channel_access_token)
def Job_position(Reply_token, TextMessage, department, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    if department:
        dp = []
        for day in department:
            result = day['name']
            data_name = result.replace(" ", "")
            # print(data_name)
            name = {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": data_name,
                    "text": result
                }
            }
            dp.append(name)
        print(dp)
        data = {
            "replyToken": Reply_token,
            "messages": [{
                "type": "text",
                "text": TextMessage,

                "quickReply": {
                    "items": dp
                }
            }]
        }

        data = json.dumps(data)  # dump dict >> Json Object
        r = requests.post(LINE_API, headers=headers, data=data)
        return 200
    else:
        not_data(Reply_token, TextMessage, Channel_access_token)
def list_name_dp(Reply_token, TextMessage, list_name, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    if list_name:
        dp = []
        for data in list_name:
            result = data
            data_name = result.replace(" ", "")
            name = {
                "type": "action",
                "action": {
                    "type": "message",
                    "label": data_name,
                    "text": result
                }
            }
            dp.append(name)

        data = {
            "replyToken": Reply_token,
            "messages": [{
                "type": "text",
                "text": TextMessage,

                "quickReply": {
                    "items": dp
                }
            }]
        }

        data = json.dumps(data)  # dump dict >> Json Object
        r = requests.post(LINE_API, headers=headers, data=data)
        return 200
    else:
        not_data(Reply_token, TextMessage, Channel_access_token)
def License(Reply_token, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "replyToken": Reply_token,
        "messages": [{
            "type": "flex",
            "altText": "ข้อมูลวันลา",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "contents": [],
                                            "size": "xl",
                                            "wrap": True,
                                            "text": "ขออภัยค่ะ!",
                                            "color": "#ffffff",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "contents": [],
                                            "size": "lg",
                                            "wrap": True,
                                            "text": "กรุณายืนยันตัวตน",
                                            "color": "#ffffff",
                                            "weight": "bold"
                                        }, {
                                            "type": "box",
                                            "layout": "vertical",
                                            "spacing": "sm",
                                            "contents": [
                                                {
                                                    "type": "button",
                                                    "flex": 2,
                                                    "style": "primary",
                                                    "color": "#aaaaaa",
                                                    "action": {
                                                        "type": "uri",
                                                        "label": "เข้าสู่ระบบ",
                                                        "uri": "https://liff.line.me/1654261096-MeJgQvVX"
                                                    }
                                                }
                                            ]
                                        }

                                    ],
                                    "spacing": "sm"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "contents": [],
                                                    "size": "sm",
                                                    "wrap": True,
                                                    "margin": "lg",
                                                    "color": "#ffffffde",
                                                    "text": "การเก็บข้อมูลไลน์ ในการรับการแจ้งเตือนต่างๆ พร้อมทั้งสอบถามข้อมูลผ่านไลน์ หากไม่ยืนยันตัวตนคุณจะไม่สามารถใช้งานได้"
                                                }
                                            ]
                                        }
                                    ],
                                    "paddingAll": "13px",
                                    "backgroundColor": "#ffffff1A",
                                    "cornerRadius": "2px",
                                    "margin": "xl"
                                }
                            ]
                        }
                    ],
                    "paddingAll": "20px",
                    "backgroundColor": "#464F69"
                }
            }



        }
        ]

    }

    data = json.dumps(data)  # dump dict >> Json Object
    requests.post(LINE_API, headers=headers, data=data)
    return 200
def not_data(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    TextMessage = "ไม่พบ" + TextMessage

    data = {
        "replyToken": Reply_token,
        "messages": [{
            "type": "flex",
            "altText": "Error",
            "contents":{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "image",
        "url": "https://img.icons8.com/cotton/512/000000/error-cloud.png",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        "gravity": "center"
      },
      {
        "type": "image",
        "url": "https://img.icons8.com/cotton/512/000000/error-cloud.png",
        "position": "absolute",
        "aspectMode": "fit",
        "aspectRatio": "1:1",
        "offsetTop": "0px",
        "offsetBottom": "0px",
        "offsetStart": "0px",
        "offsetEnd": "0px",
        "size": "full"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "size": "xl",
                            "color": "#000000",
                            "text": TextMessage
                        }
                    ]
                }
            ],
            "spacing": "none"
          }
        ],
        "position": "absolute",
        "offsetBottom": "0px",
        "offsetStart": "0px",
        "offsetEnd": "0px",
        "paddingAll": "20px"
      },

    ],
    "paddingAll": "0px"
  }
}

        }
        ]

    }



    data = json.dumps(data)  ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():

    if request.method == 'POST':
        # ---------------list Department-----------------
        department = Department()
        dp = []
        for data_dp in department:
            result = data_dp['name']
            dp.append(result)
        # ----------------ข้อมูลพนักงาน-------------------
        list = list_emp()

        # ---------------รับต่าจากไลน์-----------------
        payload = request.json
        print(payload)
        Reply_token = payload['events'][0]['replyToken']
        message = payload['events'][0]['message']['text']
        userId = payload['events'][0]['source']['userId']


        data_line = dataEMP(userId)

        if data_line:
            # ---------------เช็คค่า-----------------
            if "ข้อมูลวันลา" in message:
                Reply_messasge = 'ข้อมูลวันลา'
                emp = dataEMP(userId)
                name = emp[0]['name']
                days = dayleave(name)
                Leaves_days = Leaves_Requests(name)

                day_data(Reply_token, Reply_messasge, days,
                         Leaves_days, Channel_access_token)
            elif "ข้อมูลขอวันลาเพิ่ม" in message:
                Reply_messasge = 'ข้อมูลขอวันลาเพิ่ม'
                emp = dataEMP(userId)
                name = emp[0]['name']
                Allocations = dayleave_state(name)

                Allocation(Reply_token, Reply_messasge,
                           Allocations, Channel_access_token)
            elif "ข้อมูลขอลางาน" in message:
                Reply_messasge = 'ข้อมูลขอลางาน'

                emp = dataEMP(userId)
                name = emp[0]['name']
                result = Leaves_Requests(name)

                LeavesRe(Reply_token, Reply_messasge,
                         result, Channel_access_token)

            elif "เพิ่มเติม" in message:
                Reply_messasge = 'เครื่องมือช่วย'
                more(Reply_token, Reply_messasge, Channel_access_token)

            elif "เช็คข้อมูล" in message:
                Reply_messasge = 'กรุณาเลือกรายการด้านล่างค่ะ!'
                check_data(Reply_token, Reply_messasge, Channel_access_token)
            elif "ข้อมูลพนักงาน" in message:
                Reply_messasge = 'กรุณาเลือกแผนกที่ต้องการค้นหาค่ะ!'
                Job_position(Reply_token, Reply_messasge,
                             department, Channel_access_token)
            elif message in dp:
                Reply_messasge = 'รายชื่อบุคลากรในแผนก ' + message
                dp_id = Department_id(message)
                # print(dp_id)
                list_name = emp_dp(dp_id)

                list_name_dp(Reply_token, Reply_messasge,
                             list_name, Channel_access_token)
            elif message in list:
                Reply_messasge = message
                result = emp_name(message)
                set_emp(Reply_token, Reply_messasge,
                        result, Channel_access_token)
        else:
            License(Reply_token, Channel_access_token)
        return request.json, 200
    elif request.method == 'GET':
        return 'this is method GET!!!', 200
    else:
        abort(400)
