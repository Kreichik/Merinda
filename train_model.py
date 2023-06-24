# Файл train_model.py, который является библиотекой
import os
import cv2
count = 0
def create_photo(name):
    cap = cv2.VideoCapture(0)
    if not os.path.exists(f'data/{name}'):
        os.makedirs(f'data/{name}')
    count = 0
    print("Чтобы сделать снимок нажми ПРОБЕЛ, для того чтобы завершить нажмите ESC")
    while True:
        ret, frame = cap.read()
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1)
        if key == ord(' '):
            filename = f"capture_{count}.jpg"
            filepath = os.path.join(f'data/{name}', filename)
            cv2.imwrite(filepath, frame)

            print(f"Изображение {filename} сохранено в папку {name}")
            img = cv2.imread(f"data/{name}/capture_{count}.jpg")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
                faces = img[y:y + h, x:x + w]
                cv2.imwrite(f"face_{count}.jpg", faces)
            count += 1
        if key == 27:
            print("Изображения успешно обработаны")
            break
    cap.release()
    cv2.destroyAllWindows()

while True:
    img = cv2.imread(f"data/altynay/capture_{count}.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
        faces = img[y:y + h, x:x + w]
        cv2.imwrite(f"face_{count}.jpg", faces)
    count += 1