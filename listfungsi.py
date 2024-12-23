import os
import pandas as pd
import glob
from datetime import date
import numpy as np

def converter(text):
  test = text
  hh = int(test.split(":")[0])
  mm = int(test.split(":")[1])
  ss = int(test.split(":")[2])

  cvt = (hh*3600)+(mm*60)+(ss)

  return cvt

def res_data(data, datax):
  test = data.copy()
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

  test['code'] = test['Action']
  test['label.text'] = test['code']
  test['label.group'] = 'Event'

  test = test[['index', 'start', 'end', 'code', 'label.text', 'label.group']]
  test['label.text'] = test['label.text'].str.title()

  test1 = datax.copy()
  test1 = test1[[ 'Num', 'Act Name', 'Team']].reset_index()
  test1['label.text'] = ''
  for i in range(len(test1)):
    test1['label.text'][i] = str(test1['Num'][i])+'-'+test1['Act Name'][i]
  test1['label.group'] = 'Player'
  test1 = test1[['index', 'label.text', 'label.group']]

  test2 = datax.copy()
  test2 = test2[[ 'Num', 'Act Name', 'Team']].reset_index()
  test2['label.text'] = test2['Team']
  test2['label.group'] = 'Team'
  test2 = test2[['index', 'label.text', 'label.group']]

  test3 = datax.copy()
  test3 = test3[['Sub 1', 'Sub 2', 'Sub 3', 'Sub 4']].reset_index()
  test3 = test3.fillna('None')
  test3['label.text'] = test3['Sub 1'] + ' - ' + test3['Sub 2'] + ' - ' + test3['Sub 3'] + ' - ' + test3['Sub 4']
  test3['label.group'] = 'Comment'
  test3 = test3[['index', 'label.text', 'label.group']]

  temp = test.copy()

  test = pd.merge(temp, test1, on='index', how='left', suffixes=('_1', '_2'))
  test = pd.merge(test, test2, on='index', how='left')
  test = pd.merge(test, test3, on='index', how='left')

  test = test[(test['label.text_1'] != 'Subs') & (test['label.text_1'] != 'Concede Goal') & (test['label.text_1'] != 'Cleansheet') & (test['label.text_1'] != 'Winning Goal') & (test['label.text_1'] != 'Create Chance')].reset_index(drop=True)

  test = test.drop(['index'], axis=1).sort_values(['start', 'end']).reset_index(drop=True).reset_index()
  test.rename(columns = {'index':'ID'}, inplace = True)

  test = test[['ID', 'code', 'start', 'end', 'label.group_1', 'label.text_1', 'label.group_2', 'label.text_2', 'label.group_x', 'label.text_x', 'label.group_y', 'label.text_y']]

  return test

def cleandata(datax, tm, info):
  data = datax.copy()
  data = data[['Min', 'Num', 'Act Name', 'Team', 'Action']].reset_index()
  data = data[(data['Action']=='save') | (data['Action']=='penalty save') | (data['Action']=='goal') | (data['Action']=='penalty goal') | (data['Action']=='penalty missed') | (data['Action']=='own goal') | (data['Action']=='shoot on target') | (data['Action']=='shoot off target') | (data['Action']=='shoot blocked') | (data['Action']=='miss big chance') | (data['Action']=='key pass') | (data['Action']=='assist') | (data['Action']=='cross') | (data['Action']=='cross failed') | (data['Action']=='tackle') | (data['Action']=='intercept')].reset_index(drop=True)
  data['Mins'] = data['Min'].str.split(':').str[0]
  data['Mins_1'] = data['Mins'].str.split('+').str[0]
  data['Mins_1'] = data['Mins_1'].astype(int)
  data['Mins_2'] = data['Mins'].str.split('+').str[1]
  data['Mins_2'] = data['Mins_2'].fillna(0)
  data['Mins_2'] = data['Mins_2'].astype(int)
  data['Mins'] = data['Mins_1']+data['Mins_2']
  data['Secs'] = data['Min'].str.split(':').str[1]
  data['Secs'] = data['Secs'].astype(int)

  tempdata = data.reset_index(drop=True)
  fixdata = res_data(tempdata, datax)
  fixdata['start'] = fixdata['start']+tm
  fixdata['end'] = fixdata['end']+tm
  if (info=='Babak 2'):
    fixdata['start'] = fixdata['start']-1500
    #fixdata['start'] = fixdata['start']-2700
    fixdata['end'] = fixdata['end']-1500
    #fixdata['end'] = fixdata['end']-2700
  elif (info=='Babak 3'):
    fixdata['start'] = fixdata['start']-3000
    #fixdata['start'] = fixdata['start']-5400
    fixdata['end'] = fixdata['end']-3000
    #fixdata['end'] = fixdata['end']-5400
  elif (info=='Babak 4'):
    fixdata['start'] = fixdata['start']-4500
    #fixdata['start'] = fixdata['start']-6300
    fixdata['end'] = fixdata['end']-4500
    #fixdata['end'] = fixdata['end']-6300

  return fixdata
