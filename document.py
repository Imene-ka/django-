from pymongo import MongoClient
import basededonnee
import term
import math
from nltk.tokenize import word_tokenize
#client=MongoClient()
#db=client['my-database']
#col=db['document']
#col.drop()


"""if col.find().count()==0 :
   i=0
   fichier=open("/home/client/project/firstproject/templates/Corpus_OHSUMED.txt","r")
   for ligne in fichier :
      if ligne=="<DOC>\r\n":
         i=i+1
      else :
         if ligne=="</DOC>\r\n":
              col.insert_one({"num":i,"titre":titre,"abstract":abstract})
         else :
            if ligne!="<ABSTRACT>\r\n" :
              if "<TITLE>" in ligne :
                 l=ligne.replace("<TITLE>","")
                 l=l.replace("</TITLE>","")
                 titre=l.replace("\r\n","")
              else :
                 if "</ABSTRACT>" in ligne :
                    l=ligne.replace("</ABSTRACT>","")
                    abstract=l.replace("\r\n","") """


"""json_list=db.get_ligne({"doc":2})
for i in json_list :
   print i[u"poids"]"""
def exist(e,l):
     for e1 in l :
       if e1.get_nom() == e.get_nom() :
          return True
     return False
def calculet(t,nbr):
    result=[]
    h=list(set(t))
    for mot in h :
        tm=term.t(nbr,mot,0,1,0,0,frequence(mot,t),0)
        result.append(tm)
    return result
def calculea(a,nbr):
    result=[]
    h=list(set(a))
    for mot in h :
        tm=term.t(nbr,mot,0,0,1,frequence(mot,a),0,len(a))
        result.append(tm)
    return result
def calcule_frequence(t,a,nbr):
     r1=calculet(t,nbr)
     r2=calculea(a,nbr)
     result=[]
     for mot1 in r1 :
       for mot2 in r2 :
          if mot1.get_nom()==mot2.get_nom() :
             result.append(term.t(nbr,mot1.get_nom(),0,1,1,mot2.get_fa(),mot1.get_ft(),mot2.get_a()))   
     for m1 in r1 :
       if not exist(m1,result) :
           result.append(m1) 
     for m2 in r2 :
       if not exist(m2,result) :
           result.append(m2) 
     return result 
def calcule(s):
    nbr=0
    i=0
    cons="bcdfghjklmnpqrstvwxz"
    voy="aeouyi"
    while i<(len(s)-1):
       if ((s[i] in cons) and (s[i+1] in voy)) :
          nbr=nbr+1
       i=i+1
    return nbr

def verif(s):
    if s.endswith("sses") :
       s=s[0:(len(s)-4)]+"es"
    if s.endswith("ies") :
       s=s[0:(len(s)-3)]+"i"
    if s.endswith("s") :
       s=s[0:(len(s)-1)]
    if s.endswith("ed") and calcule(s[0:(len(s)-2)])>0 :
       s=s[0:(len(s)-2)]
    if s.endswith("ing") and calcule(s[0:(len(s)-3)])>0 :
       s=s[0:(len(s)-3)]
    if s.endswith("y") :
       s=s[0:(len(s)-1)]+"i"
    if s.endswith("ational") and calcule(s[0:(len(s)-7)])>0:
       s=s[0:(len(s)-7)]+"ate"
    if s.endswith("tional") and calcule(s[0:(len(s)-6)])>0 :
       s=s[0:(len(s)-6)]+"tion"
    if s.endswith("izer") and calcule(s[0:(len(s)-4)])>0:
       s=s[0:(len(s)-4)]+"ize"
    if s.endswith("alize") and calcule(s[0:(len(s)-5)])>0:
       s=s[0:(len(s)-5)]+"al"
    if s.endswith("ize") and calcule(s[0:(len(s)-3)])>1 :
       s=s[0:(len(s)-3)]
    return s
def elimin(ligne):
    new_line=[]
    for l in ligne :
       new_line.append(verif(l))
    return new_line
def not_stoplist(l,db):
    stoplist=db.get_stoplist()
    for s in stoplist :
        if (l in s) :
           return False
    return True
             
def elimine_mot_vide(db,ligne):
    car=["!",";",",",":",".","?","-","_","(",")","{","}","[","]"]
    new_line=[]
    for l in ligne :
       if l not in car and not_stoplist(l,db):
           new_line.append(l) 
    return new_line
def calcule_poids(t,a):
     r1=calcule_poidst(t)
     r2=calcule_poidsa(a)
     result=[]
     for mot1 in r1 :
       for mot2 in r2 :
          if mot1.get_nom()==mot2.get_nom() :
             result.append(trme.t(mot1.get_nom(),mot1.get_poids()+mot2.get_poids(),1,1))   
     for m1 in r1 :
       if not exist(m,result) :
           result.append(m1) 
     for m2 in r2 :
       if not exist(m,result) :
           result.append(m2) 
     return result
def frequence(m,l):
    f=0
    for mot in l :
      if mot==m :
         f=f+1
    return f
def calcule_poids(titre,abstract,ft,fa,a,nbr):
     if titre==0:
        p=((float(fa)/float(a))*math.log(float(nbr)/2001,10))
     else :
        if abstract == 0 :
           p=float(ft)
        else :
           p=((float(fa)/float(a))*math.log(float(nbr)/2001,10))+float(ft)
     return p
def update_base(db):
    nb=2001
    i=1
    while i<nb+1 :
       json_list=db.get_ligne({"doc":i})
       for j in json_list :
          db.update_ligne({"term":j[u"term"],"doc":j[u"doc"]},{"poids":calcule_poids(j[u"titre"],j[u"abstract"],j[u"ft"],j[u"fa"],j[u"a"],db.get_ligne({"term":j[u"term"]}).count())})
       i=i+1
def nbr_doc():
   nbr=0
   fichier=open("/home/client/project/firstproject/templates/Corpus_OHSUMED.txt","r")
   for ligne in fichier :
      if ligne=="<DOC>\r\n":
         nbr=nbr+1
   fichier.close() 
   return nbr
def tokenizez(db):
   i=0
   fichier=open("/home/client/project/firstproject/templates/Corpus_OHSUMED.txt","r")
   for ligne in fichier :
      if ligne=="<DOC>\r\n":
         i=i+1
      else :
         if ligne=="</DOC>\r\n":
              r=calcule_frequence(titre,abstract,i)
              for result in r :
                    #tem=term.t(i,result.get_nom(),0,result.get_titre(),result.get_abstract(),result.get_ft(),result.get_fa(),result.get_a())
                    js={"doc":i,"term":result.get_nom(),"poids":0.0,"titre":result.get_titre(),"abstract":result.get_abstract(),"fa":result.get_fa(),"ft":result.get_ft(),"a":result.get_a()}
                    db.insert_doc(js)
         else :
           if ligne!="<ABSTRACT>\r\n" :
              if "<TITLE>" in ligne :
                 l=ligne.replace("<TITLE>","")
                 l=l.replace("</TITLE>","")
                 l=l.replace("\r\n","")
                 l=l.lower()
                 titre=elimin(elimine_mot_vide(db,word_tokenize(l)))
              else :
                 if "</ABSTRACT>" in ligne :
                     l=ligne.replace("</ABSTRACT>","")
                     l=l.replace("\r\n","")
                     l=l.lower()
                     abstract=elimin(elimine_mot_vide(db,word_tokenize(l)))
   
   fichier.close()
#print col.find().count()
#c=col.find_one({'num':2})
#print c[u'titre']
db=basededonnee.database()
db.collection.drop()
print "fin de supprission"
"""print db.collection.count()
update_base(db)
json_list=db.get_ligne({"doc":2})
for i in json_list :
   print i
   print i[u"poids"]"""
#print calcule_poids(0,1,0,2,54,14)
#print calcule_poids(1,0,5,0,0,17)
#print calcule_poids(1,1,4,5,87,17)
print db.collection.find().count()
tokenizez(db)
print "fin token"
update_base(db)
print "fin update"
print db.collection.find().count()
print nbr_doc()

             
