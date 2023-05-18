import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import nltk
from nltk.metrics import precision, recall, f_measure
from difflib import get_close_matches


# Funcție pentru încărcarea dicționarului din fișier


def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-16') as file:
        text = file.read()
        words = text.split()
        dictionary = {word: None for word in words}
    return dictionary







# Funcție pentru corectarea erorilor în text
def correct_errors(dictionary, text):
    tokenized_text = nltk.word_tokenize(text)
    corrected_text = []

    for word in tokenized_text:
        if word not in dictionary:
            closest_match = get_close_matches(word, dictionary.keys(), n=1, cutoff=0.8)
            if closest_match:
                corrected_text.append(closest_match[0])
            else:
                corrected_text.append(word)
        else:
            corrected_text.append(word)

    return ' '.join(corrected_text)

# Funcție pentru calcularea măsurilor de evaluare
# Funcție pentru calcularea măsurilor de evaluare
def evaluate_results(original_text, corrected_text):
    original_tokens = set(nltk.word_tokenize(original_text))
    corrected_tokens = set(nltk.word_tokenize(corrected_text))

    tp = len(original_tokens.intersection(corrected_tokens))
    fp = len(corrected_tokens - original_tokens)
    fn = len(original_tokens - corrected_tokens)

    precision_score = precision(set(original_tokens), set(corrected_tokens))
    recall_score = recall(set(original_tokens), set(corrected_tokens))
    f1_score = f_measure(set(original_tokens), set(corrected_tokens))

    return precision_score, recall_score, f1_score


# Funcție pentru deschiderea fișierului de text
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
        corrected_text = correct_errors(dictionary, text)
        precision_score, recall_score, f1_score = evaluate_results(text, corrected_text)
        messagebox.showinfo('Rezultate', f'Precision: {precision_score:.2f}\nRecall: {recall_score:.2f}\nF1 Score: {f1_score:.2f}')

# Funcție pentru închiderea aplicației
def exit_app():
    root.destroy()

# Încărcare dicționar
dictionary = load_dictionary('TextPentruDictionar.txt')

# Creare interfață grafică
root = tk.Tk()
root.title('Corectare Text')
root.geometry('300x150')

# Butonul pentru deschiderea fișierului de text
open_button = tk.Button(root, text='Deschide fișier', command=open_file)
open_button.pack(pady=20)

# Butonul pentru închiderea aplicației
exit_button = tk.Button(root, text='Ieșire', command=exit_app)
exit_button.pack()

# Rulare interfață grafică
root.mainloop()
