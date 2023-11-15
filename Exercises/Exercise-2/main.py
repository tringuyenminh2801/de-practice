import requests
import polars as pl

from bs4 import BeautifulSoup

web_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"

def getPageContent(url: str) -> str:
    r = requests.get(url=url, allow_redirects=True)
    print(f"Status code: {r.status_code}")
    soup = BeautifulSoup(markup=r.content, features='html.parser')
    if r.status_code == 200:
        page_content = soup.text
    else:
        print(f"Cannot get the content of {url}\n")
        page_content = None
    return page_content

def findFileNameByPattern(pageContentByLines: list[str], pattern: str, extension: str) -> str:
    for line in pageContentByLines:
        if pattern in line:
            fileName = f"{line.split(sep=extension)[0]}{extension}"
            break
    return fileName

def main():
    pageContent = getPageContent(url=web_url)
    if pageContent is None:
        print(f"Found nothing from the web, exit the program")
        exit()
    pageContentByLines = pageContent.split(sep="\n")
    print("Find file name...")
    fileName = findFileNameByPattern(pageContentByLines=pageContentByLines,
                                     pattern="2022-02-07 14:03",
                                     extension=".csv")
    print(f"Found file name: {fileName}")
    fileLink = f"{web_url}{fileName}"
    print(f"Download the file from url {fileLink}...")
    r = requests.get(url=fileLink, allow_redirects=True)
    df = pl.read_csv(source=r.content) if r.status_code == 200 else None
    if df is not None:
        df = df.filter(pl.col("HourlyDryBulbTemperature") == pl.col("HourlyDryBulbTemperature").max())
        print(df)

if __name__ == "__main__":
    main()
