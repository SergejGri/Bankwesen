import Reader as rd


def main():
    path_ = r''
    path_fin = r''
    csv_reader = rd.Reader(path_,path_fin)

    csv_reader.plot()


if __name__ == "__main__":
    main()
