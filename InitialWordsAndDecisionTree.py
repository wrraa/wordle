
#说明：本文件只需要在更改了words_alpha.txt文件后运行一次，其他时候不需要运行

import os
import shutil
import numpy as np
from collections import Counter
from graphviz import Digraph
from multiprocessing import Pool,cpu_count

from GameLogic import mark,GuessState,filtrate_words

def initial_words():
    #把不同长度的单词分开，并写到不同的文件中
    with open ('words_alpha.txt') as word_file:
        words_lst=word_file.readlines()
        assert len(words_lst)==len(set(words_lst))
        words_lst=[word.strip() for word in words_lst]
        min_length=len(min(words_lst,key=len))
        if min_length<3:
            min_length=3
        max_length=len(max(words_lst,key=len))
        #check there are only letters in the word
        for word in words_lst:
            for letter in word:
                assert letter.isalpha()
        if os.path.exists('WordsClassifiedByLength')==True:
            shutil.rmtree('WordsClassifiedByLength')
        os.mkdir('WordsClassifiedByLength')
        for i in range(min_length,max_length+1):
            print('--- word_length: ',i,' ---')
            words_lst_of_length=[word for word in words_lst if len(word)==i]
            if len(words_lst_of_length)!=0:
                with open ('WordsClassifiedByLength\\Length_'+str(i)+'.txt','w') as file:
                    for word in words_lst_of_length:
                        file.write(word+'\n')


def load_words(word_length):
    with open('WordsClassifiedByLength\\Length_'+str(word_length)+'.txt') as word_file:
        words_lst = word_file.readlines()
    words_lst=[word.strip() for word in words_lst]
    return words_lst


def get_entrophy(args):
    idx,word_lst,L=args
    guessed=word_lst[idx]
    count_dict = Counter(tuple(mark(answer, guessed)) for answer in word_lst)
    probabilities = np.array(list(count_dict.values())) / L
    entrophy = -np.sum(probabilities * np.log2(probabilities))
    #打印进度条，不换行
    print('\r',guessed,'  {}/{}'.format(idx+1,L),end='')
    return entrophy

def find_best_tree(graph,word_lst):
    #找出最优决策树，原地修改graph
    #graph：graphviz.Digraph()
    L=len(word_lst)
    if L==1:
        #注意：添加的节点名称有可能是graphviz的关键字,所以要加上'_',但是label碰到关键字会自动加上引号
        graph.node(word_lst[0]+'_',label=word_lst[0])
        print('\n'+word_lst[0]+'_')
        return
    #对于小规模不使用pool，大规模使用pool，500为分界
    if L<500:
    #find max entrophy
        entrophy_lst=np.zeros(L)
        for idx in range(L):
            guessed=word_lst[idx]
            count_dict = Counter(tuple(mark(answer, guessed)) for answer in word_lst)
            probabilities = np.array(list(count_dict.values())) / L
            entrophy_lst[idx] = -np.sum(probabilities * np.log2(probabilities))
            #打印进度条，不换行
            print('\r',guessed,'  {}/{}'.format(idx+1,L),end='')
    else:
        with Pool(cpu_count()) as p:
            res=p.map(get_entrophy,[(idx, word_lst, L) for idx in range(L)])
        entrophy_lst=np.array(res)

    max_idx=np.argmax(entrophy_lst)
    word=word_lst[max_idx]
    max_entrophy=entrophy_lst[max_idx]

    graph.node(graph.name+'_'+word,label=word+'\n'+str(round(max_entrophy,2)))
    print('\n'+graph.name+'_'+word)
    #对于筛选过后的new_word_lst，递归调用find_best_tree，将子图的根节点加入到graph的word节点下，这条边的label为state_lst
    state_lst_lst=Counter(tuple(mark(ans, word)) for ans in word_lst).keys()
    for state_lst in state_lst_lst:
        value_str=''.join([str(state.value) for state in state_lst])
        new_word_lst=filtrate_words(word_lst,word,state_lst)
        sub_graph=Digraph(name=graph.name+'_'+word+value_str)
        find_best_tree(sub_graph,new_word_lst)
        graph.subgraph(sub_graph)
        top_node=sub_graph.body[0].split('[')[0].strip()
        graph.edge(graph.name+'_'+word,top_node,label=value_str)
    return 


def initial_decision_tree():
    file_lst=os.listdir('WordsClassifiedByLength')
    word_length_lst=sorted([int(file[7:-4]) for file in file_lst])
    if os.path.exists('Trees')==True:
        shutil.rmtree('Trees')
    os.mkdir('Trees')
    os.mkdir('Trees\\Graphs')
    os.mkdir('Trees\\Pdfs')
    
    for word_length in word_length_lst:           
        words_lst=load_words(word_length)
        print('--- word_length: ',word_length,' ---')
        g=Digraph(name='_'+str(word_length)+'_')
        find_best_tree(g,words_lst)
        print('generating gv file')
        g.render('Trees\\Graphs\\Length'+str(word_length),view=False,format='gv')
        os.remove('Trees\\Graphs\\Length'+str(word_length))
        print('generating pdf file')
        g.render('Trees\\Pdfs\\Length'+str(word_length),view=False,format='pdf')
        os.remove('Trees\\Pdfs\\Length'+str(word_length))
            
    
if __name__=='__main__':
    print('Initial Words')
    initial_words()
    print('Initial Decision Tree')
    initial_decision_tree()
    print('Done')