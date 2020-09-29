# RTVS-Radio-Archive-Extra-Downloader
Tool to download choosed section from [RTVS Radio Archive Extra](https://www.rtvs.sk/radio/archiv/extra).

Install:
```bash
git clone git@github.com:marianhromiak/RTVS-Radio-Archive-Extra-Downloader.git rtvsdownloader
virtualenv rtvsdownloader
cd rtvsdownloader
. ./bin/activate
pip install -r requirements.txt
```

Example usage:
Download sections:
 * Citanie na pokracovenie
 * Rozpravky 
 * Rozhlasove hry
```bash
cd rtvsdownloader/
. ./bin/activate
python ./rtvsarchivextradownloader.py -R --download_dir='./citanie_na_pokracovanie/' -r '/radio/archiv/extra/citanie-na-pokracovanie?page=' 
python ./rtvsarchivextradownloader.py -R --download_dir='./rozpravky/' -r '/radio/archiv/extra/rozpravky?page=' 
python ./rtvsarchivextradownloader.py -R --download_dir='./rozhlasove_hry/' -r '/radio/archiv/extra/rozhlasove-hry?page=' 
deactivate
```