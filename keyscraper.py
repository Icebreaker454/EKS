# -*- coding: utf-8 -*-
import requests
from lxml import html


class KeyScraper(object):
    """
        This class implements the functionality for scraping data from the
        trialeset site containing keys for EAV 9 or other evaluations of
        ESET software
    """
    def __init__(self, url, eval_type, old_style=False):
        self.site_url = url
        self.evaluation_type = eval_type
        self.old_style = old_style

    def get_key(self):
        """
            This function gets the HTML data from given ESET keys site and
            returns the serial key or username\password (for the old ESET
            software) for activation.
        """
        response = requests.get(self.site_url)
        tree = html.fromstring(response.content)

        CLASS = 'table1'
        if self.evaluation_type == 'EAV':
            CLASS += ' table_mr'

        keys_list = tree.xpath(
            '//table[@class="%s"]/tbody/tr/td/text()' % CLASS)
        if self.old_style:
            for i, x in enumerate(keys_list):
                if x.startswith('TRIAL'):
                    yield x, keys_list[i+1]
        else:
            for x in keys_list:
                if x.isupper() and not x.startswith('TRIAL'):
                    yield x
