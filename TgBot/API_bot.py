from dataclasses import dataclass, field
import json
import magic
from pathlib import Path
import requests
import response 

def DecimalSize(size) -> str:
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while size >= 1024 and i < len(suffixes) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {suffixes[i]}"
@dataclass(init=True)
class APIClass:
    OAuth : str
    list_of_data: list = field(default_factory=list)
    resp: str = "empty"
    disc_path: str = "/"
    key_values = {"YandexDataUrl" : "https://cloud-api.yandex.net/v1/disk/resources",
                  "YandexDownloadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/download",
                  "YandexUploadUrl" : "https://cloud-api.yandex.net/v1/disk/resources/upload"}

    def GetMetaData(self):
        headers = {'Accept' : 'application/json', 'Authorization' : self.OAuth}
        list_of_dir = []
        list_of_files = []
        resp = f""
        request = requests.get(self.key_values["YandexDataUrl"], headers=headers, params={'path' : self.disc_path, 'sort' : 'path'})
        if request.status_code != 200:
            resp += f"something goes wrong : {str(request.status_code)}"
            resp += f"{request.json()['description']}"
            self.list_of_data = [resp]
        for item in request.json()["_embedded"]['items']:
            if item["type"] == 'dir':
                list_of_dir.append(item["name"])
            if item['type'] == 'file':
                list_of_files.append([item['name'], item['size'], item['modified']])
        for i in range(len(list_of_dir)):
            resp += (f"d {list_of_dir[i]}  /cd{i} \n")
            # print("d", dir, end='\n')
        for i in range(len(list_of_files)):
            resp += (f"f {i} {list_of_files[i][0]} {DecimalSize(list_of_files[i][1])} /get{i}\n")
            # print("f", i, list_of_files[i][0], DecimalSize(list_of_files[i][1]), list_of_files[i][2])
        self.list_of_data = [list_of_dir, list_of_files]
        self.resp = resp
    
    # def MetaDataDownload(self):
    #     for i in range(len(self.list_of_data[0])):
    #         resp += (f"d {self.list_of_data[0][i]}  /cd{i} \n")
    #         # print("d", dir, end='\n')
    #     for i in range(len(self.list_of_data[1])):
    #         resp += (f"f {i} {self.list_of_data[1][i][0]} {DecimalSize(self.list_of_data[1][i][1])} /get{i}\n")
    #         # print("f", i, list_of_files[i][0], DecimalSize(list_of_files[i][1]), list_of_files[i][2])
    #     self.resp = resp

    def GetUploadUrl(self, upload_path) -> str:
        headers = {'Accept' : 'application/json', 'Authorization' : self.OAuth}
        request = requests.get(self.key_values["YandexUploadUrl"], headers=headers, params={'path' : upload_path})
        if request.status_code != 200 :
            description = request.json()["description"]
            print(f"something goes wrong : {description}" + str(request.status_code))
            return ""
        return request.json()['href']

    def GetDownloadUrl(self, download_path) -> str:
        headers = {'Accept' : 'application/json', 'Authorization' : self.OAuth}
        request = requests.get(self.key_values["YandexDownloadUrl"], headers=headers, params={'path' : download_path})
        if request.status_code != 200:
            print("something goes wrong : " + str(request.status_code))
            return ""
        return request.json()['href']