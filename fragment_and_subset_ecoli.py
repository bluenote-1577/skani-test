from fasta_reader import read_fasta, write_fasta
import numpy as np
from random import seed
from random import random
import os

lengths = snakemake.params.lengths;
subset_percents = snakemake.params.percents;
ecoli_file = snakemake.input[0]
it = snakemake.params.num_its
mut_rates = snakemake.params.mut_rates

def cycle_nucs(nuc):
    if nuc == "A":
        return "C"
    elif nuc == "C":
        return "G"
    elif nuc == "G":
        return "T"
    elif nuc == "T":
        return "A"

print(lengths, subset_percents, it)

#lengths = [1000,2000,4000,8000,16000,32000]
#ecoli_file = "./data/e.coli-K12.fasta"
#subset_percents = [0.4,0.5,0.6,0.7,0.8]
#it = 20
seed(1)
for mut_rate in mut_rates:
    for item in read_fasta(ecoli_file):
        for subset_percent in subset_percents:
            for i in range(len(lengths)):
                seq = item.sequence
                avg_len = lengths[i]
                os.makedirs(f"post_data/ecoli-mut-{mut_rate}-subset-{subset_percent}-fragment-{avg_len}",exist_ok=True)
                length_vec = []
                for j in range(it):
                    with write_fasta(f"post_data/ecoli-mut-{mut_rate}-subset-{subset_percent}-fragment-{avg_len}/{j}.fa") as file:
                        counter = 0
                        len_count = 0;
                        while True:
                            counter+=1
                            frag_len = int(np.random.exponential(scale = avg_len))
                            #frag_len = avg_len
                            len_count += frag_len
                            if random() < subset_percent:
                                length_vec.append(frag_len)
                                if frag_len == 0:
                                    continue
                                if len_count + frag_len >= len(seq):
                                    break
                                b = seq[len_count:len_count + frag_len]
                                new_seq = ''.join([cycle_nucs(_) if random() > mut_rate else _ for _ in b])
                                file.write_item(f"ctg{counter}", new_seq)

                sum_frag_len = sum(length_vec)
                length_vec.sort()
                running_sum = 0
                for l in length_vec:
                    if running_sum > sum_frag_len/2:
                        rat = l / avg_len
                        print(f"N50 is {l}, rat is {rat}")
                        break
                    running_sum += l


