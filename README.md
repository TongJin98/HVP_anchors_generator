# Anchors Generator for Human Vaccines Project 

This python file reads in fasta file of V genes or J genes in T-cell
or B-cell to translate DNA genes to amino acids and then finding the index of
the last occurrence of cysteine in the V genes or the first occurence of
phenylalanine followed by glycine in J genes.

## Getting Started

Download the file anchors_generator.py and put it in the same directory as a folder with all sequence files (fata files).
Use command line 

```
python anchors_generator.py -i <full path of input file> -o <full path to output file>
```

## Built With

* [Biopython](https://biopython.org/) - Used to parse in the fasta files 


## Author

* **Tong Jin** 
