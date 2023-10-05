#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
#get_ipython().run_line_magic('matplotlib', 'inline')
import itertools
import json


# In[5]:


data = pd.read_csv("youtube-comments.csv",error_bad_lines=False,usecols =["Comment"])
data.head()


# In[6]:


data.info()


# In[7]:


data[data['Comment'].duplicated(keep=False)].sort_values('Comment').head(8)


# In[8]:


data = data.drop_duplicates('Comment')


# In[9]:


punc = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
stop_words = text.ENGLISH_STOP_WORDS.union(punc)
desc = data['Comment'].values
vectorizer = TfidfVectorizer(stop_words = list(stop_words))
X = vectorizer.fit_transform(desc)


# In[10]:


word_features = vectorizer.get_feature_names_out()
print(len(word_features))
print(word_features[100:300])
wordFile=open("wordsOutput.txt", "w", encoding="utf-8")
outputString=""
for _ in word_features:
    outputString+=_+"\n"
wordFile.write(outputString)
wordFile.close()


# In[11]:


stemmer = SnowballStemmer('english')
tokenizer = RegexpTokenizer(r'[a-zA-Z\']+')

def tokenize(text):
    return [stemmer.stem(word) for word in tokenizer.tokenize(text.lower())]


# In[12]:


vectorizer2 = TfidfVectorizer(stop_words = list(stop_words), tokenizer = tokenize)
X2 = vectorizer2.fit_transform(desc)
word_features2 = vectorizer2.get_feature_names_out()
print(len(word_features2))
print(word_features2[:50]) 


# In[13]:


vectorizer3 = TfidfVectorizer(stop_words = list(stop_words), tokenizer = tokenize, max_features = 1000)
X3 = vectorizer3.fit_transform(desc)
words = vectorizer3.get_feature_names_out()


# In[14]:


from sklearn.cluster import KMeans
wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
    kmeans.fit(X3)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11),wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('elbow.png')
plt.show()


# In[15]:


kmeans = KMeans(n_clusters = 3, n_init = 20) 
kmeans.fit(X3)
# We look at 3 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))


# In[16]:


# print("Prediction")

Y = vectorizer3.transform(data["Comment"].values)
prediction = kmeans.predict(Y)
# print(prediction)

c1,c2,c3=[],[],[]

for (i,j) in zip(prediction,data["Comment"].values):
    if i == 0:
        c1.append(j)
    elif i == 1:
        c2.append(j)
    elif i == 2:
        c3.append(j)
    

print(json.dumps(c1[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c2[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c3[:10], indent = 2, ensure_ascii = False),"\n\n")
ans = pd.DataFrame()
ans["prediction"] = prediction
ans["prediction"].value_counts()


# In[17]:


que = ["what", "why", "when", "where", "name", "how", "does", "which", "would", "could", "should", "has", "have", "whom", "whose", "question"]

# This is amazing. Thank you for showing all these sensor capabilities. Really inspires ideas for me
count = []
count1 = 0
for i in c1:
    z=i.lower()
    if any(q in z for q in que):
        count1+=1
count.append(count1)

count1=0
for i in c2:
    z=i.lower()
    if any(q in z for q in que):
        count1+=1
count.append(count1)

count1=0
for i in c3:
    z=i.lower()
    if any(q in z for q in que):
        count1+=1
count.append(count1)

print(count)
# print(json.dumps(questions, indent = 2, ensure_ascii = False))


# In[18]:


kmeans = KMeans(n_clusters = 5, n_init = 20)
kmeans.fit(X3)
# We look at 5 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))


# In[23]:


print("Prediction")

Y = vectorizer3.transform(data["Comment"].values)
prediction = kmeans.predict(Y)
# print(prediction)

c1,c2,c3,c4,c5=[],[],[],[],[]

for (i,j) in zip(prediction,data["Comment"].values):
    if i == 0:
        c1.append(j)
    elif i == 1:
        c2.append(j)
    elif i == 2:
        c3.append(j)
    elif i == 3:
        c4.append(j)
    elif i == 4:
        c5.append(j)
    
outputFile = open("kmeansOutput.txt","w")
outputFile.write(json.dumps(c1[:10], indent = 2))
outputFile.write(json.dumps(c2[:10], indent = 2))
outputFile.write(json.dumps(c3[:10], indent = 2))
outputFile.write(json.dumps(c4[:10], indent = 2))
outputFile.write(json.dumps(c5[:10], indent = 2))
outputFile.close()
print(json.dumps(c1[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c2[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c3[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c4[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c5[:10], indent = 2, ensure_ascii = False),"\n\n")

ans = pd.DataFrame()
ans["prediction"] = prediction
ans["prediction"].value_counts()


# In[30]:


que = ["what", "why", "when", "where", "name", "how", "does", "which", "would", "could", "should", "has", "have", "whom", "whose", "question"]

# This is amazing. Thank you for showing all these sensor capabilities. Really inspires ideas for me
count = []
count1 = 0
for i in c1:
    z=i.lower()
    if any(q in z for q in que):
        count1+=1
count.append(count1)

count1=0
for i in c2:
    z=i.lower()
    if any(q in z for q in que):
        count1+=1
count.append(count1)

count1=0
for i in c3:
    z=i.lower()
    if any(q in z for q in que):
        count1+=1
count.append(count1)

count1=0
for i in c4:
    z=i.lower()
    if any(q in z for q in que):
        count1+=1
count.append(count1)

count1=0
for i in c5:
    z=i.lower()
    if any(q in z for q in que):
        count1+=1
count.append(count1)

print(count)


# In[33]:


kmeans = KMeans(n_clusters = 6, n_init = 20)
kmeans.fit(X3)
# We look at 6 the clusters generated by k-means.
common_words = kmeans.cluster_centers_.argsort()[:,-1:-26:-1]
for num, centroid in enumerate(common_words):
    print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))

print("Prediction")

Y = vectorizer3.transform(data["Comment"].values)
prediction = kmeans.predict(Y)
# print(prediction)

c1,c2,c3,c4,c5,c6=[],[],[],[],[],[]

for (i,j) in zip(prediction,data["Comment"].values):
    if i == 0:
        c1.append(j)
    elif i == 1:
        c2.append(j)
    elif i == 2:
        c3.append(j)
    elif i == 3:
        c4.append(j)
    elif i == 4:
        c5.append(j)
    elif i == 5:
        c6.append(j)

print(json.dumps(c1[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c2[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c3[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c4[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c5[:10], indent = 2, ensure_ascii = False),"\n\n")
print(json.dumps(c6[:10], indent = 2, ensure_ascii = False),"\n\n")

ans = pd.DataFrame()
ans["prediction"] = prediction
ans["prediction"].value_counts()
# In[22]:


que = ["what", "why", "when", "where", "name", "how", "does", "which", "would", "could", "should", "has", "have", "whom", "whose", "question"]

# This is amazing. Thank you for showing all these sensor capabilities. Really inspires ideas for me

questions = []
for i in data["Comment"]:
    z=i.lower()
    if any(q in z for q in que):
        questions.append(i)
        
print(len(questions))
print(json.dumps(questions, indent = 2, ensure_ascii = False))
questionsFile=open("questionsOutput.txt","w",encoding="utf-8")
questionsFile.write(json.dumps(questions,indent=2, ensure_ascii=False))
questionsFile.close()


# In[ ]:



