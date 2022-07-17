import json
import magic
from pathlib import Path
import requests
import response 

class API:
    key_values = {"YandexDataUrl" : "https://cloud-api.yandex.net/v1/disk/resources",
                           "YandexDownloadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/download",
                           "YandexUploadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/upload"}
    def __init__(self, config_path):
        # self.request = requests() how to create a variable with response type
        self.config = json.load(open(config_path))
        # self.key_values = {"YandexDataUrl" : "https://cloud-api.yandex.net/v1/disk/resources",
        #                    "YandexDownloadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/download",
        #                    "YandexUploadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/upload"}
        # print("test APi init")
    def GetDownloadUrl(self, path, headers) -> str:
        request = requests.get(self.key_values["YandexDownloadUrl"], headers=headers, params={'path' : path})
        if request.status_code != 200 :
            print("something goes wrong : " + str(request.status_code))
            return ""
        return request.json()['href']

    def CreateFileFromUrl(self, url, file_name):
        request = requests.get(url=url)
        with open(file_name, "wb") as file:
            file.write(request.content)
    
    def GetMetaData(self, path, headers) -> list:
        list_of_dir = []
        list_of_files = []
        request = requests.get(self.key_values["YandexDataUrl"], headers=headers, params={'path' : path, 'sort' : 'path'})
        if request.status_code != 200 :
            print("something goes wrong : " + str(request.status_code))
            print(request.json()['description'])
            exit()
        for item in request.json()["_embedded"]['items'] :
            if item["type"] == 'dir':
                list_of_dir.append(item["name"])
            if item['type'] == 'file':
                list_of_files.append([item['name'], item['size'], item['modified']])
        for dir in list_of_dir:
            print("d", dir, end='\n')
        for i in range(len(list_of_files)):
            print("f",i, list_of_files[i][0], list_of_files[i][1], list_of_files[i][2])
        return [list_of_dir, list_of_files]

    def GetUploadUrl(self, download_path, headers) -> str:
        request = requests.get(self.key_values["YandexUploadUrl"], headers=headers, params={'path' : download_path})
        if request.status_code != 200 :
            print("something goes wrong : " + str(request.status_code))
            return ""
        return request.json()['href']

    def PutFile(self, url, headers, file_path) :
        request = requests.put(url, data=open(file_path, 'rb'), headers=headers)
        if request.status_code != 201 and request.status_code != 202 :
            print("something goes wrong : " + str(request.status_code))
            return False
        return True

    def UploadScript(self, file_path, file_name, disk_path):
        mime = magic.Magic(mime=True)
        Content_type = mime.from_file(str(file_path))
        headers = {'Accept' : 'application/json', 'Authorization' : self.config['OAuth']}
        headers_send = {'Content-type' : Content_type, 'Slug' : file_name}
        download_url = self.GetUploadUrl(disk_path + '/' + file_name, headers)
        if download_url == "" :
            exit()
        self.PutFile(download_url, headers_send, str(file_path))

    def DownloadScript(self):
        headers = {'Accept' : 'application/json', 'Authorization' : self.config['OAuth']}
        list_of_data = self.GetMetaData('/', headers=headers)
        path = '/'
        req = input()
        while req != "exit":
            if "cd" in req:
                trash, number =  req.split()
                if number == "..":
                    path = str(Path(path).parent)
                    list_of_data = self.GetMetaData(path, headers=headers)
                    req = input()
                    continue
                if int(number) >= len(list_of_data[0]):
                    print("Wrong dir number")
                    req = input()
                    continue
                path += list_of_data[0][int(number)]
                path += '/'
                list_of_data = self.GetMetaData(path, headers=headers)
                req = input()
                continue
            elif "get" in req:
                trash, number = req.split()
                if int(number) >= len(list_of_data[1]):
                    print("Wrong file number")
                    req = input()
                    continue
                path += list_of_data[1][int(number)][0]
                download_url = self.GetDownloadUrl(path, headers)
                self.CreateFileFromUrl(download_url, list_of_data[1][int(number)][0])
            else:
                print("Wrong command")
                req = input()
                continue
            req = input()