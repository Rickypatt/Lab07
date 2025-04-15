from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getUmiditaMedia(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, avg(s.Umidita) as Umedia
                        from situazione s 
                        where month(`Data`) = %s
                        group BY s.Localita"""
            cursor.execute(query,(mese,))
            for row in cursor:
                result.append([row["Localita"], row["Umedia"]])

            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def get_situazioni_meta_mese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.Localita, s.Umidita, s.`Data` 
                        from situazione s 
                        where MONTH(s.Data) = %s and DAY(s.Data)<=15
                        order by s.Data ASC"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"], row["Data"], row["Umidita"]))

            cursor.close()
            cnx.close()
            return result



if __name__ == '__main__':
    dao = MeteoDao()
    print(dao.getUmiditaMedia(2))
    print(dao.get_situazioni_meta_mese(2))