class AFD(object):
    def __init__(self, stari, inputs, starea_finala, starea_initiala, tranzitiile):

        self.stari = stari
        self.Inputs = inputs
        self.Starea_finala = starea_finala
        self.Starea_initala = starea_initiala
        self.Tranzitiile = tranzitiile


    def getTranzitie(self, stare, input):
        return self.Tranzitiile.get((stare, input))
    def getStariAccesibile(self):
        stare_accesibila = {self.Starea_initala}
        for input in self.Inputs:
            stare_posibila = self.getTranzitie(self.Starea_initala, input)
            if stare_posibila is not None:
                stare_accesibila.add(stare_posibila)
        size = 0
        while len(stare_accesibila) > size:
            size = len(stare_accesibila)
            stare_noua = set()
            for stare in stare_accesibila:
                for input in self.Inputs:
                    stare_posibila = self.getTranzitie(stare, input)
                    if stare_posibila is not None:
                        stare_noua.add(stare_posibila)
            stare_accesibila.update(stare_noua)

        return stare_accesibila


    def stergeStariInaccesibile(self):

        stari_accesibile = self.getStariAccesibile()

        self.stari = set(stare for stare in self.stari if stare in stari_accesibile)
        self.Starea_finala = set(stare for stare in self.Starea_finala if stare in stari_accesibile)
        self.Tranzitiile = {k: v for k, v in self.Tranzitiile.items() if k[0] in stari_accesibile}


    def sortTuple(self, a, b):
        return (a, b) if a < b else (b, a)

    def createMatrice(self):
        matrice = dict()
        toate_starile = sorted(self.stari)

        for i in range(len(toate_starile) - 1):
            for j in range(i + 1, len(toate_starile)):
                matrice[self.sortTuple(toate_starile[i], toate_starile[j])] = \
                    ((toate_starile[i] in self.Starea_finala) ^ (toate_starile[j] in self.Starea_finala))

        for i in range(len(toate_starile) - 1):
            for j in range(i + 1, len(toate_starile)):

                for input in self.Inputs:
                    transition1 = self.getTranzitie(toate_starile[i], input)
                    transition2 = self.getTranzitie(toate_starile[j], input)

                    if (transition1 is not None) and (transition2 is not None):
                        if matrice.get(self.sortTuple(transition1, transition2)):
                            matrice[self.sortTuple(toate_starile[i], toate_starile[j])] = True

        return matrice


    def GasesteStareAsemanatoare(self, matrice):

        stare_asemanatoare = list()
        toate_starile = sorted(self.stari)

        for i in range(len(toate_starile) - 1):
            for j in range(i + 1, len(toate_starile)):
                if not matrice.get(self.sortTuple(toate_starile[i], toate_starile[j])):
                    stare_asemanatoare.append(self.sortTuple(toate_starile[i], toate_starile[j]))

        return stare_asemanatoare


    def minimize(self):

        AFD_minimizat = AFD(self.stari, self.Inputs, self.Starea_finala, self.Starea_initala, self.Tranzitiile)

        AFD_minimizat.stergeStariInaccesibile()
        matrice = AFD_minimizat.createMatrice()
        stare_asemanatoare = AFD_minimizat.GasesteStareAsemanatoare(matrice)

        for stare in stare_asemanatoare:
            for input in AFD_minimizat.Inputs:

                try:
                    del AFD_minimizat.Tranzitiile[(stare[1], input)]
                except:
                    pass
                try:
                    AFD_minimizat.stari.remove(stare[1])
                except:
                    pass

                try:
                    AFD_minimizat.Starea_finala.remove(stare[1])
                except:
                    pass
                if stare[1] == AFD_minimizat.Starea_initala:
                    AFD_minimizat.Starea_initala = stare[0]

        for key in AFD_minimizat.Tranzitiile.keys():
            for stare in stare_asemanatoare:
                if AFD_minimizat.Tranzitiile.get(key) == stare[1]:
                    AFD_minimizat.Tranzitiile[key] = stare[0]

        return AFD_minimizat


    def printDFA(self):

        print(",".join(sorted(self.stari)))
        print(",".join(sorted(self.Inputs)))
        print(",".join(sorted(self.Starea_finala)))
        print(self.Starea_initala)
        for item in sorted(self.Tranzitiile.items()):
            print("{},{}->{}".format(item[0][0], item[0][1], item[1]))



def FunctileDeTranzitie():

    tranzitii = dict()
    while True:
        try:
            functie = input()
            if functie == "\n" or functie == "":
                break
            functie = functie.split("->")
            tranzitii[tuple(functie[0].split(","))] = functie[1]
        except:
            break
    return tranzitii


def main():

    toate_stariile = set(input().split(","))
    inputs = set(input().split(","))
    Stari_finale = set(input().split(","))
    Stari_initiale = input()
    Tranzitiile = FunctileDeTranzitie()

    AFD_initial = AFD(toate_stariile, inputs, Stari_finale, Stari_initiale, Tranzitiile)

    AFD_minimizat = AFD_initial.minimize()
    AFD_minimizat.printDFA()


if __name__ == "__main__":
    main()

"""
Input :
1,2,3
a,b,c
2,3
1
1,a->2
1,b->1
1,c->1
2,a->1
2,b->1
2,c->2
3,a->1
3,b->3
3,c->2

Output:
1,2
a,b,c
2
1
1,a->2
1,b->1
1,c->1
2,a->1
2,b->1
2,c->2
"""