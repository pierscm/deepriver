import sqlite3
import matplotlib.pyplot as plt
import numpy as np


conn = sqlite3.connect('playerdata.db')
cur = conn.cursor()

cur.execute("select stack from data where name = 'ourbot1'")
ourbot1_results = cur.fetchall()

cur.execute("select stack from data where name = 'ourbot2'")
ourbot2_results = cur.fetchall()

cur.execute("select stack from data where name = 'ourbot3'")
ourbot3_results = cur.fetchall()

cur.execute("select stack from data where name = 'ourbot4'")
ourbot4_results = cur.fetchall()

print(ourbot1_results)
ourbots_avg = []
for x in range(len(ourbot1_results)):
    ourbots_avg.append(0)
    ourbots_avg[x] += ourbot1_results[x][0]
    ourbots_avg[x] += ourbot2_results[x][0]
    ourbots_avg[x] += ourbot3_results[x][0]
    ourbots_avg[x] += ourbot4_results[x][0]
    ourbots_avg[x] = ourbots_avg[x] - 40000
    ourbots_avg[x] = ourbots_avg[x]/4

cur.execute("select stack from data where name = 'LooseConservative'")
lc_results = cur.fetchall()

cur.execute("select stack from data where name = 'LooseAgggressive'")
la_results = cur.fetchall()

cur.execute("select stack from data where name = 'TightAggressive'")
ta_results = cur.fetchall()

cur.execute("select stack from data where name = 'TightConservative'")
tc_results = cur.fetchall()

dummy_average = []
for x in range(len(ourbot1_results)):
    dummy_average.append(0)
    dummy_average[x] += lc_results[x][0]
    dummy_average[x] += ta_results[x][0]
    dummy_average[x] += la_results[x][0]
    dummy_average[x] += tc_results[x][0]
    dummy_average[x] = dummy_average[x] - 40000
    dummy_average[x] = dummy_average[x]/4





dummy_average = (lc_results+la_results+ta_results+tc_results)

plt.axes().get_xaxis().set_visible(True)
plt.plot(ourbots_avg)
#plt.plot(dummy_average)
#plt.plot(ourbot1_results)
#plt.plot(ourbot2_results)
#plt.plot(ourbot3_results)
#plt.plot(ourbot4_results)
#plt.plot(lc_results)
#plt.plot(la_results)
#plt.plot(ta_results)
#plt.plot(tc_results)
plt.legend(["ourbots_average", "dummy_average", "ourbot1", "Ourbot2", "Ourbot3", "Ourbot4", "LooseConservative", "LooseAgggressive", "TightAggressive", "TightConservative"], loc = 'upper left')

plt.show()

cur.close()
conn.close()