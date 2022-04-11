import matplotlib.pyplot as plt
import re,time
raw_text = '''
AC	21012
AG	222111
AT	30033
CA	32212
CG	23333
CT	32210
GA	302312
GC	32332
GT	23332
TA	32322
TC	22032
TG	23232
'''

corected_text = '''
AC	3322
AG	32223
AT	3322
CA	12332
CG	3123
CT	13333
GA	33323
GC	3333
GT	3222
TA	3232
TC	1203
TG	3312
'''

names = ['AC','CA','AG','GA','AT','TA','CG','GC','CT','TC','GT','TG']

raw_dic = {}
for line in re.split('\n',raw_text):
    if line.strip():
        record = re.split('\t',line.strip())
        raw_dic[record[0]] = int(record[1])

corected_dic = {}
for line in re.split('\n',corected_text):
    if line.strip():
        record = re.split('\t',line.strip())
        corected_dic[record[0]] = int(record[1])

values_raw_count = sum(list(raw_dic.values()))
values_corected_count = sum(list(corected_dic.values()))
# print(values_raw_count)
# print(values_corected_count)
values_raw_num = [raw_dic[x]/values_raw_count for x in names]
values_corected_num = [corected_dic[x]/values_corected_count for x in names]
print(values_raw_num)
print(values_corected_num)
fig, axs = plt.subplots(1,1)
#figsize=(9, 3), sharey=True

axs.scatter(names, values_raw_num,label="x",color='#c9d9d2')
axs.scatter(names, values_corected_num,label="y",color='#e84d64')

fig.suptitle('Precent Plotting')
plot_handle, plot_labels = axs.get_legend_handles_labels()
print(plot_labels)
axs.legend(plot_handle, plot_labels)
plt.show()
#plt.savefig(fname='xxx.png', dpi=300)
