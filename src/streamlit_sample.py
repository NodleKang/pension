import streamlit as st
import pandas as pd
import plotly.express as px

################ Model ################
class Model:

   def __init__(self):
      self.df = pd.DataFrame(px.data.gapminder())
      self.ylist = [int(i) for i in self.df['year'].unique()]
      self.yearStart = self.ylist[0]
      self.yearEnd = self.ylist[-1]
      self.yearStep = self.ylist[1]-self.ylist[0]

   def chart(self,year):
      return px.scatter(self.df[self.df['year'] == year],
         x = 'lifeExp', y = 'gdpPercap',
         title = f'Year: {year}',
         color='continent',size='pop')

   header = 'Gapminder에서 가져온 세계적인 통계'

   description ='''
      GDP와 기대 수명이 어떻게 달라지는지 알아보세요.
      슬라이더를 움직여서 표시할 연도를 변경하세요.
   '''

   sliderCaption='연도를 선택하세요.'

####### View #######
def view(model):

    from streamlit_option_menu import option_menu
    with st.sidebar:
        choose = option_menu("강노들 자산관리",
                             options=["월말자산", "연금관리"],
                             menu_icon="list",)

    # menu_items = {
    #     "Home": "home",
    #     "월말자산": "month_end_assets",
    #     "연금현황": "pensions"
    # }
    # menu_selection = st.sidebar.selectbox("메뉴 선택", list(menu_items.keys()))

    # Header
    st.header(model.header)

    commentaryCol, spaceCol, chartCol = st.columns((2,1,6))

    # Description
    with commentaryCol:
        st.write(model.description)

    # Year Slider
    year = st.slider(model.sliderCaption,
                     model.yearStart, model.yearEnd,
                     model.yearStart, model.yearStep)

    # Chart
    with chartCol:
        st.plotly_chart(model.chart(year),
                        use_container_width=True)

####### Stert #######
view(Model())
