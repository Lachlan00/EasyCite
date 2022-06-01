# Donwload citation
import pyperclip
import urllib.request
from urllib.error import HTTPError
import bibtexparser
from bibtexparser.bparser import BibTexParser
import os
import subprocess
from scidownl import *
import glob
from termcolor import colored, cprint
import sys
import re
# local
from config import directoryDict

# other config
doi_base_url = 'http://dx.doi.org/'
prompt_colour = 'blue'

# Update scihub links
print('\nUpdating SciHub links..')
bash_command = "scidownl domain.update"
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

# yes or no query
def yes_or_no(question):
    reply = str(input(colored(question+' (y/n): ', prompt_colour, attrs=['bold']))).lower().strip()
    if reply == 'y':
        return True
    if reply == 'n':
        return False
    else:
        return yes_or_no("Not a vaild response..")

# Setup directory
print(colored('\nWhich bibliogrpahy do you want to use?', prompt_colour, attrs=['bold']))
for i in range(0,len(directoryDict)):
    print(str(i+1)+'. '+list(directoryDict.keys())[i])
bib_no = int(input(colored('\nEnter value: ', prompt_colour, attrs=['bold'])).lower()) - 1
print(colored('\nUsing bibliogrpahy '+list(directoryDict.keys())[bib_no], prompt_colour, attrs=['bold']))
bib_output = list(directoryDict.values())[bib_no]['bib']
pdf_output = list(directoryDict.values())[bib_no]['pdf']

# Get citation data
while True:
    command = input(colored('\nPress Enter to get DOI from clipboard.. ', prompt_colour, attrs=['bold'])).lower()
    if command == 'exit' or command == 'q' or command == 'quit':
        print('\nClosing program..\n')
        sys.exit()
    doi = pyperclip.paste().upper()
    doi = re.sub(r'\s+', '', doi)
    doi = doi.replace('http://doi.org/'.upper(),'')
    doi = doi.replace('https://doi.org/'.upper(),'')
    print('Getting bib file for DOI: '+doi.lower())
    # get bib citation
    url = doi_base_url + doi
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/x-bibtex')
    try:
        with urllib.request.urlopen(req) as f:
            bibtex_str = f.read().decode()
        print('')
        print(bibtex_str)
        # parse to bib
        bibtex = bibtexparser.loads(bibtex_str)
        # make new cite key
        # get authors
        if 'author' in bibtex.entries[0]:
            auth_str = bibtex.entries[0]['author']
        elif 'editor' in bibtex.entries[0]:
            auth_str = bibtex.entries[0]['editor']
        else:
            print("\nNo author or editor present in bib file. Manual entry required!")
            continue
        # get primary author
        primary_auth = auth_str.split(" and ")[0]
        # get last name and first name
        name_parts = bibtexparser.customization.splitname(primary_auth)
        # get year
        pub_year = bibtex.entries[0]['year']
        # cite_key
        cite_key = name_parts['last'][0].capitalize()+':'+bibtex.entries[0]['year']
        file_key = name_parts['last'][0].capitalize()+'_'+bibtex.entries[0]['year']
        # clean keys of bad characters characters
        cite_key = ''.join(ch for ch in cite_key if ch.isalnum() or ch == ':')
        file_key = ''.join(ch for ch in file_key if ch.isalnum() or ch == '_')  
        # check if correct paper before continue
        if not (yes_or_no('\nPaper data correct?')):
            print('Download aborted..')
            continue
        # check if cite key already used and if so add letter suffix
        suffix = ''
        if os.path.isfile(bib_output+'/'+file_key+'.bib'):
            # make sure not the same paper
            with open(bib_output+'/'+file_key+'.bib') as fp:
                bib_prev = bibtexparser.load(fp)
            if 'doi' in bib_prev.entries[0]:    
                if bibtex.entries[0]['doi'].upper() == bib_prev.entries[0]['doi'].upper().replace(
                    'http://doi.org/'.upper(),'').replace('https://doi.org/'.upper(),''):
                    print('Error: Paper already exists in citation library!')
                    print('Download aborted..')
                    continue
            # manual check
            print('\nSimilar paper found in library:\ns')
            with open(bib_output+'/'+file_key+'.bib') as fp:
                bib_lines = ''.join(fp.readlines())
            print(bib_lines)
            if (yes_or_no('\nIs this the same paper?')):
                print('Download aborted..')
                continue
            # add suffix
            for code in range(ord('b'), ord('z') + 1): 
                letter = str(chr(code))
                if os.path.isfile(bib_output+'/'+file_key+letter+'.bib'):
                    continue
                else:
                    suffix = letter
                    break
        # sub back in new cite key
        bibtex.entries[0]['ID'] = cite_key+suffix
        # save the bib file
        print('\nSaving .bib file..')
        with open(bib_output+'/'+file_key+suffix+'.bib', 'w') as fp:
            bibtexparser.dump(bibtex, fp)

        if not (yes_or_no('\nTry to download PDF?')):
            continue

        print('\nDownloading PDF..')
        # Get the PDF
        scihub_download(doi, out=pdf_output+'/'+file_key+suffix)
        # move file from temp folder to main
        # OBSOLETE
        # print('Failed to download PDF..')
        # remove_file = glob.glob(pdf_output+'/'+file_key+suffix+'*.tmp')
        # if (len(remove_file) > 0):
        #     os.remove(remove_file[0])

    except HTTPError as e:
        if e.code == 404:
            print('\nError: DOI not found.')
        else:
            print('\nError: Service unavailable.')
