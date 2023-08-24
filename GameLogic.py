from enum import Enum

class GuessState(Enum):
    PositionCorrect=1
    PositionIncorrect=2
    NotInWord=3


def mark(answer,guessed):
    #return the list of GuessState of each letter
    # assert len(answer)==len(guessed)
    L=len(answer)
    result=[GuessState.NotInWord]*L
    for i in range(L):
        if answer[i]==guessed[i]:
            result[i]=GuessState.PositionCorrect
            answer=answer[:i]+'*'+answer[i+1:]
            guessed=guessed[:i]+'*'+guessed[i+1:]  #cant use remove
    
    # result=[GuessState.PositionCorrect if answer[i]==guessed[i] else GuessState.NotInWord for i in range(L)]

    
    for i in range(L):
        if guessed[i]!='*':
        # if result[i]==GuessState.NotInWord:
            if guessed[i] in answer:
                result[i]=GuessState.PositionIncorrect
                answer=answer[:answer.index(guessed[i])]+'*'+answer[answer.index(guessed[i])+1:]            

    return result


def filtrate_single_word(word,guessed,GuessState_lst):
    L=len(word)
    for i in range(L):
        if GuessState_lst[i]==GuessState.PositionCorrect and word[i]!=guessed[i]:
            return False
        if GuessState_lst[i]!=GuessState.PositionCorrect and word[i]==guessed[i]:
            return False
        if GuessState_lst[i]==GuessState.PositionCorrect and word[i]==guessed[i]:
            word=word[:i]+'*'+word[i+1:]
            guessed=guessed[:i]+'*'+guessed[i+1:]
    for i in range(L):
        if guessed[i]!='*':
            if GuessState_lst[i]==GuessState.PositionIncorrect:
                if guessed[i] in word:    
                    word=word[:word.index(guessed[i])]+'*'+word[word.index(guessed[i])+1:]            
                else:
                    return False
            elif GuessState_lst[i]==GuessState.NotInWord:
                if guessed[i] in word:
                    return False
    return True


def filtrate_words(words_lst,guessed,GuessState_lst):
    #return the words_lst after filtrate
    return [word for word in words_lst if filtrate_single_word(word,guessed,GuessState_lst)]