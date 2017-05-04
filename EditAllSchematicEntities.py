## Edit All Schematic Entities (EASE)-- KiCAD Annotation Adapter

#Version: 1
#Author: Brittany Scheid <brittany.h.scheid@gmail.com>


#This script allows users to load a kiCAD schematic script into a .csv file.
#All annotated part names will be extracted to the file along with their
#corresponding fields. The fields can be easily edited, and then the .csv
#can be reloaded to update the schematic file.

#NOTE: The schematic components in the project MUST be annotaed first, and duplicate references should not exist

#1) Call schematicToCSV
#2) User Edits CSV File
#3) Call updateSchematic

import csv
import os
import itertools
import tkinter as tk
from tkinter import filedialog as fd


SCH_COL_NUM= 0 #Index of schematic name column in filearray
REF_COL_NUM= 1 #Index of reference column in filearray



#Create .csv from schematic file
def schematicToCSV(dirPath, schFilename, csvFilename):
 
    fullArray= schematicToCSVhelper(dirPath, schFilename, [])
    
    with open(dirPath+csvFilename, 'w', newline='') as output:
        writer= csv.writer(output)
        writer.writerows(fullArray)

    return fullArray

#Recursive function to populate component array
def schematicToCSVhelper(dirPath, schFilename, compArr):
    with open(dirPath+schFilename, 'r') as schematic:
        for line in schematic:
            if line[0:5]=="F 0 \"": #Component

                if line[5]=="#": continue #ignore power components
                
                ind=len(compArr)
                compArr.append([schFilename])
                while line[0]=="F":
                    compArr[ind].append(line.split('"')[1])
                    line=schematic.readline()
            if line[0:4]=="F1 \"":  #Sheet
                compArr=schematicToCSVhelper(dirPath, line.split('"')[1], compArr)

    return compArr
        

#Update schematic file with .csv
def CSVToSchematic(dirpath, schFilename, csvFilename):

    #loads 2d array from .csv file
    with open(dirpath+csvFilename, 'rU') as f:
        reader= csv.reader(f)
        filearray = list(reader)
       
    CSVToSchematicHelper(dirpath, schFilename, filearray)
    return
    
            
#Helper function
def CSVToSchematicHelper(dirpath, schFilename, filearray):

    #Keep a backup copy (os.remove handling necessary for Windows filesystems)
    if os.path.exists(dirpath+"old_"+schFilename):
        os.remove(dirpath+"old_"+schFilename)
    os.rename(dirpath+schFilename, dirpath+"old_"+schFilename)
    newfile=open(dirpath+schFilename, 'w') #Blank document to copy to

    #Retrieve schematic-specific component array 
    subarray= [comp_line for i,comp_line in enumerate(filearray) if comp_line[0]== schFilename]
    subarray=list(itertools.zip_longest(*subarray)) #transpose array


    with open(dirpath+"old_"+schFilename, 'r+') as schematic:
        for line in schematic:
            
            #Update component lines in .sch file
            if line[0:5]=="$Comp":
                while line[0]!= "F":
                    newfile.write(line)
                    line=schematic.readline()

                if line[5]=="#": continue #ignore power components

                #Use unique component name as key to find corresp. row index in filearray
                key=line.split('"')[1]
                ref_index= subarray[REF_COL_NUM].index(key)
                newfile.write(line)

                line=schematic.readline()
                while line[0]=="F":
                    field_index= int(line[2])
                    temp=line.split('"');

                    #Replace line description with sanitized description from filearry
                    temp[1]=subarray[field_index+1][ref_index].replace('"',"")


                    #Hide annotations 
                    if field_index > 1:
                        temp[2]=temp[2].split(' ')
                        temp[2][6]="0001"
                        temp[2]=' '.join(temp[2])
                           
                    newline='"'.join(temp)
                    newfile.write(newline)

                    line=schematic.readline()

                #Add additional fields to newfile
                    
                temp=['','',newline.replace("\n"," ").split('"')[2],'','\n']
                
                while field_index < len(subarray)-2:
                    field_index+=1
                    temp[0]='F '+str(field_index)+' '
                    ref_name=subarray[field_index+1][ref_index]
                    temp[1]= "" if ref_name == None else ref_name.replace('"',"")
                    temp[3]='Field'+str(field_index)

                    newline='"'.join(temp)
                    newfile.write(newline)

            #Recurse to Sheet
            if line[0:4]=="F1 \"":  
                CSVToSchematicHelper(dirpath, line.split('"')[1], filearray)
                               
            newfile.write(line)            

    newfile.close()

    return
                    

if __name__== "__main__":

    print('Choose schematic file to update')
    #Open File Browser    
    root = tk.Tk()
    root.withdraw()
    input_file=fd.askopenfilename(filetypes =(("Project Files (.pro)", "*pro"),("Schematic Files (.sch)", "*sch"),("All Files", "*.*")))
    dirPath=os.path.split(input_file)[0]+"/"

    schFilename=os.path.split(input_file)[1]
    schFilename=schFilename[0:-4]+".sch"
    csvFilename=schFilename[0:-4]+"_Editor.csv"

    #Convert to .csv for editing
    print('Converting to spreadsheet, the file will open automatically...')
    schematicToCSV(dirPath, schFilename, csvFilename)
    os.system("start "+dirPath+csvFilename)  

    #Overwrite old file
    overwrite=input("overwrite "+schFilename+" with data from "+ csvFilename +" (y/n)? ")
    if overwrite=="y":
        CSVToSchematic(dirPath, schFilename, csvFilename)
        print('Update Complete')
    else: print('Overwrite canceled')
    



                






    
