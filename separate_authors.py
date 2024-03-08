# -*- coding: utf-8 -*-


import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
from datetime import datetime
import  collections, os, sys, time
import xlrd,xlsxwriter
import re
from Config import *
import sys, os

RE_D = re.compile('\d')


def get_author_affiliation(author,affiliation_list):
    author_affiliation = ""

    author_no_list = re.findall('\d+', author)
    for author_no in author_no_list:
        for affliation in affiliation_list:
            try:
                affi_no = re.findall('\d+', affliation)
                if author_no and affi_no and author_no == affi_no[0]:
                    author_affiliation = author_affiliation + affliation.replace(affi_no[0],"") + ";"
            except Exception as e:
                print (e)

    return author_affiliation.rstrip(";")

def get_column_index(sheet,column_name):

    for col_index in range(sheet.ncols):
        if sheet.cell(0,col_index).value.strip() == column_name.strip():
            return col_index
    return -1

if __name__ == "__main__":



    source_file_obj = xlrd.open_workbook(source_file)
    source_file_sheet = source_file_obj.sheet_by_index(0)

    workbook = xlsxwriter.Workbook(new_file_name)	
    worksheet = workbook.add_worksheet("Authors")

    worksheet.set_tab_color('#538ED5')
    worksheet.set_column('A:A', 10)#Abstract ID
    worksheet.set_column('B:B', 20)#Manual ID
    worksheet.set_column('C:C', 50)#Authors
    worksheet.set_column('D:D', 50)#Author Affiliation
    worksheet.freeze_panes(1, 0)

    f = workbook.add_format({'bold':True,'bg_color':'#4F81BD','border':1, 'font_name':'Arial', 'font_size':9, 'align':'center', 'valign':'center', 'border':1})					
    f1 = workbook.add_format({'border':1, 'bg_color':'#B8CCE4', 'font_name':'Arial', 'font_size':8, 'text_wrap': True, 'align':'left', 'valign':'top'})
    f2 = workbook.add_format({'border':1, 'bg_color':'#DBE5F1', 'font_name':'Arial', 'font_size':8, 'text_wrap': True, 'align':'left', 'valign':'top'})

    worksheet.write(0,0,"source_id",f)
    worksheet.write(0,1,"manual_id",f)
    worksheet.write(0,2,"authors",f)
    worksheet.write(0,3,"author_affiliation",f)

    source_id_index = get_column_index(source_file_sheet,"source_id")
    manual_id_index = get_column_index(source_file_sheet,"manual_id")
    authors_index = get_column_index(source_file_sheet,"authors")
    affi_index = get_column_index(source_file_sheet,"author_affiliation")
    try:
        write_row = 1
        for row in range(source_file_sheet.nrows):	
            if row == 0:
                continue
            
            source_id = source_file_sheet.cell(row, source_id_index).value
              
            
            manual_id = source_file_sheet.cell(row, manual_id_index).value.strip()
            authors = source_file_sheet.cell(row, authors_index).value.strip()
            authors_affi = source_file_sheet.cell(row, affi_index).value.strip()

            if delimiter_type == 1:
                affi_list = authors_affi.split(";")
                if True:#manual_id == "AAT_ADPD_367":
                    if RE_D.search(authors):

                        author_list = authors.split(";")
                        last_author = ""
                        author_str = ""
                        for idx,author in enumerate(author_list):
                            #author_affiliation = [affi for affi in authors_affi.split(";") if author.strip()[-1] in affi]
                            if idx == 0:
                                author_str = author

                            if (idx + 1) != len(author_list):
                                if author_list[idx+1].isdigit():
                                    author_str = author_str + "," + author_list[idx+1]		
                                    continue
                            if write_row % 2 == 1:
                                f = f1
                            else:
                                f = f2

                            author_affiliation = get_author_affiliation(author_str.strip(),affi_list)							
                                
                            if author_affiliation:
                                worksheet.write(write_row,0,source_id,f)
                                worksheet.write(write_row,1,manual_id,f)
                                worksheet.write(write_row,2,re.sub(r'[0-9]+', '', author_str.strip()).rstrip(","),f)
                                worksheet.write(write_row,3,author_affiliation,f)					
                            else:
                                worksheet.write(write_row,0,source_id,f)
                                worksheet.write(write_row,1,manual_id,f)
                                worksheet.write(write_row,2,author,f)
                                worksheet.write(write_row,3,'',f)
                            write_row = write_row + 1

                            if (idx + 1) != len(author_list):
                                author_str = author_list[idx+1]

                    else:
                        if write_row % 2 == 1:
                            f = f1
                        else:
                            f = f2				
                        worksheet.write(write_row,0,source_id,f)
                        worksheet.write(write_row,1,manual_id,f)
                        worksheet.write(write_row,2,authors,f)
                        worksheet.write(write_row,3,'',f)
                        write_row = write_row + 1

            elif delimiter_type == 2:
                author_list = authors.split(";")
                author_affiliation_list =  authors_affi.split(";")
                #print(author_affiliation_list)
                author_affiliation = ""
                
                #Modified by Vineet Chaurasiya on 23-07-2018
             
                for idx,author in enumerate(author_list):				
                    if write_row % 2 == 1:
                        f = f1
                    else:
                        f = f2
                    count = 0
                    if author:
                        while count < 5:
                           
                            if author[-1] == '.':
                                author = author[:-1]
                            count +=1
                    
                        if author[-1].isdigit():
                            if ',' in author[-3:]:
                            #if ',' in author:
                                #author_nos = author.rsplit(',',1)[1]
                                #author_nos = author[-3:].split(',')
                                #author = author.split(',')[0]
                                for x in author:
                                    if x.isdigit():
                                        i = author.index(x)
                                        nums = author[i:]
                                        author = author[:i]
                                        break
              
                                if nums:
                                    if ',' in nums:
                                        author_nos = nums.split(',')
                                
                                #print(author_nos)
                                #author = author.strip()
                                #first_no = re.findall('\d+', author)
                                
                                #author_nos = first_no + author_nos
                                aff_list= []
                                
                                for author_no in author_nos:
                                    if author_no:
                                        for author_aff in author_affiliation_list:
                                            author_aff_no = re.findall('\d+', author_aff[:3])
                                            try:
                                                author_aff_no = author_aff_no[0]
                                            except:
                                                author_aff_no = author_aff_no
                                            if author_no == author_aff_no:
                                                author_affiliation = author_aff.strip()[1:]
                                                if author_affiliation:
                                                    if author_affiliation[0].isdigit():
                                                        author_affiliation = author_affiliation[1:]
                                                aff_list.append(author_affiliation)
                                
                                
                                count = 0
                                while count < 3:
                                    if author[-1] == '.':
                                        author = author[:-1]
                                    count +=1
                                if author[-1].isdigit():
                                    author = author[:-1]
                                if author[-1].isdigit():
                                    author = author[:-1] 
                                affiliation_to_write = '; '.join(aff_list)
                            
                            else:
                                if author.strip():
                                    count = 0
                                    first_no = re.findall('\d+', author)
                                    
                                    while count < 3:
                                        if author[-1] == '.':
                                            author = author[:-1]
                                        count +=1
                                    if author[-1].isdigit():
                                        author = author[:-1] 
                                    if author[-1].isdigit():
                                        author = author[:-1] 
                                    if first_no:
                                        for author_aff in author_affiliation_list:
                                            author_aff_no = re.findall('\d+', author_aff[:3])
                                                
                                            if first_no == author_aff_no:
                                                affiliation_to_write = author_aff.strip()[1:]
                                                if affiliation_to_write:
                                                    if affiliation_to_write[0].isdigit():
                                                        affiliation_to_write = affiliation_to_write[1:]
                        
                        elif idx < len(author_affiliation_list):
                            if author[-1].isdigit():
                                author = author[:-1]
                            if author[-1].isdigit():
                                author = author[:-1]     
                            affiliation_to_write = author_affiliation_list[idx]
                            if affiliation_to_write:
                                if affiliation_to_write[0].isdigit():
                                    affiliation_to_write = affiliation_to_write[1:]
                         
                        elif idx+1 > len(author_affiliation_list):
                            affiliation_to_write = ''
                        
                        worksheet.write(write_row,0,source_id,f)
                        worksheet.write(write_row,1,manual_id,f)
                        worksheet.write(write_row,2,author.strip(),f)
                        worksheet.write(write_row,3,affiliation_to_write.strip(),f)
                        write_row = write_row + 1


            # if manual_id == "AAT_ADPD_4":
            # 	break
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    workbook.close()

