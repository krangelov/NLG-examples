import pgf
from collections import namedtuple

pgf_file = 'Facts.pgf'
country_file = 'countries.tsv'

def get_countries(filename):
    countries = []
    Country = namedtuple('Country',
                'country capital area population continent currency')
    file = open(filename)
    for line in file:
        fields = Country(*line.split('\t'))
        countries.append(fields)
    return countries

  
def country_facts(c):
  object = mkApp('NameObject', [mkName(c.country)])
  return [
    mkApp('AttributeFact',[mkApp(prop,[]),object,val])
      for (prop,val) in [
        ('capital_Attribute',    mkApp('NameValue',[mkName(c.capital)])),
        ('area_Attribute',       mkApp('IntValue', [mkInt(c.area)])),
        ('population_Attribute', mkApp('IntValue', [mkInt(c.population)])),
        ('continent_Attribute',  mkApp('NameValue',[mkName(c.continent)])),
        ('currency_Attribute',   mkApp('NameValue',[mkName(c.currency)]))
        ]
    ]

def mkApp(f,xs):
    return pgf.Expr(f,xs)

def mkInt(s):
    return pgf.readExpr(str(s))

def mkName(s):
    return mkApp('StringName',[pgf.readExpr(str('"' + s + '"'))])

def main():
    gr = pgf.readPGF(pgf_file)
    countries = get_countries(country_file)
    langs = list(gr.languages.values())
    for lang in langs:
        text = []
        for c in countries:
            for t in country_facts(c):
                text.append(lang.linearize(t))
        print('\n'.join(text))
    
if __name__ == "__main__":
    main()

