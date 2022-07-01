#!/usr/bin/env python
# coding: utf-8

# ## Exploring Data

# In[120]:


import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


# In[2]:


# Get csv data
path = 'C:/Users/1412r/OneDrive/Desktop/Thesis/Data/socialchoicedata.csv' # Enter the local path
df = pd.read_csv(path, header=0)

# Housekeeping
index = [i for i in range(1, len(df)+1)]
df.drop('Unnamed: 0', inplace=True, axis=1)
df.set_index(pd.Index(index), inplace=True)
df.head()
## df.isnull().sum() # checking for empty values along columns


# In[3]:


# Accounting for switch in toprow payoff being mine or others'

df['TopRow'] = df['TopRowPayoffs']=='Me'

df['MeLeft'] = df['TopRow']*df['ValueUpLeft']+(1-df['TopRow'])*df['ValueLowerLeft'] # When top row is mine take my payoff
df['MeRight'] = df['TopRow']*df['ValueUpRight']+(1-df['TopRow'])*df['ValueLowerRight'] # otherwise take the bottom row payoff

df['OtherLeft'] = df['TopRow']*df['ValueLowerLeft']+(1-df['TopRow'])*df['ValueUpLeft']
df['OtherRight'] = df['TopRow']*df['ValueLowerRight']+(1-df['TopRow'])*df['ValueUpRight']


# In[4]:


df.head()


# In[5]:


# Dependence of choice on who gets more

diff_L = df['MeLeft']-df['OtherLeft'] # if positive then I get more than the other guy if I choose Left
diff_R = df['MeRight']-df['OtherRight']

# Plotting choice vs who gets more
fig, axes = plt.subplots(nrows=1, ncols=2, sharey='row')
fig.suptitle('Dependence of choice on who gets more')

bp_L = sns.boxplot(x=df['LeftRight'], y=diff_L, ax=axes[0])
bp_L.set_ylabel('Difference of payoffs in Left')
bp_R = sns.boxplot(x=df['LeftRight'], y=diff_R, ax=axes[1])
bp_R.set_ylabel('Difference of payoffs in Right')


# The graphs are close to being mirror images, that is because the reasons to choose Left when it is favourable would be the same when Right is choosen when it was favourable so both will produce the same result. Hence the mirror image.
# 
# This misses the information about if I choose more for me what happens to the other guy. These plots just compare that if I choose left how much more do it get from the other guy.
# 
# At average if the difference is close to zero participants accept the lottery, if it is close to -100 they reject the lottery and accept the other one. But it is not clear what participants do when the difference is close to 100, they more often reject the lottery but how to what extent do they accept the other lottery?
# 
# ***

# ### Comparision with other
# 
# Notations:
# Left: Left lottery
# Right: Right lottery
# 
# 
# 28/06/22:
# 
# Checking the decision made based on the difference of the payoffs in the two lotteries.
# - Set up data, auhtors changed the position where the payoffs were displyed, made it consistent
# - Set up two boxplots to see the likelihood of the choices between Left and Right. Choice is on x axis and difference in me payoff and other payoff is on the y axis.
# - Made two plots. One shows choice vs difference for Left, second for Right.
# 
# Observations
# - When Left gives me very less than other then I tend to reject it more often.
# - When Left gives more than other by a large margin (>100) tendency to accept decreases.
# - But there is a greater tendency to reject Left when the difference is even a little negative (ie other gets more then even 0).
# - So participants not so keen on accepting higher offers but keen on rejecting lower offers.
# 
# 
# 
# ### Utility maximization
# (After comparing self to other)
# 
# 29/06/22:
# 
# 
# 

# In[6]:


# Checking what happens in the upper half of the boxplot

# How much more does Left give compared to Right to me and to other respectively?
diff_me = df['MeLeft']-df['MeRight'] # If diff_me is positive I should like Left more than Right
diff_other = df['OtherLeft']-df['OtherRight']

# So when both lotteries give me more than the other I look for the lottery that gives me more
exp2 = diff_me>=0 # when left gives me more
exp1 = (diff_R>=100)&(diff_L>=100) # index for when both lotteries give me more than 100 wrt other
# print(sum(exp))


# In[7]:


# Plotting frequency
sns.catplot(x=df['LeftRight'][exp2&exp1], kind='count', data=df)


# Have no idea what is happening!

# ### Miscellaneous

# In[8]:


# Plotting kernel density plots for Me vs Other

fig1, axes1 = plt.subplots(nrows=1, ncols=2, sharey='row')
fig1.suptitle('Dependence of choice on who gets more')

kde1 = sns.kdeplot(x=df['LeftRight'], y=diff_L, ax=axes1[0])
## kde1.set_ylabel('Difference of payoffs in Left')
kde2 = sns.kdeplot(x=df['LeftRight'], y=diff_R, ax=axes1[1])
## kde2.set_ylabel('Difference of payoffs in Right')


# In[9]:


# Plotting kde plot for Left vs Right

fig2, axes2 = plt.subplots(nrows=1, ncols=2, sharey='row')
fig2.suptitle('Utility maximization')

kde3 = sns.kdeplot(x=df['LeftRight'], y=diff_me, ax=axes2[0])
## kde3.set_ylabel('Difference of payoffs for Me')
kde4 = sns.kdeplot(x=df['LeftRight'], y=diff_other, ax=axes2[1])
## kde4.set_ylabel('Difference of payoffs for Other')


# # Grid Search

# Method: Brute force
# 
# Split the data set into two: one in which participants choose self payoff more than other payoff and the other which is the other way round.
# - ignoring the entries where equal payoffs are chosen for both participants
# 
# then regress for alpha and beta seperately (using gridsearchcv)
# 
# 30/06/22:

# In[113]:


from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression


# In[152]:


# Preparing the data set for Gridsearch
# y is LeftRight
# x1 is self payoff
# x2 is other payoff
# y = (1-alpha)x1+(alpha)x2 in data_alpha and y = (1-beta)x1+(beta)x2


# In[125]:


df_alpha = pd.DataFrame(index=pd.Index(index), columns=['y', 'x1', 'x2'])
df_alpha[['y', 'x1', 'x2']] = df[['LeftRight', 'MeLeft', 'OtherLeft']][df['MeLeft']>df['OtherLeft']]
df_alpha[['y', 'x1', 'x2']] = df[['LeftRight', 'MeRight', 'OtherRight']][df['MeRight']>df['OtherRight']]
df_alpha.dropna(inplace=True)
df_alpha['x2'] = df_alpha['x2']-df_alpha['x1']
df_alpha.head()


# In[153]:


df_beta = pd.DataFrame(index=pd.Index(index), columns=['y', 'x1', 'x2'])
df_beta[['y', 'x1', 'x2']] = df[['LeftRight', 'MeLeft', 'OtherLeft']][df['MeLeft']<df['OtherLeft']]
df_beta[['y', 'x1', 'x2']] = df[['LeftRight', 'MeRight', 'OtherRight']][df['MeRight']<df['OtherRight']]
df_beta['x2'] = df_beta['x2']-df_beta['x1']
df_beta.dropna(inplace=True)
df_beta.head()


# In[149]:


grid = {'C': np.logspace(-6, 0, 50), 'penalty': ['l1', 'l2']} # 10 raised to the power -0.30102999566 gives 0.5
logreg=LogisticRegression(solver = 'liblinear')
logreg_cv=GridSearchCV(logreg,grid,cv=3,scoring='f1')

logreg_cv.fit(df_alpha[['x1', 'x2']], df_alpha['y'])

print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("best score :",logreg_cv.best_score_)


# In[157]:


grid = {'C': np.logspace(-6, -0.1249387366, 100), 'penalty': ['l1', 'l2']} # 10 raised to the power -0.1249387366 gives 0.75
logreg=LogisticRegression(solver = 'liblinear')
logreg_cv=GridSearchCV(logreg,grid,cv=3,scoring='f1')

logreg_cv.fit(df_beta[['x1', 'x2']], df_beta['y'])

print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("best score :",logreg_cv.best_score_)


# In[ ]:




