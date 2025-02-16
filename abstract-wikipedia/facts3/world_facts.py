import sys
sys.path.append('../facts2/')
from data_facts import *

import pgf

gr = pgf.readNGF("/usr/local/share/x86_64-linux-ghc-8.8.4/gf-3.11.0/www/robust/Parse.ngf")
gr.embed("wordnet")

from wordnet.api import *

def continent_text(factsys,data,cont=None):
    import wordnet as w

    cont_data = [d for d in data if cont in [d.continent,None]]
    ncountries = len(cont_data)
    largestpop = max(cont_data, key=lambda c: int(c.population)).country
    largestarea = max(cont_data, key=lambda c: int(c.area)).country
    totalpop = round(sum([int(c.population) for c in cont_data])/1000000,2)

    if cont:
        obj = mkNP(pgf.ExprFun(cont))
    else:
        obj = mkNP(the_Det, w.world_4_N)

    doc = []
    doc.append(mkPhr(mkUtt(mkS(w.ExistNPAdv(mkNP(mkDigits(ncountries), w.country_1_N), mkAdv(w.in_1_Prep, obj)))),fullStopPunct))
    doc.append(mkPhr(mkUtt(mkS(mkCl(mkNP(the_Det, w.PossNP(mkCN(w.total_1_A, w.population_1_N),obj)), mkNP(mkDet(w.num(w.pot4as5(w.pot4float(pgf.Expr(totalpop))))))))),fullStopPunct))
    doc.append(mkPhr(mkUtt(mkS(w.and_Conj,mkListS(mkS(mkCl(mkNP(pgf.ExprFun(largestpop)), mkVP(w.have_1_V2,mkNP(the_Quant,singularNum,mkOrd(w.large_1_A),mkCN(w.population_1_N)))))
                                                 ,mkS(mkCl(mkNP(pgf.ExprFun(largestarea)), mkVP(w.have_1_V2,mkNP(the_Quant,singularNum,mkOrd(w.large_1_A),mkCN(w.area_6_N)))))))),fullStopPunct))

    billions = [mkNP(pgf.ExprFun(c.country)) for c in cont_data if int(c.population) > 1000000000]
    if len(billions) == 1:
        doc.append(mkPhr(mkUtt(mkS(billions[0],mkNP(w.the_only_Quant, mkCN(w.country_1_N, mkAdv(w.with_Prep,mkNP(mkDet(a_Quant,mkNum(w.over_AdN,mkCard(w.num(w.pot51)))),mkCN(w.inhabitant_1_N))))))),fullStopPunct))
    elif len(billions) > 1:
        doc.append(mkPhr(mkUtt(mkS(mkCl(mkNP(w.and_Conj,mkListNP(*billions)),mkNP(mkDet(w.the_only_Quant,pluralNum), mkCN(w.country_1_N, mkAdv(w.with_Prep,mkNP(mkDet(a_Quant,mkNum(w.over_AdN,mkCard(w.num(w.pot51)))),mkCN(w.inhabitant_1_N)))))))),fullStopPunct))

    return doc

def world_texts(factsys,data):
    texts = [continent_text(factsys,data)]
    for cont in {d.continent for d in data}:
        texts.append(continent_text(factsys,data,cont))
    return texts

if __name__ == "__main__":
    factsys = FactSystem(gr)
    factsys.run('../data/countries.tsv',world_texts)
