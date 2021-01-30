## Mapping
bwa mem -t 12 -M -R "@RG\tID:<sample prefix>\tLIB:$F\tPL:ILLUMINA\tSM:<sample prefix>" <reference genome> <R1> <R2> | samtools view -bS - > bwa/<mapping file>

## Map statistics
samtools flagstat bwa/<mapping file> -O tsv > bwa/stat/<map statistics>

## Coverage
samtools sort <mapping file>  <sorted mapping file>
samtools index <sorted mapping file>
samtools depth -a <sorted mapping file> -o <coverage table>
bedtools multicov -bams <sorted mapping files> -bed <genes coordinates> > <mean coverage for every genes>

## Family and functional annotation
pfam_scan.pl -fasta <protein fasta> -dir ./ -o <results>
makeblastdb -in <protein fasta A. thaliana> -dbtype prot
makeblastdb -in <protein fasta C. bursa-pastoris> -dbtype prot
blastp -query <protein fasta C. bursa-pastoris> faa -db <protein fasta A. thaliana> -out <results> -evalue 1E-5 -outfmt 6

## Genotyping
gatk --java-options "-Xmx4g" HaplotypeCaller \
   -R <reference genome> \
   -I <sorted mapping file> \
   -O <genotyping results> \
   -L <genes coordinates>

gatk --java-options "-Xmx4g" SelectVariants \
   -R <reference genome> \
   -V <genotyping results> \
   -O <low coverage sites> \
   --select "DP < 6"
vcftools --vcf <genotyping results> --remove-indels --max-alleles 2 --recode --recode-INFO-all --out <SNP>
vcftools --vcf <genotyping results> --keep-only-indels --max-alleles 2 --recode --recode-INFO-all --out <indels>
bcftools view -i 'DP>=6' <файл с SNP> > <SNP with normal coverage>
bcftools view -i 'DP>=6' <файл с инделями> > <Indels with normal coverage>

gatk --java-options "-Xmx4g" FastaAlternateReferenceMaker \
   -R <reference genome> \
   -V <SNP with normal coverage> \
   -O <consensus sequense>\
   --snp-mask <low coverage sites> \
   -L <genes coordinates>
   
   
## Fst
bgzip <SNP with normal coverage>
tabix <zipped SNP with normal coverage>
bcftools merge <zipped SNP with normal coverage> -O vcf -o <multi VCF>
populations -V <multi VCF> \
                    -M <population map> \
                    --fstats \
                    --smooth-fstats \
                    --bootstrap-fst 100 \
                    --plink \
                    -O ./
plink --file <.ped>--recode --out <another ped>

## Admixture
admixture -K3 <another ped>





