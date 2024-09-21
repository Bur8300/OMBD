import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage

def destroy_frames():
    try:
        frame2.destroy()
    except:
        pass
    try:
        actor_frame.destroy()
    except:
        pass
    try:
        movie_frame.destroy()
    except:
        pass
    try:
        comment_frame.destroy()
    except:
        pass
    try:
        main_frame.destroy()
    except:
        pass
    try:
        frame_watch.destroy()
    except:
        pass
    try:
        frame.destroy()
    except:
        pass
    try:
        add_movie_frame.destroy()
    except:
        pass
    try:
        add_actor_frame.destroy()
    except:
        pass
    try:
        frame_m2a.destroy()
    except:
        pass
    try:
        last_frame1.destroy()
    except:
        pass

class User():
    def __init__(self,id, name) -> None:
        self.id = id
        self.name =  name
        print(self.name, self.id)

class Actor():
    def __init__(self,id):
        self.id = id
        self.id, self.name, self.born = self.get_info()
        self.movies = self.load_movies()
        self.associatives = self.get_associatives()
        self.rating = self.get_rating()

    def get_rating(self):
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = "SELECT rating FROM commentrating WHERE movie_or_actor_id = ?;"
        cursor.execute(query, (self.id,))
        rating_lst = cursor.fetchall()
        if len(rating_lst) == 0:
            return "No Rating"
        else:
            sum_rating = sum([x[0] for x in rating_lst])
            return "%.2f"%(sum_rating / len(rating_lst))


    def get_info(self):
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"""SELECT * FROM people WHERE id = ?"""
        data_tuple = (f'{self.id}',)
        cursor.execute(query,data_tuple)
        return cursor.fetchall()[0]


    def load_movies(self):
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"""SELECT movie_id FROM stars WHERE person_id = ?;"""
        data_tuple = (f'{self.id}',)
        cursor.execute(query,data_tuple)

        movies= []

        for id in [x[0] for x in cursor.fetchall()]:
            query = f"SELECT * FROM movies WHERE id = ?"
            data_tuple = (f'{id}',)
            cursor.execute(query,data_tuple)
            movies.append(cursor.fetchall()[0])
        
        return movies
    
    def get_associatives(self):
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()

        actors = dict()

        for movie in self.movies:
            query = f"SELECT person_id FROM stars WHERE movie_id = ?;"
            data_tuple = (f'{movie[0]}',)
            cursor.execute(query,data_tuple)
            for person in cursor.fetchall():
                if person[0] != self.id:
                    if person[0] in actors.keys():
                        actors[person[0]] += 1
                    else:
                        actors[person[0]] = 1

        actors_lst = []

        for actor in actors.keys():
            conn = sqlite3.connect("database1.db")
            cursor = conn.cursor()
            query = f"""SELECT * FROM people WHERE id = ?"""
            data_tuple = (f'{actor}',)
            cursor.execute(query,data_tuple)

            actors_lst.append(list(cursor.fetchall()[0]) + [actors[actor]])

        actors_lst.sort(key=lambda x: x[-1])
        print(actors_lst)
        return actors_lst
    
    

class Movie():
    def __init__(self,id):
        self.id = id
        self.id, self.title, self.year = self.get_info()
        self.actors = self.get_actors()
        self.rating = self.get_rating()

    def get_rating(self):
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = "SELECT rating FROM commentrating WHERE movie_or_actor_id = ?;"
        cursor.execute(query, (self.id,))
        rating_lst = cursor.fetchall()
        if len(rating_lst) == 0:
            return "No Rating"
        else:
            sum_rating = sum([x[0] for x in rating_lst])
            return "%.2f"%(sum_rating / len(rating_lst))


    def get_info(self):
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"SELECT * FROM movies WHERE id = ?;"
        data_tuple = (f'{self.id}',)
        cursor.execute(query,data_tuple)
        return cursor.fetchall()[0]  
    
    def get_actors(self):
        actors = []
        actors_id_lst = []
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"SELECT person_id FROM stars WHERE movie_id = ?;"
        data_tuple = (f'{self.id}',)
        cursor.execute(query,data_tuple)
        actors_id_lst = cursor.fetchall()
        for a in actors_id_lst:
            conn = sqlite3.connect("database1.db")
            cursor = conn.cursor()
            query = f"SELECT * FROM people WHERE id = ?;"
            data_tuple =(f'{a[0]}',)
            cursor.execute(query,data_tuple)
            b = cursor.fetchall()
            print(b)
            actors.append(list(b[0])) 

        return actors

def load_watchlists_frame():
    global last_frame1
    destroy_frames()

    watchlists_lst = []

    last_frame1= ttk.Frame(window)
    last_frame1.pack()

    last_frame = ttk.Frame(last_frame1)
    last_frame.pack()

    last_canvas = tk.Canvas(last_frame,height = 700, width=550)
    last_canvas.pack(side="left",fill="both",expand=True)

    last_scroll = ttk.Scrollbar(last_frame,orient="vertical")
    last_scroll.pack(side="right", fill="y")

    last_canvas.configure(yscrollcommand=last_scroll.set)
    last_scroll.config(command=last_canvas.yview)

    conn = sqlite3.connect("database1.db")
    cursor = conn.cursor()
    query = "SELECT * FROM watchlists"
    cursor.execute(query)

    for data in cursor.fetchall():
        user_id = data[0]
        print(user_id)
        query = "select username from accounts_data where id = ?"
        cursor.execute(query,(user_id,))
        username = cursor.fetchall()[0][0]
        watchlist_id = data[1]
        print(watchlist_id)
        watchlist_name = data[2]
        movies = []
        query = "SELECT movie_id FROM watch WHERE watchlist_id = ?;"
        cursor.execute(query,(str(watchlist_id),))

        for m in cursor.fetchall():
            query = f"SELECT * FROM movies WHERE id = ?;"
            cursor.execute(query, (m))
            movies.append(cursor.fetchall()[0][1])

        watchlists_lst.append([username,watchlist_name,movies])
        

    last_canvas.bind("<Configure>", lambda e: last_canvas.configure(scrollregion= last_canvas.bbox("all")))

    last_second_frame = ttk.Frame(last_canvas)
    
    last_canvas.create_window((0,0), window=last_second_frame, anchor="n")

    for watchlist in watchlists_lst:
        ttk.Label(last_second_frame, text=f"Watchlist {watchlist[1]}, created by {watchlist[0]}").pack(anchor="w")
        for movie in watchlist[2]:
            ttk.Label(last_second_frame, text=f"    {movie}").pack(anchor="w")
        ttk.Label(last_second_frame,text="###################################").pack(anchor="w")
        ttk.Label(last_second_frame,text=" ").pack()

    last_back = ttk.Button(last_frame1,text="Back", command=load_frame2)
    last_back.pack(side="bottom")


        

def create_watchlist(lst, name):
    try:
        conn = sqlite3.connect("database1.db")
        query = "CREATE TABLE IF NOT EXISTS watchlists (user_id TEXT, watchlist_id INT, watchlist_name TEXT)"
        conn.execute(query)
        print("Created")
        query = "CREATE TABLE IF NOT EXISTS watch (watchlist_id INT, movie_id TEXT)"
        conn.execute(query)
        print("Created")
        query = "SELECT watchlist_id FROM watchlists"
        cursor = conn.cursor()
        cursor.execute(query)
        len_watchlists = len(cursor.fetchall())
        print("Fetched")
        query = "INSERT INTO watchlists (user_id, watchlist_id, watchlist_name) VALUES(?,?,?)"
        print(str(user.id),len_watchlists + 1, name)
        cursor.execute(query,(str(user.id),int(len_watchlists + 1), str(name)))
        print("Inserted")

        for id in [x[0] for x in lst]:
            query = "INSERT INTO watch (watchlist_id, movie_id) VALUES(?,?)"
            print(id)
            cursor.execute(query,(int(len_watchlists + 1),str(id)))
        conn.commit()
        conn.close()
    except:
        messagebox.showerror("Error","Something Went Wrong!")
    else:
        messagebox.showinfo("Confirmed", "Your wathclist has been created")






def load_create_watchlist_frame():
    destroy_frames()
    
    global frame_watch

    watch_list = []
    
    frame_watch = ttk.Frame(window)
    frame_watch.pack()

    user_input_frame = ttk.LabelFrame(frame_watch)
    user_input_frame.pack(pady=10)

    name_watchlist_label = ttk.Label(user_input_frame, text="Enter your watchlist name: ")
    name_watchlist_label.grid(row=0,column=0)

    name_watchlist = ttk.Entry(user_input_frame)
    name_watchlist.grid(row=0,column=1)

    movie_search_label = ttk.Label(user_input_frame, text="Search Movie:")
    movie_search_label.grid(row=1,column=0)

    movie_search = ttk.Entry(user_input_frame)
    movie_search.grid(row=1,column=1)

    for widget in user_input_frame.winfo_children():
        widget.grid_configure(pady=5, padx=5)

    def movie_list():
        global movie_lst, scroll, label
        try:
            movie_lst.destroy()
            scroll.destroy()
            label.destroy()
        except:
            pass

        result_frame = ttk.Frame(user_input_frame)
        result_frame.grid(row=3,column=0,columnspan=2)

        label = ttk.Label(result_frame, text="#################################################")
        label.pack()

        scroll = ttk.Scrollbar(result_frame,orient="vertical")
        scroll.pack(side="right",fill="y")

        movie_lst = ttk.Treeview(result_frame, yscrollcommand=scroll.set,show="tree")
        for data in load_data("movies",1000, movie_search.get()):
            movie_lst.insert("","end", text= data[1], values=data)
        movie_lst.pack(side="left",fill="both",expand=True)
        scroll.config(command=movie_lst.yview)

        movie_lst.bind("<<TreeviewSelect>>", add_2_watchlist)
    
    search_button = ttk.Button(user_input_frame, text="Enter",command= movie_list)
    search_button.grid(row=2,column=0,columnspan=2)

    watchlist = ttk.Treeview(frame_watch, show="tree")
    watchlist.pack()

    def add_2_watchlist(_):
        movie = movie_lst.item(movie_lst.selection()[0])["values"]
        print(movie)
        if movie not in watch_list:
            watch_list.append(movie)
            print(watch_list)
            watchlist.insert("","end",text=movie[1])

    button_frame = ttk.Frame(frame_watch)
    button_frame.pack(side="bottom",pady=10)

    done_button = ttk.Button(button_frame, text="Done", command= lambda: create_watchlist(watch_list, name_watchlist.get()))
    done_button.pack(side="top")

    back_button = ttk.Button(button_frame, text="Back", command= load_frame2)
    back_button.pack(side="bottom",pady=15)



    
def load_movie_add_frame():
    global add_movie_frame
    destroy_frames()

    add_movie_frame = ttk.Frame(window)
    add_movie_frame.pack()

    add_movie_label_frame = ttk.LabelFrame(add_movie_frame)
    add_movie_label_frame.pack(pady=200)

    ttk.Label(add_movie_label_frame, text="Movie Name: ").grid(row=0,column=0)
    ttk.Label(add_movie_label_frame, text="Release Date: ").grid(row=1,column=0)

    add_movie_name_entry = ttk.Entry(add_movie_label_frame)
    add_movie_name_entry.grid(row=0,column=1)

    add_movie_birth_entry = ttk.Spinbox(add_movie_label_frame, from_= 0, to="infinity")
    add_movie_birth_entry.grid(row=1,column=1)

    def add_movie():
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = "SELECT id FROM movies"
        cursor.execute(query)
        new_id = int(cursor.fetchall()[-1][-1]) + 1
        birth = add_movie_birth_entry.get()
        print(birth)

        query = "INSERT INTO movies (id, title, year) VALUES(?,?,?);"
        try:
            birth = int(birth)
        except:
            birth = ""
        try:
            cursor.execute(query,(str(new_id),add_movie_name_entry.get().title(),str(birth)))
            conn.commit()
            conn.close()
        except:
            pass
        else:
            messagebox.showinfo(title="Succesful",message="Movie succesfully added :)")

    add_movie_button = ttk.Button(add_movie_label_frame, text="Add", command= add_movie)
    add_movie_button.grid(row=3, column=0,columnspan=2)

    for widget in add_movie_label_frame.winfo_children():
        widget.grid_configure(padx=10, pady=20)

    ttk.Button(add_movie_frame, text="Back", command=load_frame2).pack()
    

def load_actor_add_frame():
    global add_actor_frame
    destroy_frames()

    add_actor_frame = ttk.Frame(window)
    add_actor_frame.pack()

    add_actor_label_frame = ttk.LabelFrame(add_actor_frame)
    add_actor_label_frame.pack(pady=200)

    ttk.Label(add_actor_label_frame, text="Actor Name: ").grid(row=0,column=0)
    ttk.Label(add_actor_label_frame, text="Birth Date: ").grid(row=1,column=0)

    add_actor_name_entry = ttk.Entry(add_actor_label_frame)
    add_actor_name_entry.grid(row=0,column=1)

    add_actor_birth_entry = ttk.Spinbox(add_actor_label_frame, from_= 0, to="infinity")
    add_actor_birth_entry.grid(row=1,column=1)

    def add_actor():
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = "SELECT id FROM people"
        cursor.execute(query)
        new_id = int(cursor.fetchall()[-1][-1]) + 1
        birth = add_actor_birth_entry.get()
        print(birth)

        query = "INSERT INTO people (id, name, birth) VALUES(?,?,?);"
        try:
            birth = int(birth)
        except:
            birth = ""
        try:
            cursor.execute(query,(str(new_id),add_actor_name_entry.get().title(),str(birth)))
            conn.commit()
            conn.close()
        except:
            pass
        else:
            messagebox.showinfo(title="Succesful",message="Actor succesfully added :)")

    add_actor_button = ttk.Button(add_actor_label_frame, text="Add", command= add_actor)
    add_actor_button.grid(row=3, column=0,columnspan=2)

    for widget in add_actor_label_frame.winfo_children():
        widget.grid_configure(padx=10, pady=20)

    ttk.Button(add_actor_frame, text="Back", command=load_frame2).pack()

    

    
def load_A2M_frame():
    global frame_m2a
    destroy_frames()

    selected_movies= []

    frame_m2a = tk.Frame(window)
    frame_m2a.pack()

    m2a_moive_frame = ttk.Frame(frame_m2a)
    m2a_moive_frame.pack()

    ttk.Label(m2a_moive_frame,text="#########################################################").pack()

    m2a_actor_frame = ttk.Frame(frame_m2a)
    m2a_actor_frame.pack(pady=30)

    ttk.Label(m2a_actor_frame,text="#########################################################").pack()
    
    movie_select_label = tk.Label(m2a_moive_frame,text="Please select a movie")
    movie_select_label.pack(side="top")

    movie_entry = ttk.Entry(m2a_moive_frame)
    movie_entry.pack()

    movie_enter = ttk.Button(m2a_moive_frame, text="Enter", command= lambda: create_movies(movie_entry.get().title()))
    movie_enter.pack(pady=5)

    def create_movies(title):
        global scroll, movie_tree
        try:
            scroll.destroy()
            movie_tree.destroy()
        except:
            pass
        scroll = ttk.Scrollbar(m2a_moive_frame, orient="vertical")
        scroll.pack(side="right", fill="y")

        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"select * from movies where title like ?;"
        data_tuple = (f'%{title}%',)
        cursor.execute(query, data_tuple)

        movie_tree = ttk.Treeview(m2a_moive_frame,yscrollcommand=scroll.set, show="tree")
        for m in sorted(cursor.fetchall(), key=lambda x: x[1]):
            movie_tree.insert("","end",text=m[1], values=m)
        movie_tree.pack(side="left",fill="both", expand=True)
        scroll.config(command=movie_tree.yview)
        def movie_select(_):
            selected_movies.append(movie_tree.item(movie_tree.selection()[0])["values"][1])
            movie_select_label.configure(text=f"Selected movies are {', '.join(selected_movies)}")
        movie_tree.bind("<<TreeviewSelect>>",movie_select)

###########################################################

    actor_select_label = tk.Label(m2a_actor_frame,text="Please select a actor")
    actor_select_label.pack(side="top")

    actor_entry = ttk.Entry(m2a_actor_frame)
    actor_entry.pack()

    actor_enter = ttk.Button(m2a_actor_frame, text="Enter", command= lambda: create_actors(actor_entry.get().title()))
    actor_enter.pack(pady=5)

    def create_actors(title):
        global scroll1, actor_tree
        try:
            scroll1.destroy()
            actor_tree.destroy()
        except:
            pass
        scroll1 = ttk.Scrollbar(m2a_actor_frame, orient="vertical")
        scroll1.pack(side="right", fill="y")

        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"select * from people where name like ?;"
        data_tuple = (f'%{title}%',)
        cursor.execute(query,data_tuple)

        actor_tree = ttk.Treeview(m2a_actor_frame,yscrollcommand=scroll1.set, show="tree")
        for m in sorted(cursor.fetchall(), key=lambda x: x[1]):
            actor_tree.insert("","end",text=m[1], values=m)
        actor_tree.pack(side="left",fill="both", expand=True)
        scroll1.config(command=actor_tree.yview)
        def actor_select(_):
            global selected_actor
            selected_actor = (actor_tree.item(actor_tree.selection()[0])["values"][1])
            actor_select_label.configure(text=f"Selected actor is {selected_actor}")
        actor_tree.bind("<<TreeviewSelect>>",actor_select)

    button_frame = ttk.Frame(frame_m2a)
    button_frame.pack(side="bottom",pady=10)

    done_button = ttk.Button(button_frame, text="Done", command= lambda: connect_actor_to_movies(selected_actor,selected_movies))
    done_button.pack(side="top")

    back_button = ttk.Button(button_frame, text="Back", command=load_frame2)
    back_button.pack(side="bottom", pady=15)
    
def load_M2A_frame():
    global frame_m2a
    destroy_frames()

    frame_m2a = tk.Frame(window)
    frame_m2a.pack()

    m2a_moive_frame = ttk.Frame(frame_m2a)
    m2a_moive_frame.pack()

    ttk.Label(m2a_moive_frame,text="#########################################################").pack()

    m2a_actor_frame = ttk.Frame(frame_m2a)
    m2a_actor_frame.pack(pady=30)

    ttk.Label(m2a_actor_frame,text="#########################################################").pack()
    
    movie_select_label = tk.Label(m2a_moive_frame,text="Please select a movie")
    movie_select_label.pack(side="top")

    movie_entry = ttk.Entry(m2a_moive_frame)
    movie_entry.pack()

    movie_enter = ttk.Button(m2a_moive_frame, text="Enter", command= lambda: create_movies(movie_entry.get()))
    movie_enter.pack(pady=5)

    def create_movies(title):
        global scroll, movie_tree
        try:
            scroll.destroy()
            movie_tree.destroy()
        except:
            pass
        scroll = ttk.Scrollbar(m2a_moive_frame, orient="vertical")
        scroll.pack(side="right", fill="y")

        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"select * from movies where title like ?;"
        data_tuple =(f'%{title}%',)
        cursor.execute(query,data_tuple)

        movie_tree = ttk.Treeview(m2a_moive_frame,yscrollcommand=scroll.set, show="tree")
        for m in sorted(cursor.fetchall(), key=lambda x: x[1]):
            movie_tree.insert("","end",text=m[1], values=m)
        movie_tree.pack(side="left",fill="both", expand=True)
        scroll.config(command=movie_tree.yview)
        def movie_select(_):
            global selected_movie
            selected_movie = movie_tree.item(movie_tree.selection()[0])["values"][1]
            movie_select_label.configure(text=f"Selected movie is {selected_movie}")
        movie_tree.bind("<<TreeviewSelect>>",movie_select)

###########################################################

    actor_select_label = tk.Label(m2a_actor_frame,text="Please select a actor")
    actor_select_label.pack(side="top")

    actor_entry = ttk.Entry(m2a_actor_frame)
    actor_entry.pack()

    actor_enter = ttk.Button(m2a_actor_frame, text="Enter", command= lambda: create_actors(actor_entry.get().title()))
    actor_enter.pack(pady=5)

    selected_actors= []

    def create_actors(title):
        global scroll1, actor_tree
        try:
            scroll1.destroy()
            actor_tree.destroy()
        except:
            pass
        scroll1 = ttk.Scrollbar(m2a_actor_frame, orient="vertical")
        scroll1.pack(side="right", fill="y")

        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"select * from people where name like ?;"
        data_tuple = (f"%{title}%",)
        cursor.execute(query,data_tuple)

        actor_tree = ttk.Treeview(m2a_actor_frame,yscrollcommand=scroll1.set, show="tree")
        for m in sorted(cursor.fetchall(), key=lambda x: x[1]):
            actor_tree.insert("","end",text=m[1], values=m)
        actor_tree.pack(side="left",fill="both", expand=True)
        scroll1.config(command=actor_tree.yview)
        def actor_select(_):
            selected_actors.append(actor_tree.item(actor_tree.selection()[0])["values"][1])
            actor_select_label.configure(text=f"Selected actors are {', '.join(selected_actors)}")
        actor_tree.bind("<<TreeviewSelect>>",actor_select)

    button_frame = ttk.Frame(frame_m2a)
    button_frame.pack(side="bottom", pady=10)

    done_button = ttk.Button(button_frame, text="Done", command= lambda: connect_movie_to_actors(selected_movie,selected_actors))
    done_button.pack(side="top")

    back_button = ttk.Button(button_frame, text="Back", command=load_frame2)
    back_button.pack(side="bottom",pady=15)

    
def load_comments(movie_or_actor):
    global main_frame
    destroy_frames()

    main_frame = ttk.Frame(window)
    main_frame.pack()

    frame_back = ttk.Frame(main_frame)
    frame_back.pack()

    back_button = ttk.Button(frame_back, text="Back", command= lambda: load_actor_frame(movie_or_actor) if type(movie_or_actor) == Actor else load_movie_frame(movie_or_actor))
    back_button.pack()

    canvas_commnets = tk.Canvas(main_frame, height=750,width=550)
    canvas_commnets.pack(side="left",fill="both", expand=True)
    
    scroll_barr = ttk.Scrollbar(main_frame, orient="vertical")
    scroll_barr.pack(side="right", fill="y")

    scroll_barry = ttk.Scrollbar(main_frame, orient="horizontal")
    scroll_barry.pack(side="bottom", fill="x")

    canvas_commnets.configure(yscrollcommand=scroll_barr.set, xscrollcommand=scroll_barry.set)
    scroll_barr.config(command=canvas_commnets.yview)
    scroll_barry.config(command=canvas_commnets.xview)

    conn = sqlite3.connect("database1.db")
    cursor = conn.cursor()
    query_for_users = "SELECT * FROM accounts_data"
    cursor.execute(query_for_users)
    users = dict()
    for u in cursor.fetchall():
        users[u[2]] = u[0]
    query = f"SELECT * FROM commentrating WHERE movie_or_actor_id = ?"
    data_tuple = (str(movie_or_actor.id),)
    cursor.execute(query,data_tuple)
    comments = cursor.fetchall()

    
    canvas_commnets.bind("<Configure>", lambda e: canvas_commnets.configure(scrollregion= canvas_commnets.bbox("all")))

    second_frame = ttk.Frame(canvas_commnets)

    canvas_commnets.create_window((0,0), window=second_frame, anchor="n")


    for comment in comments:
        ttk.Label(second_frame, text=f"Comment of {users[int(comment[0])]}, Rating: {comment[2]}").pack(anchor="w")
        ttk.Label(second_frame, text=f"{comment[3]}").pack(anchor="w")
        ttk.Label(second_frame, text="   ").pack(anchor="w")
        ttk.Label(second_frame, text="###############################################").pack(anchor="w")
        ttk.Label(second_frame, text="   ").pack(anchor="w")




def load_comment(actor):
    global comment_frame
    destroy_frames()

    
    comment_frame = ttk.Frame(window)
    comment_frame.pack()

    up_frame = ttk.LabelFrame(comment_frame)
    up_frame.pack()

    frame123 =ttk.LabelFrame(up_frame)
    frame123.pack(side="left")

    if type(actor) == Actor:
        actor_label = ttk.Label(frame123, text=f"Comment about {actor.name}:")
        actor_label.pack()
    else:
        actor_label = ttk.Label(frame123, text=f"Comment about {actor.title}:")
        actor_label.pack()
    
    Text = tk.Text(up_frame)
    Text.pack(side="right")

    Rating = ttk.Combobox(frame123, values=[1,2,3,4,5,6,7,8,9,10])
    Rating.pack()

    def insert_comment(actor):
        comment = Text.get("1.0",'end-1c')
        user_id = str(user.id)
        idma = actor.id
        try:
            rating = int(Rating.get())
            assert 0< rating <= 10
        except:
            messagebox.showerror("Error", "Rating must be number between 1 and 10")
        else:
            conn = sqlite3.connect("database1.db")
            cursor = conn.cursor()
            query = f"""INSERT INTO commentrating VALUES(?,?,?,?)"""
            data_tuple= (user_id,str(idma),rating,comment)
            cursor.execute(query,data_tuple)
            conn.commit()
            conn.close()
            messagebox.showinfo("Confirmed", "Your comment has been sended!")
            load_actor_frame(actor) if type(actor) == Actor else load_movie_frame(actor) 

        print(f"""{actor.name if type(actor) == Actor else actor.title}'s rating: {rating}
{user.name}'s comment:
{comment}""")

    comment_button = ttk.Button(frame123, text="Send", command= lambda: insert_comment(actor))
    comment_button.pack()

    if type(actor) == Actor:
        back_button = ttk.Button(comment_frame,text="Back", command=lambda: load_actor_frame(actor))
        back_button.pack()
    else:
        back_button = ttk.Button(comment_frame,text="Back", command=lambda: load_movie_frame(actor))
        back_button.pack()           


def create_output(table, num, name):
    global frame2, button,mylist,scroll
    try:
        scroll.destroy()
        mylist.destroy()
    except:
        pass
    try:
        num = int(num.strip(" "))
    except:
        num = 10

    scroll = ttk.Scrollbar(frame2, orient="vertical")
    scroll.pack(side="right", fill="y")
    
    mylist = ttk.Treeview(frame2,yscrollcommand=scroll.set, show="tree")

    for data in load_data(table,int(num), name):
        mylist.insert("","end", text=data[1], values=data)
    mylist.pack(side="left",fill="both", expand=True)
    scroll.config(command=mylist.yview)
    if table == "people":
        def item_select(_):
            print(mylist.item(mylist.selection()[0])["values"])
            load_actor_frame(Actor(mylist.item(mylist.selection()[0])["values"][0]))
    else:
        def item_select(_):
            print(mylist.item(mylist.selection()[0])["values"])
            load_movie_frame(Movie(mylist.item(mylist.selection()[0])["values"][0]))

    mylist.bind("<<TreeviewSelect>>", item_select)
    

def load_data(table, num, name):
    conn = sqlite3.connect("database1.db")
    cursor = conn.cursor()
    if table == "movies":
        field = "title"
    else:
        field = "name"
    query = f"select * from {table} where {field} like ?;"
    cursor.execute(query,("%"+name+"%",))
    return cursor.fetchmany(num)


def load_frame1():
    global frame, account_name, account_password, user_info

    #Ana Frame
    frame = ttk.Frame(window)
    frame.pack()

    #Input Frame
    user_info = ttk.LabelFrame(frame,text="User Information")
    user_info.grid(column=0,row=1, pady=200)

    username_label = ttk.Label(user_info, text="Username:")
    account_name = ttk.Entry(user_info)
    username_label.grid(row=0,column=0)
    account_name.grid(row=0,column=1)

    password_label = ttk.Label(user_info, text="Password:")
    account_password = ttk.Entry(user_info)
    password_label.grid(row=1,column=0)
    account_password.grid(row=1,column=1)

    enter_button = ttk.Button(user_info, text="Login", command= enter)
    enter_button.grid(row=3,column=0)

    create_button = ttk.Button(user_info, text="Create Account", command= create)
    create_button.grid(row=3,column=1)


    for widget in user_info.winfo_children():
        widget.grid_configure(padx=10,pady=10)
    pass   

def load_frame2():
    
    global frame, frame2, button, filter_variable, search_entry, search_filter,search_frame

    destroy_frames()
    
    frame2 = ttk.Frame(window)
    frame2.pack()

    Menu = tk.Menu(window)

    Options = tk.Menu(Menu, tearoff= 0)
    Menu.add_cascade(label="Options", menu=Options)
    Options.add_command(label="Match M2A", command= load_M2A_frame)
    Options.add_command(label="Match A2M", command= load_A2M_frame)
    Options.add_command(label="Add Actor", command= load_actor_add_frame)
    Options.add_command(label="Add Movie", command= load_movie_add_frame)
    Options.add_command(label="Create Watchlist", command= load_create_watchlist_frame)
    Options.add_command(label="Watchlists", command= load_watchlists_frame)

    window.config(menu= Menu)


    image_label = ttk.Label(frame2, text="photo" ,image = img_tk)
    image_label.pack()   

    search_frame = ttk.LabelFrame(frame2)
    search_frame.pack()

    search_label = ttk.Label(search_frame,text="Search Place:")
    search_label.grid(row=0, column=0)

    search_entry = ttk.Entry(search_frame)
    search_entry.grid(row=0,column=1,columnspan=3)

    search_filter = ttk.Spinbox(search_frame, from_=10, to="infinity")
    search_filter.grid(row=1,column=0)

    filter_variable = tk.StringVar(frame2,"movies")

    movie_filter = ttk.Radiobutton(search_frame, text="Movie", value="movies", variable=filter_variable)
    movie_filter.grid(row=1, column=1)

    actor_filter = ttk.Radiobutton(search_frame, text="Actor", value="people",  variable=filter_variable)
    actor_filter.grid(row=1,column=2)

    for widget in search_frame.winfo_children():
        widget.grid_configure(padx=10,pady=10)

    button = ttk.Button(search_frame, text="Click", command= lambda: create_output(filter_variable.get(), search_filter.get(), search_entry.get().title()))
    button.grid(row=2,column=0,columnspan=3)

def load_actor_frame(actor):
    global actor_frame, movie_frame
    destroy_frames()

    actor_frame = ttk.Frame(window)
    actor_frame.pack()

    image_label = ttk.Label(actor_frame, text="photo" ,image = img_tk)
    image_label.pack()  

    actor_info_frame = ttk.LabelFrame(actor_frame)
    actor_info_frame.pack()

    actor_name_label = ttk.Label(actor_info_frame, text="Name:")
    actor_name_label.grid(column=0,row=0)

    actor_name = ttk.Label(actor_info_frame, text=" ".join(actor.name.split(" ")[:-1]))
    actor_name.grid(column=1,row=0)

    actor_surname_label = ttk.Label(actor_info_frame, text="Surname:")
    actor_surname_label.grid(column=0,row=1)

    actor_surname = ttk.Label(actor_info_frame, text=actor.name.split(" ")[-1])
    actor_surname.grid(column=1,row=1)

    actor_birth_label = ttk.Label(actor_info_frame, text="Birth Date:")
    actor_birth_label.grid(column=0,row=2)

    actor_birth = ttk.Label(actor_info_frame, text=actor.born)
    actor_birth.grid(column=1,row=2)

    actor_rating_label = ttk.Label(actor_info_frame, text="Rating:")
    actor_rating_label.grid(column=0,row=3)

    actor_rating = ttk.Label(actor_info_frame, text=actor.rating)
    actor_rating.grid(column=1,row=3)

    comment_button = ttk.Button(actor_info_frame, text="Comment", command=lambda: load_comment(actor))
    comment_button.grid(row=4,column=0)

    comments_button = ttk.Button(actor_info_frame, text="Comments", command=lambda: load_comments(actor))
    comments_button.grid(row=4,column=1)

    associates_label = ttk.Label(actor_info_frame, text="Associated Actors")
    associates_label.grid(row=5,column=0)

    associates_tree = ttk.Treeview(actor_info_frame, show="tree")
    associates_tree.grid(row=6,column=0)

    for a in actor.associatives:
        print(a)
        associates_tree.insert(parent="",index=0,values=a, text=a[1])

    def actor_select(_):
        print(associates_tree.item(associates_tree.selection()[0])["values"])
        load_actor_frame(Actor(associates_tree.item(associates_tree.selection()[0])["values"][0]))

    associates_tree.bind("<<TreeviewSelect>>", actor_select)

    movies_label = ttk.Label(actor_info_frame, text="Movies")
    movies_label.grid(row=5,column=1)

    movies_tree = ttk.Treeview(actor_info_frame, show="tree")
    movies_tree.grid(row=6,column=1)

    for a in actor.movies:
        movies_tree.insert(parent="",index=0,values=a, text=a[1])

    def movie_select(_):
        load_movie_frame(Movie(movies_tree.item(movies_tree.selection()[0])["values"][0]))

    movies_tree.bind("<<TreeviewSelect>>",  movie_select)

    back_button = ttk.Button(actor_frame, text="Back", command= load_frame2)
    back_button.pack()


def load_movie_frame(movie):
    global movie_frame
    destroy_frames()

    movie_frame = ttk.Frame(window)
    movie_frame.pack()

    image_label = ttk.Label(movie_frame, text="photo" ,image = img_tk)
    image_label.pack()

    movie_info_frame = ttk.LabelFrame(movie_frame)
    movie_info_frame.pack()

    movie_name_label = ttk.Label(movie_info_frame, text="Title:")
    movie_name_label.grid(column=0,row=0)

    movie_name = ttk.Label(movie_info_frame, text=movie.title)
    movie_name.grid(column=1,row=0)

    movie_year_label = ttk.Label(movie_info_frame, text="Release Date:")
    movie_year_label.grid(column=0,row=1)

    actor_birth = ttk.Label(movie_info_frame, text=movie.year)
    actor_birth.grid(column=1,row=1)

    actor_rating_label = ttk.Label(movie_info_frame, text="Rating:")
    actor_rating_label.grid(column=0,row=2)

    actor_rating = ttk.Label(movie_info_frame, text=movie.rating)
    actor_rating.grid(column=1,row=2)

    comment_button = ttk.Button(movie_info_frame, text="Comment", command= lambda: load_comment(movie))
    comment_button.grid(row=3,column=0)

    comments_button = ttk.Button(movie_info_frame, text="Comments", command= lambda: load_comments(movie))
    comments_button.grid(row=3, column=1)

    actors_label = ttk.Label(movie_info_frame, text="Actors:")
    actors_label.grid(row=4,column=0,columnspan=2)

    actors_tree = ttk.Treeview(movie_info_frame, show="tree")
    actors_tree.grid(row=5,column=0,columnspan=2)

    for a in movie.actors:
        print(a)
        actors_tree.insert(parent="",index=0,values=a, text=a[1])

    def actor_select(_):
        print(actors_tree.item(actors_tree.selection()[0])["values"])
        load_actor_frame(Actor(actors_tree.item(actors_tree.selection()[0])["values"][0]))
    
    actors_tree.bind("<<TreeviewSelect>>", actor_select)

    back_button = ttk.Button(movie_frame, text="Back", command= load_frame2)
    back_button.pack()



def enter():
    global user
    username = account_name.get()
    password = account_password.get()

    try:
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"select * from accounts_data where username = ?"
        data_tuple = (f'{username}',)
        cursor.execute(query,data_tuple)
        lst = cursor.fetchone()
        assert lst != None
        user = User(lst[2], lst[0])
        if lst[1] == password:
            print("Login is succesful")
            load_frame2()
            print(f"""Username: {username}\nPassword: {password}""")
        else:
            messagebox.showerror("Error", "Your password is wrong.")
        conn.close()
    except AssertionError:
        messagebox.showerror("Error", "This username does not exists.")
    except:
        messagebox.showerror("Error", "Something went wrong")
    
def create():

    global account_password_b
    global account_password, account_name

    user_info.destroy()
    
    user_info_b = ttk.LabelFrame(frame,text="User Information")
    user_info_b.grid(column=0,row=1, pady=200)

    username_label = ttk.Label(user_info_b, text="Username:")
    account_name = ttk.Entry(user_info_b)
    username_label.grid(row=0,column=0)
    account_name.grid(row=0,column=1)

    password_label = ttk.Label(user_info_b, text="Password:")
    account_password = ttk.Entry(user_info_b)
    password_label.grid(row=1,column=0)
    account_password.grid(row=1,column=1)

    password_label_b = ttk.Label(user_info_b, text="Password:")
    account_password_b = ttk.Entry(user_info_b)
    password_label_b.grid(row=2,column=0)
    account_password_b.grid(row=2,column=1)

    create_button_b = ttk.Button(user_info_b, text="Create", command= enter_create)
    create_button_b.grid(row=3,column=1)

    for widget in user_info_b.winfo_children():
        widget.grid_configure(padx=10,pady=10)

def enter_create():
    global user
    password1 = account_password.get()
    password2 = account_password_b.get()

    if password1 != password2:
        messagebox.showerror(title= "Error", message="Passwords must match")
    elif password1 == "":
        messagebox.showerror(title= "Error", message= "Password cannot be blank")
    else:
        try:
            conn = sqlite3.connect("database1.db")

            table_create_query = """CREATE TABLE IF NOT EXISTS accounts_data
            (username TEXT, password TEXT, id INT)"""
            conn.execute(table_create_query)

            username = account_name.get()
            cursor = conn.cursor()
            query = f"SELECT * FROM accounts_data WHERE username = ?"
            data_insert_tuple = (f'{username}',)
            cursor.execute(query,data_insert_tuple)

            if cursor.fetchall() != []:
                messagebox.showerror("Error", "This name is already taken")
            else:
                query = "select * from accounts_data"
                cursor.execute(query)
                len_database = len(cursor.fetchall())
                data_insert_query = """INSERT INTO accounts_data (username, password ,id) VALUES
                (?,?,?)"""
                data_insert_tuple =(username, password1, len_database + 1)
                cursor = conn.cursor()
                cursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()
                conn.close()
                user = User(str(len_database + 1), username)
                load_frame2()
        except:
            messagebox.showerror(title="Error", message="Something went wrong!")
        else:
            messagebox.showinfo("Confirmed", "Your account has been created.")

def connect_movie_to_actors(movie_name, actors_lst):
    try:
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"SELECT id FROM movies WHERE title = ?;"
        data_tuple = (f"{movie_name}",)
        cursor.execute(query,data_tuple)
        movie_id = cursor.fetchall()[0][0]
        print(movie_id)

        already_in = [x[0] for x in Movie(movie_id).actors]
        print(already_in)

        actors_id_lst = []
        for a in actors_lst:
            query = f"SELECT id FROM people WHERE name = ?;"
            data_tuple = (f'{a}',)
            cursor.execute(query,data_tuple)
            actors_id_lst.append(cursor.fetchone()[0])
            print(actors_id_lst)
        print(actors_id_lst)

        new_ids = list(filter(lambda x: x not in already_in, actors_id_lst))
        print(new_ids)

        for id in new_ids:
            print(id)
            conn = sqlite3.connect("database1.db")
            cursor = conn.cursor()
            query = "INSERT INTO stars (person_id, movie_id) VALUES(?,?);"
            data = (str(id),str(movie_id))
            cursor.execute(query,data)
            conn.commit()
            conn.close()
    except EOFError as e:
        print(e)
        messagebox.showerror(title="Error", message= "Something Went Wrong!")
    else:
        messagebox.showinfo(title="Confirmed", message= "Actors are succesfully added")
        




def connect_actor_to_movies(actor_name, movies_lst):
    try:
        conn = sqlite3.connect("database1.db")
        cursor = conn.cursor()
        query = f"SELECT id FROM people WHERE name = ?;"
        data_tuple = (f'{actor_name}',)
        cursor.execute(query,data_tuple)
        actor_id = cursor.fetchall()[0][0]

        already_in = [x[0] for x in Actor(actor_id).movies]
        print(already_in)

        movies_id_lst = []
        for a in movies_lst:
            query = f"SELECT id FROM movies WHERE title = ?;"
            data_tuple = (f'{a}',)
            cursor.execute(query,data_tuple)
            movies_id_lst.append(cursor.fetchone()[0])
        print(movies_id_lst)

        new_ids = list(filter(lambda x: x not in already_in, movies_id_lst))

        print(new_ids)

        for id in new_ids:
            conn = sqlite3.connect("database1.db")
            cursor = conn.cursor()
            query = f"INSERT INTO stars (person_id, movie_id) VALUES(?,?);"
            data = (str(actor_id),str(id))
            cursor.execute(query, data)
            conn.commit()
            conn.close()
    except EOFError as e:
        print(e)
        messagebox.showerror(title="Error", message= "Something Went Wrong!")
    else:
        messagebox.showinfo(title="Confirmed", message= "Movies are succesfully added")

#Window
window = tk.Tk()
window.title("OMBD")
window.geometry("600x800")
window.minsize(width=600,height=800)
window.maxsize(width=600,height=800)

img_tk = PhotoImage(file="spider.png")

load_frame1()

window.mainloop()