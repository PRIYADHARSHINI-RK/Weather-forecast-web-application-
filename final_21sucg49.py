import json
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import Image, ImageTk

root = Tk()
root.title("Weather API")
root.geometry("898x470+304+204")
root.configure(bg="#57adff")
root.resizable(False, False)

root.geometry()
def getWeather():

    city = textfield.get()
    api_key = "da4bad9437ce7bffedacebb90767cf09"
    # forecast
    api_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response = requests.get(api_url)
    city = textfield.get()

    geolocator = Nominatim(user_agent="geoapiExcercises")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()

    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

    timezone.config(text=result)
    long_lat.config(text=f"{(location.latitude, 4)}°N,{round(location.longitude, 4)}°E")

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    if response.status_code == 200:
        weather_data = response.json()
        display_weather(weather_data)
    else:
        messagebox.showinfo("Error", "Unable to fetch weather data.")


def display_weather(weather_data):
    description = weather_data['list'][0]['weather'][0]['description']
    temp = weather_data['list'][0]['main']['temp']
    humidity = weather_data['list'][0]['main']['humidity']
    pressure = weather_data['list'][0]['main']['pressure']
    wind = weather_data['list'][0]['wind']['speed']
#Condition::percepitation/rain

    t.config(text=(temp, "°C"))
    h.config(text=(humidity, "%"))
    p.config(text=(pressure, "hPa"))
    w.config(text=(wind, "m/s"))
    d.config(text=description)

    farm_text = "Suitable"
    fish_text = "Suitable"
    emp_text = "Suitable"
    farm_color = "#183E0C"
    fish_color = "#183E0C"
    emp_color = "#183E0C"
    if humidity>80:
        farm_text = "Not Suitable"
        fish_text = "Not Suitable"
        emp_text = "Not Suitable"
        farm_color = "#D90C0C"
        fish_color = "#D90C0C"
        emp_color = "#D90C0C"
    elif humidity<60 and wind < 3.0:
        farm_text = "Suitable"
        fish_text = "Suitable"
        emp_text = "Suitable"
        farm_color = "#183E0C"
        fish_color = "#183E0C"
        emp_color = "#183E0C"
    elif humidity<60 and (3.0< wind < 4.0):
        farm_text = "Suitable"
        fish_text = "Managable"
        emp_text = "Suitable"
        farm_color = "#183E0C"
        fish_color = "#F5E038"
        emp_color = "#183E0C"
    elif humidity<60 and ( wind > 4.0):
        farm_text = "Managable"
        fish_text = "Not Suitable"
        emp_text = "Managable"
        farm_color = "#F5E038"
        fish_color = "#D90C0C"
        emp_color = "#F5E038"
    elif (60<humidity<80) and (wind<3.0):
        farm_text = "Suitable"
        fish_text = "Managable"
        emp_text = "Suitable"
        farm_color = "#183E0C"
        fish_color = "#F5E038"
        emp_color = "#183E0C"

    elif (60<humidity<80) and ((3.0<wind<4.0)or wind>4.0):
        farm_text = "Not Suitable"
        fish_text = "Not Suitable"
        emp_text = "Not Suitable"
        farm_color = "#D90C0C"
        fish_color = "#D90C0C"
        emp_color = "#D90C0C"
    temp_label=Label(root, height=1,width=15, font=("Helvetica", 11),  bg="#57adff")
    temp_label.place(x=785, y=125)
    farm = Label(root, text=farm_text, font=("Helvetica", 11), fg=farm_color, bg="#57adff")
    farm.place(x=785, y=125)

    temp_label2=Label(root, height=1,width=15, font=("Helvetica", 11),  bg="#57adff")
    temp_label2.place(x=815, y=155)
    fish = Label(root, text=fish_text, font=("Helvetica", 11), fg=fish_color,bg="#57adff")
    fish.place(x=815, y=155)

    temp_label3=Label(root, height=1,width=15, font=("Helvetica", 11),  bg="#57adff")
    temp_label3.place(x=805, y=185)
    emp = Label(root, text=emp_text, font=("Helvetica", 11), fg=emp_color,bg="#57adff")
    emp.place(x=805, y=185)

    # Display daily icons
    for i in range(1, 8):
        try:
            daily_icon = weather_data['list'][i*5]['weather'][0]['icon']
            set_daily_icon(i, daily_icon, weather_data)
            print(daily_icon)
        except IndexError:
            set_daily_icon(i, 'default')


def set_daily_icon(day_index, icon, weather_data):
    global day1_temp,day2_temp,day3_temp,day4_temp,day5_temp,day6_temp,day7_temp

    icon_path = f"icon/{icon}@2x.png" if icon != 'default' else 'icon/default_icon.png'
    icon_image = Image.open(icon_path)

    # Resize the image
    icon_image = icon_image.resize((50, 50))


# Convert to PhotoImage
    icon_image = ImageTk.PhotoImage(icon_image)

    if day_index == 1:
        firstimage.config(image=icon_image)
        firstimage.image = icon_image
        day_temp=weather_data['list'][day_index*5]['main']['temp_max']
        night_temp=weather_data['list'][day_index*5]['main']['temp_min']
        day1_temp.config(text=f"day:{day_temp}\nnight:{night_temp}")

    elif day_index == 2:
        secondimage.config(image=icon_image)
        secondimage.image = icon_image
        day_temp=weather_data['list'][day_index*5]['main']['temp_max']
        night_temp=weather_data['list'][day_index*5]['main']['temp_min']
        day2_temp.config(text=f"day:{day_temp}\nnight:{night_temp}")

    elif day_index == 3:
        thirdimage.config(image=icon_image)
        thirdimage.image = icon_image
        day_temp=weather_data['list'][day_index*5]['main']['temp_max']
        night_temp=weather_data['list'][day_index*5]['main']['temp_min']
        day3_temp.config(text=f"day:{day_temp}\nnight:{night_temp}")

    elif day_index == 4:
        fourthimage.config(image=icon_image)
        fourthimage.image = icon_image
        day_temp=weather_data['list'][day_index*5]['main']['temp_max']
        night_temp=weather_data['list'][day_index*5]['main']['temp_min']
        day4_temp.config(text=f"day:{day_temp}\nnight:{night_temp}")

    elif day_index == 5:
        fifthimage.config(image=icon_image)
        fifthimage.image = icon_image
        day_temp=weather_data['list'][day_index*5]['main']['temp_max']
        night_temp=weather_data['list'][day_index*5]['main']['temp_min']
        day5_temp.config(text=f"day:{day_temp}\nnight:{night_temp}")

    elif day_index == 6:
        sixthimage.config(image=icon_image)
        sixthimage.image = icon_image
        day_temp=weather_data['list'][day_index*5]['main']['temp_max']
        night_temp=weather_data['list'][day_index*5]['main']['temp_min']
        day6_temp.config(text=f"day:{day_temp}\nnight:{night_temp}")

    elif day_index == 7:
        seventhimage.config(image=icon_image)
        seventhimage.image = icon_image
        day_temp=weather_data['list'][day_index*5]['main']['temp_max']
        night_temp=weather_data['list'][day_index*5]['main']['temp_min']
        day7_temp.config(text=f"day:{day_temp}\nnight:{night_temp}")



# icon
image_icon = PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)

# rounded box
rounded_box = Canvas(root, width=150, height=200, bg="#57adff", highlightthickness=0)
rounded_box.create_rectangle(0, 0, 150, 200, fill="#57adff", outline="#57adff")
rounded_box.place(x=30, y=110)

rounded_box_right = Canvas(root, width=150, height=200, bg="#57adff", highlightthickness=0)
rounded_box_right.create_rectangle(0, 0, 150, 200, fill="#57adff", outline="#57adff")
rounded_box_right.place(x=700, y=110)

# labels
Label(root, text="Temperature", font=('Helvetica,9'), fg="white", bg="#57adff").place(x=30, y=120)
Label(root, text="Humidity", font=('Helvetica,9'), fg="white", bg="#57adff").place(x=30, y=150)
Label(root, text="Pressure", font=('Helvetica,8'), fg="white", bg="#57adff").place(x=30, y=180)
Label(root, text="Wind Speed", font=('Helvetica,7'), fg="white", bg="#57adff").place(x=30, y=210)
Label(root, text="Description", font=('Helvetica,6'), fg="white", bg="#57adff").place(x=30, y=240)

# additional labels on the right
Label(root, text="Farmer:", font=('Helvetica,11'), fg="white", bg="#57adff").place(x=710, y=120)
Label(root, text="Fisherman:", font=('Helvetica,11'), fg="white", bg="#57adff").place(x=710, y=150)
Label(root, text="Employee:", font=('Helvetica,11'), fg="white", bg="#57adff").place(x=710, y=180)

# search box
Search_image = PhotoImage(file="Images/Rounded Rectangle 3.png")
myimage = Label(image=Search_image, bg="#57adff")
myimage.place(x=240, y=120)

weat_image = PhotoImage(file="Images/Layer 7.png")
weatherimage = Label(root, image=weat_image, bg="#203243")
weatherimage.place(x=290, y=127)

textfield = tk.Entry(root, justify='center', width=15, font=('poppins', 25, 'bold'), bg="#203243", border=0, fg="white")
textfield.place(x=370, y=130)

Search_icon = PhotoImage(file="Images/Layer 6.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#203243", command=getWeather)
myimage_icon.place(x=620, y=125)

# Bottom box
frame = Frame(root, width=900, height=180, bg="#212120")
frame.pack(side=BOTTOM)

# bottom boxes
firstbox = PhotoImage(file="Images/Rounded Rectangle 2.png")
secondbox = PhotoImage(file="Images/Rounded Rectangle 2 copy.png")

Label(frame, image=firstbox, bg="#212120").place(x=30, y=20)
Label(frame, image=secondbox, bg="#212120").place(x=300, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=400, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=500, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=600, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=700, y=30)
Label(frame, image=secondbox, bg="#212120").place(x=800, y=30)

# clock (place the time)
clock = Label(root, font=("Helvetica", 30, 'bold'), fg="white", bg="#57adff")
clock.place(x=30, y=20)

# timezone
timezone = Label(root, font=("Helvetica", 20), fg="white", bg="#57adff")
timezone.place(x=700, y=20)

long_lat = Label(root, font=("Helvetica", 10), fg="white", bg="#57adff")
long_lat.place(x=700, y=50)

# Values of temperature, humidity, pressure, wind speed, description
t = Label(root, font=("Helvetica", 11), fg="white", bg="#57adff")
t.place(x=150, y=120)
h = Label(root, font=("Helvetica", 11), fg="white", bg="#57adff")
h.place(x=150, y=150)
p = Label(root, font=("Helvetica", 11), fg="white", bg="#57adff")
p.place(x=150, y=180)
w = Label(root, font=("Helvetica", 11), fg="white", bg="#57adff")
w.place(x=150, y=210)
d = Label(root, font=("Helvetica", 11), fg="white", bg="#57adff")
d.place(x=150, y=240)


# first cell
firstframe = Frame(root, width=232, height=133, bg="#282829")
firstframe.place(x=35, y=315)

day1 = Label(firstframe, font="arial 20", bg="#282829", fg="#fff")
day1.place(x=70, y=5)

firstimage = Label(firstframe, bg="#282829")
firstimage.place(x=40, y=40)  # Adjusted the position

day1_temp= Label(firstframe,font="arial 07 bold", bg="#282829", fg="#57adff")
day1_temp.place(x=90, y=50)

# second cell
secondframe = Frame(root, width=72, height=117, bg="#282829")
secondframe.place(x=305, y=325)

day2 = Label(secondframe, bg="#282829", fg="#fff")
day2.place(x=10, y=2)

secondimage = Label(secondframe, bg="#282829")
secondimage.place(x=7, y=20)

day2_temp= Label(secondframe,font="arial 07 bold", bg="#282829", fg="#FFFFFF")
day2_temp.place(x=4, y=70)

# third cell
thirdframe = Frame(root, width=72, height=115, bg="#282829")
thirdframe.place(x=405, y=325)

day3 = Label(thirdframe, bg="#282829", fg="#fff")
day3.place(x=10, y=2)

thirdimage = Label(thirdframe, bg="#282829")
thirdimage.place(x=7, y=20)

day3_temp= Label(thirdframe,font="arial 07 bold", bg="#282829", fg="#FFFFFF")
day3_temp.place(x=3, y=70)

# fourth cell
fourthframe = Frame(root, width=72, height=115, bg="#282829")
fourthframe.place(x=505, y=325)

fourthimage = Label(fourthframe, bg="#282829")
fourthimage.place(x=7, y=20)

day4 = Label(fourthframe, bg="#282829", fg="#fff")
day4.place(x=10, y=2)

day4_temp= Label(fourthframe,font="arial 07 bold", bg="#282829", fg="#FFFFFF")
day4_temp.place(x=3, y=70)

# fifth cell
fifthframe = Frame(root, width=72, height=115, bg="#282829")
fifthframe.place(x=605, y=325)

day5 = Label(fifthframe, bg="#282829", fg="#fff")
day5.place(x=10, y=2)

fifthimage = Label(fifthframe, bg="#282829")
fifthimage.place(x=7, y=20)

day5_temp= Label(fifthframe,font="arial 07 bold", bg="#282829", fg="#FFFFFF")
day5_temp.place(x=3, y=70)

# sixth cell
sixthframe = Frame(root, width=72, height=115, bg="#282829")
sixthframe.place(x=705, y=325)

day6 = Label(sixthframe, bg="#282829", fg="#fff")
day6.place(x=10, y=2)

sixthimage = Label(sixthframe, bg="#282829")
sixthimage.place(x=7, y=20)

day6_temp= Label(sixthframe,font="arial 07 bold", bg="#282829", fg="#FFFFFF")
day6_temp.place(x=3, y=70)
# seventh cell
seventhframe = Frame(root, width=72, height=115, bg="#282829")
seventhframe.place(x=805, y=325)

day7 = Label(seventhframe, bg="#282829", fg="#fff")
day7.place(x=10, y=2)

seventhimage = Label(seventhframe, bg="#282829")
seventhimage.place(x=7, y=20)

day7_temp= Label(seventhframe,font="arial 07 bold", bg="#282829", fg="#FFFFFF")
day7_temp.place(x=3, y=70)

first=datetime.now()
day1.config(text=first.strftime("%A")[:3])

second=first+timedelta(days=1)
day2.config(text=second.strftime("%A")[:3])

third=first+timedelta(days=2)
day3.config(text=third.strftime("%A")[:3])

fourth=first+timedelta(days=3)
day4.config(text=fourth.strftime("%A")[:3])

fifth=first+timedelta(days=4)
day5.config(text=fifth.strftime("%A")[:3])

sixth=first+timedelta(days=5)
day6.config(text=sixth.strftime("%A")[:3])

seventh=first+timedelta(days=6)
day7.config(text=seventh.strftime("%A")[:3])


root.mainloop()