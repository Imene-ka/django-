from pymongo import MongoClient
import nltk
import math
from nltk.tokenize import word_tokenize
import term
import basededonnee

def calcule(s):
    nbr=0
    i=0
    cons="bcdfghjklmnpqrstvwxz"
    voy="aeouyi"
    while i<(len(s)-1):
       if ((s[i] in cons) and (s[i+1] in voy)) or ((s[i+1] in cons) and (s[i] in voy)) :
          nbr=nbr+1
       i=i+1
    return nbr

def verif(s):
    m=calcule(s)
    if s.endswith("sses") :
       s=s[0:(len(s)-4)]+"es"
    if s.endswith("ies") :
       s=s[0:(len(s)-3)]+"i"
    if s.endswith("s") :
       s=s[0:(len(s)-1)]
    if s.endswith("ed") and m>0 :
       s=s[0:(len(s)-2)]
    if s.endswith("ing") and m>0 :
       s=s[0:(len(s)-3)]
    if s.endswith("y") :
       s=s[0:(len(s)-1)]+"i"
    if s.endswith("ational") and m>0:
       s=s[0:(len(s)-7)]+"ate"
    if s.endswith("tional") and m>0 :
       s=s[0:(len(s)-6)]+"tion"
    if s.endswith("izer") and m>0:
       s=s[0:(len(s)-4)]+"ize"
    if s.endswith("alize") and m>0:
       s=s[0:(len(s)-5)]+"al"
    if s.endswith("ize") and m>1 :
       s=s[0:(len(s)-3)]
    return s
def elimin(ligne):
    new_line=[]
    for l in ligne :
       new_line.append(verif(l))
    return new_line
def not_stop_list(term,stoplist):
    for i in stoplist :
       if term in i :
          return False
    return True
def elimine_mot_vide(stoplist,ligne):
    car=["!",";",",",":",".","?","-","_","(",")","{","}","[","]"]
    new_line=[]
    for l in ligne :
       if (l not in car) and not_stop_list(l,stoplist):
          new_line.append(l)
    return new_line
def exist(e,l):
     for e1 in l :
       if e1.get_nom() == e.get_nom() :
          return True
     return False
def calculet(ti,t,nbr):
    result=[]
    h=list(set(t))
    for mot in h :
        pos=[i for i,x in enumerate(ti,1) if x==mot]
        tm=term.t(nbr,mot,0,1,0,0,t.count(mot),0,pos)
        result.append(tm)
    return result
def calculea(ai,a,nbr):
    result=[]
    h=list(set(a))
    for mot in h :
        pos=[i for i,x in enumerate(ai,1) if x==mot]
        tm=term.t(nbr,mot,0,0,1,a.count(mot),0,len(a),pos)
        result.append(tm)
    return result
def calcule_frequence(ti,ai,t,a,nbr):
     r1=calculet(ti,t,nbr)
     r2=calculea(ai,a,nbr)
     result=[]
     for mot1 in r1 :
       for mot2 in r2 :
          if mot1.get_nom()==mot2.get_nom() :
             pos=mot1.get_pos()+mot2.get_pos()
             result.append(term.t(nbr,mot1.get_nom(),0,1,1,mot2.get_fa(),mot1.get_ft(),mot2.get_a(),pos))   
     for m1 in r1 :
       if not exist(m1,result) :
           result.append(m1) 
     for m2 in r2 :
       if not exist(m2,result) :
           result.append(m2) 
     return result 
def calcule_poids(titre,abstract,ft,fa,a,nbr):
     if titre==0:
        p=((float(fa)/float(a))*math.log(2001/float(nbr),10))
     else :
        if abstract == 0 :
           p=float(ft)
        else :
           p=((float(fa)/float(a))*math.log(2001/float(nbr),10))+float(ft)
     return p
def update_base(db):
    nb=2001
    i=1
    while i<nb+1 :
       json_list=db.get_ligne({"doc":i})
       for j in json_list :
          db.update_ligne({"term":j[u"term"],"doc":j[u"doc"]},{"poids":calcule_poids(j[u"titre"],j[u"abstract"],j[u"ft"],j[u"fa"],j[u"a"],db.count_term({"term":j[u"term"]}))})
       i=i+1
def tokenizez(db):
   i=1
   stoplist=db.get_stoplist()
   while i<2001 :
     document=db.get_document({"num":i})
     t=elimin(word_tokenize(document[u"titre"]))
     a=elimin(word_tokenize(document[u"abstract"]))
     titre=elimine_mot_vide(stoplist,t)
     abstract=elimine_mot_vide(stoplist,a)
     r=calcule_frequence(t,a,titre,abstract,i)
     for result in r :
         js={"doc":i,"term":result.get_nom(),"poids":0.0,"titre":result.get_titre(),"abstract":result.get_abstract(),"fa":result.get_fa(),"ft":result.get_ft(),"a":result.get_a(),"pos":result.get_pos()}
         db.insert_doc(js)
     i=i+1
   update_base(db)   
db=basededonnee.database()
if db.get_collection_count()!=0 :
    db.collection.drop()
    print "ok la collection vide "+str(db.get_collection_count())
if db.get_collection_count()==0 :
    tokenizez(db)
    print "ok la collection remplir"
print db.get_collection_count()
result=db.get_ligne({"doc":2})
som=0
for i in result :
   som=som+i[u"fa"]+i[u"ft"]
print som
print db.get_ligne({"doc":2}).count()

