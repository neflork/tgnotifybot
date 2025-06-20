import tkinter as tk

def convert():
    try:
        meters = float(entry.get())
        feet = meters * 3.28084
        result_label.config(text=f"{meters} м = {feet:.2f} футов")
    except ValueError:
        result_label.config(text="Введите число!")

# Создаем главное окно
root = tk.Tk()
root.title("Конвертер метров в футы")

# Поле ввода
entry = tk.Entry(root, width=20)
entry.pack(pady=10)

# Кнопка конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert)
convert_button.pack(pady=5)

# Метка для результата
result_label = tk.Label(root, text="Введите метры")
result_label.pack(pady=10)

# Запускаем приложение
root.mainloop()