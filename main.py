from gridmodel import GridModel

def main():

    width, height = 10, 10
    init_positive, init_negative = 40, 40

    model = GridModel(width, height, init_positive, init_negative)
    model.visualise()


if __name__ == "__main__":
    main()