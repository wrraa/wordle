#use tkinter to slove wordle
from GameLogic import *
from GenerateWidget import *
from InitialWordsAndDecisionTree import load_words
import tkinter as tk
import random
import subprocess

def open_decision_tree(word_length):
    subprocess.Popen(['start','.\\Trees\\Pdfs\\Length{}.pdf'.format(word_length)],shell=True)

def on_key_press(event, canvas, text_item_lst,answer,word_listbox):
    # 按键响应函数
    # 在canvas上的第focused_rect_idx_global个矩形画出按键对应的字母
    # 没有回车时不能换行，一行写满时不能再写，但可以删除
    # 当按键为回车时，换行
    # 不在行尾时回车就什么也不做
    # 当按键为退格时，删除上一个字母，但不能删除上一行的字母
    word_length=len(text_item_lst[0])
    guess_chance=len(text_item_lst)

    global focused_rect_idx_global
    global word_lst_global

    x=focused_rect_idx_global[0]
    y=focused_rect_idx_global[1]
    flag=focused_rect_idx_global[2]
    if flag!='ingame':
        return
    key = event.char
    if key == '\r' and y==word_length:
        # 按下回车键
        guessed=''
        for i in range(y):
            guessed += canvas.itemcget(text_item_lst[x][i],'text')
        print('guessed: ',guessed)
        result=mark(answer,guessed)

        # filtrate
        word_lst_global=filtrate_words(word_lst_global,guessed,result)
        word_listbox.delete(0,'end')
        for word in word_lst_global: 
            word_listbox.insert('end',word)

        for i in range(y):
            if result[i]==GuessState.PositionCorrect:
                canvas.itemconfigure(text_item_lst[x][i],fill='light green')
            elif result[i]==GuessState.PositionIncorrect:
                canvas.itemconfigure(text_item_lst[x][i],fill='yellow')
            elif result[i]==GuessState.NotInWord:
                canvas.itemconfigure(text_item_lst[x][i],fill='gray')
        if guessed==answer:
            print('You win!')
            focused_rect_idx_global[2]='win'
        elif x==guess_chance-1:
            print('You lose!')
            focused_rect_idx_global[2]='lose'
        focused_rect_idx_global[1] =0
        focused_rect_idx_global[0] +=1
    elif key == '\b' and y>0:
        # 按下退格键
        focused_rect_idx_global[1] -= 1
        canvas.itemconfigure(text_item_lst[x][y-1], text="")
    elif key.isalpha() and y<word_length and x<guess_chance:
        # 按下字母键
        canvas.itemconfigure(text_item_lst[x][y], text=key.lower())
        focused_rect_idx_global[1] += 1


def new_game(root,word_length,guess_chance):
    words_lst=load_words(word_length)
    answer=random.choice(words_lst)
    print('answer: ',answer)

    global focused_rect_idx_global
    global word_lst_global
    word_lst_global=words_lst

    focused_rect_idx_global=[0,0,'ingame']
    try:
        #stop the previous game and update the canvas
        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas) or isinstance(widget, tk.Listbox):
                widget.destroy()
    except:
        print('no previous game')
    canvas=tk.Canvas(root,bg='white',height=600,width=600)
    canvas.place(x=100,y=0)

    root.update()

    res=generate_rect_and_textbox(canvas,word_length,guess_chance,5)
    # rect_id_lst=res[0]
    text_item_lst=res[1]

    word_listbox=tk.Listbox(root,width=20,height=20)
    word_listbox.place(x=canvas.winfo_x()+canvas.winfo_width(),y=30)
    
    root.update()

    scrollbar = tk.Scrollbar(root, command=word_listbox.yview)
    scrollbar.place(x=word_listbox.winfo_x() + word_listbox.winfo_width(), y=30, height=word_listbox.winfo_height())
    
    word_listbox.config(yscrollcommand=scrollbar.set)

    word_listbox_label=tk.Label(root,text='Possible Word List',font=('Arial', 10))
    word_listbox_label.place(x=canvas.winfo_x()+canvas.winfo_width(),y=0)

    tree_button=tk.Button(root,text='Open Decision Tree',command=lambda:open_decision_tree(word_length))
    tree_button.place(x=canvas.winfo_x()+canvas.winfo_width(),y=word_listbox.winfo_y()+word_listbox.winfo_height()+10)

    canvas.bind('<KeyPress>', lambda event: on_key_press(event,canvas,text_item_lst,answer,word_listbox))
    canvas.bind('<Button-1>',lambda event:canvas.focus_set())
    canvas.focus_set()


if __name__=='__main__':
    word_length_default=5
    guess_chance_default=6
    root_size=[1000,700]

    root=tk.Tk()
    root.title('Wordle')
    root.geometry(str(root_size[0])+'x'+str(root_size[1]))

    boxes=generate_spinbox(root,word_length_default,guess_chance_default)
    word_length_box=boxes[0]
    guess_chance_box=boxes[1]
    newgame_button=tk.Button(root,text='New Game',command=lambda:new_game(root,int(word_length_box.get()),int(guess_chance_box.get())))
    newgame_button.place(x=0,y=120)

    root.update()

    new_game(root,word_length_default,guess_chance_default)

    root.mainloop()