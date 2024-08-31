import re
import keyword
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

#----------------------------------HELPERS----------------------------------------

def nextComma(a, start):
    lists = 0
    dicts = 0
    Quotes = False
    #print("finding comma in ", a[start:])
    while start<len(a):
        if a[start]==',' and lists<=0 and dicts<=0 and not Quotes:
            return start
        elif a[start]=='\\':
            start+=1
        elif a[start]=='[' and dicts<=0 and not Quotes:
            lists+=1
        elif a[start]=='{' and lists<=0 and not Quotes:
            dicts+=1
        elif a[start] == '"' and lists<=0 and dicts<=0:
            if Quotes=='"':
                Quotes=False
            elif Quotes==False:
                Quotes='"'
        elif a[start]=="'" and lists<=0 and dicts<=0:
            if Quotes=="'":
                Quotes=False
            elif Quotes==False:
                Quotes="'"
        elif a[start]==']':
            lists=max(0, lists-1)
        elif a[start]=='}':
            dicts= max(0, dicts-1)
        start+=1
    return len(a)-1

def nextBrace(a, start, brace) ->list:
    #start daggara brace undi and next closing kosam vetukutundi. 
    #invalid paranthesis ki False return chestundi
    #closing brace dorkithe dani index return chestundi ledante last index return chestundi
    #Tokens_isExpression() lo tokens splitting kosam vadutunnam
    braces={'[':']', '{':'}', '(':')'}
    stack = [braces[brace]]
    quotes = False
    i = start+1
    #Vachina braces valid aithe(out of string) stack paina/loki operations chestunnam till
    #either stack aina aipovali ante end brace dorikinattu
    #or input a aina aipovali ante end brace ledu so last index eh return chestunnattu
    while stack and i<len(a):
        if a[i] in ']})' and quotes==False:
            if stack and stack[-1]==a[i]:
                stack.pop()
            else:
                return [False, "Invalid closing paranthesis"]
        elif a[i] in '{([' and quotes==False:
            stack.append(braces[a[i]])
        elif a[i]=='"' or a[i]=="'":
            if quotes:
                if quotes==a[i]:
                    quotes = False
            else:
                quotes = a[i]
        elif a[i]=='\\':
            i+=1
        i+=1
    return [True, i-1]

def nextDot(a, start) ->list:
    #Idi Dot dorkithe [True, location] istundi, lednate [False, "No Dot Found"]
    lists = 0
    dicts = 0
    Quotes = False
    #print("finding dot in ", a[start:])
    while start<len(a):
        if a[start]=='.' and lists<=0 and dicts<=0 and not Quotes:
            return [True, start]
        elif a[start]=='\\':
            start+=1
        elif a[start]=='[' and dicts<=0 and not Quotes:
            lists+=1
        elif a[start]=='{' and lists<=0 and not Quotes:
            dicts+=1
        elif a[start] == '"' and lists<=0 and dicts<=0:
            if Quotes=='"':
                Quotes=False
            elif Quotes==False:
                Quotes='"'
        elif a[start]=="'" and lists<=0 and dicts<=0:
            if Quotes=="'":
                Quotes=False
            elif Quotes==False:
                Quotes="'"
        elif a[start]==']':
            lists=max(0, lists-1)
        elif a[start]=='}':
            dicts= max(0, dicts-1)
        start+=1
    return [False, "Missing Dot '.' operator."]

def keyValuePair(a):
    quotes=False
    pivot = 0
    while pivot<len(a):
        if a[pivot]=='"':
            if quotes=='"':
                quotes = False
            elif quotes==False:
                quotes = '"'
        elif a[pivot]=="'":
            if quotes=="'":
                quotes = False
            elif quotes ==False:
                quotes = "'"
        elif a[pivot]==':' and quotes == False:
            key = a[:pivot]
            value = a[pivot+1:]
            
            res = ExtractDataType(value)
            if res[0]:
                value = res[1]
                res = ExtractDataType(key)
                if res[0]:
                    key = res[1]
                else:
                    return res
                if type(key) in [list, dict]:
                    return [False, f'Unhashable type ->{key}']
                return [True, [key, value]]
            else:
                return res
        elif a[pivot]=="\\":
            pivot+=1
        pivot+=1
    return [False, "Invalid key-value pair"]

def __print_variables_list(data):
    print(end='[')
    first = False
    for e in data:
        if first:
            print(end= ', ')
        first = True
        if type(e)==int or type(e)==float:
            print(f"{Fore.LIGHTWHITE_EX}{e}", end = '')
        if type(e)==type(None):
            print(f"{Fore.LIGHTMAGENTA_EX}{e}", end = '')
        elif type(e)==str:
            print(f"{Fore.GREEN}\"{e}\"", end = '')
        elif type(e) == bool:
            print(f"{Fore.LIGHTBLUE_EX}{e}", end = '')
        elif type(e) == type:
            print(f"{Fore.LIGHTGREEN_EX}{e}", end = '')
        elif type(e) == list:
            __print_variables_list(e)
        elif type(e) == dict:
            __print_variables_dict(e)
        
    print(']', end = '')

def __print_variables_dict(data):
    first = False
    print(end='{')
    for key in data.keys():
        if first:
            print(end= ', ')
        first = True
        #print key
        if type(key)==str:
            print(f"{Fore.LIGHTRED_EX}\"{key}\"", end = '')
        else:
            print(f"{Fore.LIGHTRED_EX}{key}", end = '')
        #print ":"
        print(end=': ')
        #print value
        if type(data[key])==int or type(data[key])==float:
            print(f"{Fore.LIGHTWHITE_EX}{data[key]}", end = '')
        if type(data[key])==type(None):
            print(f"{Fore.LIGHTMAGENTA_EX}{data[key]}", end = '')
        elif type(data[key])==str:
            print(f"{Fore.GREEN}\"{data[key]}\"", end = '')
        elif type(data[key]) == bool:
            print(f"{Fore.LIGHTBLUE_EX}{data[key]}", end = '')
        elif type(data[key]) == type:
            print(f"{Fore.LIGHTGREEN_EX}{data[key]}", end = '')
        elif type(data[key]) == list:
            __print_variables_list(data[key])
        elif type(data[key]) == dict:
            __print_variables_dict(data[key])
    print('}', end = '')

def __print_variables(d): #just prints the variables assigned
    print("{")
    for i in d.keys():
        if type(d[i])==type(None):
            print(f"\t{Fore.LIGHTWHITE_EX}{i} {Fore.RESET}= {Fore.LIGHTMAGENTA_EX}{d[i]}", end='')
        if type(d[i])==int or type(d[i])==float:
            print(f"\t{Fore.LIGHTWHITE_EX}{i} {Fore.RESET}= {Fore.LIGHTWHITE_EX}{d[i]}", end='')
        elif type(d[i])==str:
            print(f"\t{Fore.LIGHTWHITE_EX}{i} {Fore.RESET}= {Fore.GREEN}\"{d[i]}\"", end='')
        elif type(d[i]) == bool:
            print(f"\t{Fore.LIGHTWHITE_EX}{i} {Fore.RESET}= {Fore.LIGHTBLUE_EX}{d[i]}", end='')
        elif type(d[i]) == list:
            print(f"\t{Fore.LIGHTWHITE_EX}{i} {Fore.RESET}=", end = ' ')
            __print_variables_list(d[i])
        elif type(d[i]) == dict:
            print(f"\t{Fore.LIGHTWHITE_EX}{i} {Fore.RESET}=", end = ' ')
            __print_variables_dict(d[i])
        elif type(d[i]) == type:
            print(f"\t{Fore.LIGHTWHITE_EX}{i} {Fore.RESET}= {Fore.LIGHTGREEN_EX}{d[i]}", end = '')
        print()
    print("}")

#----------------------------------VALIDATORS---------------------------------------

#Validating variable names

def ValidVariableName(a) -> list:
    i = len(a)-1
    while i>=0:
        if a[i]==' ':
            i-=1
        else:
            a = a[:i+1]
            break
    if a in keyword.kwlist:#If it's a keyword
        return [False, f"Syntax Error: Cannot assign to {a}"]
    if a!="":
        if 97<=ord(a[0])<=122 or 65<=ord(a[0])<=90 or ord(a[0])==95:
            for i in range(1, len(a)):
                if 97<=ord(a[i])<=122 or 65<=ord(a[i])<=90 or ord(a[i])==95 or a[i] in '0987654321':
                    continue
                else:
                    return [False, "Invalid Variable Name"]
            #EVERTHING IS TRUE -
            return [True, a.strip()]
    return [False, "Invalid Variable Name"]

#DATA-TYPE validatators

def ValidBoolean(a) -> list: 
    a = a.strip()
    if (len(a)==4 and a=='True'):
        return [True, True]
    if (len(a)==5 and a=='False'):
        return [True, False]
    return [False, False]

def ValidNoneType(a) -> list:
    a = a.strip()
    if a=="None":
        return [True, None]
    else:
        return [False, "Invalid NoneType assigned"]

def ValidFloat(a) -> list:
    a = a.strip()
    try:
        point = a.index('.')
        if ValidInteger(a[:point])[0] or a[:point]=='':
            if ValidInteger(a[point+1:])[0] or a[point+1:]=='':
                return [True, float(a)]
        return [False, "Invalid Float Data"]
    except Exception as e:
        return[False, e]

def ValidVariable(a) -> list:
    a = a.strip()
    if a in _sessionVariables.keys():
        return [True, _sessionVariables[a]]
    return [False, "Variable is not Defined"]

def ValidInteger(a) -> list:
    try:
        a = int(a)
        return [True, a]
    except Exception as e:
        return [False, e]

def ValidString(a) -> list:
    a = a.strip()
    if len(a)>=2:
        if a[0]=="'" and a[-1]=="'": #single quote string
            i=1
            while i<len(a)-1:
                if a[i]=="\\":
                    i+=1
                    if len(a)-1==i:
                        return [False, "Unclosed string"]
                elif a[i]=="'":
                    return [False, "Ambiguous string value"]
                i+=1
            return [True, a[1:len(a)-1]] #a is already stripped
        elif a[0]=='"' and a[-1]=='"': #double quote string
            i = 1
            while i<len(a)-1:
                if a[i]=="\\":
                    i+=1
                    if len(a)-1==i:
                        return [False, "Unclosed string"]
                elif a[i]=='"':
                    return [False, "Ambiguous string value"]
                i+=1
            return [True, a[1:len(a)-1]] #a is already stripped
    return [False, "Invalid string assignment"]

def ValidList(a) -> list:
    a = a.strip()
    if len(a)>=2:
        if a=='[]':
            return [True, []]
        listdata = []
        if a[0]=='[' and a[-1]==']':
            i = 0
            j = 1
            while j<len(a):
                j = nextComma(a, j)
                #print("Comma in ", j, f", ExtractDataType({a[i+1:j]})")
                res = ExtractDataType(a[i+1:j].strip())
                #print("Extracted result = ", res)

                if res[0]:
                    listdata.append(res[1])
                else:
                    return [False, "Invalid List Datatype"]
                i = j
                j = i+1

            return [True, listdata]
    return [False, "Invalid List Datatype"]

def ValidDict(a) -> list:
    a = a.strip()
    if len(a)>=2:
        if a=='{}':
            return [True, {}]
        dictdata = {}
        if a[0]=='{' and a[-1]=='}':
            i = 0
            j = 1
            while j<len(a):
                j = nextComma(a, j)
                
                res = keyValuePair(a[i+1:j].strip())

                if res[0]:
                    dictdata[res[1][0]] = res[1][1]
                else:
                    return res
                i = j
                j = i+1

            return [True, dictdata]
    return [False, "Invalid Dictionary Datatype"]

def ExtractDataType(data) ->list:
    data = data.strip()

    #If data is boolean
    res = ValidBoolean(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is None
    res = ValidNoneType(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is float
    res = ValidFloat(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is integer
    res = ValidInteger(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is another variable
    res = ValidVariable(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is string
    res = ValidString(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is list
    res = ValidList(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is dict
    res = ValidDict(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is a builtin function
    res = isBuiltinFunction(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If Expression is found in parameters of other methods which extracting data using extractDatatype
    res = isExpression(data)
    if res[0]:
        data = res[1]
        return True, data
    
    res = isListBuiltinFunction(data)
    if res[0]:
        data = res[1]
        return [True, data]

    return [False, f"Cannot solve the token->{data}"] #-----------> Returning only built-in result as errors reasons

#--------------------------------COMMAND_TYPE--------------------------------------

def isSimpleAssignment(s) -> list:#returns [variable_name, Data||Value] or [False, error_reason] 
    try:
        pivot = s.index('=')
    except:
        return [False, "Invalid Assignment"]
    variable = s[:pivot]
    data = s[pivot+1:]
    #Check valid variable name first.
    res = ValidVariableName(variable)
    if res[0]:
        variable = res[1]
        #Check valid data with datatypes
        res = isExpression(data)
        if res[0]:
            data = res[1]
            return [variable, data]
        return res
    return res

#---------------------------Universal Inbuil Functions----------------------------

def _type(simple) -> list:
    try:
        simple = simple.strip()
        res = ExtractDataType(simple)
        if res[0]:
            res[1] = type(res[1])
            return [True, res[1]]
        return [False, 'Invalid positional argument']
    except Exception as e:
        return [False, e]

def _len(simple) -> list:
    try:
        simple = simple.strip()
        iterables = [dict, str, list, tuple, set]
        res = ExtractDataType(simple)
        if res[0]:
            if type(res[1]) in iterables:
                return [True, len(res[1])]
        return [False, "Object is not iterable"]
    except Exception as e:
        return [False, e]

def _int(simple) -> list:
    try:
        simple = simple.strip()
        res = ExtractDataType(simple)
        if res[0]:
            return [True, int(res[1])]
        return [False, "Invalid positional argument"]
    except Exception as e:
        return [False, e]

def _list(simple) -> list:
    try:
        simple = simple.strip()
        res = ExtractDataType(simple)
        if res[0]:
            return [True, list(res[1])]
        return [False, "Invalid positional argument"]
    except Exception as e:
        return [False, e]

def _float(simple) -> list:
    try:
        simple = simple.strip()
        res = ExtractDataType(simple)
        if res[0]:
            return [True, float(res[1])]
        return [False, "Invalid positional argument"]
    except Exception as e:
        return [False, e]

def _dict(simple) -> list:
    try:
        simple = simple.strip()
        res = ExtractDataType(simple)
        if res[0]:
            return [True, dict(res[1])]
        return [False, "Invalid positional argument"]
    except Exception as e:
        return [False, e]

def _str(simple) -> list:
    try:
        simple = simple.strip()
        res = ExtractDataType(simple)
        if res[0]:
            return [True, str(res[1])]
        return [False, "Invalid positional argument"]
    except Exception as e:
        return [False, e]

def _bool(simple) -> list:
    try:
        simple = simple.strip()
        res = ExtractDataType(simple)
        if res[0]:
            return [True, bool(res[1])]
        return [False, "Invalid positional argument"]
    except Exception as e:
        return [False, e]

def _abs(simple) -> list:
    try:
        simple = simple.strip()
        res = ExtractDataType(simple)
        if res[0]:
            return [True, abs(res[1])]
        return [False, "Invalid datatype"]
    except Exception as e:
        return [False, e]

def _sum(simple) -> list: #we get "list, start = 2"
    #start should be the keyword for an argument
    try:
        simple = simple.strip()
        simple = '(' + simple + ')'
        i = 0
        j = 1
        args = []
        while j<len(simple):
            j = nextComma(simple, j)
            #print("Comma in ", j, f", ExtractDataType({a[i+1:j]})")
            args.append(simple[i+1:j])
            i = j
            j = i+1
        if len(args)==1:
            res = ExtractDataType(args[0])
            if res[0]:
                return [True, sum(res[1])]
        if len(args)==2:
            res1 = ExtractDataType(args[0])
            res2a = isSimpleAssignment(args[1].strip())
            res2b = ExtractDataType(args[1])
            print(res1, res2a, res2b)
            try:
                if res1[0] and res2a[0]:
                    if res2a[0]=='start':
                        return [True, sum(res1[1], res2a[1])]
                    else:
                        return [False, "Invalid keyword argument"]
                elif res1[0] and res2b[0]:
                    return [True, sum(res1[1], res2b[1])]
                else:
                    return [False, "Invalid keyword arguments"]
            except:
                return  [False, "Invalid operation"]
        return [False, "Invalid positional argument"]
    except Exception as e:
        return [False, e]

def isBuiltinFunction(data):
    data = data.strip()
    _builtins = ['type', 'len', 'int', 'list', 'float', 'dict', 
                'str', 'bool', 'abs', 'sum']
    _builtinsMethods = [_type, _len, _int, _list, _float, _dict,
                        _str, _bool, _abs, _sum]
    for b in range(len(_builtins)):
        if len(data)>len(_builtins[b])+2 and data[:len(_builtins[b])+1]==_builtins[b]+'(' and data[-1]==')':
            res = _builtinsMethods[b](data[len(_builtins[b])+1:-1])
            return res #getting list as a return type
    return [False, "Invalid built-in function"]

#------------------------------List Inbuilt functions----------------------------

def _listAppend(listName, parameters) ->list:
    parameters = parameters.strip()
    res = isExpression(parameters)
    if res[0]:
        if type(listName)==list: #either we get direct list
            listName.append(parameters)
        else: #or we get already stored list variable
            _sessionVariables[listName].append(res[1])
        return [True,None]
    return res

def _listInsert() ->list:
    return

def _listRemove() ->list:
    return

def _listPop() ->list:
    return

def _listIndex() ->list:
    return

def _listCount() ->list:
    return

def _listSort() ->list:
    return

def _listReverse() ->list:
    return

def _listCopy() ->list:
    return

def _listClear() ->list:
    return

def isListBuiltinFunction(data) ->list: #Accepts "list.method()" as data.
    data = data.strip()
    nextDotIndex = nextDot(data, 0)
    if nextDotIndex[0]:
        listName = data[:nextDotIndex[1]].rstrip()
        presentListMethod = data[nextDotIndex[1]+1:].strip()
        
        directList = isExpression(listName) #might give a direct list also like [1,2,3].append(23)

        if directList[0]:
            if listName not in _sessionVariables.keys():
                listName = directList[1]

            listInbuiltsNames = ['append', 'insert', 'remove', 'pop', 'index', 'count',
                            'sort', 'reverse', 'copy', 'clear']
            listInbuilts = [_listAppend, _listInsert, _listRemove, _listPop, _listIndex, _listCount,
                            _listSort, _listReverse, _listCopy, _listClear]
            for i in range(len(listInbuilts)):
                if len(presentListMethod)>len(listInbuiltsNames[i])+2:
                    try:
                        openBrace = presentListMethod.index('(')
                        if presentListMethod[:openBrace]==listInbuiltsNames[i] and presentListMethod[-1]==')':
                            res = listInbuilts[i](listName, presentListMethod[openBrace+1:len(presentListMethod)-1])
                            return res
                    except:
                        # print(listInbuiltsNames[i], 'ruled out')
                        good = True
            return [False, f"AttributeError: 'list' object has no attribute {presentListMethod}"]
        else:
            return [False, f"NameError: name '{listName}' is not defined"]
    return nextDotIndex


#--------------------------------Solving Expression------------------------------

#Exclusively for expressions only, to avoid death recursive calls

def solveToken(data) -> list:
    
    data = data.strip()
    #If data is boolean
    res = ValidBoolean(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is float
    res = ValidFloat(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is integer
    res = ValidInteger(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is another variable
    res = ValidVariable(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is string
    res = ValidString(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is list
    res = ValidList(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is dict
    res = ValidDict(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    #If data is a builtin function
    res = isBuiltinFunction(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    res = isListBuiltinFunction(data)
    if res[0]:
        data = res[1]
        return [True, data]
    
    return [False, f"Cannot solve the token->{data}"]

def isExpression(data) -> list: #input data expression directly
    data = data.strip()
    tokens = []

    start = -1
    end = 0
    quotes = False
    while end<len(data):
        if data[end]=='(' and quotes == False:
            res = nextBrace(data, end, '(')
            if res[0]:
                #2 cases a)Method- (1,2,3).append()  b)Simple- (1,len(x),3)  , NextToken
                searchNextDot = res[1]+1 #closing brace index +1
                DotFound = False
                while searchNextDot<len(data):
                    if data[searchNextDot]=='.':
                        DotFound = True
                        break
                    elif data[searchNextDot]!=' ':
                        break
                    searchNextDot+=1
                if DotFound: #Method- (1,2,3).append()
                    end = searchNextDot
                    continue
                else: #Simple- (1,len(x),3)  , NextToken
                    tokens.append(data[start+1: res[1]+1].strip())
                    start = res[1]
                    end = start
            else:
                return res
        elif data[end]=='[' and quotes == False:
            res = nextBrace(data, end, '[')
            if res[0]:
                #2 cases a)Method- [1,2,3].append()  b)Simple- [1,len(x),3]  , NextToken
                searchNextDot = res[1]+1 #closing brace index +1
                DotFound = False
                while searchNextDot<len(data):
                    if data[searchNextDot]=='.':
                        DotFound = True
                        break
                    elif data[searchNextDot]!=' ':
                        break
                    searchNextDot+=1
                if DotFound: #Method- [1,2,3].append()
                    end = searchNextDot
                    continue
                else: #Simple- [1,len(x),3]  , NextToken
                    tokens.append(data[start+1: res[1]+1].strip())
                    start = res[1]
                    end = start
                tokens.append(data[start+1: res[1]+1].strip())
                start = res[1]
                end = start
            else:
                return res
        elif data[end]=='{' and quotes == False:
            res = nextBrace(data, end, '[')
            if res[0]:
                #2 cases a)Method- {1,2,3}.append()  b)Simple- {1,len(x),3}  , NextToken
                searchNextDot = res[1]+1 #closing brace index +1
                DotFound = False
                while searchNextDot<len(data):
                    if data[searchNextDot]=='.':
                        DotFound = True
                        break
                    elif data[searchNextDot]!=' ':
                        break
                    searchNextDot+=1
                if DotFound: #Method- {1,2,3}.append()
                    end = searchNextDot
                    continue
                else: #Simple- {1,len(x),3}  , NextToken
                    tokens.append(data[start+1: res[1]+1].strip())
                    start = res[1]
                    end = start
                tokens.append(data[start+1: res[1]+1].strip())
                start = res[1]
                end = start
            else:
                return res
        elif data[end] in '+-/*%' and quotes==False:
            tokens.append(data[start+1:end].strip())
            tokens.append(data[end].strip())
            start = end
        elif data[end]=='"' or data[end]=="'":
            if quotes:
                if quotes==data[end]:
                    quotes=False
            else:
                quotes=data[end]
        elif data[end]=='\\':
            end+=1
        end+=1
    tokens.append(data[start+1:end].strip()) #the final un-appended token

    while '' in tokens: #removing unnecessary empty tokens
        tokens.remove('')
    # print("Divided Tokens = ",tokens)

    for i in range(len(tokens)):
        if tokens[i] not in '+-()}{[]*/^':
            #might have another sub expression
            if len(tokens[i])>2 and (tokens[i][0],tokens[i][-1]) == ('(', ')'):
                #This token[i] is a sub-expression
                # print("Found sub expression = ",tokens[i][1:len(tokens[i])-1])
                res = isExpression(tokens[i][1:len(tokens[i])-1])
                if res[0]:
                    if type(res[1])==str:
                        res[1] = '"'+res[1]+'"'
                    tokens[i] = str(res[1])
                else:
                    return res
            #might not be an expression || solvable extract data-types(inbuilts(), simple datatypes, list&dict.inbuilts())
            else:
                res = solveToken(tokens[i])
                if res[0]:
                    if type(res[1])==str: #To identify difference between a string and variable
                        res[1] = '"'+res[1]+'"'
                    tokens[i] = str(res[1])
                else:
                    # print("Got error while converting token = ",tokens[i])
                    return res
    # print("Tokens after solving each individually = ",tokens)
    try:
        res = ' '.join(tokens) #Even the space while joining is important because
        # print("joined tokens->",res)
        res = eval(res)
        # print(f'Result ({tokens}) = {res}')
        return [True, res]
    except Exception as e:
        # print(f"Failed calculating result of Tokens({tokens}), because->{e}")
        return [False, e]

#---------------TILL WHERE DID WE ACHIEVE? ----------------------------
'''
TOMORROW's tasks- 
1. Implement below
    1a. List inbuilts (*not developed yet) @.operators on list
    1b. Dict inbuilts (*not developed yet) @.operators on dict
    1c. Str inbuilts (*not developed yet) @.operators on str
2. Implement Boolean operations like "no", "!", use it as a delimiter in expressions.

FIX ERROR computations-
a=[1, 2, 3+len([1,2])-(3*4)*(2),str([1,3]) str(2)]
You're using inbuilt eval() to solve the expression tokens.. Do it manually

'''

#---------------------------------------MAIN--------------------------------------

#IMPORTANT VARIABLES

_sessionVariables = dict() #stores all the user created local variables

print(f"{Fore.CYAN}{Back.WHITE}pythonDB is currently running")
print()
s = input(f"{Fore.BLUE}>>>{Fore.RESET}")
while s!='_exit_':
    if s == '!variables':
        __print_variables(_sessionVariables)
    else:#only 2 kind of inputs, either '!variables' or anything
        assignment = isSimpleAssignment(s) #Command Type-1
        if assignment[0]!=False:
            _sessionVariables[assignment[0]]=assignment[1]
            print(f"{Fore.LIGHTGREEN_EX}Successful Assignment of {Fore.LIGHTWHITE_EX}{assignment[0]} = {Fore.LIGHTWHITE_EX}{assignment[1]}")
            #print(f"{Back.GREEN}Successful Assignment {Fore.RESET}of {Fore.LIGHTWHITE_EX}{assignment[0]} = {assignment[1]}")
        else:
            print(f"{Fore.RED}ERROR: {assignment[1]}")
            #print(f"{Back.RED}ERROR: {assignment[1]}")

        #CommandType- Expression
        expression = isExpression(s)
        if expression[0]!=False and assignment[0]==False:
            print(f"{Fore.LIGHTBLUE_EX}{expression[1]}")
        elif assignment[0]==False:
            print(f"{Fore.LIGHTRED_EX}{expression[1]}")

    print()
    s = input(f"{Fore.BLUE}>>>{Fore.RESET}")

