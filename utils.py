import docx2txt
import io
import os
import re
import pandas as pd

def extract_text_from_docx(doc_path):
    '''
    Helper function to extract plain text from .docx files

    :param doc_path: path to .docx file to be extracted
    :return: string of extracted text
    '''
    try:
        text = docx2txt.process(doc_path)
        return text
    except KeyError:
        return ''

def extract_text_from_doc(doc_path):
    '''
    Helper function to extract plain text from .doc files

    :param doc_path: path to .doc file to be extracted
    :return: string of extracted text
    '''
    try:
        try:
            from subprocess import DEVNULL, STDOUT, check_call, check_output
            from time import sleep
            check_call(["lowriter","--convert-to","docx",doc_path], stdout=DEVNULL, stderr=STDOUT)
            #opt=os.system("lowriter --convert-to docx "+ doc_path)
        except ImportError:
            return 'ERROR'
        cwd=os.getcwd()
        file_name=doc_path.split('/')[-1]
        file_name_docx='.'.join(file_name.split('.')[:-1])+'.docx'
        if not os.path.exists(file_name_docx):
            sleep(1)
        text = extract_text_from_docx(file_name_docx)
        return text
    except KeyError:
        return ''
       
def extract_text(file_path):
    '''
    Wrapper function to detect the file extension and call text
    extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    ext=file_path.split('.')[-1]
    if ext == 'docx':
        text = extract_text_from_docx(file_path)
    elif ext == 'doc':
        text = extract_text_from_doc(file_path)
    print(text)
    return text

def extract_name(nlp_text, matcher):
    '''
    Helper function to extract name from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param matcher: object of `spacy.matcher.Matcher`
    :return: string of full name
    '''
    pattern = [[{'POS': 'PROPN'}, {'POS': 'PROPN'}]]

    matcher.add('NAME', None, *pattern)

    matches = matcher(nlp_text)
    
    for _, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():
            return span.text
       
def extract_email(text):
    '''
    Helper function to extract email id from text

    :param text: plain text extracted from resume file
    '''
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None
    
def extract_mobile_number(text, custom_regex=None):
    '''
    Helper function to extract mobile number from text

    :param text: plain text extracted from resume file
    :return: string of extracted mobile numbers
    '''
    indian_mobile=r"\+?\d[\d -]{8,12}\d"
    if not custom_regex:
        phone = re.findall(re.compile(indian_mobile), text)
    else:
        phone = re.findall(re.compile(custom_regex), text)
    if phone:
        number = ''.join(phone[0])
        return number    

def extract_skills(nlp_text, noun_chunks, skills_file=None):
    '''
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    
    if not skills_file:
        data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv'))
    else:
        data = pd.read_csv(skills_file)
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams
    #for token in noun_chunks:
    #    token = token.text.lower().strip()
    #    if token in skills:
    #        skillset.append(token)
    #print(skillset)
    return skillset        

