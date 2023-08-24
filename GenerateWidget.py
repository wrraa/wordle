import tkinter as tk

def generate_rect_and_textbox(canvas , word_length: int , guess_chance: int , r=5):
    '''
    在canvas上均匀分布word_length*guess_chance个矩形，两边预留r的空隙,返回矩形id的列表矩阵和文本id的列表矩阵
    '''
    c_width=canvas.winfo_width()
    c_height=canvas.winfo_height()
    # print(c_height,c_width)
    a=(c_width-2*r)/word_length
    b=(c_height-2*r)/guess_chance
    rect_id_lst=[[[] for i in range(word_length)] for j in range(guess_chance)]
    text_item_lst=[[[] for i in range(word_length)] for j in range(guess_chance)]
    for i in range(guess_chance):
        for j in range(word_length):
            #draw block in the middle upper
            left=r+j*a
            top=r+i*b
            rect_id_lst[i][j]=canvas.create_rectangle(left,top,left+a,top+b)
            text_item_lst[i][j]=canvas.create_text(left+a/2,top+b/2,text='',font=('Arial', int(min(a,b)/2)))
            # print(text_item_lst)
    return (rect_id_lst,text_item_lst)


def generate_spinbox(root,word_length_default,guess_chance_default):

    word_length_label=tk.Label(root,text='Word Length',font=('Arial', 10))
    word_length_label.place(x=0,y=0)

    word_length_box=tk.Spinbox(root,from_=3,to=10,increment=1,width=5,font=('Arial', 20))
    word_length_box.delete(0,'end')
    word_length_box.insert(0,word_length_default)
    word_length_box.config(state='readonly')
    word_length_box.place(x=0,y=30)

    guess_chance_label=tk.Label(root,text='Guess Chance',font=('Arial', 10))
    guess_chance_label.place(x=0,y=60)

    guess_chance_box=tk.Spinbox(root,from_=3,to=10,increment=1,width=5,font=('Arial', 20))
    guess_chance_box.delete(0,'end')
    guess_chance_box.insert(0,guess_chance_default)
    guess_chance_box.config(state='readonly')
    guess_chance_box.place(x=0,y=90)

    return (word_length_box,guess_chance_box)

