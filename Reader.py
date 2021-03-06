import os
import sqlite3
from datetime import date
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('credit.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS credit (
                        date TEXT,
                        value REAL
                        )""")
        self.conn.commit()
        self.conn.close()

    def add_data(self, date, value):
        self.conn = sqlite3.connect('credit.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT date, value FROM credit WHERE date=? OR value=?", (date, value))

        duplicates = self.c.fetchone()

        if duplicates:
            print('ignoring duplicates')
        else:
            with self.conn:
                self.c.execute("INSERT INTO credit VALUES (?, ?)", (date, value))

    def get_data(self):
        self.conn = sqlite3.connect('credit.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT date, value FROM credit")
        rows = self.c.fetchall()
        date_list = [x[0] for x in rows]
        value_list = [x[1] for x in rows]
        self.c.close()
        return date_list, value_list


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
        self.db = DB()
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

    def parse_line(self):
        with open(self.file, 'r') as f:
            for line in f:
                if ':60F:' in line:
                    z, date_T= self._year_trafo(line.split('EUR')[0], trafo=True)
                    credit = line.split('EUR')[1]
                    credit = credit.replace(',', '.')
                    credit = int(z)*float(credit)
                    self.db.add_data(date=date_T, value=credit)

    def _year_trafo(self, expr, trafo=False):
        z = 1
        if self.mode == 'MT940':
            ex = expr[5]
            if ex == 'D':
                z = -1
            expr = expr[-6:]
            day_ = expr[-2:]
            month_ = expr[2:4]
            year_ = expr[:2]
        else:
            ex = expr[5]
            if ex == 'D':
                z = -1
            year_ = expr.split('.')[2]
            month_ = expr.split('.')[1]
            day_ = expr.split('.')[0]
        if trafo:
            date_ = day_ + '.' + month_ + '.' + str(20) + year_
            return z, date_
        else:
            return z, year_, month_, day_


class PDFCreator:
    def __init__(self):
        self.fig, self.ax = plt.subplots(nrows=1, ncols=1)
        #self.ax.set_title('Test')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Value [\texteuro%1.0fB]')
        self.db = DB()
        self.plot()

    def _get_delta_t(self):
        y0, m0, d0 = self._year_trafo(self.df['Buchungstag_YYYY'].min())
        y1, m1, d1 = self._year_trafo(self.df['Buchungstag_YYYY'].max())
        d0 = date(int(y0), int(m0), int(d0))
        d1 = date(int(y1), int(m1), int(d1))
        delta = d1 - d0
        return delta

    def plot(self):
        x, y = self.db.get_data()

        #x = self.df['Buchungstag_YYYY']
        #y = self.df['Betrag']

        self.ax.set_xticklabels(x[::], rotation=45)
        #self.fig, ax = plt.subplots(nrows=1, ncols=1)
        self.ax.plot(x, y)

        plt.show()

    '''
    def _get_delta_t(self):
        y0, m0, d0 = self._year_trafo(self.df['Buchungstag_YYYY'].min())
        y1, m1, d1 = self._year_trafo(self.df['Buchungstag_YYYY'].max())
        d0 = date(int(y0), int(m0), int(d0))
        d1 = date(int(y1), int(m1), int(d1))
        delta = d1 - d0
        return delta
    '''