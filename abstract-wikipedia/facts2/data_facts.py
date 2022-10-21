import pgf
from collections import namedtuple


class FactSystem:
    def __init__(self,gr):
        self.grammar = gr

    def get_data(self,filename):
        with open(filename) as file:
            fieldnames = file.readline().split()
            Data = namedtuple('Data', fieldnames)
            for line in file:
                yield Data(*line.split('\t'))
        
    def run(self,datafile,fact_generator):
        gr = self.grammar
        data = sorted(self.get_data(datafile))
        for lang in gr.languages.values():
            for doc in fact_generator(self,data):
                text = []
                for tree in doc:
                    lin = lang.linearize(tree)
                    if lin: text.append(lin[0].upper() + lin[1:])
                print(' '.join(text))
            print()
