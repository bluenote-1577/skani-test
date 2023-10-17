import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import math
import numpy as np
import sys

aniu_D2 = "precomputed_results/D2_aniu.txt"
D5_aniu = "precomputed_results/D5_aniu.txt"
D5_skani = "../precomputed_results/D5_skani.txt"
skani_D2 = "precomputed_results/D2_skani.txt"
mash_D2 = "../precomputed_results/D2_mash.txt"
D5_mash = "../precomputed_results/D5_mash.txt"
fastani_gtdb = "../precomputed_results/gtdb_fastani.txt"
fastani_D2 = "../precomputed_results/D2_fastani.txt"
D5_fastani = "../precomputed_results/D5_fastani.txt"
contain_D2 = "./D2_contain.tsv"
ref_file_i = [aniu_D2]
other_files_i = [[contain_D2, skani_D2]]
#plt.style.use(['science'])

plt.rcParams.update({'font.size': 7})
plt.rcParams.update({'figure.autolayout': True})
plt.rcParams.update({'font.family':'arial'})
cm = 1/2.54  # centimeters in inches
fig = plt.figure(figsize=(18*cm, 6*cm))
d_max = 100000
n50_thresh = 0

#cmap = plt.rcParams['axes.prop_cycle'].by_key()['color']
cmap = sns.color_palette("muted")
line_colour = cmap[5]
for j in range(1):
    refs_to_ani = dict()
    ref_file = ref_file_i[j]
    other_files = other_files_i[j]
    for line in open(ref_file, 'r'):
        spl = line.split()
        if "skani" in ref_file or "aniu" in ref_file:
            other_ref = spl[0]
        elif "aai" in ref_file:
            other_ref = spl[2]
        else:
            other_ref = spl[1]
        other_ref = other_ref.split("/")[-1]
        other_ref = other_ref.split(".")[0]

        if "fastani" in ref_file or "anim" in ref_file:
            refs_to_ani[other_ref] = [float(spl[2])]
        elif "mash" in ref_file:
            refs_to_ani[other_ref] = [(1 - float(spl[2])) * 100]
        elif "aniu" in ref_file:
            refs_to_ani[other_ref] = [float(spl[3])]
        elif "aai" in ref_file:
            if spl[4] == "Label":
                continue
            refs_to_ani[other_ref] = [float(spl[4])]
        else:
            refs_to_ani[other_ref] = [float(spl[10])]

    for file in other_files:
        if "sourmash" in file:
            for line in open(file, 'r'):
                spl = line.split(',')
                other_ref = spl[2]
                other_ref = other_ref.split("/")[-1][0:-4]
                other_ref = other_ref.split(".")[0]
                if other_ref in refs_to_ani:
                    try:
                        ani = float(spl[7])
                        refs_to_ani[other_ref].append(ani * 100)
                    except ValueError:
                        x = 5

                continue
        else:
            for line in open(file, 'r'):
                spl = line.split()
                if "skani" in file or "aniu" in file:
                    other_ref = spl[0]
                    if "NaN" in line:
                        continue
                else:
                    other_ref = spl[0]
                other_ref = other_ref.split("/")[-1]
                other_ref = other_ref.split(".")[0]
                if other_ref in refs_to_ani:
                    try:
                        if "fastani" in file or "anim" in file:
                            refs_to_ani[other_ref].append(float(spl[2]))
                        elif "mash" in file:
                            refs_to_ani[other_ref].append((1 - float(spl[2])) * 100)
                        elif "aniu" in file:
                            refs_to_ani[other_ref].append(float(spl[3]))
                        elif "fastaai" in file:
                            refs_to_ani[other_ref].append(float(spl[-1]))
                        elif "contain" in file:
                            refs_to_ani[other_ref].append(float(spl[10]))
                        else:
                            refs_to_ani[other_ref].append(float(spl[2]))
                    except:
                        x = 5


    todel = []
    for key in refs_to_ani.keys():
        if len(refs_to_ani[key]) < len(other_files) + 1:
            todel.append(key)
    for key in todel:
        del refs_to_ani[key]

    points = np.array([x for x in refs_to_ani.values()])
    diff = 0
    worst = "na"
    sort_vec = []
    smallest_val = 100
    for (key,value) in refs_to_ani.items():
        for val in value:
            if val < smallest_val:
                smallest_val = val
        sort_vec.append((key,value))

    sort_vec  = sorted(sort_vec, key=lambda x: abs(x[1][0] - x[1][1]), reverse=True)
    oned_sort = np.array([x[1] for x in sort_vec])
    lr_results = []
    l1_results = []
    ax = plt.subplot(1,1,j+1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')


    #print(stats.spearmanr(oned_sort), 'spearman')
    for i in range(len(other_files)):
        #print(other_files[i])
        l1_results.append(np.linalg.norm([x[1][0] - x[1][i+1] for x in sort_vec], ord=1))
        lr_results.append(stats.linregress(oned_sort[:,0], oned_sort[:,i+1]))
        print(other_files[i], 'R: ', lr_results[-1].rvalue)
        print(other_files[i], 'MAE: ', l1_results[-1]/ len(oned_sort))
        #print(stats.spearmanr(oned_sort[:,0], oned_sort[:,i+1]), 'spearman')


    text1 = f"({lr_results[0].rvalue:.3f}, {(l1_results[0])/len(oned_sort):.3f})"
    #text2 = f"({lr_results[1].rvalue:.3f}, {(l1_results[1])/len(oned_sort):.3f})"
    #text3 = f"({lr_results[2].rvalue:.3f}, {(l1_results[2])/len(oned_sort):.3f})"
    
    #result_text = text1 + '\n' + text2 + '\n' + text3 
    #xloc = 0.72
    #yloc = 0.10
    #label_text = "Pearson R, MAE"
    #if j == 1:
    #    title = "B. fragilis genomes (n = 318, m= 1)"
    #    method_text = "FastANI\nMash\nskani"

    #    plt.text(xloc-0.07,yloc+0.2, label_text,transform=ax.transAxes)
    #    plt.text(xloc,yloc, result_text,transform=ax.transAxes)
    #    plt.text(xloc-0.25,yloc, method_text,transform=ax.transAxes)
    #elif j == 2:
    #    title = "Parks MAGs (n = 7901, m = 1)"
    #    method_text = "FastANI\nmash\nskani"

    #    plt.text(xloc-0.07,yloc+0.2, label_text,transform=ax.transAxes)
    #    plt.text(xloc,yloc, result_text,transform=ax.transAxes)
    #    plt.text(xloc-0.25,yloc, method_text,transform=ax.transAxes)
    #else:
    #    title = "B.anthracis genomes (n = 571, m = 1)"
    #    method_text = "FastANI\nMash\nskani"

    #    plt.text(xloc-0.07,yloc+0.2, label_text,transform=ax.transAxes)
    #    plt.text(xloc,yloc, result_text,transform=ax.transAxes)
    #    plt.text(xloc-0.25,yloc, method_text,transform=ax.transAxes)

    for i in range(len(other_files)):
        label = ""
        vals = f"Pearson R = {lr_results[i].rvalue:.3f}, L1 = {int(l1_results[i])}"
        vals = ""
        marker = 'o'
        c = cmap[0]
        if 'fastani' in other_files[i]:
            marker = 's'
            label = f"FastANI" + vals
            c = cmap[1]
        elif 'sourmash' in other_files[i]:
            marker = '^'
            label = f"sourmash AAI" + vals
            c = cmap[3]
        elif 'fastaai' in other_files[i]:
            marker = 'x'
            label = f"FastAAI" + vals
            c = cmap[4]
        elif 'mash' in other_files[i]:
            marker = 'D'
            label = f"mash" + vals
            c = cmap[2]
        elif 'skani' in other_files[i]:
            marker = 'o'
            if 'refseq' in other_files[i] or 'aai' in other_files[i]:
                label = f"skani AAI" + vals
            else:
                label = f"skani" + vals

        #plt.scatter(points[:,0], points[:,i+1], label = other_files[i], alpha = 0.75)
        if len(points) > d_max:
            ax.plot(points[:d_max,0], points[:d_max,i+1],  marker, label = label, fillstyle='none', alpha=1.0, ms = 5.0, c=c, mew=1.0)
        else:
            ax.plot(points[:,0], points[:,i+1], marker , label = label, fillstyle='none', alpha=1.0, ms = 5.0, c=c, mew=1.0)
        #plt.plot(points[:,0], points[:,i+1],  'o', label = other_files[i], alpha=0.5)
    if 'aniu' in ref_file:
        plt.xlabel("OrthoANIu ANI")
        plt.ylabel("Method ANI")
    else:
        plt.xlabel("EzAAI AAI")
        plt.ylabel("Method AAI")
    plt.legend(loc='upper left')
    plt.legend(frameon=False)
    ax.plot(range(int(smallest_val),101), range(int(smallest_val),101), c = line_colour)


plt.show()
