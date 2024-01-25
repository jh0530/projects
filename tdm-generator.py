#!/usr/bin/env python3
import sys
import os

# MAIN METHOD
def main():
    ''' Establish the input and output paths '''
    input_path = sys.argv[1]
    output_dir = sys.argv[2]

    ''' Create the output directory '''
    os.makedirs(output_dir)

    '''get the list of filenames and print them to the new 
    text file in output dir '''
    make_lofiles(input_path, output_dir)

    ''' take the input path and print out the content of that path's files
    into the new output directory's file '''
    read_and_print_contents(input_path, output_dir)
    
    ''' take the list of files and all their terms and make a 
    list of lists (each of these sublists containing a 'term + #' string '''
    terms_of_files_list = get_terms_for_matrix(input_path)

    ''' take the list of lists described above and make it into a dictionary 
    of dictionaries '''
    dict_of_dicts = termlist_list_to_dict(terms_of_files_list)

    ''' take the dictionary described above and makes the matrix ''' 
    get_matrix(dict_of_dicts, output_dir)

# SEND FILENAMES TO SORTED_DOCS.TXT
def make_lofiles(file_path, output_dir):

    # get the actual list of filenames
    lofiles = os.listdir(file_path)
    lofiles = sorted(lofiles)

    # write the list to sorted_documents
    with open(os.path.join(output_dir, "sorted_documents.txt") , 'w') as f:
        for file in lofiles:
            f.write(file + '\n')

# READ AND PRINT CONTENT (TERMS)
def read_and_print_contents(file_path, output_dir):
    ''' reads input file ("sorted_documents.txt") and prints 
    them to output file ("sorted_terms.txt") '''
    
    with open(os.path.join(output_dir, "sorted_documents.txt"), 'r') as f:
        sorted_filenames = f.read().splitlines()
    
    # initialize the set of terms
    all_terms = set()

    for filename in sorted_filenames:
        with open(os.path.join(file_path, filename), 'r') as input_file:
            content = input_file.read().split("\n")
            for line in content:
            # Remove numbers and split terms
                term = line.split(" ")[0].strip()
            # add the term to the set of terms
                if term:   
                    all_terms.add(term)

    # Sort and print the terms to the output file
    all_terms = sorted(all_terms)
    with open(os.path.join(output_dir, "sorted_terms.txt"), 'w') as output_file:
        for term in all_terms:
            output_file.write(term + '\n')

# GET THE TERMS THAT WILL GO INTO THE MATRIX 
def get_terms_for_matrix(file_path):
    # Reads and sorts the cumulative frequencies for all the terms 
    # in all the files in the given directory, makes them into a dictionary
    list_of_files_terms = []

    files = os.listdir(file_path)
    files = sorted(files)
    
    for file in files:
        list_for_file = []
        with open(os.path.join(file_path, file), 'r') as f:
            term = f.read().splitlines() 
            list_for_file.extend(term)
            list_of_files_terms.append(list_for_file)
    return list_of_files_terms

# GET THE LIST OF TERMS AND THEIR NUMBER AND USE THIS TO POPULATE A DICTIONARY
def termlist_list_to_dict(list_of_lists_of_terms):
    term_dict = {}
    for i, term_list in enumerate(list_of_lists_of_terms):
        term_dict[i] = {}
        for term_entry in term_list:
            term, count = term_entry.split()
            term_dict[i][term] = int(count)
    return term_dict

# TAKE THE DICTIONARY OF DICTIONARIES AND MAKE A MATRIX OUT OF IT, THEN...
# PRINT THIS TO THE OUTPUT FILE 
def get_matrix(dictionary_of_dictionaries, output_directory):
    # create a set  to store the unique terms
    unique_terms = set()

    # collect all unique terms from the sub-dictionaries 
    for sub_dict in dictionary_of_dictionaries.values():
        unique_terms.update(sub_dict.keys())

    # Sort the unique terms
    sorted_terms = sorted(unique_terms)

    # output_file = "td_matrix.txt"
    with open(os.path.join(output_directory, "td_matrix.txt"), 'w') as f:
        # Write the dimensions of the matrix to the file
        f.write(f"{len(sorted_terms)} {len(dictionary_of_dictionaries)}\n")

        # Populate the matrix with the term counts and write them to the file
        for i, term in enumerate(sorted_terms):
            row = []
            for j, sub_dict in dictionary_of_dictionaries.items():
                row.append(str(sub_dict.get(term, 0))) # returns zero if "get" is unsuccessful
            f.write(" ".join(row) + '\n')


if __name__ == "__main__":
    main()