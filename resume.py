import spacy 
import utils
from spacy.matcher import Matcher
from collections import Counter
import pandas as pd
import os
class res_class():
    
    def __init__(self,file_name):
        self.file_name=file_name
        self.nlp = spacy.load("en_core_web_sm")

    def extract_text(self):
        """
            extract_text function extracts the text from
            doc or docx file by calling extract_text from
            utils module(utils file)
            at the end each paragraph is stored as element
            of list
        """
        self.text=utils.extract_text(self.file_name)
        self.temp_list=self.text.split('\n')
        len_temp_list=len(self.temp_list)
        for i in range(len_temp_list-1,-1,-1):
            self.temp_list[i]=' '.join(self.temp_list[i].split()).lower()
            if len(self.temp_list[i])<2:
                   self.temp_list.pop(i)        
    
    
        
    def div_sec(self):
        """
            div_sec function divide the text extracted
            from document into different sections or
            we can say under different titles if encountered
            as paragraph.
            titles are stored in titles.csv file.
            final output is dictionary having title as key
            and the text under them as value
        """
        self.info={"introduction":['']}
        flag="introduction"
        #fields=["summary","employment","education","skills","awards","achievements","roles and responsibilities","experiences","experience","education qualification","work experience","technical skills","programming skills","key skills","projects"]
        data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'titles.csv'))
        fields = list(data.columns.values)
        for x in self.temp_list:
            if len(x)>1:
                if(x in fields):
                    flag=x
                else:
                    try:
                        self.info[flag].append(x)
                    except:
                        self.info[flag]=[]
                        self.info[flag].append(x)           
    
  
    def sec_based_extraction(self):
        """
            sec_based_extraction is a function to
            extract name, email, phone, skills from
            text under each section.
            all these informations are extracted using
            functions from utils module
            final output is dictionary with title as key
            and extracted details as value
        """
        matcher = Matcher(self.nlp.vocab)
        self.first_info={}
        for key,value in self.info.items():
            #print(' '.join(value))
            __text=' '.join(value)
            __nlp=self.nlp(__text)
            name = utils.extract_name(__nlp, matcher)
            email = utils.extract_email(__text)
            mobile = utils.extract_mobile_number(__text)   
            skills = utils.extract_skills(__nlp,__nlp.noun_chunks,)
            new_dic={}
            new_dic['name']=name
            new_dic['email']=email
            new_dic['mobile']=mobile
            new_dic['skills']=skills
            new_dic['comp_text']=__text
            self.first_info[key]=new_dic
        print(self.first_info)

    
    
    def extract_skills(self):
        """
            extract_skills function combine all skills
            extracted from sec_based_extraction and 
            using counter checks the word count of each
            skill mentioned in resume.
            final output is list of all skills with their
            count.
        """
        self.skill_list=[]
        for key,value in self.first_info.items():
            self.skill_list=self.skill_list + value['skills']       
        skill_freq = Counter(self.skill_list)
        
        com_skills = skill_freq.most_common(30)
        self.common_skills=[]
        for skill in com_skills:
            self.common_skills.append(skill)
        #print(self.common_skills)
        

    
    def div_skills(self):
        """
            div_skills function divide skills
            into two sections
            1) key_skills and
            2) intermediate_skills
        """
        max_skill=self.common_skills[0][1]
        per_div=max_skill*60//100
        self.key_skills=list(filter(lambda x:x[1]>=per_div,self.common_skills))
        self.inter_skills=list(filter(lambda x:x[1]<per_div,self.common_skills))
        print("Key_skills_are : ")
        print(self.key_skills)
        print("intermediate_skills_are : ")
        print(self.inter_skills)

    def process(self):
        """
            process function combines all required
            functions to extract information from
            resume
        """
        self.extract_text()
    
        self.div_sec()
        self.sec_based_extraction()
        self.extract_skills()
        self.div_skills()
        self.ls_key_skills=[]
        self.ls_inter_skills=[] 
        for skill in self.key_skills:
            self.ls_key_skills.append(skill[0])
        for skill in self.inter_skills:
            self.ls_inter_skills.append(skill[0])

     
    def show_details(self):
        """
            show_details function show all extracted
            details from resume
        """
        print("\nName: ",self.first_info['introduction']['name'])
        print("\nEmail: ",self.first_info['introduction']['email'])
        print("\nContact No.: ",self.first_info['introduction']['mobile'])
        print("\nKEY Skills:")
        print(', '.join(self.ls_key_skills))
        print("\nIntermidate Skills:")
        print(', '.join(self.ls_inter_skills))
        print('\n')
     
