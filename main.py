import Reader as rd



def main():
    path_ = r'C:\Users\Rechenfuchs\Desktop\Projekte\Bankwesen'
    path_fin = r'C:\Users\Rechenfuchs\Desktop\Projekte\Bankwesen\processed_files'
    csv_reader = rd.Reader(path_,path_fin)

    csv_reader.plot()



if __name__ == "__main__":
    main()