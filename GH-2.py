import argparse
import json
import requests
import response 

def GetDownloadUrl(path, headers) -> str:
    YandexDownloadUrl = "https://cloud-api.yandex.net/v1/disk/resources/download"
    request = requests.get(YandexDownloadUrl, headers=headers, params={'path' : path})
    if request.status_code != 200 :
        print("something goes wrong : " + str(request.status_code))
        return ""
    return request.json()['href']

def CreateFileFromUrl(url, file_name):
    request = requests.get(url=url)
    with open(file_name, "wb") as file:
        file.write(request.content)

def GetMetaData(path, headers) -> list:
    list_of_dir = []
    YandexDataUrl = "https://cloud-api.yandex.net/v1/disk/resources"
    request = requests.get(YandexDataUrl, headers=headers, params={'path' : path, 'sort' : 'path'})
    if request.status_code != 200 :
        print("something goes wrong : " + str(request.status_code))
        print(request.json()['description'])
        exit()
    # print(len(request.json()["_embedded"]['items']))
    for item in request.json()["_embedded"]['items'] :
        if item["type"] == 'dir':
            list_of_dir.append(item["name"])
    for dir in list_of_dir:
        print(dir, end='\n')
    if len(list_of_dir) == 0:
        print("There are no dirs")
    return list_of_dir

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(
    #     usage="%(prog)s [-d] FILE...",
    #     description="Download your file to your YandexDisk."
    # )
    config = json.load(open('config.json'))
    headers = {'Accept' : 'application/json', 'Authorization' : config['OAuth']}
    download_url = GetDownloadUrl('/test/Student2ID.jpeg', headers)
    # CreateFileFromUrl(download_url, "test.jpg")
    # print(download_url)
    list_of_dir = GetMetaData('/', headers=headers)
    dir_number = input()
    while dir_number != "exit":
        if int(dir_number) >= len(list_of_dir):
            print("Wrong dir number")
            break
        list_of_dir = GetMetaData(('/' + list_of_dir[int(dir_number)]), headers=headers)
        if len(list_of_dir) == 0:
            break
        dir_number = input()