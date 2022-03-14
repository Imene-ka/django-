from pymongo import MongoClient

class database():
      collection=None
      def __init__(self):
            self.client=MongoClient()
            self.db=self.client['my-database']
            self.collection=self.db['collection']
            self.stop_list=self.db['stoplist']
            self.document=self.db['document']
            if self.document.find().count()==0:
                set_document()
            if self.stop_list.find().count()==0 :
                fichier=open("/home/client/project/firstproject/templates/stoplist.txt","r")
                for ligne in fichier:
                  if ligne[1:]!="\r\n":
                     oj={'alpha':ligne[0],'mot':ligne[0:(len(ligne)-2)]}
                     self.stop_list.insert_one(oj)
                fichier.close()
      def get_collection_count(self):
          return self.collection.find().count()
      def count_term(self,condition):
           c=self.collection.find(condition).count()
           return c
      def get_collection(self):
           return self.collection.find()
      def insert_doc(self,data):
           self.collection.insert_one(data)
      def update_ligne(self,condition,data):
           self.collection.update_one(condition,{"$set":data})
      def get_ligne(self,condition):
           c=self.collection.find(condition)
           return c
      def get_stoplist(self):
           s=self.stop_list.find()
           stoplist=[]
           for e in s :
              stoplist.append(str(e[u'mot']))
           return stoplist
      def set_document(self):
            i=0
            fichier=open("/home/client/project/firstproject/templates/Corpus_OHSUMED.txt","r")
            for ligne in fichier :
               if ligne=="<DOC>\r\n":
                   i=i+1
               else :
                  if ligne=="</DOC>\r\n":
                      document.insert_one({"num":i,"titre":titre,"abstract":abstract})
                  else :
                     if ligne!="<ABSTRACT>\r\n" :
                         if "<TITLE>" in ligne :
                             l=ligne.replace("<TITLE>","")
                             l=l.replace("</TITLE>","")
                             titre=l.replace("\r\n","")
                         else :
                             if "</ABSTRACT>" in ligne :
                                 l=ligne.replace("</ABSTRACT>","")
                                 abstract=l.replace("\r\n","") 
      def get_document(self,condition):
           return self.db.document.find_one(condition)
           


           







