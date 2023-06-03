from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

def get_service(api_name, api_version, scopes, key_file_location):
    credentials = service_account.Credentials.from_service_account_file(key_file_location)
    scoped_credentials = credentials.with_scopes(scopes)
    service = build(api_name, api_version, credentials=scoped_credentials)
    return service

def main():
    scope = 'https://www.googleapis.com/auth/drive'
    key_file_location = '/tmp/doc-ocr-388705-d0bfd4c96f1d.json'


    try:
        service = get_service(
            api_name='drive',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

        imgfile = "in.jpg"
        txtfile = "out.txt"

        root_id = '19R5hikx4bgbgsiC3LvA4bg1GSHIDYlly'
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        print(items)
        for item in items:
            if item['name'] == 'doc-ocr':
                root_id = item['id']

        from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
        import io

        file_metadata = {
            'name': imgfile,
            'parents': [root_id],
        }
        media = MediaFileUpload('/tmp/Scan0001.jpg',
                                mimetype='image/png', resumable=True)
        file_img = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        file_metadata = {
            'name': txtfile,
            'parents': [root_id],
            'mimeType': 'application/vnd.google-apps.document'
        }
        file_txt = service.files().copy(fileId=file_img['id'], fields='id', body=file_metadata).execute()

        with open(txtfile, 'wb') as file:
            request = service.files().export_media(fileId=file_txt['id'], mimeType='text/plain')
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')


        service.files().delete(fileId=file_txt['id']).execute()
        service.files().delete(fileId=file_img['id']).execute()

    except HttpError as e:
        print(e)


if __name__ == "__main__":
    main()