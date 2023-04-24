import numpy as np

def parse_matrix(mat_file, cutoff = 0):
    fastani_add = 0.0
    count = 0
    dist_dict = dict()
    ref_vec = []
    dist_mat = []
    ani_cumulative = 0 
    ani_counts = 0
    labels = []
    for line in open(mat_file,'r'):
        if count == 0:
            if 'mash' in mat_file:
                length = int(line.rstrip())
            elif len(line.split('\t')) > 2:
                length = len(line.split('\t'))
                labels = line.split('\t')
            else:
                length = int(line.split('\t')[-1].rstrip())
            dist_mat = np.zeros((length,length))
        elif count == 0 and 'anim' in mat_file:
            length = len(line.split())
            dist_mat = np.zeros((length,length))
        if count != 0:
            spl = line.split()
            if 'sour' in mat_file:
                ref = labels[count-1].rstrip().split("/")[-1]
                endpoints = range(0,count-1)
            else:
                ref = spl[0]
                ref = ref.split("/")[-1]
                endpoints = range(1,count)
            if ".fa" not in ref:
                ref += ".fa"
            ref_vec.append(ref)
            for i in endpoints:
                try:
                    if "fastani" in mat_file:
                        ani = min(100,float(spl[i])+fastani_add)
                    elif "mash" in mat_file:
                        ani = (1 - float(spl[i])) * 100
                    else:
                        if float(spl[i]) <= 1:
                            ani = float(spl[i]) * 100
                        else:
                            ani = float(spl[i])
                    if 'sour' in mat_file:
                        dist_mat[count-1][i] = ani
                    else:
                        dist_mat[count-1][i-1] = ani
                    ani_cumulative += ani
                    ani_counts += 1
                except:
                    if 'sour' in mat_file:
                        dist_mat[count-1][i] = 0
                    else:
                        dist_mat[count-1][i-1] = 0

        count+= 1
    for i in range(len(ref_vec)):
        for j in range(i):
            dist_dict[(ref_vec[i],ref_vec[j])] = dist_mat[i][j]
#            dist_dict[(ref_vec[j],ref_vec[i])] = dist_mat[i][j]
    if ani_cumulative / ani_counts > cutoff:
        #print(ani_cumulative/ ani_counts)
        return dist_dict
    else:
        return dict()

def parse_dist_file(dist_file):
    dist_dict = dict()
    for line in open(dist_file, 'r'):
        if 'ANI' in line:
            continue
        spl = line.split()
        main_ref = spl[0]
        main_ref = main_ref.split("/")[-1]
        other_ref = spl[1]
        other_ref = other_ref.split("/")[-1]
        if "fast" in dist_file or "anim" in dist_file:
            dist_dict[(main_ref,other_ref)] = float(spl[2])
        elif "mash" in dist_file:
            dist_dict[(main_ref,other_ref)] = (1 - float(spl[2])) * 100
        elif "aniu" in dist_file:
            dist_dict[(main_ref,other_ref)] = float(spl[3])
        else:
            dist_dict[(main_ref,other_ref)] = float(spl[2]) 

    return dist_dict

def parse_skani_dist_file(dist_file):
    dist_dict = dict()
    for line in open(dist_file, 'r'):
        spl = line.split()
        main_ref = spl[0]
        main_ref = main_ref.split("/")[-1]
        other_ref = spl[1]
        other_ref = other_ref.split("/")[-1]
        if "ANI" in line:
            continue
        dist_dict[(main_ref,other_ref)] = [float(spl[2]), float(spl[3]), float(spl[4]), float(spl[-5]), float(spl[-4]), float(spl[-3]), float(spl[-2]), float(spl[-1])]
    return dist_dict


