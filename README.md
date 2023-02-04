# skani-test

Benchmarking results and scripts for skani.

### Requirements:
1. [conda](https://www.anaconda.com/)

```sh
git clone https://github.com/bluenote-1577/skani-test
cd skani-test
conda env create -f env.yml
conda activate bioinf
```

This will load a conda environment with all binaries available in PATH. 

## Jupyter notebook plots

All plots are stored in jupyter notebooks. 

```
#you may need to install jupyter notebook 
cd notebooks
jupyter notebook
```

Make sure that your current working directory is `skani-test/notebooks`.

All notebooks can be re-run to generate the plots. Certain options can be changed in each notebook, e.g. N50 thresholds in the ANI plots, wall-clock
vs cpu-clock. All results are pre-supplied; for re-benchmarking, see below. For the ani-divergence-learn.ipynb and ANI_violin_supp_diff.ipynb notebooks, you will have to run `gzip -d` all files in the supp_results folder.

## Re-benchmarking

### Quickly testing skani

To quickly test skani for creating a clustered heatmap of ~200 genomes, do the following commands:

```
# make sure you're in the skani-test directory 
./skani triangle 2328/* -t 20 > skani_mat.txt
python scripts/clustermap_triangle.py skani_mat.txt
```

This will take < 10 seconds and you should see skani's distance matrix as a cluster heatmap appear. 

### Re-benchmarking all methods for database search

The data sets used for database search can get quite large, so are not included here by default. To get them, do the following:

1. `mkdir references` 
2. run the following commands to generate the 3 main data sets:
```
# gtdb database
wget https://data.gtdb.ecogenomic.org/releases/release207/207.0/genomic_files_reps/gtdb_genomes_reps_r207.tar.gz
tar -xf gtdb_genomes_reps_r207.tar.gz
mv gtdb_genomes_reps_r207 references

# e.coli genomes
wget http://enve-omics.ce.gatech.edu/data/public_fastani/D3.tar.gz
tar -xf D3.tar.gz
mv D3 references

# refseq representative complete/chromosome genomes
ncbi-genome-download --assembly-levels complete,chromosome --refseq-categories representative --formats fasta bacteria,viral,archaea,fungi
mkdir references/refseq
cp refseq/*/GCF_*/*.fna.gz references/refseq
```

Then edit the time_results.sh file to modify the # of threads used, and where the /bin/time binary is located (usually /usr/bin/time or /bin/time). To regenerate
all benchmarking files, run 
```
./time_results.sh
```

NOTE: Make sure to change the number of threads in `time_results.sh` (default: 20).

### Re-benchmarking all methods for the distance matrix plot

The 195 genomes in the species level bin used for the distance matrix from Pasolli et al. is included in this repository.

To re-generate the distance matrices and timing benchmarks, just run 
```
./time_2328_results.sh
```

and change the number of threads (default: 1).

### Re-benchmarking Pasolli et al. cophenetic correlation, etc

To reproduce the cophenetic correlation results and the ANI vs contamination/incompleteness regression plot, you need to download all genomes from Pasolli et al. 
located at http://segatalab.cibio.unitn.it/data/Pasolli_et_al.html. Specifically the Part 1 - 5 files. These files are about 350 GB in total. 

After downloading these files, extract them and place them in `references`. Then run

`snakemake -c40 -s Snakefile.smk -R ani_folders_25_to_50_files`

This uses 40 threads and will take a day or two. 

## Re-benchmarking Soil, Ocean eukaryotic, archaea MAGs.

We describe how to obtain the datasets below. 

### Ocean eukaryotic MAGs

We use eukaryotic ocean MAGs from two studies. 

"Eukaryotic genomes from a global metagenomic dataset illuminate trophic modes and biogeography of ocean plankton" - Alexander et al (2021). Also known as the TOPAZ MAGs. Available at: https://osf.io/gm564/.

"Functional repertoire convergence of distantly related eukaryotic plankton lineages abundant in the sunlit ocean" - Delmont et al (2022). MAGs are available at https://www.genoscope.cns.fr/tara/localdata/data/SMAGs-v1/SMAGs_contigs_individual.fna.tar.gz.

### OceanDNA archaea MAGs 

We use archaea MAGs from the study "The OceanDNA MAG catalog contains over 50,000 prokaryotic genomes originated from various marine environments" by Nishimura and Yoshizawa (2022). We use the non-representative archaea mags available here: https://doi.org/10.6084/m9.figshare.c.5564844.v1. The archaea mags are labelled OceanDNA-a*.fa.

### Soil MAGs 

We use soil MAGs from the study "Consistent Metagenome-Derived Metrics Verify and Delineate Bacterial Species Boundaries" by Olm et al (2020). The soil MAGs are avilable here: https://figshare.com/collections/Genomes_for_consistent_metagenome-derived_metrics_verify_and_define_bacterial_species_boundaries/4508162/1

### Regeneration

We run the exact same commands as in the Pasolli et al dataset on these 4 sets of MAGs (two eukaryotic sets) to generate the files in the supp_results folder. See the snakemake file for reference. 
