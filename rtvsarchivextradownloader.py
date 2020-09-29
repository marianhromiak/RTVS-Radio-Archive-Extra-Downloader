#!/usr/bin/env python3
"""
Documentation, License etc.

@package rtvsarchivextradownloader
"""
from requests import get
from lxml import html, etree
from argparse import ArgumentParser
import os.path
import datetime
import re
import logging
from time import sleep
from random import random
import shutil

logger = logging.getLogger()

URL_MATCH = re.compile(r"var url = \"//(.*)&&\" \+ ruurl")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--download_dir",
        "-d",
        help="Directory to download mp3 from rtvs",
        default="~/Downloads",
    )
    parser.add_argument(
        "--relpath",
        "-r",
        help="Relative path to https://rtvs.sk/ for " "archive extra section",
        default="/radio/archiv/extra/rozhlasove-hry?page=",
    )
    parser.add_argument(
        "--random-delay",
        "-R",
        help="Add random delay between download archives",
        action="store_true",
    )

    args = parser.parse_args()
    args.download_dir = os.path.realpath(os.path.expanduser(args.download_dir))
    return args


class RTVSArchivExtraDownloaderSection:
    def __init__(
        self,
        download="~/Downloads",
        url="/radio/archiv/extra/rozhlasove-hry",
        rdelay=False,
    ):
        """param:
                download: directury where to save downloaded files
                url: url for section in rtvs archiv extra
                rrdelay: random delay between archive request
        """
        self.download = download
        self.sectionURL = url
        self.baseURL = "https://www.rtvs.sk"
        self.rdelay = rdelay

    def downloadPlay(self, filename, link):
        """Download link to filename

        param:
                filename: filename to store file from url
                link: url to web archive
        """
        # save mp3 from link to filename
        outputf = self.download + "/" + filename

        dlink = None
        if os.path.isfile(outputf) and os.path.getsize(outputf) > 0:
            logging.info(f"Filename {outputf} already dowloaded")
            return -1

        pomurl = self.baseURL + link
        try:
            r = get(pomurl)
            m = URL_MATCH.search(r.text)
            r = get(f"https://{m.group(1)}")
            j = r.json()
            dlink = j["playlist"][0]["sources"][0]["src"]
        except Exception as e:
            logging.info(f"Cannot get mp3 link for {filename} ")
            logging.error(e)

        if dlink:
            with get(dlink, stream=True) as r:
                with open(outputf, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
            logging.info(f"Downloaded {outputf}")

    def crawler(self):
        """crawl through to archive list in choosed section
        """
        pomurl = self.baseURL + self.sectionURL
        r = get(pomurl + "1")
        doc = html.fromstring(r.text)
        footer = doc.xpath("//nav")[-1]

        # get how many pages we need to crawl
        for i in footer.iterlinks():
            e = i[0]
            pom = e.attrib
            if "title" in pom and pom["title"] == "Koniec":
                pagescount = int(pom["href"].split("=")[1])

        # go through all pages
        for i in range(1, pagescount + 1):
            r = get(pomurl + str(i))
            body = html.fromstring(r.text).find_class("list--radio-series")[0]

            for row in body.iterchildren():
                for e in row.iterlinks():
                    link = e[2]

                    pom = [
                        x.strip().replace(" ", "_")
                        for x in row.text_content().split("\n")
                        if len(x.strip()) > 0
                    ]
                    pom[1], pom[2] = pom[2], pom[1]
                    date_time_obj = datetime.datetime.strptime(pom[1], "%d.%m.%Y_%H:%M")
                    pom[1] = date_time_obj.strftime("%Y%m%d_%H:%M")
                    pom[2] = pom[2].replace("/", ":")

                    fname = "-".join(pom) + ".mp3"

                    if self.rdelay:
                        sleep(random())
                    self.downloadPlay(fname, link)


def main():
    args = parse_args()
    rtvsRozHryURL = args.relpath
    rdelay = args.random_delay
    dwnld = RTVSArchivExtraDownloaderSection(args.download_dir, rtvsRozHryURL, rdelay)
    dwnld.crawler()
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

