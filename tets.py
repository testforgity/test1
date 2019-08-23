from tkinter import *
from tkinter.ttk import *
from git import Repo

def click_share():
    global treeAdded
    global treeModified
    # git add
    # git commit -m
    # git push
    #print(text.get("1.0", 'end-1c'))
    #print(len(text.get("1.0", 'end-1c')))
    for t in treeAdded.selection():
        if treeAdded.get_children(t):
            add_child(treeAdded, t)
        else:
            print(t)
            repo.git.add(t[:-1])

    treeAdded.destroy()
    treeAdded = create_treeAdded()
    build_tree(treeAdded, repo.untracked_files)

    for t in treeModified.selection():
        if treeModified.get_children(t):
            add_child(treeModified, t)
        else:
            print(t)
            repo.git.add(t[:-1])

    treeModified.destroy()
    treeModified = create_treeModified()
    build_tree(treeModified, take_modified_path())

    t = repo.index.commit(text.get("1.0", 'end-1c')) #'Testing javaman\'s program'
    origin = repo.remote(name='test')
    origin.push(t)
    # tree.insert('', END, values=(text.get("1.0", 'end-1c'),))
    # tree.config(height=len(tree.get_children()))
    # print(tree.selection())


def create_treeAdded():
    treeAdded = Treeview(frame_added)
    treeAdded.heading('#0', text='Новые файлы:')
    return treeAdded


def create_treeModified():
    treeModified = Treeview(frame_modified)
    treeModified.heading('#0', text='Измененные файлы:')
    return treeModified


def add_child(tree, parent):
    for child in tree.get_children(parent):
        if tree.get_children(child):
            add_child(tree, child)
        else:
            repo.git.add(child[:-1])


def build_tree(tree, track_files):
    tree.column('#0', width=440)

    dicti = {}

    counter = 0
    for r in track_files:  # проходимся по всем путям до новых файлов
        path_helper = r.split('/')  # получаем лист со всеми директориями по пути до файла
        path_maker = ''
        for p in path_helper:
            path_maker = path_maker + p + '/'
            if dicti.get(path_maker) is None:
                dicti[path_maker] = counter
                counter = counter + 1

    dict_helper = ['!']

    for (k, v) in dicti.items():
        num_helper = k.rfind('/')
        key_helper = k[:num_helper]
        num_helper2 = key_helper.rfind('/')
        key_helper2 = key_helper[:num_helper2] + '/'
        is_added = False
        for ad in dict_helper:
            if ad == key_helper2:
                k_helper = k.replace(ad, '')
                tree.insert(ad, 'end', text=k_helper[:-1], iid=k)
                dict_helper.append(k)
                is_added = True
                break
        if is_added:
            continue
        else:
            tree.insert('', 'end', text=k[:-1], iid=k)
            dict_helper.append(k)
    tree.pack(side=TOP)


def take_modified_path():
    i = 0
    helper = []
    while i < len(repo.index.diff(None)):
        h = repo.index.diff(None)[i].a_path
        helper.append(h)
        i = i + 1
    return helper


#fixme treeModified

path_to_directory = 'C:\\Users\\practic\Desktop\\gg'
repo = Repo(path_to_directory)
modified = take_modified_path() #modified.pop().a_path
print(modified)

root = Tk()
root.title("CommitMaster")
root.geometry("800x600")

Label(root, width=100).pack(side=BOTTOM)

frame_push = Frame(root)
frame_push.pack(side=BOTTOM)

frame_commit = Frame(root)
frame_commit.pack(side=BOTTOM)

infoLabel = Label(root, width=100)
infoLabel.pack(side=BOTTOM)

frame_added = Frame(root)
frame_added.pack(side=BOTTOM)

Label(root, width=100).pack(side=BOTTOM)

frame_modified = Frame(root)
frame_modified.pack(side=BOTTOM)

text = Text(frame_commit, height=5, width=55)

btn = Button(frame_push, text='Отправить', width=12, command=click_share)
btn.pack(side=BOTTOM)

lbl1 = Label(frame_push, width=50)  # width=100, height=15
lbl1.pack(side=BOTTOM)

text.pack(side=BOTTOM)

# boxAdded = Combobox(frame_added, height=5)
# boxAdded['values'] = ['Новые файлы'] # вытащить все new файлы
# boxAdded.pack(side=TOP)
treeAdded = create_treeAdded()
build_tree(treeAdded, repo.untracked_files)

label_added = Label(frame_added)
label_added.pack(side=TOP)

# boxChanged = Combobox(frame_modified, height=5)
# boxChanged['values'] = ['Изменения'] # вытащить все modified файлы
# boxChanged.pack(side=TOP)

treeModified = Treeview(frame_modified)
treeModified.heading('#0', text='Измененные файлы:')
build_tree(treeModified, modified)

label_changed = Label(frame_modified)
label_changed.pack(side=TOP)

# tree = Treeview(root, show='headings')
# tree["columns"] = ['Changes']
# tree.heading('Changes', text='Изменения')
# tree.pack()


root.mainloop()
