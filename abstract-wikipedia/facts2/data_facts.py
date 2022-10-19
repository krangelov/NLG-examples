import pgf
from collections import namedtuple


class FactSystem:
    def __init__(self,gr,lang1):
        self.grammar = gr
        self.language1 = lang1   # the language in which entities are parsed to trees

    def get_data(self,filename):
        data = []
        with open(filename) as file:
            fieldnames = file.readline().split()
            Data = namedtuple('Data', fieldnames)
            for line in file:
                fields = Data(*line.split('\t'))
                data.append(fields)
        return data

    # can raise ParseError
    def str2exp(self,cat,s):
        eng = self.grammar.languages[self.language1]
        pp = eng.parse(s,cat=pgf.readType(cat))
        _,e = pp.__next__()
        return e

    def exp2str(self,exp):
        eng = self.grammar.languages[self.language1]
        return eng.linearize(exp)

    def data2lin(self,cat,s):
        return self.exp2str(self.str2exp(cat,s))
        
    def run(self,datafile,fact_generator):
        gr = self.grammar
        data = sorted(self.get_data(datafile))
        for lang in gr.languages.values():
            text = []
            for doc in fact_generator(self,data):
                for tree in doc:
                    lin = lang.linearize(tree)
                    if lin: text.append(lin[0].upper() + lin[1:])
            print('\n'.join(text))
            print()


def simple_facts(factsys,data):
    "for each tuple in data, generate an attribute fact for each field"
    fields = factsys.fieldnames.split()    
    facts = []
    for tuple in data:
        object = factsys.str2exp("Object",tuple[0])
        for (attr,val) in [(fields[i],tuple[i]) for i in range(1,len(fields))]:
            fact = pgf.Expr("AttributeFact", [
                    factsys.str2exp("Attribute",attr),
                    object,
                    factsys.str2exp("Value",val)])
            facts.append(fact)
    return facts


def example_run():
    gr = pgf.readPGF('Countries.pgf')
    factsys = FactSystem(
        'country capital area population continent currency',
        gr,
        'CountriesEng'
        )
            
    factsys.run('../data/countries.tsv',simple_facts)

if __name__ == "__main__":
    example_run()
