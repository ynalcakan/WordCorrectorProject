#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
import re
import sys
import os

def wanted():
   return raw_input("'halt' kapatmak icin...\n1. Kelimeleri Texte Aktar: 'getwcounts'\n2. Kelimeleri Excele Aktar: 'egetwcounts'\n3. Arttribute Secim: 'getatt'"
                    "\n4. Tum Twitleri Duzelt: 'getfix'\n5. Tek Bir Kelime: 'sfix'\n""Lets Start: ")


def getwordfix():
    import re
    import collections

    def words(text): return re.findall('[a-z]+', text.lower())

    def train(features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    NWORDS = train(words(file('big.txt').read()))

    alphabet = 'abcdefg�h�ijklmno�pqrs�tu�xqwvyz'

    def edits1(word):
        splits = [(word[:i], word[i:])
                  for i in range(len(word) + 1)]
        inserts = [a + c + b
                            for a, b in splits
                                for c in alphabet]
        deletes = [a + b[1:]
                   for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:]
                      for a, b in splits
                        if len(b)>1]
        replaces = [a + c + b[1:]
                    for a, b in splits
                        for c in alphabet
                            if b]
        return set(inserts + transposes + replaces + deletes)

    def known_edits2(word):
        return set(e2
                    for e1 in edits1(word)
                        for e2 in edits1(e1)
                            if e2 in NWORDS)

    def known(words):
        return set(w
                    for w in words
                        if w in NWORDS)

    def correct(word):
        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
        return max(candidates, key=NWORDS.get)

    with open("positivesamsung.txt","r") as fp:
        lines = fp.read()
    ptw = re.sub("[^\w]"," ",lines).split()
    with open("negativesamsung.txt","r") as fn:
        lines2 = fn.read()
    ntw = re.sub("[^\w]"," ",lines2).split()
    with open("notrsamsung.txt","r") as fno:
        lines3 = fno.read()
    notw = re.sub("[^\w]"," ",lines3).split()
    with open("sonuc.txt") as fa:
        fa=open("sonuc.txt",'w')
        fpp=open("fPozitif tweetler.txt",'w')
        fnn=open("fNegatif tweetler.txt",'w')
        fno=open("fNotr tweetler.txt",'w')
    for c in range(3):
        if c == 0:
            inwords = ptw
        elif c == 1:
            inwords = ntw
        else:
            inwords = notw
        for x in inwords:
            flag = 0
            if x == correct(x):
                continue
            else:
                y=x
                if len(x)>4:
                    if x[(len(x)-3):len(x)]=='cem':
                        x = x[0:len(x)-3]+'cegim'
                    if x[(len(x)-3):len(x)]=='cam':
                        x = x[0:len(x)-3]+'cagim'
                    if x[(len(x)-3):len(x)]=='caz':
                        x = x[0:len(x)-3]+'cagiz'
                    if x[(len(x)-3):len(x)]=='cez':
                        x = x[0:len(x)-3]+'cegiz'
                    if x[(len(x)-3):len(x)]=='yom':
                        x = x[0:len(x)-3]+'yorum'
                    if x[(len(x)-3):len(x)]=='yoz':
                        x = x[0:len(x)-3]+'yoruz'
                    if x[(len(x)-3):len(x)]=='in':
                        x = x[0:len(x)-2]+'nim'
                    if x[(len(x)-5):len(x)]=='micem':
                        x = x[0:len(x)-5]+'meyecegim'
                    if x[(len(x)-5):len(x)]=='micek':
                        x = x[0:len(x)-5]+'meyecek'
                if "her" == x[0:3] and x[3:len(x)] == correct(x[3:len(x)]):
                    kelime1 = x[0:3]
                    kelime2 = x[3:len(x)]
                    print("==>%s -->%s %s\n"%(x,kelime1,kelime2))
                    fa.write("%s --> %s %s\n"%(x,kelime1,kelime2))
                    flag = 1
                    if c == 0:
                        lines = lines.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                    elif c==1:
                        lines2 = lines2.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                    else:
                        lines3 = lines3.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                if "ayfon" == x[0:5]:
                    kelime1 = "iphone"
                    print("==>%s -->%s\n"%(x,kelime1))
                    fa.write("%s --> %s\n"%(x,kelime1))
                    flag = 1
                    if c == 0:
                        lines = lines.replace(" "+x+" "," "+kelime1+" ")
                    elif c ==1:
                        lines2 = lines2.replace(" "+x+" "," "+kelime1+" ")
                    else:
                        lines3 = lines3.replace(" "+x+" "," "+kelime1+" ")
                if "daha" == x[len(x)-4:len(x)] and x[0:len(x)-4] == correct(x[0:len(x)-4]):
                    kelime1 = x[len(x)-4:len(x)]
                    kelime2 = x[0:len(x)-4]
                    print("==>%s -->%s %s\n"%(x,kelime2,kelime1))
                    fa.write("%s --> %s %s\n"%(x,kelime2,kelime1))
                    flag = 1
                    if c == 0:
                        lines = lines.replace(" "+x+" "," "+kelime2+" "+kelime1+" ")
                    elif c ==1:
                        lines2 = lines2.replace(" "+x+" "," "+kelime2+" "+kelime1+" ")
                    else:
                        lines3 = lines3.replace(" "+x+" "," "+kelime2+" "+kelime1+" ")
                if "tsk" == x[0:3]:
                    kelime1 = "tesekkur"
                    print("==>%s -->%s\n"%(x,kelime1))
                    fa.write("%s --> %s\n"%(" "+x+" "," tesekkur "))
                    flag = 1
                    if c == 0:
                        lines = lines.replace(x,"tesekkur")
                    elif c ==1:
                        lines2 = lines2.replace(x,"tesekkur")
                    else:
                        lines3 = lines3.replace(x,"tesekkur")
                if "n" == x[0:1] and x[1:len(x)]==correct(x[1:len(x)]):
                    kelime1 = x[0:1]+"e"
                    kelime2 = x[1:len(x)]
                    print("==>%s -->%s %s\n"%(x,kelime1,kelime2))
                    fa.write("%s --> %s %s\n"%(x,kelime1,kelime2))
                    flag = 1
                    if c == 0:
                        lines = lines.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                    elif c==1:
                        lines2 = lines2.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                    else:
                        lines3 = lines3.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                if "nap" == x[0:3]:
                    kelime1 = x[0:1]+"e"
                    kelime2 = correct("yap"+x[3:len(x)])
                    print("==>%s -->%s %s\n"%(x,kelime1,kelime2))
                    fa.write("%s --> %s %s\n"%(x,kelime1,kelime2))
                    flag = 1
                    if c == 0:
                        lines = lines.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                    elif c==1:
                        lines2 = lines2.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                    else:
                        lines3 = lines3.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                if "cak" == x[len(x)-3:len(x)]:
                    kelime1 = x[0:len(x)-3]+"a"+x[len(x)-3:len(x)]
                    print("==>%s -->%s\n"%(x,correct(kelime1)))
                    fa.write("%s --> %s\n"%(x,correct(kelime1)))
                    flag = 1
                    if c == 0:
                        lines = lines.replace(" "+x+" "," "+correct(x)+" ")
                    elif c==1:
                        lines2 = lines2.replace(" "+x+" "," "+correct(x)+" ")
                    else:
                        lines3 = lines3.replace(" "+x+" "," "+correct(x)+" ")
                if "bi" == x[0:2] and x[2:len(x)] == correct(x[2:len(x)]) and len(x)>2:
                    kelime1 = x[0:2]+"r"
                    kelime2 = x[2:len(x)]
                    print("==>%s -->%s %s\n"%(x,kelime1,kelime2))
                    fa.write("%s --> %s %s\n"%(x,kelime1,kelime2))
                    flag=1
                    if c == 0:
                        lines = lines.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                    elif c==1:
                        lines2 = lines2.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                    else:
                        lines3 = lines3.replace(" "+x+" "," "+kelime1+" "+kelime2+" ")
                if flag == 0:
                    print("==> %s --> %s\n"%(y,correct(x)))
                    fa.write("%s --> %s"%(y,correct(x)))
                    fa.write("\n")
                    if c == 0:
                        lines = lines.replace(" "+x+" "," "+correct(x)+" ")
                    elif c==1:
                        lines2 = lines2.replace(" "+x+" "," "+correct(x)+" ")
                    else:
                        lines3 = lines3.replace(" "+x+" "," "+correct(x)+" ")

        if c == 0 :
            fpp.write(lines)
        elif c ==1:
            fnn.write(lines2)
        else:
            fno.write(lines3)
    fa.close()
    fpp.close()
    fnn.close()
    fno.close()

def fixapply():

    import re
    import collections

    def words(text): return re.findall('[a-z]+', text.lower())

    def train(features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    NWORDS = train(words(file('big.txt').read()))

    alphabet = 'abcdefghijklmnopqrstuvyz'

    def edits1(word):
        splits = [(word[:i], word[i:])
                  for i in range(len(word) + 1)]
        inserts = [a + c + b
                            for a, b in splits
                                for c in alphabet]
        deletes = [a + b[1:]
                   for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:]
                      for a, b in splits
                        if len(b)>1]
        replaces = [a + c + b[1:]
                    for a, b in splits
                        for c in alphabet
                            if b]
        return set(inserts + transposes + replaces + deletes)

    def known_edits2(word):
        return set(e2
                        for e1 in edits1(word)
                            for e2 in edits1(e1)
                                if e2 in NWORDS)

    def known(words): return set(w
                                    for w in words
                                        if w in NWORDS)

    def correct(word):
        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
        return max(candidates, key=NWORDS.get)
    while True:
        flag = 0
        kelime = raw_input("Cikis icin halt\nDuzeltilecek Kelime: ")
        if kelime=="halt" or "":
            break
        else:
            if kelime == correct(kelime):
                print("\n*** Girilen Kelime Dogru ***\n")
            else:
                y=kelime
                if len(kelime)>4:
                    if kelime[(len(kelime)-3):len(kelime)]=='cem':
                        kelime = kelime[0:len(kelime)-3]+'cegim'
                    if kelime[(len(kelime)-3):len(kelime)]=='cam':
                        kelime = kelime[0:len(kelime)-3]+'cagim'
                    if kelime[(len(kelime)-3):len(kelime)]=='caz':
                        kelime = kelime[0:len(kelime)-3]+'cagiz'
                    if kelime[(len(kelime)-3):len(kelime)]=='cez':
                        kelime = kelime[0:len(kelime)-3]+'cegiz'
                    if kelime[(len(kelime)-3):len(kelime)]=='yom':
                        kelime = kelime[0:len(kelime)-3]+'yorum'
                    if kelime[(len(kelime)-3):len(kelime)]=='yoz':
                        kelime = kelime[0:len(kelime)-3]+'yoruz'
                    if kelime[(len(kelime)-3):len(kelime)]=='in':
                        kelime = kelime[0:len(kelime)-2]+'nim'
                if "her" == kelime[0:3] and kelime[3:len(kelime)]==correct(kelime[3:len(kelime)]):
                    kelime1 = kelime[0:3]
                    kelime2 = kelime[3:len(kelime)]
                    print("\n==>%s -->%s %s\n"%(kelime,kelime1,kelime2))
                    flag = 1
                if "ayfon" == kelime[0:5]:
                    kelime1 = "iphone"
                    print("\n==>%s -->%s\n"%(kelime,kelime1))
                    flag = 1
                if "daha" == kelime[len(kelime)-4:len(kelime)] and kelime[0:len(kelime)-4]==correct(kelime[0:len(kelime)-4]):
                    kelime1 = kelime[len(kelime)-4:len(kelime)]
                    kelime2 = kelime[0:len(kelime)-4]
                    print("\n==>%s -->%s %s\n"%(kelime,kelime2,kelime1))
                    flag = 1
                if "tsk" == kelime[0:3]:
                    kelime1 = "tesekkur"
                    print("\n==>%s -->%s\n"%(kelime,kelime1))
                    flag = 1
                if "n" == kelime[0:1] and kelime[1:len(kelime)]==correct(kelime[1:len(kelime)]):
                    kelime1 = kelime[0:1]+"e"
                    kelime2 = kelime[1:len(kelime)]
                    print("\n==>%s -->%s %s\n"%(kelime,kelime1,kelime2))
                    flag = 1
                if "nap" == kelime[0:3]:
                    kelime1 = kelime[0:1]+"e"
                    kelime2 = correct("yap"+kelime[3:len(kelime)])
                    print("\n==>%s -->%s %s\n"%(kelime,kelime1,kelime2))
                    flag = 1
                if "cak" == kelime[len(kelime)-3:len(kelime)]:
                    kelime1 = kelime[0:len(kelime)-3]+"a"+kelime[len(kelime)-3:len(kelime)]
                    print("\n==>%s -->%s\n"%(kelime,correct(kelime1)))
                    flag = 1
                if "bi" == kelime[0:2] and kelime[2:len(kelime)] == correct(kelime[2:len(kelime)]):
                    kelime1 = kelime[0:2]+"r"
                    kelime2 = kelime[2:len(kelime)]
                    print("\n==>%s -->%s %s\n"%(kelime,kelime1,kelime2))
                    flag=1
                if flag == 0:
                    print("\n==> %s --> %s ***\n"%(y,correct(kelime)))


def origin():
    import re
    import collections

    def words(text): return re.findall('[a-z]+', text.lower())

    def train(features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    NWORDS = train(words(file('big.txt').read()))

    alphabet = 'abcdefghijklmnopqrstuvyz'

    def edits1(word):
        splits = [(word[:i], word[i:])
                  for i in range(len(word) + 1)]
        inserts = [a + c + b
                            for a, b in splits
                                for c in alphabet]
        deletes = [a + b[1:]
                   for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:]
                      for a, b in splits
                        if len(b)>1]
        replaces = [a + c + b[1:]
                    for a, b in splits
                        for c in alphabet
                            if b]
        return set(inserts + transposes + replaces + deletes)

    def known_edits2(word):
        return set(e2
                        for e1 in edits1(word)
                            for e2 in edits1(e1)
                                if e2 in NWORDS)

    def known(words): return set(w
                                    for w in words
                                        if w in NWORDS)

    def correct(word):
        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
        return max(candidates, key=NWORDS.get)
    while True:
        y = raw_input("kok bul:")
        if y == "halt":
            break
        else:
            for t in range(2,len(y)+1):
                if y[0:t]+"mak" == correct(y[0:t]+"mak") or y[0:t]+"mek" == correct(y[0:t]+"mek"):
                    print("kok = %s"%y[0:t])
                    break


def fillwords():
    global words
    global plines
    global nlines
    global nolines
    rpt = 0
    with open("fixed_lg_pozitif.txt") as fn:
        lines = fn.read()
        plines = lines.split('\n')
    wordlist = re.sub("[^\w]"," ",lines).split()
    fn.close()
    with open("fixed_lg_negatif.txt") as fp:
        lines2 = fp.read()
        nlines =lines2.split('\n')
    wordlist2 = re.sub("[^\w]"," ",lines2).split()
    fp.close()
    with open("fixed_lg_notr.txt") as fno:
        lines3 = fno.read()
        nolines =lines3.split('\n')
    wordlist3 = re.sub("[^\w]"," ",lines3).split()
    fno.close()
    # except:
    #     print("Dosyalar bulunamad?...")
    #     input(" ")
    #     return 0
    words=[]
    xx=0
    def isequal(q,p):
        for z in range(0,q+1,4):
            try:
                if words[z]==wl[p]:
                    return z
            except:
                pass
    for x in range(0,(len(wordlist)+len(wordlist3)+len(wordlist3))*4):
        words.append('0')
    for times in range(3):
        if times ==0:
            wl=wordlist
        elif times == 1:
            wl=wordlist2
        else:
            wl=wordlist3
        print(len(wl))
        print(len(words))
        xy=0
        while (xy<len(wl)):
            if xx == 0 and wl==wordlist:
                words[xx]=wl[xy]
                xy+=1
                xx+=1
                words[xx]='1'
            else:
                if xx%4==0:
                    if isequal((xx),xy)== None:
                        words[xx]=wl[xy]
                        if times ==0:
                            words[xx+1]='1'
                        elif times ==1:
                            words[xx+2]='1'
                        else:
                            words[xx+3]='1'
                        xy+=1
                        xx+=1
                    else:
                        if times ==0:
                            a=1
                        elif times ==1:
                            a=2
                        else:
                            a=3
                        deger = isequal((xx),xy)
                        countstr = words[deger+a]
                        countint = int(countstr)
                        countint +=1
                        words[deger+a]=countint
                        xy+=1
                        rpt+=1
                else:
                    xx+=1

def getwcounts():
    
    # try:
    fillwords()
    ss=0
    with open("Durum.txt") as fa:
        fa=open("Durum.txt",'w')
        for xa in words:
            fa.write('%s '%xa)
            ss+=1
            if ss%4==0:
                fa.write('\n')
        fa.close()
    # for xa in range(len(words)):
    #     if xa%4==3:
    #          print(words[xa-3],' ',words[xa-2],' ',words[xa-1],' ',words[xa])

def egetwcounts():
    import xlwt
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Python Sheet 1",cell_overwrite_ok=True)
    fillwords()
    for inex in range(len(words)):
        stxt = int(inex/4)
        if inex%4==0:
            sheet1.write(stxt,0,str(words[inex]))
        elif inex%4==1:
            sheet1.write(stxt,1,int(words[inex]))
        elif inex%4==2:
            sheet1.write(stxt,2,int(words[inex]))
        else:
            sheet1.write(stxt,3,int(words[inex]))
    book.save('words.xls')
    # ss=0
    # with open("Durum.txt") as fa:
    #     fa=open("Durum.txt",'w')
    #     for xa in words:
    #         fa.write('%s '%xa)
    #         ss+=1
    #         if ss%4==0:
    #             fa.write('\n')
    #     fa.close()
    # for xa in range(len(words)):
    #     if xa%4==3:
    #          print(words[xa-3],' ',words[xa-2],' ',words[xa-1],' ',words[xa])
    # return

def getattributes():
    import math
    global selcatt
    fed = raw_input("-------------------------------------------------\nEnformasyon Degeri: \nLutfen 0 ile 2 arasi bir deger girin: ")
    fmink = raw_input("-------------------------------------------------\nMin. Deger: \nLutfen 1 ile 7 arasi bir deger girin: ")
    fmink = int(fmink)
    fed = float(fed)
    fillwords()
    selcatt = [':)',':(',':d']
    for em in range(int(len(words)/4)):
        if em%4==3:
            if ((int(words[em-2])+int(words[em-1])+int(words[em]))>=fmink):
                if(float(math.fabs(float(math.fabs(int(words[em-2])-int(words[em-1]))+math.fabs(int(words[em-2])-int(words[em]))+math.fabs(int(words[em-1])-int(words[em])))/float(int(words[em-2])+int(words[em-1])+int(words[em]))))>=fed):
                    if(len(words[em-3])>2):
                        selcatt.append(words[em-3])
                        # print(words[em-3]+"-->"+str(float(math.fabs(float(math.fabs(int(words[em-2])-int(words[em-1]))+math.fabs(int(words[em-2])-int(words[em]))+math.fabs(int(words[em-1])-int(words[em])))/float(int(words[em-2])+int(words[em-1])+int(words[em]))))))
                        # selcatt.append(math.fabs((int(words[em-2])-int(words[em-1]))/(int(words[em-2])+int(words[em-1])+int(words[em]))))

def writeatt():
    getattributes()
    # for sb in range(int(len(plines)+len(nlines)+len(nolines))*(int(len(selcatt)/2))):
    #     zeros.append('0')
    with open("REF.txt") as fa:
        fa=open("REF.txt",'w')
        fa.writelines('@relation APPLE')
        fa.write('\n\n')
        for xa in selcatt:
            fa.write('@Attribute %s REAL'%xa)
            fa.write('\n')
        fa.writelines('@attribute class-att {positive,negative,notr}')
        fa.write('\n\n')
        fa.writelines('@data')
    for i in range(3):
        zeros=[]
        if i == 0:
            wstate = plines
            state ='positive'
        elif i == 1:
            wstate = nlines
            state = 'negative'
        else:
            wstate = nolines
            state = 'notr'
        for xr in range(len(wstate)):
            swords = wstate[xr].split(' ')
            swords2 = []
            for sww in swords:
                if sww not in swords2:
                    swords2.append(sww)
            for sa in selcatt:
                aflag = True
                for sw in swords2:
                    if sa == sw:
                        # sindex = selcatt.index(sa)
                        zeros.append('1')
                        aflag = False
                        filter(lambda a:a !=sw, swords)
                if aflag==True:
                    zeros.append('0')
        pr = len(selcatt)
        prp = 0
        for xxr in zeros:
            if prp%pr==0:
                if prp>=len(selcatt):
                    fa.write(state)
                fa.write('\n')
                fa.write('%s,'%xxr)
            else:
                fa.write('%s,'%xxr)
            prp+=1
        fa.write(state)
    fa.close()
    return




while True:
    inp = wanted()
    if inp=="halt":
       break
    if inp=="getwcounts":
        getwcounts()
        print("\nislem tamamlandi....\n")
    elif inp=="egetwcounts":
        egetwcounts()
        print("\nislem tamamlandi....\n")
    elif inp=="getatt":
        writeatt()
        print("\nislem tamamlandi....\n")
    elif inp=="getfix":
        getwordfix()
    elif inp=="sfix":
        fixapply()
    elif inp=="forg":
        origin()


