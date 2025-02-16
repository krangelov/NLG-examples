import sys
sys.path.append('../facts2/')
from data_facts import *

import pgf

gr = pgf.readNGF("/usr/local/share/x86_64-linux-ghc-8.8.4/gf-3.11.0/www/robust/Parse.ngf")
gr.embed("wordnet")

from wordnet.api import *

# explicit trees via embedded grammar module, takes 0.214s
def country_texts_embedded(factsys,data):
    import wordnet as w
    
    facts = []
    for tuple in data:
        doc = []
        doc.append(mkCl(mkNP(pgf.ExprFun(tuple.country)),mkNP(mkNP(a_Det,w.country_1_N),mkAdv(w.with_Prep,mkNP(mkDigits(int(tuple.population)),w.inhabitant_1_N)))))
        doc.append(mkCl(mkNP(mkDet(w.it_Pron),w.area_6_N),mkNP(mkDigits(int(tuple.area)),mkCN(w.square_1_A,w.kilometre_1_N))))
        doc.append(mkS(w.and_Conj,mkListS(mkS(mkCl(mkNP(the_Det,w.PossNP(mkCN(w.capital_3_N),mkNP(pgf.ExprFun(tuple.country)))),mkNP(pgf.ExprFun(tuple.capital)))),
                                          mkS(mkCl(mkNP(mkDet(w.it_Pron),mkCN(w.currency_1_N)),mkNP(pgf.readExpr(tuple.currency)))))))
        facts.append(doc)
    return facts

if __name__ == "__main__":
    factsys = FactSystem(gr)
    factsys.run('../data/countries.tsv',country_texts_embedded)
