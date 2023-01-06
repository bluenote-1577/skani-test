rm -r *_skani_sketch
threads=50
bintime_var=/bin/time
mkdir refseq_sourmash_sketches
rm ./e.coli-K12.fasta.sig

#gtdb
$bintime_var -v -o times/skani_gtdb_sketch.time ./skani sketch -o gtdb_skani_sketch -l gtdb_all.txt -t$threads
$bintime_var -v -o times/skani_gtdb_query.time ./skani search -d gtdb_skani_sketch data/e.coli-K12.fasta -o results/gtdb_skani.txt -t$threads
$bintime_var -v -o times/mash_gtdb_sketch.time mash sketch -o gtdb_mash_sketch -l gtdb_all.txt -p $threads 
$bintime_var -v -o times/mash_gtdb_dist.time mash dist gtdb_mash_sketch.msh data/e.coli-K12.fasta -p $threads > results/gtdb_mash.txt

#d3
$bintime_var -v -o times/skani_D3_sketch.time ./skani sketch -o D3_skani_sketch ./references/D3/* -t$threads
$bintime_var -v -o times/skani_D3_query.time ./skani search -d D3_skani_sketch data/e.coli-K12.fasta -o ./results/D3_skani.txt -t$threads
$bintime_var -v -o times/mash_D3_sketch.time mash sketch -o D3_mash_sketch ./references/D3/*.fna -p $threads 
$bintime_var -v -o times/mash_D3_dist.time mash dist D3_mash_sketch.msh data/e.coli-K12.fasta -p $threads > results/D3_mash.txt
$bintime_var -v -o times/fastani_D3.time fastANI --rl ./d3_l.txt -q data/e.coli-K12.fasta -t $threads -o results/D3_fastani.txt  2> times/fastani_D3_log.txt

#refseq
$bintime_var -v -o times/skani_refseq_sketch.time ./skani sketch -o refseq_skani_sketch ./references/refseq/* -t$threads
$bintime_var -v -o times/skani_refseq_query.time ./skani triangle ./refseq_skani_sketch/* -o ./results/refseq_skani-variety.txt -t$threads
$bintime_var -v -o times/mash_refseq_sketch.time mash sketch -o refseq_mash_sketch ./references/refseq/*.fna -p $threads 
$bintime_var -v -o times/mash_refseq_dist.time mash triangle refseq_mash_sketch.msh -E -p $threads > results/refseq_mash-variety.txt
$bintime_var -v -o times/fastani_refseq.time fastANI --rl ./refseq.txt --ql ./refseq.txt -t $threads -o results/refseq_fastani-variety.txt  2> times/fastani_refseq_log.txt


#seq_aai
#$bintime_var -v -o times/skani_refseq_sketch.time ./skani sketch -o refseq_skani_sketch references/refseq_all/* -t$threads -a
#$bintime_var -v -o times/skani_refseq_query.time ./skani search -d refseq_skani_sketch data/e.coli-K12.fasta -o ./results/refseq_skani_aai-k12.txt -t$threads
#rm -r fastaai_refseq_all
#$bintime_var -v -o times/fastaai_refseq_sketch.time fastaai build_db -g references/refseq_all/ -o fastaai_refseq_all --threads 20
#$bintime_var -v -o times/fastaai_refseq_dist.time fastaai simple_query -g data/e.coli-K12.fasta --target fastaai_refseq_all/database/FastAAI_database.sqlite.db -o tt
#mv ./tt/results/e_coli_K12_results.txt results/refseq_fastaai-k12.txt
#$bintime_var -v -o times/sourmash_refseq_sketch.time parallel -j $threads -a ./sourmash_sketch_cmd.txt 
#sourmash sketch translate data/e.coli-K12.fasta
#$bintime_var -v -o times/sourmash_refseq_search.time sourmash search ./e.coli-K12.fasta.sig ./refseq_sourmash_sketches/*.sig --max-containment -t 0.0 -n0 -o results/refseq_sourmash_aai-k12.txt
#
#


