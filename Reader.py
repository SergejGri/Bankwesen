import os
import numpy as np
from datetime import date
from datetime import datetime
from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt


class Reader:
    def __init__(self, path, path_fin):
        self.path = path
        self.path_fin = path_fin
        self.df = None
        self.get_files()
        self.plot()

    def get_files(self):
        for p in os.listdir(self.path):
            if os.path.isfile(p) and p.endswith('.csv') or p.endswith('.CSV'):
                self.df = pd.read_csv(p, sep=";", encoding='cp1252')
                print(p)
                self.df['Buchungstag_YYYY'] = self.df['Buchungstag'].apply(lambda a: self._year_trafo(a, trafo=True))
                self.df['Valutadatum_YYYY'] = self.df['Valutadatum'].apply(lambda a: self._year_trafo(a, trafo=True))

    def create_dash(self):
        pass

    def db_key_word(self):
        pass

    def plot(self):
        delta = self._get_delta_t()
        self.df = self.df.iloc[:, ::-1]
        x = self.df['Buchungstag_YYYY'].columns
        y = self.df['Betrag']

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.plot(x, y)
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

    @staticmethod
    def _year_trafo(expr, trafo=False):
        if np.isnan(expr):
            pass
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