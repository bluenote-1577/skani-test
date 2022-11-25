# skani-test

Benchmarking results and scripts for skani.

### Requirements:
1. conda

```sh
git clone htttps://github.com/bluenote-1577/skani-test
cd skani-test
conda env create -f env.yml
conda activate bioinf
```

This will load a conda environment with all binaries available in PATH. 

## Plotting scripts

See the `notebooks` folder for jupyter notebooks used to generate plots for the paper. All results are precomputed and stored in this repository.

All notebooks can be re-run to generate the plots. Certain options can be changed in each notebook, e.g. N50 thresholds in the ANI plots, wall-clock
vs cpu-clock. 

## Re-benchmarking

### Re-benchmarking for database search

The data sets used for database search can get quite large, so are not included here by default. To get them, do the following:

1. `mkdir references` 
2. run the following commands to generate the 3 main data sets:
```
# gtdb database
wget https://data.ace.uq.edu.au/public/gtdb/data/releases/release207/207.0/genomic_files_reps/gtdb_genomes_reps_r207.tar.gz
tar -xf gtdb_genomes_reps_r207.tar.gz
mv gtdb_genomes_reps_r207 references

# e.coli genomes
wget http://enve-omics.ce.gatech.edu/data/public_fastani/D3.tar.gz
tar -xf D3.tar.gz
mv D3 references

# refseq representative complete/chromosome genomes
ncbi-genome-download --assembly-levels complete,chromosome --refseq-categories representative --formats fasta bacteria,viral,archaea,fungi
mkdir refseq_all
cp refseq/*/GCF_*/*.fna.gz references/refseq_all
```

Then edit the time_results.sh file to modify the # of threads used, and where the /bin/time binary is located (usually /usr/bin/time or /bin/time). To regenerate
all benchmarking files, run `./time_results.sh`. 

### Re-benchmarking distance matrix plot

The 195 genomes in the species level bin used for the distance matrix is included in this repository. 

To re-generate the distance matrices and timing benchmarks, just run `./time_2328_results.sh`.

### Re-benchmarking Pasolli et al. cophenetic correlation, etc

To reproduce the cophenetic correlation results and the ANI vs contamination/incompleteness regression plot, you need to download all genomes from Pasolli et al. 
located at http://segatalab.cibio.unitn.it/data/Pasolli_et_al.html. Specifically the Part 1 - 5 files. 

After downloading these files, extract them and place them in `references`. Then run

`snakemake -c40 -s Snakefile.smk -R ani_folders_25_to_50_files`

This uses 40 threads and will take a day or two. 
