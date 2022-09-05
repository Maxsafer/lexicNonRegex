from os import listdir

# interpret
def printSymbol(index, line, symb, hardToken):
  if symb in reconocidos:
    if symb in ["<", "<=", ">", ">=", "=="]:
      print(f'Token: OPREL {reconocidos.index(symb)}, Lexema: {symb} on line {line} index {index}.')
      
    elif symb in ["+", "-", "*", "/", "%", "**", "++", "--"]:
      print(f'Token: OPAR {reconocidos.index(symb)}, Lexema: {symb} on line {line} index {index}.')
    
    elif symb == " ":
      print(f'Token: SPACE {reconocidos.index(symb)}, Lexema: {symb} on line {line} index {index}.')
    
    elif symb == "=":
      print(f'Token: ASIG {reconocidos.index(symb)}, Lexema: {symb} on line {line} index {index}.')
      
  else:
    if symb.isdigit():
      print(f'Token: ENT {reconocidos.index("ent")}, Lexema: {symb} on line {line} index {index}.')
      
    elif len(symb) == 1 and couldBePartOfID(symb) or hardToken == 'multiID':
      print(f'Token: ID {reconocidos.index("id")}, Lexema: {symb} on line {line} index {index}.')

    elif hardToken == 'isReal':
      print(f'Token: REAL {reconocidos.index("real")}, Lexema: {symb} on line {line} index {index}.')
      
    else:
      print(f'Token: ERR, Lexema: {symb} not recognized on line {line} index {index}.')

def lexLuthor(inputStrings):
  doubleFlag = 0
  isNumber = 0
  isId = 0
  isReal = ""

  tempNum = ""
  tempNumInd = 0
  tempId = ""
  tempIdInd = 0
  
  # iteramos sobre input
  for y,string in enumerate(inputStrings):
    
    # itereamos para cada char
    for x, char in enumerate(string):

      # si las flags estan desactivadas
      if doubleFlag == 0 and isNumber == 0 and isId == 0:
        
        # si string len es mayor o igual a x + 1 
        if len(string) >= x+1:
          # si no es el ultimo, checa que hay despues
          if len(string) != x+1: 
            # si lo que sigue es vacio
            if string[x+1] == " ":
              printSymbol(x, y, char, '')
            # en el que estamos es vacio
            elif char == " ":
              printSymbol(x, y, " ", '')
            # es doble
            else:
              # si double symbol pero inicia con num
              if char.isdigit():
                isNumber = 1
                tempNumInd = x
                tempNum += char
              
              # si es double symbol pero inicia con letra
              elif couldBePartOfID(char):
                isId = 1
                tempIdInd = x
                tempId += char
                
              # manda el double symbol
              else:
                printSymbol(x, y, f'{char}{string[x+1]}', '')
                doubleFlag = 1
          
          # es el ultimo char
          else:
            printSymbol(x, y, char, '')
  
      # si las flags estan activas
      else:
        # logic system for large integers
        if isNumber == 1:
          tempNum += char
          if len(string) != x+1: # estamos en el ultimo?
            if not string[x+1].isdigit(): # el que sigue no es digito 
              if string[x+1] == ".": # el que sigue es punto
                isReal = "isReal"
              else:
                printSymbol(tempNumInd, y, tempNum, isReal)
                tempNum = ""
                isNumber = 0
            elif char == ".": # el que sigue si es digito y el actual es punto
              isReal = "isReal"
          else:
            printSymbol(tempNumInd, y, tempNum, isReal)
            tempNum = ""
            isNumber = 0
  
        # logic system for long IDs
        elif isId == 1:
          if couldBePartOfID(char):
            tempId += char
            if len(string) != x+1:
              if not couldBePartOfID(string[x+1]):
                printSymbol(tempIdInd, y, tempId, 'multiID')
                tempId = ""
                isId = 0
            else:
              printSymbol(tempIdInd, y, tempId, 'multiID')
              tempId = ""
              isId = 0
          
        # double symbols flag
        doubleFlag = 0
    print(' ')

def couldBePartOfID(char):
  if char.isdigit(): 
    return True
  else:
    char = ord(char)
    for x in range(ord('A'),ord('z')+1):
      if x not in range(91, 97):
        if char == x:
          return True
  return False

def inputText():
  inputStrings = []
  files = []
  counter = 0
  for file in listdir('./'):
    if file.endswith(".txt"):
      counter += 1
      print(f'{counter}. {file}')
      files.append(file)
  chosen = int(input())-1
  f = open(f'{files[chosen]}', "r")
  for row in f:
    inputStrings.append(row.replace("\n", ""))
  return inputStrings
  
if __name__ == '__main__':
  reconocidos = [" ", "id", "ent", "real", "<", "<=", ">", ">=", "==", "=", "+", "-", "*", "/", "%", "**", "++", "--"]
  inputText = inputText()
  lexLuthor(inputText)