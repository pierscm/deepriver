import sqlite3
import matplotlib.pyplot as plt
import numpy as np


conn = sqlite3.connect('test.db')
cur = conn.cursor()

cur.execute("select stack from data where name = 'ourbot1'")
ourbot1_results = cur.fetchall()

cur.execute("select stack from data where name = 'LooseConservative'")
lc_results = cur.fetchall()

cur.execute("select stack from data where name = 'LooseAgggressive'")
la_results = cur.fetchall()

cur.execute("select stack from data where name = 'TightAggressive'")
ta_results = cur.fetchall()

cur.execute("select stack from data where name = 'TightConservative'")
tc_results = cur.fetchall()

plt.axes().get_xaxis().set_visible(False)
plt.plot(ourbot1_results)
plt.plot(lc_results)
plt.plot(la_results)
plt.plot(ta_results)
plt.plot(tc_results)
plt.legend(["Ourbot", "LooseConservative", "LooseAgggressive", "TightAggressive", "TightConservative"], loc = 'upper left')

plt.show()

cur.close()
conn.close()