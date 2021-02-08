# This code translates given 6-character or 8-character NES Game Genie codes.
# It outputs the address, data, and compare values they correlate to
# and it displays the translation process. 
# For a description of the translation see these NES Game Genie Technical Notes
#   - http://tuxnes.sourceforge.net/gamegenie.html
# To verify this code see this online NES Game Genie code Encoder & Decoder
#   - http://games.technoplaza.net/ggencoder/js/

from tabulate import tabulate

def getHex(c): 
    if c == 'A': 
        return 0x0 
    elif c == 'P':
        return 0x1
    elif c == 'Z': 
        return 0x2
    elif c == 'L': 
        return 0x3
    elif c == 'G':
        return 0x4
    elif c == 'I': 
        return 0x5
    elif c == 'T': 
        return 0x6
    elif c == 'Y':
        return 0x7
    elif c == 'E': 
        return 0x8
    elif c == 'O': 
        return 0x9
    elif c == 'X':
        return 0xA
    elif c == 'U': 
        return 0xB
    elif c == 'K': 
        return 0xC
    elif c == 'S':
        return 0xD
    elif c == 'V': 
        return 0xE
    elif c == 'N': 
        return 0xF
    else: 
        return None 

def translateGG(code,isEight): 

    code.upper()
    

    table = []
    
    nums = ["n0","n1","n2","n3","n4","n5"]

    if isEight: 
        nums += ["n6","n7"]

    table.append(nums)


    table.append([c for c in code])

    n = []
    for c in code: 
        h = getHex(c) 
        if h is None: 
            print("Invalid characters present.")
            return 
        n.append(h)
    
    
    table.append(n)
    
    print(tabulate([table[0],table[1],table[2]], tablefmt="plain"))
    print()

    print("Address") 
    print()
    a1 = (n[3]&7)<<12
    a2 = ((n[5]&7)<<8) 
    a3 = ((n[4]&8)<<8)
    a4 = ((n[2]&7)<<4) 
    a5 = ((n[1]&8)<<4)
    a6 = (n[4]&7)
    a7 = (n[3]&8)
    
    print("address = 0x8000 + (("+str(bin(n[3]))+" & "+ str(bin(7)) +") <<  12)")
    print("| (("+str(bin(n[5]))+" & "+str(bin(7))+") << 8) | (("+str(bin(n[4]))+" & "+str(bin(8))+") << 8)")
    print("| (("+str(bin(n[2]))+" & "+str(bin(7))+") << 4) | (("+str(bin(n[1]))+" & "+str(bin(8))+") << 4)")
    print("| ("+str(bin(n[4]))+" & "+str(bin(7))+") | ("+str(bin(n[3]))+" & "+str(bin(8)))

    print()

    print("address = 0x8000 + "+ str(bin(a1)))
    print("| "+str(bin(a2))+" | "+str(bin(a3)))
    print("| "+str(bin(a4))+" | "+str(bin(a5)))
    print("| "+str(bin(a6))+" | "+str(bin(a7)))


    address = 0x8000 + a1 | a2 | a3 | a4 | a5 | a6 | a7
    address = hex(address)
    print("= "+ str(address))

    print()
    print("Data")
    print()



    d1 = (n[1]&7) << 4
    d2 = (n[0]&8) << 4
    d3 = (n[0]&7) 
    if isEight:
        diff = 7 
    else: 
        diff = 5 

    d4 = (n[diff]&8)

    

    print("data = (("+str(bin(n[1]))+" & "+str(bin(7))+") << 4) | (("+str(bin(n[0]))+" & "+str(bin(8))+") << 4")
    print("| ("+str(bin(n[0]))+" & "+str(bin(7))+") | ("+str(bin(n[diff]))+" & "+str(bin(8)))

    print()

    print("data = "+str(bin(d1))+" | "+str(bin(d2)))
    print("| "+str(bin(d3))+" | "+str(bin(d4)))

    data = d1 | d2 | d3 | d4 
    data = hex(data)
    print("= "+str(data))

    if isEight: 
        
        print()
        print("Compare")
        print()

        c1 = (n[7]&7) << 4
        c2 = (n[6]&8) << 4
        c3 = (n[6]&7)
        c4 = (n[5]&8) 


        print("compare = (("+str(bin(n[7]))+" & "+str(bin(7))+") << 4) | (("+str(bin(n[6]))+" & "+str(bin(8))+") << 4")
        print("| ("+str(bin(n[6]))+" & "+str(bin(7))+") | ("+str(bin(n[5]))+" & "+str(bin(8)))

        print()

        print("compare = "+str(bin(c1))+" | "+str(bin(c2)))
        print("| "+str(bin(c3))+" | "+str(bin(c4)))

        compare = c1 | c2 | c3 | c4 
        compare = hex(compare)
        print("= "+ str(compare))
        print()


code = str(input("Enter a NES Game Genie Code: "))
code = code.replace(" ","")
print()

if len(code)==8:
    
    translateGG(code,True)
elif len(code)==6: 
    translateGG(code,False)
else: 
    print("Codes must be either 6 characters or Eight characters long.")
