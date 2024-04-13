from models.portfolio import ModelPortfolio


def main():

    mp = ModelPortfolio('퇴직연금', '성장형')

    mp = ModelPortfolio('퇴직연금', '중립형')

    mp = ModelPortfolio('퇴직연금', '안정형')

    mp = ModelPortfolio('연금저축', '성장형')

    mp = ModelPortfolio('연금저축', '중립형')

    mp = ModelPortfolio('연금저축', '안정형')


if __name__ == "__main__":
    main()
