import streamlit as st
from data.data_loader import DataLoader
from data.data_processor import DataProcessor
from data.cache_manager import CacheManager
import yaml


def load_config(config_path: str) -> dict:
    config: dict

    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        raise Exception("Configuration file not found")
    except yaml.YAMLError:
        raise Exception("Error parsing the configuration file")

    return config

def main():

    # Streamlit 멀티페이지 앱 기능 활용
    # Streamlit 세션 상태에 data_processor가 없으면 데이터를 가져와서 저장
    if 'data_processor' not in st.session_state:
        config = load_config('C:/Workspace/pension/resources/config/config.yaml')

        cache_manager = CacheManager(config["cache"]["expiration_time"])
        data_loader = DataLoader(config["google_sheets"], config["worksheets"])
        data_processor = DataProcessor(data_loader, cache_manager)

        # 초기 데이터 로딩 및 캐싱
        data_processor.load_and_cache_data()

        st.session_state['data_processor'] = data_processor

    st.set_page_config(
        layout='wide',
        page_title="강노들 자산현황",
        page_icon="👋",
    )
    st.title("Welcome to Data Analysis App")
    st.write("Please select a page from the sidebar to start exploring the data.")

if __name__ == "__main__":
    main()
