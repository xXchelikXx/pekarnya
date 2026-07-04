from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import pandas
import collections


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

year_of_foundation = 2010
now_year = datetime.datetime.now().year
age = now_year - year_of_foundation

prelast_number = age//10%10
last_number = age%10

if last_number == 1:
    if prelast_number == 1:
        year_form = "лет"
    else:
        year_form = "год"
elif 4 >= last_number >= 2:
    if prelast_number == 1:
        year_form = "лет"
    else:
        year_form = "года"
elif 9 >= last_number >= 5 or last_number == 0:
    year_form = "лет"


bakeries_info = pandas.read_excel('cakes3.xlsx', na_values=['N/A', 'NA'], keep_default_na=False).to_dict("records")
bakeries_products = collections.defaultdict(list)

for bakerie in bakeries_info:
    bakeries_products[bakerie["Категория"]].append(bakerie)


rendered_page = template.render(
    age = age,
    year_form = year_form,
    bakeries_products = bakeries_products,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
