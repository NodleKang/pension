from model.portfolio import ModelPortfolio

mp = ModelPortfolio('퇴직연금', '성장형')
mp.print_assets()

mp = ModelPortfolio('퇴직연금', '중립형')
mp.print_assets()

mp = ModelPortfolio('퇴직연금', '안정형')
mp.print_assets()

mp = ModelPortfolio('연금저축', '성장형')
mp.print_assets()

mp = ModelPortfolio('연금저축', '중립형')
mp.print_assets()

mp = ModelPortfolio('연금저축', '안정형')
mp.print_assets()
