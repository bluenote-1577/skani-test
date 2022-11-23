import numpy as np
from collections import defaultdict
import fastcluster as fc
import umap
import seaborn as sns
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(100000)
from scipy.cluster import hierarchy
import scipy
import sys
#sparse_mat = "./references/final_results/sgb_triangle_skani_s0.9_c200.matrix.sparse"
#sparse_mat = "./references/skani_res.matrix.sparse"
#sparse_mat = "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part2/2021/skani_res.sparse"
#sparse_mat = "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part2/2043/skani_res.sparse"
sparse_mat_skani_median = "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part2/2328/median.sparse"
sparse_mat_skani = "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part2/2328/skani_mat.sparse"
sparse_mat_mash = "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part2/2328/mash_tri.txt"
sparse_mat_fastani = "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part2/2328/fastani_list.txt"
sparse_mats = [sparse_mat_mash, sparse_mat_fastani, sparse_mat_skani,sparse_mat_skani_median ]
from sklearn.datasets import load_digits
from sklearn.manifold import MDS,TSNE,SpectralEmbedding
import hdbscan
import pandas as pd
cm = 1/2.54
plt.rcParams.update({'font.size': 7})
plt.rcParams.update({'figure.autolayout': True})
plt.rcParams.update({'font.family':'arial'})


for (ell,sparse_mat) in enumerate(sparse_mats):
    labels_ref = []
    labels_map = dict()
    labels_set = set()
    x = []
    y = []
    z = []
    import umap.plot

    af_cutoff = 0.50
    scale = 50
    mod = 1

    counter = 0
    for line in open(sparse_mat,'r'):
        counter += 1
        spl = line.split('\t')
        ref1 = spl[0]
        ref2 = spl[1]
        if hash(ref1) % mod != 0 or hash(ref2) % mod != 0:
            continue
        if ref1 == ref2:
            continue
        if 'mash' in sparse_mat:
            ani = 1 - float(spl[2])
        elif "skani" in sparse_mat or "median" in sparse_mat:
            if 'ANI' in line:
                continue
            ani = float(spl[2])
        elif "fastani" in sparse_mat:
            ani = float(spl[2])/100

        af = float(spl[3])
        if ref1 not in labels_set:
            labels_map[ref1] = len(labels_ref)
            labels_ref.append(ref1)
            labels_set.add(ref1)
        if ref2 not in labels_set:
            labels_map[ref2] = len(labels_ref)
            labels_ref.append(ref2)
            labels_set.add(ref2)
        if ani < 0.90:
            continue
        else:
            #new_ani = 1 * np.exp(scale*(1 - ani))/scale
            new_ani = 1 - ani
            #print(new_ani,ani)
            x.append(labels_map[ref1])
            y.append(labels_map[ref2])
            x.append(labels_map[ref2])
            y.append(labels_map[ref1])
            z.append(new_ani)
            z.append(new_ani)

    print(len(labels_set))
    mat = np.ones((len(labels_set),len(labels_set))) * 1.00
    mat[x,y] = z
    np.fill_diagonal(mat,0)

    condensed = scipy.spatial.distance.squareform(mat)
    cmap = sns.cm.rocket_r
    Z = fc.linkage(condensed, 'average')
    labels = hierarchy.fcluster(Z, t=0.02, criterion='distance')
    cl = [(i,x) for (i,x) in enumerate(labels)]
    c_dict = defaultdict(list);
    for (i,x) in cl:
        c_dict[x].append((labels_ref[i], i))
    for thing in c_dict:
        print(len(c_dict[thing]))
        for line in c_dict[thing]:
            print(line[0])
    cg = sns.clustermap(mat, row_linkage = Z, col_linkage = Z, figsize=(5.5*cm, 5.5*cm), vmax = 0.03, vmin = 0.00, cbar_pos=None, dendrogram_ratio = 0.1, cmap = cmap)
    cg.tick_params(bottom=False, right=False)
    ax = cg.ax_heatmap
    ax.set(xticklabels=[])
    ax.set(yticklabels=[])
    if ell == 0:
        ax.set_title("Mash", fontsize = 7)
        plt.savefig("./figures/2328_mash.pdf")
    elif ell == 1:
        ax.set_title("FastANI", fontsize = 7)
        plt.savefig("./figures/2328_fastani.pdf")
    elif ell == 2:
        ax.set_title("skani", fontsize = 7)
        plt.savefig("./figures/2328_skani.pdf")
    elif ell == 3:
        ax.set_title("skani median", fontsize = 7)
        plt.savefig("./figures/2328_skani_median.pdf")
    plt.show()
#
exit()

mat = np.exp(scale * mat) / scale
#mat = scipy.sparse.csr_matrix((z, (x, y)), shape=(len(labels_set),len(labels_set)))
#print(scipy.sparse.csgraph.connected_components(mat))
#print(mat)

#embedding = TSNE(n_components=2, metric = 'precomputed', perplexity = 1)
hover_data = pd.DataFrame({'ref':labels_ref,
                           'label':fc})
dense = mat
embedding = umap.UMAP( metric = 'precomputed').fit(dense)

labels = fc
print(labels)
p = umap.plot.points(embedding)
#p.get_legend().remove()
plt.show()
#umap.plot.output_file('./output_test.html')
#p = umap.plot.interactive(embedding, labels=fc, hover_data=hover_data, point_size=2)
#p.get_legend().remove()
#umap.plot.show(p)


#cl = embedding.transform(dense)

#labels = hdbscan.HDBSCAN(
#    min_samples=1,
#    min_cluster_size=30,
#).fit_predict(cl)
#embedding = MDS(n_components=2, dissimilarity = 'precomputed')
#X_transformed = embedding.fit_transform(mat.toarray())
#X_transformed = embedding.fit_transform(mat.toarray())
#X_transformed.shape
#print(labels)
# in row_dict we store actual meanings of rows, in my case it's russian words
#clusters = {}
#n = 0
#for item in labels:
#    if item in clusters:
#        clusters[item].append(labels_ref[n])
#    else:
#        clusters[item] = [labels_ref[n]]
#    n +=1
#
#for item in clusters:
#    print("Cluster ", item)
#    for i in clusters[item]:
#        print(i)
#ax = umap.plot.points(embedding,labels=fc)
#ax.get_legend().remove()
#plt.show()

#plt.scatter(X_transformed[:,0], X_transformed[:,1])
#plt.show()
#

