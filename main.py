from gridmodel import GridModel

def main():
    width, height = 10, 10
    init_positive, init_negative, init_neutral = 40, 40, 5

    model = GridModel(width, height, init_positive, init_negative, init_neutral)
    model.visualise()


if __name__ == "__main__":
    main()