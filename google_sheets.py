import httplib2
import googleapiclient
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from config import SERVICE_ACCOUNT_FILE

table_id = '1T6LblCdK8mv9AaAkKyjmZxuFkYEC5f27xX4yuSWfIgc'

def update_table(table_id, arr, ranges):
    #ranges = 'Действие!A1:AS10000'
    serv_acc = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = serv_acc.authorize(httplib2.Http())
    table_connect = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth, cache_discovery=False)

    r = table_connect.spreadsheets().values().batchUpdate(
        spreadsheetId=table_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": ranges,
                 "values": arr},
            ]}
    ).execute()


def get_table(table_id, ranges):
    #ranges = 'Действие!A1:AS10000'
    serv_acc = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = serv_acc.authorize(httplib2.Http())
    table_connect = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth, cache_discovery=False)
    iiiiiiii = table_connect.spreadsheets().values().batchGet(spreadsheetId=table_id, ranges=ranges,
                                                    valueRenderOption='FORMATTED_VALUE',
                                                    dateTimeRenderOption='FORMATTED_STRING').execute()

    result = iiiiiiii['valueRanges'][0]['values']
    return result

