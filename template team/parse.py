import re
f = list(''.join(open('template.html').readlines()))
print (''.join(f))

def parse(content):
    results = []
    text = []
    node_list = []
    
    while content:
        temp = ''
        
        #####INCOMING SOMETHING#####
        
        if content[0] == '{' and content[1] == '%': 

            #decide if it is an if or an end

            #removing {%
            content.pop(0) 
            content.pop(0)
            
            results.append(text)
            

            
            #####INCOMING IFNODE#####
            
            if ''.join(content).startswith(' if'):
                
                iftext = []
                predicate = []
                
                #remove if
                content.pop(0)
                content.pop(0)
                content.pop(0)
                content.pop(0)

                #while we haven't reached the end of the tags
                while content[1]!='}' and content[0]!='%':

                #store the character as the part of the predicate
                    predicate.append(content.pop(0))

                #removing %}
                content.pop(0) 
                content.pop(0)
                
                parse(content)
                iftext.append(''.join(predicate).strip())
                print(iftext)

            #####INCOMING END#####
                
            elif ''.join(content).startswith(' end'):
                iftrue = []
                
                #while we haven't reached the end of the tags
                while content[1]!='}' and content[0]!='%': 
                    content.pop(0)

                #removing %}
                content.pop(0) 
                content.pop(0)

                return 

        #####INCOMING PYTHONNODE#####
        elif content[0] == '{' and content[1] == '{':

            #remove double squiggly
            content.pop(0)
            content.pop(0)
            
            pythonnode = []

            while content[0]!= '}' and content[1]!='}':
                pythonnode.append(content.pop(0))

            #remove double squiggly
            content.pop(0)
            content.pop(0)

            print(''.join(pythonnode))
            
        else: #text node
            text.append(content.pop(0))

    return node_list
parse(f)

"""
Parse()
IF we find a {%
    THEN try to find the the corresponding end if

Parse()
    T = ""
    IF we find a {%
        IF {% end
            THEN return with whatever you've found so far
        ELIF {% IF
            PARSE from end of condition
    ELSE add to the text we've found
"""
