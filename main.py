import sqlite3
import Reader as rd




def extend_db():
    pass

def main():
    path_ = r'C:\Users\Rechenfuchs\Desktop\Projekte\Bankwesen'
    path_fin_ = r'C:\Users\Rechenfuchs\Desktop\Projekte\Bankwesen\processed_files'

    db_reader = rd.DB()
    csv_reader = rd.Reader(path_, path_fin_, mode='MT940')
    pdf_creator = rd.PDFCreator()


    extend_db()

if __name__ == "__main__":
    main()