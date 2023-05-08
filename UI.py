import tkinter
import requests

from tkinter import *
import requests

root = Tk()
root.title("Restaurant App")
root.geometry("400x400")

def register():

    data = {
        "username": username.get(),
        "password": password.get(),
        "photo": photo.get(),
        "mobile": mobile.get(),
        "address": address.get()
    }
    response = requests.post(url, json=data)
    print(response.json())

def associate():

    data = {"restaurant_id": restaurant_id.get()}
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.put(url, json=data, headers=headers)
    print(response.json())

def take_order():

    data = {
        "customer_name": customer_name.get(),
        "table_id": table_id.get(),
        "items": items.get()
    }
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.post(url, json=data, headers=headers)#replace the url, comp7033-8fb0726ce29c.json
    print(response.json())

username_label = Label(root, text="Username:")
username_label.pack()
username = Entry(root)
username.pack()

password_label = Label(root, text="Password:")
password_label.pack()
password = Entry(root, show="*")
password.pack()

photo_label = Label(root, text="Photo:")
photo_label.pack()
photo = Entry(root)
photo.pack()

mobile_label = Label(root, text="Mobile:")
mobile_label.pack()
mobile = Entry(root)
mobile.pack()

address_label = Label(root, text="Address:")
address_label.pack()
address = Entry(root)
address.pack()

restaurant_id_label = Label(root, text="Restaurant ID:")
restaurant_id_label.pack()
restaurant_id = Entry(root)
restaurant_id.pack()

customer_name_label = Label(root, text="Customer Name:")
customer_name_label.pack()
customer_name = Entry(root)
customer_name.pack()

table_id_label = Label(root, text="Table ID:")
table_id_label.pack()
table_id = Entry(root)
table_id.pack()

items_label = Label(root, text="Items:")
items_label.pack()
items = Entry(root)
items.pack()

register_button = Button(root, text="Register", command=register)
register_button.pack()

associate_button = Button(root, text="Associate", command=associate)
associate_button.pack()

take_order_button = Button(root, text="Take Order", command=take_order)
take_order_button.pack()

root.mainloop()


