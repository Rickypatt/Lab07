import copy
from database.meteo_dao import MeteoDao

class Model:

    def __init__(self):
        self.n_soluzione = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []

    def getUmiditaMedia(self,mese):
        return MeteoDao().getUmiditaMedia(mese)

    def calcola_sequenza(self,mese):
        self.n_soluzione = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        situazioni = MeteoDao.get_situazioni_meta_mese(mese)
        self._ricorsione([],situazioni)
        return self.soluzione_ottima, self.costo_ottimo

    def trova_possibili_step(self, parziale,lista_situazioni):
        giorno = len(parziale)+1
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati

    def is_admissible(self,candidate,parziale):
        #vincolo sui 6 giorni:
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter >= 6:
            return False

        #vincolo sulla permanenza
        if len(parziale) == 0:
            return True

        if len(parziale) < 3:
            if candidate.localita != parziale[0].localita:
                return False

        else:
            if parziale[-3].localita != parziale[-2].localita or parziale[-3].localita != parziale[-1].localita or parziale[-2].localita != parziale[-1].localita:
                if parziale[-1].localita != candidate.localita:
                    return False
        #altrimenti ok
        return True

    def _calcola_costo(self,parziale):
        costo = 0
        #costo umidita
        for situazione in parziale:
            costo += situazione.umidita

        #costo cambio città
        for i in range(len(parziale)):
            #se i due giorni precedenti non sono stato nella stessa città pago 100
            if i >= 2 and (parziale[i-1].localita == parziale[i].localita or parziale[i-2].localita == parziale[i].localita):
                costo +=100
        return costo

    def _ricorsione(self,parziale,lista_situazioni):

        #condizione terminale
        if len(parziale) == 15:
            self.n_soluzione += 1
            costo = self._calcola_costo(parziale)
            if self.costo_ottimo == -1 or self.costo_ottimo > costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)

        #condizione ricorsiva
        else:
            #Cercare le città per il giorno che mi serve
            candidates = self.trova_possibili_step(parziale,lista_situazioni)
            #Provo ad aggiungere una di queste città e vado avanti
            for candidate in candidates:
                #verifica vincoli
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    self._ricorsione(parziale,lista_situazioni)
                    parziale.pop()


if __name__ == '__main__':
    m = Model()
    print(m.calcola_sequenza(2))