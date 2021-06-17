# awesome-bookmarks

awesome-bookmarks is a Python3 script to generate a markdown awesome-list from a folder of bookmarks stored/exported in HTML format. I use to rely a lot on my Firefox bookmarks to organize lists of softwares and knowledge and I want a simple way
to choose a folder and output it in an awesome-list format for sharing. It's based on top of the [Netscape Bookmarks File Parser](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser) for parsing and on [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) for rendering.

## Quickstart
```shell
./awesome-bookmarks.py -b bookmarks.html -f software/cli-tui -o README.md --header "A collection of my cli-tui software collected around"
```

## Install

I suggest you to create a dedicated [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html) to install the packages required.

```
git clone https://github.com/lgaggini/awesome-bookmarks
pip install -r requirements.txt
```

## Status
* Beta version, work in progress, code may be ugly
* Only one level deep subfolders are considered from the starting folder, generally awesome-lists have only a level of categories.

## Documentation
```shell
usage: awesome-bookmarks.py [-h] -b BOOKMARKS -f FOLDER -o OUTPUT [--header HEADER] [--footer FOOTER] [-r] [-l {debug,info,warning,error,critical}]

awesome-bookmarks, awesome-lists from your bookmarks

optional arguments:
  -h, --help            show this help message and exit
  -b BOOKMARKS, --bookmarks BOOKMARKS
                        bookmarks file path
  -f FOLDER, --folder FOLDER
                        bookmarks target folder
  -o OUTPUT, --output OUTPUT
                        target output file
  --header HEADER       header text
  --footer FOOTER       footer text
  -r, --readonly        readonly mode for debug (default disabled)
  -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                        log level (default info)
```
