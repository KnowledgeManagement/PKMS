import argparse
import json
import magic
import requests
import response 


def GetUploadUrl(upload_path, headers) -> str:
    YandexUploadUrl = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    request = requests.get(YandexUploadUrl, headers=headers, params={'path' : upload_path})
    if request.status_code != 200 :
        print("something goes wrong : " + str(request.status_code))
        return ""
    return request.json()['href']

def PutFile(url, headers, file_path) :
    request = requests.put(url, data=open(file_path, 'rb'), headers=headers)
    if request.status_code != 201 and request.status_code != 202 :
        print("something goes wrong : " + str(request.status_code))
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-u] FILE...",
        description="Download your file to your YandexDisk."
    )
    # For now we let user download only one file at the time
    parser.add_argument('-upload', '--upload', '-u', type=str, nargs=1)
    file_path = parser.parse_args().upload[0]
    filename = file_path[file_path.rfind('/') + 1 :]
    # assume that we have config.json in our root
    config = json.load(open('config.json'))
    mime = magic.Magic(mime=True)
    Content_type = mime.from_file(file_path)
    headers = {'Accept' : 'application/json', 'Authorization' : config['OAuth']}
    headers_send = {'Content-type' : Content_type, 'Slug' : filename}
    upload_url = GetUploadUrl("/test/Student2ID.jpeg", headers)
    if upload_url == "" :
        exit()
    PutFile(upload_url, headers_send, file_path)
