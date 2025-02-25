import tkinter as tk
from tkinter import ttk, messagebox
import time
import mysql.connector as mysql
import sqlite3

def system():
    root = tk.Tk()
    root.geometry("1300x800")
    root.title("Restaurant Billing System")
    root.configure(bg="#f0f0f0")  # Overall background color

    # ------------------------------
    # Define StringVar Variables for Order Details
    # ------------------------------
    orderno   = tk.StringVar()
    pizza     = tk.StringVar()
    burger    = tk.StringVar()
    icecream  = tk.StringVar()
    drinks    = tk.StringVar()
    cost      = tk.StringVar()
    subtotal  = tk.StringVar()
    tax       = tk.StringVar()
    service   = tk.StringVar()
    total     = tk.StringVar()

    # ------------------------------
    # Function Definitions
    # ------------------------------
    def Database():
        global connectn, cursor
        try:
            connectn = mysql.connect(host='localhost', database="Restaurant", user="root", password="root")
            cursor = connectn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Restaurantrecords("
                "ordno VARCHAR(255), piz VARCHAR(255), bur VARCHAR(255), "
                "ice VARCHAR(255), dr VARCHAR(255), ct VARCHAR(255), sb VARCHAR(255), "
                "tax VARCHAR(255), sr VARCHAR(255), tot VARCHAR(255))"
            )
            connectn.commit()
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def tottal():
        try:
            pi = float(pizza.get() or 0)
            bu = float(burger.get() or 0)
            ice = float(icecream.get() or 0)
            dr = float(drinks.get() or 0)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for the items.")
            return
        costpi = pi * 14
        costbu = bu * 4
        costice = ice * 6
        costdr = dr * 2
        costofmeal = costpi + costbu + costice + costdr
        ptax = costofmeal * 0.18
        sub = costofmeal
        ser = costofmeal / 99
        overall = sub + ptax + ser
        cost.set(f"{costofmeal:.2f}")
        tax.set(f"{ptax:.2f}")
        subtotal.set(f"{sub:.2f}")
        service.set(f"{ser:.2f}")
        total.set(f"{overall:.2f}")

    def reset():
        orderno.set("")
        pizza.set("")
        burger.set("")
        icecream.set("")
        drinks.set("")
        cost.set("")
        subtotal.set("")
        tax.set("")
        service.set("")
        total.set("")

    def exit_app():
        root.destroy()

    def DisplayData():
        Database()
        my_tree.delete(*my_tree.get_children())
        cur = connectn.cursor()
        cur.execute("SELECT * FROM Restaurantrecords")
        for data in cur.fetchall():
            my_tree.insert('', 'end', values=data)
        cur.close()
        connectn.close()

    def add():
        Database()
        orders = orderno.get()
        pizzas = pizza.get()
        burgers = burger.get()
        ices = icecream.get()
        drinkss = drinks.get()
        costs = cost.get()
        subtotals = subtotal.get()
        taxs = tax.get()
        services = service.get()
        totals = total.get()
        if (orders == "" or pizzas == "" or burgers == "" or ices == "" or
            drinkss == "" or costs == "" or subtotals == "" or taxs == "" or
            services == "" or totals == ""):
            messagebox.showinfo("Warning", "Please fill all fields!")
        else:
            cur = connectn.cursor()
            query = ("INSERT INTO Restaurantrecords (ordno, piz, bur, ice, dr, ct, sb, tax, sr, tot) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            values = (orders, pizzas, burgers, ices, drinkss, costs, subtotals, taxs, services, totals)
            cur.execute(query, values)
            connectn.commit()
            messagebox.showinfo("Message", "Stored successfully")
            cur.close()
            connectn.close()
            DisplayData()

    def Delete():
        Database()
        if not my_tree.selection():
            messagebox.showwarning("Warning", "Select data to delete")
            return
        result = messagebox.askquestion('Confirm', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = my_tree.focus()
            contents = my_tree.item(curItem)
            selecteditem = contents['values']
            cur = connectn.cursor()
            query = "DELETE FROM Restaurantrecords WHERE ordno = %s"
            cur.execute(query, (selecteditem[0],))
            connectn.commit()
            my_tree.delete(curItem)
            cur.close()
            connectn.close()

    # --- New: Move feedbackk definition here ---
    def feedbackk():
        feed = tk.Tk()
        feed.geometry("600x500")
        feed.title("Submit Feedback Form")
        feed.configure(bg="#dfe6e9")
        
        conn = sqlite3.connect("Restaurant.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS FEEDBACK(n TEXT, eid TEXT, feedback5 TEXT, com TEXT)")
        conn.commit()
        
        name_var = tk.StringVar()
        email_var = tk.StringVar()
        
        def submit_feedback():
            n = name_var.get()
            eid = email_var.get()
            com = txt.get('1.0', tk.END).strip()
            feedback1 = ""
            feedback2 = ""
            feedback3 = ""
            feedback4 = ""
            if checkvar1.get() == "1":
                feedback1 = "Excellent"
            if checkvar2.get() == "1":
                feedback2 = "Good"
            if checkvar3.get() == "1":
                feedback3 = "Average"
            if checkvar4.get() == "1":
                feedback4 = "Poor"
            feedback5 = " ".join(filter(None, [feedback1, feedback2, feedback3, feedback4]))
            cur.execute("INSERT INTO FEEDBACK (n, eid, com, feedback5) VALUES (?, ?, ?, ?)",
                        (n, eid, com, feedback5))
            conn.commit()
            messagebox.showinfo("Message", "Feedback submitted!")
            feed.destroy()
        
        def cancel_feedback():
            feed.destroy()
        
        tk.Label(feed, font=("Calisto MT", 15, "bold"), text="Thanks for Visiting!", fg="black", bg="#dfe6e9")\
            .pack(side=tk.TOP, pady=10)
        tk.Label(feed, font=("Calisto MT", 15), text="We're glad you chose us! Please tell us how it was!", fg="black", bg="#dfe6e9")\
            .pack(side=tk.TOP)
        
        tk.Label(feed, font=('vardana', 15), text="Name:-", fg="black", bd=10, anchor="w", bg="#dfe6e9")\
            .place(x=10, y=150)
        tk.Entry(feed, font=('vardana', 15), bd=6, insertwidth=2, bg="white", justify='right', textvariable=name_var)\
            .place(x=15, y=185)
        
        tk.Label(feed, font=('vardana', 15), text="Email:-", fg="black", bd=10, anchor="w", bg="#dfe6e9")\
            .place(x=280, y=150)
        tk.Entry(feed, font=('vardana', 15), bd=6, insertwidth=2, bg="white", justify='right', textvariable=email_var)\
            .place(x=285, y=185)
        
        tk.Label(feed, font=('vardana', 15), text="How would you rate us?", fg="black", bd=10, anchor="w", bg="#dfe6e9")\
            .place(x=10, y=215)
        checkvar1 = tk.StringVar()
        checkvar2 = tk.StringVar()
        checkvar3 = tk.StringVar()
        checkvar4 = tk.StringVar()
        c1 = tk.Checkbutton(feed, font=('Arial', 10, "bold"), text="Excellent", bg="white",
                            variable=checkvar1, onvalue="1", offvalue="0")
        c1.deselect()
        c1.place(x=15, y=265)
        c2 = tk.Checkbutton(feed, font=('Arial', 10, "bold"), text="Good", bg="white",
                            variable=checkvar2, onvalue="1", offvalue="0")
        c2.deselect()
        c2.place(x=120, y=265)
        c3 = tk.Checkbutton(feed, font=('Arial', 10, "bold"), text="Average", bg="white",
                            variable=checkvar3, onvalue="1", offvalue="0")
        c3.deselect()
        c3.place(x=220, y=265)
        c4 = tk.Checkbutton(feed, font=('Arial', 10, "bold"), text="Poor", bg="white",
                            variable=checkvar4, onvalue="1", offvalue="0")
        c4.deselect()
        c4.place(x=320, y=265)
        
        tk.Label(feed, font=('Arial', 15), text="Comments", fg="black", bd=10, anchor="w", bg="#dfe6e9")\
            .place(x=10, y=300)
        txt = tk.Text(feed, width=50, height=5)
        txt.place(x=15, y=335)
        
        tk.Button(feed, font=("Arial", 14), text="Submit", fg="black", bg="green", bd=2, command=submit_feedback)\
            .place(x=145, y=430)
        tk.Button(feed, font=("Arial", 14), text="Cancel", fg="black", bg="red", bd=2, command=cancel_feedback)\
            .place(x=245, y=430)
        
        feed.mainloop()

    def menu():
        roott = tk.Toplevel()
        roott.title("Price Menu")
        roott.geometry("300x300")
        tk.Label(roott, font=("Arial", 20, "bold"), text="ITEM LIST", fg="black", bd=10)\
            .grid(row=0, column=0)
        tk.Label(roott, font=("Arial", 20, "bold"), text="Prices", fg="black", bd=10)\
            .grid(row=0, column=3)
        tk.Label(roott, font=("Arial", 20, "bold"), text="Pizza", fg="Blue", bd=10)\
            .grid(row=1, column=0)
        tk.Label(roott, font=("Arial", 20, "bold"), text="14$", fg="blue", bd=10)\
            .grid(row=1, column=3)
        tk.Label(roott, font=("Arial", 20, "bold"), text="Burger", fg="Blue", bd=10)\
            .grid(row=3, column=0)
        tk.Label(roott, font=("Arial", 20, "bold"), text="4$", fg="blue", bd=10)\
            .grid(row=3, column=3)
        tk.Label(roott, font=("Arial", 20, "bold"), text="Ice-Cream", fg="Blue", bd=10)\
            .grid(row=4, column=0)
        tk.Label(roott, font=("Arial", 20, "bold"), text="6$", fg="blue", bd=10)\
            .grid(row=4, column=3)
        tk.Label(roott, font=("Arial", 20, "bold"), text="Drinks", fg="Blue", bd=10)\
            .grid(row=5, column=0)
        tk.Label(roott, font=("Arial", 20, "bold"), text="2$", fg="blue", bd=10)\
            .grid(row=5, column=3)
    
    # ===============================
    # Layout Frames for Order Entry and Order Records
    # ===============================
    # Top frame: Title and Time
    topframe = tk.Frame(root, bg="#34495e", height=60)
    topframe.pack(side=tk.TOP, fill=tk.X)
    tk.Label(topframe, font=('Arial', 25, 'bold'), text="Restaurant Billing System", 
             fg="white", bg="#34495e").grid(row=0, column=0, padx=20, pady=5)
    localtime = time.asctime(time.localtime(time.time()))
    tk.Label(topframe, font=('Arial', 15), text=localtime, fg="lightblue", bg="#34495e")\
        .grid(row=1, column=0, padx=20)
    
    # Left frame: Order Entry Form
    leftframe = tk.Frame(root, bg="#ecf0f1", width=700, height=700)
    leftframe.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    
    # Right frame: Order Records (expanded)
    rightframe = tk.Frame(root, bg="white")
    rightframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    labels = ["Order No.", "Pizza", "Burger", "Ice Cream", "Drinks", "Cost", 
              "Subtotal", "Tax", "Service", "Total"]
    vars_list = [orderno, pizza, burger, icecream, drinks, cost, subtotal, tax, service, total]
    
    for i, (text, var) in enumerate(zip(labels, vars_list)):
        tk.Label(leftframe, font=('Arial', 16, 'bold'), text=text, fg="black", bd=5, 
                 anchor="w", bg="#ecf0f1").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(leftframe, font=('Arial', 16), bd=6, width=10, insertwidth=4, 
                 justify='right', textvariable=var).grid(row=i, column=1, padx=10, pady=5)
    
    tk.Button(leftframe, font=('Arial', 12, 'bold'), text="Total", bg="#27ae60", fg="white",
              bd=3, padx=5, pady=5, width=5, command=tottal).grid(row=2, column=2, padx=10, pady=5)
    tk.Button(leftframe, font=('Arial', 12, 'bold'), text="Add", bg="#2980b9", fg="white",
              bd=3, padx=5, pady=5, width=5, command=add).grid(row=1, column=2, padx=10, pady=5)
    tk.Button(leftframe, font=('Arial', 12, 'bold'), text="Reset", bg="#f39c12", fg="white",
              bd=3, padx=5, pady=5, width=5, command=reset).grid(row=4, column=2, padx=10, pady=5)
    tk.Button(leftframe, font=('Arial', 12, 'bold'), text="Delete", bg="#c0392b", fg="white",
              bd=3, padx=5, pady=5, width=7, command=Delete).grid(row=4, column=3, padx=10, pady=5)
    tk.Button(leftframe, font=('Arial', 12, 'bold'), text="Exit", bg="#95a5a6", fg="white",
              bd=3, padx=5, pady=5, width=7, command=exit_app).grid(row=6, column=2, padx=10, pady=5)
    
    tk.Button(leftframe, font=('Arial', 12, 'bold'), text="Feedback", bg="#8e44ad", fg="white",
              bd=3, padx=5, pady=5, width=8, command=feedbackk).grid(row=8, column=2, padx=10, pady=5)
    tk.Button(leftframe, font=('Arial', 12, 'bold'), text="Menu", bg="#16a085", fg="white",
              bd=3, padx=5, pady=5, width=8, command=menu).grid(row=2, column=3, padx=10, pady=5)
    
    style = ttk.Style()
    style.configure("Treeview", foreground="black", rowheight=40, fieldbackground="white")
    style.map("Treeview", background=[("selected", "lightblue")])
    
    my_tree = ttk.Treeview(rightframe, columns=("ordno", "piz", "bur", "ice", "dr", "ct", "sb", "tax", "sr", "tot"), show='headings')
    my_tree.column("ordno", anchor=tk.CENTER, width=80)
    my_tree.column("piz", anchor=tk.CENTER, width=60)
    my_tree.column("bur", anchor=tk.CENTER, width=50)
    my_tree.column("ice", anchor=tk.CENTER, width=80)
    my_tree.column("dr", anchor=tk.CENTER, width=50)
    my_tree.column("ct", anchor=tk.CENTER, width=50)
    my_tree.column("sb", anchor=tk.CENTER, width=120)
    my_tree.column("tax", anchor=tk.CENTER, width=50)
    my_tree.column("sr", anchor=tk.CENTER, width=120)
    my_tree.column("tot", anchor=tk.CENTER, width=70)
    
    my_tree.heading("ordno", text="Order No", anchor=tk.CENTER)
    my_tree.heading("piz", text="Pizza", anchor=tk.CENTER)
    my_tree.heading("bur", text="Burger", anchor=tk.CENTER)
    my_tree.heading("ice", text="Ice Cream", anchor=tk.CENTER)
    my_tree.heading("dr", text="Drinks", anchor=tk.CENTER)
    my_tree.heading("ct", text="Cost", anchor=tk.CENTER)
    my_tree.heading("sb", text="Subtotal", anchor=tk.CENTER)
    my_tree.heading("tax", text="Tax", anchor=tk.CENTER)
    my_tree.heading("sr", text="Service", anchor=tk.CENTER)
    my_tree.heading("tot", text="Total", anchor=tk.CENTER)
    
    my_tree.pack(fill=tk.BOTH, expand=True)
    
    DisplayData()
    
    root.mainloop()

system()
