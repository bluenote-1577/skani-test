mut_rates = [1.0]
percents = [0.40,0.50,0.60,0.70,0.80,0.90]
average_lengths = [2000, 4000, 8000, 16000, 32000, 64000]
num_its = 20
THREADS = 20
percents_str = [str(x) for x in percents]
lengths_str = [str(x) for x in average_lengths]
mut_rates_str = [str(x) for x in mut_rates]

rule all:
    input:

#Get the checkm file for each folder in Pasolli et al. (2019) with between 25 and 50 genomes. 
#Requires checkm. A precomputed file exists in the precomputed_files/ folder. 
rule checkm_folders_less_50_files:
    input:
        "references/SGB_genome_fastas_part1/",
        "references/SGB_genome_fastas_part2/",
        "references/SGB_genome_fastas_part3/",
        "references/SGB_genome_fastas_part4/",
        "references/SGB_genome_fastas_part5/"
    output:
        "references/SGB_genome_fastas_part1/25-50/",
        "references/SGB_genome_fastas_part2/25-50/",
        "references/SGB_genome_fastas_part3/25-50/",
        "references/SGB_genome_fastas_part4/25-50/",
        "references/SGB_genome_fastas_part5/25-50/"
    run: 
        import glob
        for inp in input:
            folders = glob.glob(inp + "/*")
            print(folders)
            for folder in folders:
                print(folder)
                fastas = glob.glob(folder + "/*.fa")
                print(fastas)
                if len(fastas) == 0:
                    continue
                if len(fastas) > 25 and len(fastas) < 50:
                    shell(f"checkm lineage_wf {folder} {folder}/checkm_out -x fa --pplacer_threads 7 -t 30 -r --tab_table >> results/25-50-checkm.txt")
                    shell(f"gstawk {folder}/*.fa >> results/25-50-gstawk.txt")

#Calculate ANI for all methods for folders with between 25 and 50 genomes. 
#Requires sourmash, mash, fastani, skani, and pyani to be in PATH. 
rule ani_folders_25_to_50_files:
    input:
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part1/",
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part2/",
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part3/",
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part4/",
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part5/"
    output:
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part1/25-50/",
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part2/25-50/",
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part3/25-50/",
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part4/25-50/",
        "/home/jshaw/scratch/2022_sketched_distance/references/SGB_genome_fastas_part5/25-50/"
    run:
        import glob
        for i in range(len(input)):
            folders = glob.glob(input[i] + "/*")
            print(folders)
            shell(f"mkdir -p {output}")
            for folder in folders:
                print(folder)
                fastas = glob.glob(folder + "/*.fa")
                print(fastas)
                if len(fastas) > 25 and len(fastas) < 50:
                    num = folder.split('/')[-1]
                    skani_out = output[i] + "/skani_" + num
                    skani_out_rob = output[i] + "/skani-robust_" + num
                    mash_out = output[i] + "/mash_" + num
                    fastani_out = output[i] + "/fastani_" + num
                    sourmash_out = output[i] + "/sour_" + num
                    sourmash_out_normal = output[i] + "/sour-normal_" + num
                    #skani 
                    shell(f"skani triangle {folder}/*.fa -o {skani_out} -t 20")
                    shell(f"skani triangle {folder}/*.fa --robust -o {skani_out_rob} -t 20")
                    #Mash
                    shell(f"mash triangle {folder}/*.fa -p 20 > {mash_out}")
                    shell(f"ls {folder}/*.fa > l.txt")
                    #fastani
                    shell(f"fastANI --rl l.txt --ql l.txt --matrix -o {fastani_out} -t 40")
                    #sourmash
                    shell(f"sourmash sketch dna {folder}/*.fa --output-dir {folder}")
                    shell(f"sourmash compare {folder}/*.sig --csv {sourmash_out} --ani --max-containment")
                    shell(f"sourmash sketch dna {folder}/*.fa --output-dir {folder}")
                    shell(f"sourmash compare {folder}/*.sig --csv {sourmash_out_normal} --ani")
                    shell(f"rm {folder}/*.sig")
                    #anim
                    out_name = output[0] + "/anim_" + num
                    shell(f"average_nucleotide_identity.py -m ANIm -i {folder} -o {out_name} --workers 40");

#Fragment and subset an e.coli genome. 
rule fragment_and_subset_random_genome:
    input:
        "data/e.coli-K12.fasta",
    output:
        expand("post_data/ecoli-mut-{mut_rate}-subset-{percent}-fragment-{length}/{it}.fa",mut_rate=mut_rates, percent=percents,length=average_lengths, it=range(num_its))
    params:
        mut_rates = mut_rates,
        num_its = num_its,
        lengths = average_lengths,
        percents = percents,
    script:
        "fragment_and_subset_ecoli.py"



