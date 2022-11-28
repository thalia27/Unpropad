import os


from flask import Flask, request, render_template, send_from_directory


from selenium import webdriver

from datetime import datetime

import glob
import os
import cv2

import time
from datetime import timedelta




project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './')
app = Flask(__name__, template_folder=template_path)

def speed_and_file_func():
    web_driver = r"C:\Users\irsyanti.t\Documents\chromedriver_win32\chromedriver.exe"
    driver = webdriver.Chrome(web_driver)
    driver.get('http://badboihcr019.bcc.pg.com:9092/kapacitor/v1/tasks/line_speed/line_speed')
    time.sleep(1)
    data_from_bb = driver.find_element_by_tag_name("body").text

    A = data_from_bb.split(",")

    B = data_from_bb.replace("{", "")
    B = B.replace("}", "")
    B = B.replace("[", "")
    B = B.replace("]", "")
    B = B.replace("T", "_")
    B = B.split(",")
    now = datetime.now()


    final_time = now + timedelta(hours=5)
    dt_string_final = final_time.strftime("%Y-%m-%d_%H:%M")
    index = [idx for idx, s in enumerate(B) if dt_string_final in s]
    index_need = index[0] + 1
    print(index_need)
    line_speed_current = B[(index_need)]
    print(line_speed_current)
    driver.quit()
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d")
    list_of_files = glob.glob('//blisscr119.bcc.pg.com/Images/Defect/' + dt_string + '/**/**/*.bmp')
    try:
        latest_file = max(list_of_files, key=os.path.getctime)
    except:
        pass
    if int(line_speed_current) == 0:

        #dt_string = "20211119"
          # * means all if need specific format then *.csv
        try:

            print(latest_file)
            filename_time = os.path.basename(latest_file)
            filename_time = filename_time.split("_")[4]
            times = list(filename_time)
            time_hr = times[0]+times[1]
            time_min = times[2]+times[3]
            time_sec = times[4] + times[5]
            filename_time = "Linie stoppt. Das letzte Defektbild wurde heute um " + time_hr+ ":" + time_min+ ":" +time_sec+ " Uhr aufgenommen."
            img = cv2.imread(latest_file)
            cv2.imwrite("images/recent.bmp",img)
        except:
            filename_time = "Linie stoppt, aber kein Defektbild kann gefunden werden"
            img = cv2.imread("404/not_found.jpg")
            cv2.imwrite("images/recent.bmp", img)

    else:
        try:
            filename_time = os.path.basename(latest_file)
            filename_time = filename_time.split("_")[4]
            times = list(filename_time)
            time_hr = times[0] + times[1]
            time_min = times[2] + times[3]
            time_sec = times[4] + times[5]
            filename_time = "Linie läuft. Das letzte Defektbild wurde heute um " + time_hr + ":" + time_min + ":" + time_sec + " Uhr aufgenommen."
            img = cv2.imread(latest_file)
            cv2.imwrite("images/recent.bmp", img)
        except:
            filename_time = "Linie läuft, aber kein aktuelles Defektbild kann gefunden werden"
            img = cv2.imread("404/not_found.jpg")
            cv2.imwrite("images/recent.bmp", img)

    return filename_time

@app.route('/upload/<filename>')
def send_image(filename):
    speed_and_file_func()
    return send_from_directory("images", filename)

@app.route('/L19')
def get_gallery():
    image_names_a = speed_and_file_func()
    image_names = os.listdir('./images')
    speed_and_file_func()
    for filename in image_names:
        filepath = os.path.join('./images', filename)
        os.remove(filepath)
    #print(image_names)
    return render_template("index.html", image_names=image_names, image_names_a =image_names_a )

if __name__ == "__main__":
    app.debug = True
    app.run(host='155.128.200.98', port=5000)
