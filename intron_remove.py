import glob
from Bio import AlignIO
import pandas as pd
import os
fasta = glob.glob(path+ directory+"*.fasta")
scaff_names=pd.read_csv(path+"scaf_names_gene_names.txt", sep="\t", names = ['coord', 'gene'])
exons=pd.read_csv(path+"Capsella_bursa_pastoris.gff", sep="\t", names = ['contig','version', 'cds', 'begin',
'end', 'V5', "V6", 'V7', 'gene'])
exons = exons[exons.cds != 'gene']
for i in range(0, len(fasta)):
  try:
    alignment = AlignIO.read(open(fasta[i]), "fasta")
    gene = "Gene="+fasta[i].split("/")[-1][:-6]+';'
    gene_mark = exons.query("gene == @gene")
    gene_mark = gene_mark.reset_index(drop = True)
    f = open(path+ directory+'New/'+fasta[i].split("/")[-1][:-6]+"_new.fna", "w")
    for j in range(0,(len(alignment))):
      f = open(path+ directory+'New/'+fasta[i].split("/")[-1][:-6]+"_new.fna", "a")
      f.write("\n"+">"+alignment[j].id+"\n")
      if gene_mark.shape[0] == 1:
        end = int((gene_mark.end[0]-gene_mark.begin[0]))
        f.write(str(alignment[j].seq[0:end+1]))
      else:
        end = int((gene_mark.end[0]-gene_mark.begin[0]))
        f.write(str(alignment[j].seq[0:end+1]))
        for g in range(1,gene_mark.shape[0]):
          intron_length = (gene_mark.begin[g]-gene_mark.end[g-1])
          length_last = int((gene_mark.end[g-1]-gene_mark.begin[g-1]))
          end_last = int((gene_mark.end[g-1]-gene_mark.begin[0]))
          begin_next = intron_length+end_last
          length = (gene_mark.end[g]-gene_mark.begin[g])
          end_next = begin_next+length+1
          f.write(str(alignment[j].seq[begin_next:end_next]))
  except ValueError:
    print("file " + fasta[i] + " ok")
arr = os.listdir(path + directory+'New/')
for j in range(0, len(arr)):
 try:
    alignment = AlignIO.read(open(path + directory+'New/' + arr[j]), "fasta")
    record = alignment[0]
    if record.seq[0:3] == "ATG":
        print("good file " + arr[j])
    else:
        f = open(path + directory+'New/' + arr[j], "w")
        for i in range(0,(len(alignment))):
        f = open(path + directory+'New/' + arr[j], "a")
        f.write(">"+alignment[i].id+"\n")
        f.write(str(alignment[i].seq.reverse_complement()+'\n'))
        f.close()
  except ValueError:
     print("file " + arr[j] + " doesn't exist")
