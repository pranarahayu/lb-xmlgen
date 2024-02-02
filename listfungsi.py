import os
import pandas as pd
import glob
from datetime import date
import numpy as np

def datacleaner(data):
  test = data.copy()
  test = test[['Min', 'Num', 'Act Name', 'Team', 'Action']].reset_index()

  test['Action'] = test['Action'].str.replace('passing', 'pass')
  test['Mins'] = test['Min'].str.split(':').str[0]
  test['Mins_1'] = test['Mins'].str.split('+').str[0]
  test['Mins_1'] = test['Mins_1'].astype(int)
  test['Mins_2'] = test['Mins'].str.split('+').str[1]
  test['Mins_2'] = test['Mins_2'].fillna(0)
  test['Mins_2'] = test['Mins_2'].astype(int)
  test['Mins'] = test['Mins_1']+test['Mins_2']
  test['Secs'] = test['Min'].str.split(':').str[1]
  test['Secs'] = test['Secs'].astype(int)
  test['start'] = (((test['Mins']*60)+test['Secs'])-5)-60
  test['end'] = (((test['Mins']*60)+test['Secs'])+5)+60
  test = test[['index', 'start', 'end', 'Act Name', 'Team', 'Action']]

  test['code'] = test['Action']
  test['label.text'] = test['code']
  test['label.group'] = 'Event'

  test = test[['index', 'start', 'end', 'code', 'label.text', 'label.group']]
  test['label.text'] = test['label.text'].str.title()

  test1 = data.copy()
  test1 = test1[[ 'Num', 'Act Name', 'Team']].reset_index()
  test1['label.text'] = ''
  for i in range(len(test1)):
    test1['label.text'][i] = str(test1['Num'][i])+'-'+test1['Act Name'][i]
  test1['label.group'] = 'Player'
  test1 = test1[['index', 'label.text', 'label.group']]

  test2 = data.copy()
  test2 = test2[[ 'Num', 'Act Name', 'Team']].reset_index()
  test2['label.text'] = test2['Team']
  test2['label.group'] = 'Team'
  test2 = test2[['index', 'label.text', 'label.group']]

  testdata = pd.merge(test, test1, on='index', how='left')
  testdata = pd.merge(testdata, test2, on='index', how='left')

  testdata = testdata.drop(['index'], axis=1).sort_values(['start', 'end']).reset_index(drop=True).reset_index()
  testdata.rename(columns = {'index':'ID'}, inplace = True)

  testdata = testdata[['ID', 'code', 'start', 'end', 'label.group_x', 'label.text_x', 'label.group_y', 'label.text_y', 'label.group', 'label.text']]

  return testdata
