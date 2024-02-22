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
  for i in range(len(test)):
    if (test['Action'][i] == 'goal') or (test['Action'][i] == 'own goal') or (test['Action'][i] == 'assist') or (test['Action'][i] == 'penalty goal') or (test['Action'][i] == 'penalty save') or (test['Action'][i] == 'conceding penalty') or (test['Action'][i] == 'penalty missed'):
      test['start'] = ((test['Mins']*60)+test['Secs'])-10
      test['end'] = ((test['Mins']*60)+test['Secs'])
    elif (test['Action'][i] == 'save') or (test['Action'][i] == 'yellow card') or (test['Action'][i] == 'red card') or (test['Action'][i] == 'miss big chance') or (test['Action'][i] == 'shoot blocked') or (test['Action'][i] == 'shoot on target') or (test['Action'][i] == 'shoot off target') or (test['Action'][i] == 'block'):
      test['start'] = ((test['Mins']*60)+test['Secs'])-7
      test['end'] = ((test['Mins']*60)+test['Secs'])+3
    elif (test['Action'][i] == 'free kick') or (test['Action'][i] == 'corner') or (test['Action'][i] == 'throw in') or (test['Action'][i] == 'goal kick'):
      test['start'] = ((test['Mins']*60)+test['Secs'])-3
      test['end'] = ((test['Mins']*60)+test['Secs'])+7
    else:
      test['start'] = ((test['Mins']*60)+test['Secs'])-5
      test['end'] = ((test['Mins']*60)+test['Secs'])+5
  test = test[['index', 'start', 'end', 'Act Name', 'Team', 'Action']]
  test['start'] = test['start']-55
  test['end'] = test['end']-55

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

  test3 = data.copy()
  test3 = test3[['Sub 1', 'Sub 2', 'Sub 3', 'Sub 4']].reset_index()
  test3 = test3.fillna('None')
  test3['label.text'] = test3['Sub 1'] + ' - ' + test3['Sub 2'] + ' - ' + test3['Sub 3'] + ' - ' + test3['Sub 4']
  test3['label.group'] = 'Comment'
  test3 = test3[['index', 'label.text', 'label.group']]

  testdata = pd.merge(test, test1, on='index', how='left', suffixes=('_1', '_2'))
  testdata = pd.merge(testdata, test2, on='index', how='left')
  testdata = pd.merge(testdata, test3, on='index', how='left')

  testdata = testdata[(testdata['label.text_1'] != 'Subs') & (testdata['label.text_1'] != 'Concede Goal') & (testdata['label.text_1'] != 'Cleansheet') & (testdata['label.text_1'] != 'Winning Goal') & (testdata['label.text_1'] != 'Create Chance')].reset_index(drop=True)

  testdata = testdata.drop(['index'], axis=1).sort_values(['start', 'end']).reset_index(drop=True).reset_index()
  testdata.rename(columns = {'index':'ID'}, inplace = True)

  testdata = testdata[['ID', 'code', 'start', 'end', 'label.group_1', 'label.text_1', 'label.group_2', 'label.text_2', 'label.group_x', 'label.text_x', 'label.group_y', 'label.text_y']]

  return testdata
