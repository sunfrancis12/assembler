import os
import json

#load optables
jsonFile = open(r'assembler_py\tables\optable.json','r')
optables = json.loads(jsonFile.read())
jsonFile.close()

#load intermediate_file
intermediate_file = open(r"assembler_py\Output\intermediate_file.txt",mode="w")

def search_optable(str):
    '''
    search from optable
    '''
    if optables.get(str) != "None": #if opcode not exist
        return False
    return True



sybol_table = {}
def search_symbol(string,LOCCTR):
    '''
    search from symbol table
    '''
    SYMBOL = string[0]
    OPCODE = string[1]
    OPERAND = string[2]
    if OPCODE =='.' or OPERAND =='.': return 0 #如果為程式註解則跳過
    
    if sybol_table.get(SYMBOL) == "None": #if symbol exist
        print(f"symbol \"{SYMBOL}\" already exist!")
        return 3
    
    sybol_table[SYMBOL] = LOCCTR # record symbol and LOCCTR
    intermediate_file.write(f"{LOCCTR}\t{SYMBOL}\t{OPCODE}\t{OPERAND}\t\n") #write into intermediate_file
    
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
        print(temp)
        return len(temp) #add LOCCTR
    else:
        #print(f"ERROR")
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

if __name__ == "__main__":
    # read source code file
    f = open(r"assembler_py\Figure\Figure2.1.txt",mode="r")
    file_list = f.readlines() #read file as a list
    #print(file_list)
    f.close()

    # PASS1
    LOCCTR = "0"
    string = file_list[0].split( ) #read first line
    if string[1] == "START": LOCCTR = string[2] #check if start
    
    for i in range(1,len(file_list)):
        string = file_list[i].replace(' ','') #replace ' '
        string = string.split('\t') #read line
        print(string)
        if string[1]=="END": break # if end break
        
        size = search_symbol(string,LOCCTR) #return the memory size
        #print(size)
        LOCCTR = add(LOCCTR,size)
        
    print(sybol_table)
