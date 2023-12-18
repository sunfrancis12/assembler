import os
import json
import sys

#load optables
jsonFile = open(r'tables\optable.json','r')
optables = json.loads(jsonFile.read())
jsonFile.close()

#crearte intermediate_file
intermediate_file = open(r"Output\intermediate_file.txt",mode="w+")

def search_optable(str):
    '''
    search from optable
    '''
    for i in optables:
        if i == str: 
            return True #if opcode not exist
    return False

sybol_table = {}
def search_symbol(string,LOCCTR):
    '''
    search from symbol table
    '''
    SYMBOL = string[0]
    OPCODE = string[1]
    OPERAND = string[2].replace('\n','') #replace '\n'
    if OPCODE =='.' or OPERAND =='.': return 0 #如果為程式註解則跳過
    
    if sybol_table.get(SYMBOL) == "None": #if symbol exist
        print(f"symbol \"{SYMBOL}\" already exist!")
        return 3
    
    sybol_table[SYMBOL] = LOCCTR # record symbol and LOCCTR
    intermediate_file.write(f"{LOCCTR}\t{SYMBOL}\t{OPCODE}\t{OPERAND}\n") #write into intermediate_file
    
    if search_optable(OPCODE):
        return 3 #add LOCCTR
    elif OPCODE == "WORD":
        return 3 #add LOCCTR
    elif OPCODE == "RESW":
        return 3*int(OPERAND) #add LOCCTR
    elif OPCODE == "RESB":
        return int(OPERAND) #add LOCCTR
    elif OPCODE == "BYTE":
        temp = OPERAND.replace("C","").replace("\'","")
        if temp.find("X")!=-1: return 1 #如果有X則回傳1
        return len(temp) #add LOCCTR
    else:
        return 3

def add(LOCCTR,size):
    '''
    LOCCTR adder
    '''
    hex_string = LOCCTR
    number = int(hex_string, 16) #tranform into deciaml
    number += int(size)
    hex_string = hex(number).replace('0x','') #tranform into hex
    return hex_string

def program_length(start,end):
    '''
    return the length of program 
    '''
    hex_start = start
    hex_end = end
    start_int = int(hex_start, 16) #tranform into deciaml
    end_int = int(hex_end, 16) #tranform into deciaml
    end_int -= start_int #end loc - start loc = program length
    return end_int
    
def gen_opject(string):
    '''
    generate object code and write into object file
    '''
    LOCCTR = string[0]
    SYMBOL = string[1]
    OPCODE = string[2]
    OPERAND = string[3].replace('\n','')
    
    if search_optable(OPCODE): #if in optable
        if not OPERAND in sybol_table: #if not in symbol table
            object_file.write(f"{LOCCTR}\t{SYMBOL}\t{OPCODE}\t{OPERAND}\tERROR\n") #write into intermediate_file
            return 
        
        op_num = optables[OPCODE] #get opcode
        OPERAND_LOC = sybol_table[OPERAND] #get symbol_table OPERAND LOC
        object_code = str(op_num) + str(OPERAND_LOC)
        object_file.write(f"{LOCCTR}\t{SYMBOL}\t{OPCODE}\t{OPERAND}\t{object_code}\n") #write into object_file
        return
    elif OPCODE == "WORD":
        temp = int(OPERAND)
        hex_string = hex(temp).replace("0x","") #轉16進制
        object_code = '{0:06s}'.format(hex_string)
        object_file.write(f"{LOCCTR}\t{SYMBOL}\t{OPCODE}\t{OPERAND}\t{object_code}\n") #write into object_file
        return 
    elif OPCODE == "BYTE":
        if OPERAND.find('X'):
            object_code = OPERAND.replace("\'","").replace("X","")
        elif OPERAND.find('C'):
            temp = OPERAND.replace("\'","").replace("C","")
            word_list = list(temp) #將字串拆成一個自元的list
            
            object_code = ""
            for i in word_list:
                word_asc = ord(i) #將自元轉acsii碼
                object_code += str(hex(word_asc)) #acsii碼轉成16進位並加入字串
        object_file.write(f"{LOCCTR}\t{SYMBOL}\t{OPCODE}\t{OPERAND}\t{object_code}\n") #write into object_file
    elif OPCODE == "RESW" or OPCODE == "RESB":
        object_file.write(f"{LOCCTR}\t{SYMBOL}\t{OPCODE}\t{OPERAND}\t\n") #write into object_file
        return 
    else:
        object_file.write(f"{LOCCTR}\t{SYMBOL}\t{OPCODE}\t{OPERAND}\tERROR\n") #write into intermediate_file
        return         

if __name__ == "__main__":
    # read source code file
    f = open(r"Figure\Figure2.1.txt",mode="r")
    source_list = f.readlines() #read file as a list
    f.close()

    # PASS1
    LOCCTR = "0"
    string = source_list[0].split( ) #read first line
    if string[1] == "START": LOCCTR = string[2] #check if start
    PROGRAM_START = LOCCTR #PROGRAM start location
    intermediate_file.write(f"{LOCCTR}\t{string[0]}\t{string[1]}\t{string[2]}\n")
    
    for i in range(1,len(source_list)):
        string = source_list[i].replace(' ','') #replace ' '
        string = string.split('\t') #read line
        if string[1]=="END":
            intermediate_file.write(f"\t{string[1]}\t{string[2]}\t\n") #write into intermediate_file
            break # if end break
        
        size = search_symbol(string,LOCCTR) #return the memory size
        LOCCTR = add(LOCCTR,size)
    
    PROGRAM_LENGTH = program_length(PROGRAM_START,LOCCTR) #program length
    print("program length: ",PROGRAM_LENGTH)
    #print(sybol_table)
    
    intermediate_file.close() #close intermediate_file filestream
    
    # PASS2
    #load intermediate_file
    intermediate_file = open(r"Output\intermediate_file.txt",mode="r")
    intermediate_list = intermediate_file.readlines() #read file as a list
    #print(intermediate_list)
    
    #create object_file
    object_file = open(r"Output\object_file.txt",mode="w")
    
    string = intermediate_list[0].split('\t') #read first line
    if string[2] != "START":  #check if start
        print("ERROR")
        sys.exit(0)
    
    for i in range(1,len(intermediate_list)):
        string = intermediate_list[i].split('\t') #read line
        #print(string)
        if string[1]=="END": # if end break
            object_file.write(f"\t{string[1]}\t{string[2]}\t\n") #write into intermediate_file
            break
        
        #print(string)
        gen_opject(string)
        
        
    intermediate_file.close() #close intermediate_file filestream
    
    
    
