import os
import sqlite3
from datetime import date
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt


class DB():
    def __init__(self):
        self.conn = sqlite3.connect('credit.db')
        self.c = self.conn.cursor()
        if not os.path.isfile('credit.db'):
            self.c.execute("""CREATE TABLE credit (
                    date TEXT,
                    value REAL
                )""")
            self.conn.commit()
            self.conn.close()




class Reader:
    def __init__(self, path, path_fin, mode=None):
        self.path = path
        self.path_fin = path_fin
        self.df = None
        self.mode = mode
        if self.mode is None:
            self.mode = 'MT940'
        self.file = None
        self.dates = []
        self.values = []

        self.check_files()


    def check_files(self):
        if self.mode == 'MT940':
            for p in os.listdir(self.path):
                if os.path.isfile(p) and p.endswith('.txt') or p.endswith('.TXT'):
                    with open(p, 'r') as f:
                        for line in f:
                            if ':20:STARTUMSE\n' in line:
                                f.close()
                                self.file = p
                                self.parse_line()
                                break
        else:
            for p in os.listdir(self.path):
                if os.path.isfile(p) and p.endswith('.csv') or p.endswith('.CSV'):
                    self.df = pd.read_csv(p, sep=";", encoding='cp1252')
                    print(p)
                    self.df['Buchungstag_YYYY'] = self.df['Buchungstag'].apply(lambda a: self._year_trafo(a, trafo=True))
                    #self.df['Valutadatum_YYYY'] = self.df['Valutadatum'].apply(lambda a: self._year_trafo(a, trafo=True))


    def feldnummern(self):
        Auftragsreferenz_Nr = ':20:'
        Bezugsreferenz = ':21:'
        Kontobezeichnung = ':25:'
        saldo_x = ':60x:'
        saldo_f = ':60F:'


    def parse_line(self):
        with open(self.file, 'r') as f:
            for line in f:
                if ':60F:' in line:
                    date_T= self._year_trafo(line.split('EUR')[0], trafo=True)
                    credit = line.split('EUR')[1]
                    credit = credit.replace(',', '.')
                    credit = float(credit)


                    self.dates.append(date_T)
                    self.values.append(credit)


    def field_number_MT940(self):
        pass


    def create_dash(self):
        pass

    def db_key_word(self):
        pass

    def plot(self):
        delta = self._get_delta_t()
        #self.df = self.df.iloc[:, ::-1]
        x = self.df['Buchungstag_YYYY']
        y = self.df['Betrag']


        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.plot(x, y)
        ax.set_xticklabels(x[::3], rotation=45)
        ax.set_xticks(x[::10])
        ax.set_title('Test')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value [\texteuro%1.0fB]')
        plt.show()

    def _get_delta_t(self):
        y0, m0, d0 = self._year_trafo(self.df['Buchungstag_YYYY'].min())
        y1, m1, d1 = self._year_trafo(self.df['Buchungstag_YYYY'].max())
        d0 = date(int(y0), int(m0), int(d0))
        d1 = date(int(y1), int(m1), int(d1))
        delta = d1 - d0
        return delta

    def _year_trafo(self, expr, trafo=False):
        if self.mode == 'MT940':
            expr = expr[-6:]
            day_ = expr[-2:]
            month_ = expr[2:4]
            year_ = expr[:2]
        else:
            year_ = expr.split('.')[2]
            month_ = expr.split('.')[1]
            day_ = expr.split('.')[0]
        if trafo:
            date_ = day_ + '.' + month_ + '.' + str(20) + year_
            return date_
        else:
            return year_, month_, day_


class PDFCreator:
    pass