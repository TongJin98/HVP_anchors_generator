'''anchors_generator.py

This python file runs to read in fasta file of V genes or J genes in T-cell
or B-cell to translate DNA genes to amino acids and then finding the index of
the last occurrence of cysteine in the V genes or the first occurence of
phenylalanine followed by glycine in J genes.
'''
import argparse
import sys
from Bio import SeqIO
import csv
import math
import re
import xlwt
import os
import parse_genes
import write_files



def main(args):

    # Read in command line arguments to variables
    input_dir = args.i
    output_dir = args.o

    if output_dir[-1] is not "/":
        output_dir += "/"

    try:
        os.makedirs(output_dir)
    except:
        pass

    #run with python excelScript.py
    book = xlwt.Workbook()

    for filename in sorted(os.listdir(input_dir), key=lambda x: x.split('.')[0][-1]):
        infile = os.path.join(input_dir, filename)
        filename = filename.split('.')[-2]
        sheet = book.add_sheet(filename)
        output_filename = f"{output_dir}{filename}"

        #if 'J-REGION' in [a for a in open(infile)][0]:
        first_line = [a for a in open(infile)][0]
        if re.split(string=first_line, pattern=r"[0-9\-]+\*")[0][-1] == 'J':
            v_or_j = 'J'
        elif re.split(string=first_line, pattern=r"[0-9\-]+\*")[0][-1] == 'V':
            v_or_j = 'V'
        #TODO: add parse D genes
        else:
            continue
            #v_or_j = args.t.upper()

        if v_or_j == "V" :
            output_data = parse_genes.parse_v_genes(infile)
            write_files.generate_extra_nucleotides_file_Vgene(output_filename,
                              output_data['gene_names'],
                              output_data['extras'],
                              output_data['amino_acids'],
                              output_data['accessions'],
                              output_data['functionalitys'],
                              output_data['partials'])
            write_files.write_excel_sheet_v(sheet, output_data)
        else:
            output_data = parse_genes.parse_j_genes(infile)
            write_files.generate_extra_nucleotides_file_Jgene(output_filename,
                                  output_data['gene_names'],
                                  output_data['extras'],
                                  output_data['amino_acids'],
                                  output_data['accessions'],
                                  output_data['functionalitys'],
                                  output_data['partials'])
            write_files.write_excel_sheet_j(sheet, output_data)
        write_files.generate_error_file(output_filename,
                    output_data['error_results'],
                    output_data['sequence'],
                    output_data['error_indexs'])
        write_files.generate_anchor_file(output_filename,
                     output_data['results'],
                     output_data['indexs'])

    excel_file_name = output_dir + "contributions.xls"
    book.save(excel_file_name)



if __name__ == '__main__':

    # Set commend line arugments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help = 'path to the input file')
    parser.add_argument('-o', help = 'path to the output file')
    args = parser.parse_args()

    if (args.i == None or args.o == None):
        print("Command line arugment error\nCorrect Usage:\npython anchors_generator.py -i <full path of input file> -o <full path to output file>")
        sys.exit()
    main(args)
