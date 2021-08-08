import Reader as rd


def main():
    path_ = r''
    path_fin_ = r''

    csv_reader = rd.Reader(path_, path_fin_, mode='MT940')
    pdf_creator = rd.PDFCreator()
    pdf_creator.create_pdf()


if __name__ == "__main__":
    main()
