#
#     Copyright (C) 2016  Siddharth Saxena
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
try:
    from bs4 import BeautifulSoup
except ImportError:
    import BeautifulSoup


class PyCurrency:
    @staticmethod
    def convert(amount, _from, _to):
        url = 'https://www.google.com/finance/converter?a={}&from={}&to={}'.format(amount, _from, _to)
        response = urllib2.urlopen(url)
        html = response.read()
        parsed = BeautifulSoup(html, 'lxml').body.find('span', attrs={'class': 'bld'}).text
        return parsed

    @staticmethod
    def codes():
        url = 'https://www.google.com/finance/converter'
        response = urllib2.urlopen(url)
        html = response.read()
        parser = BeautifulSoup(html, 'lxml').body.find_all('option')
        for code in parser:
            code = str(code).strip().split('<')[1]
            print(code.strip().split('>')[-1])


def convert(amount, _from, _to):
    return PyCurrency.convert(amount, _from, _to)


def codes():
    return PyCurrency.codes()
