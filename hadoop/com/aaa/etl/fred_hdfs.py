'''
Created on 2023. 11. 7.

@author: sehee
'''

import configparser
import os
from fredapi import fred
from pyarrow import fs
from com.aaa.etl.us_states import US_STATES
import time
from conda_libmamba_solver import state


class Fred2Hdfs(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        config = configparser.ConfigParser() # 설정파일 읽어오는 객체 생성
        path = 'C:\\Users\\권세희\\Desktop\\hadoop\\com\\aaa\\etl'
        
        os.chdir(path)
        
        config.read('resources/SystemConfig.ini') # 설정파일을 읽어와 객체 저장
        
        _api_key = config['FRED_CONFIG']['api_key']
        self._fred = fred(api_key=_api_key)
        self._hdfs = fs.HadoopFileSystem('localhost', 9000)
        
        self._list_state = [state.value for state in US_STATES]
    
    '''검색어를 입력하여 분석에 사용하게 될 데이터를 추출하는 함수'''
    def getFredDF(self, freq, state, str_search):
        str_search_text = str_search + state
        print(str_search_text)
        df_fred_col = self._fred.search(str_search_text)
        
        time.sleep(0.5)
        
        if df_fred_col is None:
            return None
        
        mask_df = (df_fred_col.title == str_search_text) & (df_fred_col.frequency_short == freq) & 
        (df_fred_col.seasonal_adjustment_short == 'NSA')
        
        df_fred_col = df_fred_col.loc[mask_df, :]
        df_fred_col['state'] = state
        
        if not df_fred_col.empty:
            df_etl_col = self._fred_col.to_frame(name='values')
            df_etl_col['realtime_start'] = df_fred_col.iloc[0].realtime_start
            df_etl_col['realtime_end'] = df_fred_col.iloc[0].realtime_end
            df_etl_col['state'] = df_fred_col.iloc[0].state
            df_etl_col['id'] = df_fred_col.iloc[0].id
            df_etl_col['title'] = df_fred_col.iloc[0].title.replace(',' , '_')
            df_etl_col['frequency_short'] = df_fred_col.iloc[0].frequency_short
            df_etl_col['units_short'] = df_fred_col.iloc[0].units_short
            df_etl_col['seasonal_adjustment_short'] = df_fred_col.iloc[0].seasonal_adjustment_short
            
            return df_etl_col
        
        
    