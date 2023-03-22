import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from config import SERVICE_ACCOUNT_FILE

spreadsheet_id = '1T6LblCdK8mv9AaAkKyjmZxuFkYEC5f27xX4yuSWfIgc'


def main(table_id):
    # ranges = 'Действие!A1:AS10000'
    serv_acc = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = serv_acc.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    values = service.spreadsheets().values().get(
        range='A1:AS100',
        spreadsheetId=spreadsheet_id,
        majorDimension='ROWS'
    ).execute()
    print(values)


main('1T6LblCdK8mv9AaAkKyjmZxuFkYEC5f27xX4yuSWfIgc')
