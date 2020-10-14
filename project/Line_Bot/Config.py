import  psycopg2
try:
    con = psycopg2.connect(database="Leave", user="odoo", password="odoo", host="non-aspire-f5-573g", port="5432")
    con.set_client_encoding('UTF8')
    print("Database opened successfully")
    cur = con.cursor()
except(con) as error:
    print("Database opened error")


Channel_secret = "aa7a35b08380992ee06312f1209a9d6e"
Channel_access_token = "r4ClYhA/byseGzn02jnFV6WIlB73p8UmbCE7iSQ6aHzlwcoaFRFheLWG9NWJJ2GK6Tx55j41syQPPxF1rGWUDQ/3wFdRDmK2onrL29Ck/pTBSoJi1bH9k2aKUE83OMBU9WnaDUTr9b6U+gwSlaYajAdB04t89/1O/w1cDnyilFU="


