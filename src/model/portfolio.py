from decimal import Decimal

class Asset:
    VALID_ASSET_TYPES = {'주식', '채권', '혼합', '현금', '대체투자'}
    VALID_MARKET_TYPES = {'신흥국', '선진국', '혼합', '원자재', '현금성자산'}
    VALID_HEDGE_INDICATORS = {'H', 'UH'}

    def __init__(self, asset_type, market_type, country, hedge_indicator, etf_code, etf_name):
        if asset_type not in self.VALID_ASSET_TYPES:
            raise ValueError(f"Invalid asset type. Allowed types: {', '.join(self.VALID_ASSET_TYPES)}")
        if market_type not in self.VALID_MARKET_TYPES:
            raise ValueError(f"Invalid market type. Allowed types: {', '.join(self.VALID_MARKET_TYPES)}")
        if hedge_indicator not in self.VALID_HEDGE_INDICATORS:
            raise ValueError(f"Invalid hedge indicator. Allowed types: {', '.join(self.VALID_HEDGE_INDICATORS)}")
        self.asset_type = asset_type
        self.market_type = market_type
        self.country = country
        self.hedge_indicator = hedge_indicator
        self.etf_code = etf_code
        self.etf_name = etf_name

    def set_weight(self, weight):
        self.weight = Decimal(str(weight))

class ModelPortfolio:
    
    VALID_PENSION_TYPE = {'퇴직연금', '연금저축'}
    VALID_PORTFOLIO_TYPE = {'성장형', '중립형', '안정형'}

    def __init__(self, pension_type, portfolio_type):
        if pension_type not in self.VALID_PENSION_TYPE:
            raise ValueError(f"Invalid pension type. Allowed types: {', '.join(self.VALID_PENSION_TYPE)}")
        if portfolio_type not in self.VALID_PORTFOLIO_TYPE:
            raise ValueError(f"Invalid portfolio type. Allowed types: {', '.join(self.VALID_PORTFOLIO_TYPE)}")

        self.pension_type = pension_type
        self.portfolio_type = portfolio_type
        self.assets = []

        if pension_type == '퇴직연금':
            self.__add_asset(Asset('주식', '선진국', '미국', 'UH', '379800', 'KODEX 미국 S&P500TR'))
            self.__add_asset(Asset('주식', '신흥국', '한국', 'UH', '294400', 'KOSEF 200TR'))
            self.__add_asset(Asset('주식', '선진국', '일본', 'UH', '241180', 'TIGER 일본니케이225'))
            self.__add_asset(Asset('주식', '신흥국', '베트남', 'UH', '245710', 'ACE 베트남VN30(합성)'))
            self.__add_asset(Asset('주식', '신흥국', '중국', 'UH', '283580', 'KODEX 차이나 CSI300'))
            self.__add_asset(Asset('주식', '신흥국', '인도', 'UH', '453810', 'KODEX 인도 Nifty50'))
            self.__add_asset(Asset('대체투자', '원자재', '금', 'UH', '411060', 'ACE KRX 금현물'))
            self.__add_asset(Asset('채권', '선진국', '미국', 'UH', '308620', 'KODEX 미국채 10년선물'))
            self.__add_asset(Asset('채권', '선진국', '미국', 'H', '453850', 'ACE 미국30년 국채액태브(H)'))
            self.__add_asset(Asset('채권', '신흥국', '한국', 'UH', '385560', 'KBSTAR KIS국고채 30년 Enhanced'))
            self.__add_asset(Asset('현금', '현금성자산', '한국', 'UH', '357870', 'TIGER CD금리투자KIS(합성)'))
            self.__add_asset(Asset('현금', '현금성자산', '미국', 'UH', '329750', 'TIGER 미국달러단기채권액티브'))

            if portfolio_type == '성장형':
                self.__set_asset_weight('379800', 0.24)
                self.__set_asset_weight('294400', 0.08)
                self.__set_asset_weight('241180', 0.03)
                self.__set_asset_weight('245710', 0.02)
                self.__set_asset_weight('283580', 0.03)
                self.__set_asset_weight('453810', 0.08)
                self.__set_asset_weight('411060', 0.19)
                self.__set_asset_weight('308620', 0.07)
                self.__set_asset_weight('453850', 0.07)
                self.__set_asset_weight('385560', 0.14)
                self.__set_asset_weight('357870', 0.025)
                self.__set_asset_weight('329750', 0.025)
            elif portfolio_type == '중립형':
                self.__set_asset_weight('379800', 0.2)
                self.__set_asset_weight('294400', 0.06)
                self.__set_asset_weight('241180', 0.02)
                self.__set_asset_weight('245710', 0.02)
                self.__set_asset_weight('283580', 0.03)
                self.__set_asset_weight('453810', 0.07)
                self.__set_asset_weight('411060', 0.16)
                self.__set_asset_weight('308620', 0.06)
                self.__set_asset_weight('453850', 0.06)
                self.__set_asset_weight('385560', 0.12)
                self.__set_asset_weight('357870', 0.1)
                self.__set_asset_weight('329750', 0.1)
            elif portfolio_type == '안정형':
                self.__set_asset_weight('379800', 0.15)
                self.__set_asset_weight('294400', 0.05)
                self.__set_asset_weight('241180', 0.02)
                self.__set_asset_weight('245710', 0.02)
                self.__set_asset_weight('283580', 0.01)
                self.__set_asset_weight('453810', 0.05)
                self.__set_asset_weight('411060', 0.12)
                self.__set_asset_weight('308620', 0.045)
                self.__set_asset_weight('453850', 0.045)
                self.__set_asset_weight('385560', 0.09)
                self.__set_asset_weight('357870', 0.2)
                self.__set_asset_weight('329750', 0.2)

        elif pension_type == '연금저축':

            self.__add_asset(Asset('주식', '선진국', '미국', 'UH', '379800', 'KODEX 미국 S&P500TR'))
            self.__add_asset(Asset('주식', '신흥국', '한국', 'UH', 'fund-vip', 'VIP한국형가치투자증권자투자신탁(C-P2e)'))
            self.__add_asset(Asset('주식', '선진국', '일본', 'UH', '241180', 'TIGER 일본니케이225'))
            self.__add_asset(Asset('주식', '신흥국', '베트남', 'UH', '245710', 'ACE 베트남VN30(합성)'))
            self.__add_asset(Asset('주식', '신흥국', '중국', 'UH', '283580', 'KODEX 차이나 CSI300'))
            self.__add_asset(Asset('주식', '신흥국', '인도', 'UH', '453810', 'KODEX 인도 Nifty50'))
            self.__add_asset(Asset('대체투자', '원자재', '금', 'UH', '411060', 'ACE KRX 금현물'))
            self.__add_asset(Asset('혼합', '혼합', '미국,한국', 'UH', '284430', 'KODEX 200미국채혼합'))
            self.__add_asset(Asset('채권', '선진국', '미국', 'H', '453850', 'ACE 미국30년 국채액태브(H)'))
            self.__add_asset(Asset('채권', '신흥국', '한국', 'UH', '385560', 'KBSTAR KIS국고채 30년 Enhanced'))
            self.__add_asset(Asset('현금', '현금성자산', '한국', 'UH', '455890', 'KBSTAR 머니마켓액티브'))

            if portfolio_type == '성장형':
                self.__set_asset_weight('379800', 0.24)
                self.__set_asset_weight('fund-vip', 0.035)
                self.__set_asset_weight('241180', 0.03)
                self.__set_asset_weight('245710', 0.02)
                self.__set_asset_weight('283580', 0.03)
                self.__set_asset_weight('453810', 0.08)
                self.__set_asset_weight('411060', 0.19)
                self.__set_asset_weight('284430', 0.115)
                self.__set_asset_weight('453850', 0.07)
                self.__set_asset_weight('385560', 0.14)
                self.__set_asset_weight('455890', 0.05)
            elif portfolio_type == '중립형':
                self.__set_asset_weight('379800', 0.2)
                self.__set_asset_weight('fund-vip', 0.02)
                self.__set_asset_weight('241180', 0.02)
                self.__set_asset_weight('245710', 0.02)
                self.__set_asset_weight('283580', 0.03)
                self.__set_asset_weight('453810', 0.07)
                self.__set_asset_weight('411060', 0.16)
                self.__set_asset_weight('284430', 0.1)
                self.__set_asset_weight('453850', 0.06)
                self.__set_asset_weight('385560', 0.12)
                self.__set_asset_weight('455890', 0.2)
            elif portfolio_type == '안정형':
                self.__set_asset_weight('379800', 0.15)
                self.__set_asset_weight('fund-vip', 0.02)
                self.__set_asset_weight('241180', 0.02)
                self.__set_asset_weight('245710', 0.02)
                self.__set_asset_weight('283580', 0.01)
                self.__set_asset_weight('453810', 0.05)
                self.__set_asset_weight('411060', 0.12)
                self.__set_asset_weight('284430', 0.075)
                self.__set_asset_weight('453850', 0.045)
                self.__set_asset_weight('385560', 0.09)
                self.__set_asset_weight('455890', 0.4)

    def __add_asset(self, asset):
        if not isinstance(asset, Asset):
            raise TypeError("Only Asset objects can be added.")
        self.assets.append(asset)

    def __set_asset_weight(self, etf_code, weight):

        for asset in self.assets:
            if asset.etf_code == etf_code:
                asset.set_weight(weight)
                break
        else:
            raise ValueError(f"No asset found with ETF code {etf_code}")

    def print_assets(self):
        if not self.assets:
            print("No assets in the portfolio.")
            return

        print(f"[{self.pension_type} {self.portfolio_type}]")
        print()

        header = f"{'Asset Type':<15} {'Market Type':<15} {'Country':<15} {'Hedge':<7} {'ETF Code':<10} {'ETF Name':<30} {'Weight (%)':>10}"
        print(header)
        print("-" * len(header))

        total_weight = Decimal('0')
        for asset in self.assets:
            weight_percentage = asset.weight * Decimal('100')
            print(
                f"{asset.asset_type:<15} {asset.market_type:<15} {asset.country:<15} {asset.hedge_indicator:<7} {asset.etf_code:<10} {asset.etf_name:<30} {weight_percentage:.3f}".rjust(
                    10))
            total_weight += asset.weight

        print("-" * len(header))
        total_weight_percentage = total_weight * Decimal('100')
        print(f"{'Total Portfolio Weight:':<103} {total_weight_percentage:.3f}%")
        print()
