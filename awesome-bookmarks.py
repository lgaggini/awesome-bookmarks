#! /usr/bin/env python

import os
import sys
from NetscapeBookmarksFileParser import NetscapeBookmarksFile
from NetscapeBookmarksFileParser import parser
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse
import logging
import coloredlogs

LOG_LEVELS = ['debug', 'info', 'warning', 'error', 'critical']
env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)),
    autoescape=select_autoescape()
)
logger = logging.getLogger('awesome-bookmarks')


def log_init(loglevel):
    """ initialize the logging system """
    FORMAT = '%(asctime)s %(levelname)s %(module)s %(message)s'
    logging.basicConfig(format=FORMAT, level=getattr(logging,
                                                     loglevel.upper()))
    coloredlogs.install(level=loglevel.upper(), stream=sys.stdout)


if __name__ == '__main__':

    description = "awesome-bookmarks, awesome-lists from your bookmarks"
    in_parser = argparse.ArgumentParser(description=description)

    in_parser.add_argument('-b', '--bookmarks', default=None,
                           help='bookmarks file path', required=True,
                           type=argparse.FileType('r', encoding='UTF-8'))
    in_parser.add_argument('-f', '--folder', default=None,
                           help='bookmarks target folder', required=True)
    in_parser.add_argument('-o', '--output', default=None,
                           help='target output file', required=True)
    in_parser.add_argument('--header', default=None,
                           help='header text', required=False)
    in_parser.add_argument('--footer', default=None,
                           help='footer text', required=False)
    in_parser.add_argument('-r', '--readonly', dest='readonly',
                           action='store_true',
                           help='readonly mode for debug (default disabled)')
    in_parser.set_defaults(readonly=False)
    in_parser.add_argument('-l', '--log-level', default=LOG_LEVELS[1],
                           help='log level (default info)', choices=LOG_LEVELS)

    options = {}
    cli_options = in_parser.parse_args()
    log_init(cli_options.log_level)
    logger.debug(cli_options)

    path_list = cli_options.folder.split('/')
    logger.debug(path_list)

    logger.info('parsing the bookmark file')
    h = NetscapeBookmarksFile(cli_options.bookmarks)
    p = parser.parse(h)
    main_tree = p.bookmarks

    for idx, folder in enumerate(path_list):
        found = False
        logger.debug('%s: %s' % (idx, folder))
        logger.debug(main_tree.items)
        for item in main_tree.items:
            if item.name == folder:
                logger.debug(item)
                main_tree = item
                found = True
        if found is False:
            logger.error('path %s doesn\'t exist' % (cli_options.folder))
            exit(2)

    logger.info('generating the data')
    tree = {}
    tree['header'] = cli_options.header
    tree['footer'] = cli_options.footer
    tree['path'] = cli_options.folder
    tree['children'] = []
    tree['shortcuts'] = []
    for item in main_tree.children:
        logger.debug(item.name)
        category = ({'name': item.name, 'shortcuts': item.shortcuts})
        tree['children'].append(category)
    for item in main_tree.shortcuts:
        logger.debug(item)
        tree['shortcuts'].append(item)

    logger.info('rendering the template')
    template = env.get_template("README.md.j2")
    logger.debug(tree)
    r_template = template.render(tree=tree)
    if not cli_options.readonly:
        try:
            with open(cli_options.output, 'w') as awesome_md:
                awesome_md.write(r_template)
        except OSError as e:
            logger.error(e)
            sys.exit(2)
    else:
        logger.info(r_template)
