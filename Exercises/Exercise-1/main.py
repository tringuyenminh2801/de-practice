import os
import time
import zipfile
import requests

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

downloadDirName = "downloads"

def timeIt(function):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = function(*args, **kwargs)
        end = time.time()
        print(f"{function.__name__} ran in {end - start:.3f} seconds\n")
        return res
    return wrapper

@timeIt
def createDirectory(dirName: str):
    workingDir = os.curdir
    newDirAbsolutePath = os.path.join(workingDir, dirName)
    if not os.path.isdir(newDirAbsolutePath):
        print(f"{dirName} not exist, creating a new one...")
        os.mkdir(newDirAbsolutePath)

@timeIt
def downloadFileByURL(url: str) -> bytes:
    r = requests.get(url=url, allow_redirects=True)
    return r.content

@timeIt
def unzipFile(currentDir: str, zipfileName: str):
    with zipfile.ZipFile(os.path.join(currentDir, zipfileName), 'r') as zip_ref:
        zip_ref.extractall(path=currentDir)

@timeIt
def main():
    createDirectory(dirName=downloadDirName)
    for uri in download_uris:
        downloadFolderName = os.path.join(os.curdir, downloadDirName)
        zipfileName = uri.split("/")[-1]
        print(f"Download zip file of {zipfileName}...")
        try:
            # DOWNLOAD THE FILE
            content = downloadFileByURL(url=uri)
            with open(os.path.join(downloadFolderName, zipfileName), "wb") as f:
                f.write(content)
            # UNZIP THE FILE
            print(f"Unzipp and extract {zipfileName}...")
            unzipFile(currentDir=downloadFolderName, zipfileName=zipfileName)
            # REMOVE THE ZIP FILE
            print(f"Removing {zipfileName}...")
            os.remove(os.path.join(downloadFolderName, zipfileName))
            print(f"Done {zipfileName}!\n--------------------------")
        except Exception as e:
            print(f"Exception occur for {zipfileName}: {e}\n--------------------------")
    pass


if __name__ == "__main__":
    main()
