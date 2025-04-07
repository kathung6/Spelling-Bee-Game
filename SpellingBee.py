# Description: A simple game in which you create as many words as possible
# given 7 letters, one of which is a must be in the word


import random
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# ----- GAME LOGIC -----

#urls of word lists
word_sources = [
    "https://www.mit.edu/~ecprice/wordlist.10000",
    "https://websites.umich.edu/~jlawler/wordlist",
]

#empty list to store words in
WORDS = []

#accesses the url and fetches the data
for url in word_sources:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            words = response.content.splitlines()
            decoded_words = [] #empty list to store decoded words in
            for word in words:
                decoded_word = word.decode("utf-8").strip() #decodes the words
                decoded_words.append(decoded_word)
            WORDS.extend(decoded_words)
        else:
            print(f"Failed to fetch words from {url}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    

#remove duplicate words
WORDS = list(set(WORDS))
    
#creating a list for words that are 7 letters long
seven_letter_words = []
for word in WORDS:
    if len(word) == 7 and "'" not in word:
        seven_letter_words.append(word)

# if there are seven letter words, a daily word is chosen at random          
if seven_letter_words:
    daily_word = random.choice(seven_letter_words)
    #golden letter is chosen  
    golden_index = random.randint(0,6)
    golden_letter = daily_word[golden_index]
else:
    print("There are no 7 letter words available in this list.")
    daily_word = "UNKNOWN"
    
# ----- GAME GUI -----
#create gui window using tkinter
root = tk.Tk()
root.title("Spelling Bee")

root.geometry("800x600")


points = 0
# displays and updates point system 
def update_points_display():
    points_label.config(text=f"Points: {points}")

#type each letter as buttons are clicked
def on_button_click(letter):
    word_entry.config(state="normal")
    current_text = word_entry.get()
    word_entry.delete(0, tk.END)
    word_entry.insert(0, current_text + letter)
    word_entry.config(state="readonly")
    
#empty string to store words
created_words = []
found_words = 0
    
# function to define what happens when the submit button is clicked
def on_enter_click():
    global points
    #creating words logic
    compliments = ["Great job!", "Fantastic!", "Wow!"]
    #ensures all words are the same format
    attempted_word = word_entry.get().strip().lower()
    true_word = ''
    
    #if the attempted word is less than 3 characters prints too short and deletes the text box
    if len(attempted_word) <= 3:
        temporary_message("Too short!")
        word_entry.config(state="normal")
        word_entry.delete(0, tk.END)
        word_entry.config(state="readonly")
        return

    #if the attempted word is in the words list created ealier and the golden letter isn't in the word: error
    if attempted_word in WORDS and golden_letter not in attempted_word:
        temporary_message("Missing golden letter")
    #if attempted word is in words and golden letter is in attempted word, it's a true word
    elif attempted_word in WORDS and golden_letter in attempted_word:
        true_word = attempted_word
        if attempted_word in created_words:
            temporary_message("You already found this word")
        else:
            temporary_message(random.choice(compliments))
            created_words.append(true_word)
            #point system: 4 letter words are one point, words longer than 4 char are 1 point each char
            if len(true_word) == 4:
                points += 1
            elif len(true_word) > 4:
                points += len(true_word)
            update_points_display()
    else:
        temporary_message("Sorry, that's not a valid word")
    
    
    #deletes text entry field and returns status to readonly
    word_entry.config(state="normal")
    word_entry.delete(0, tk.END)
    word_entry.config(state="readonly")

# shuffles the letters if shuffle button is clicked
def shuffle_click():
    random.shuffle(shuffled_letters)
    golden_index_shuffled = shuffled_letters.index(golden_letter)
    for index, letter in enumerate(shuffled_letters):
        button = tk.Button(
            button_frame, 
            text = letter.upper(),
            width=4,
            height=2,
            bg="yellow" if index == golden_index_shuffled else "lightgray",
            command=lambda l=letter: on_button_click(l)
        )
        button.grid(row=0, column=index, padx = 5, pady = 5)

# deletes the last entered letter if delete button is clicked
def on_backspace_click():
    current_text = word_entry.get()
    new_text = current_text[:-1]
    word_entry.config(state="normal")
    word_entry.delete(0, tk.END)
    word_entry.insert(0, new_text)
    word_entry.config(state="readonly")
    
def temporary_message(message, duration=2):
    popup = tk.Toplevel(root)
    popup.title("")
    label = tk.Label(popup, text=message, padx=10, pady=10)   
    label.pack() 
    
    def close_message():
        popup.destroy()
        
    popup.after(int(duration*800), close_message)
    
def levels():
    total_words = 0
    percentage_of_words = found_words/total_words
    rankings = ["beginner","good start", "moving up", "good", "solid", "nice", "great", "amazing", "genuis"]
    
    for word in WORDS:
        if golden_letter in word:
            total_words += 1
            
    if percentage_of_words >= 10:
        temporary_message(rankings[0])
    elif percentage_of_words >= 20:
        temporary_message(rankings[1])
    elif percentage_of_words >= 30:
        temporary_message(rankings[2])
    elif percentage_of_words >= 40:
        temporary_message(rankings[3])
    elif percentage_of_words >= 50:
        temporary_message(rankings[4])
    elif percentage_of_words >= 50:
        temporary_message(rankings[5])
    elif percentage_of_words >= 50:
        temporary_message(rankings[6])
    elif percentage_of_words >= 50:
        temporary_message(rankings[7])
    elif percentage_of_words >= 50:
        temporary_message(rankings[8])

        

points_label = tk.Label(root, text=f"Points: {points}")
points_label.pack(pady=10)
button_frame = tk.Frame(root)
button_frame.pack(pady=20)
shuffled_letters = list(daily_word)
random.shuffle(shuffled_letters)


golden_index_shuffled = shuffled_letters.index(golden_letter)

for index, letter in enumerate(shuffled_letters):
    button = tk.Button(
        button_frame, 
        text = letter.upper(),
        width=4,
        height=2,
        bg="yellow" if index == golden_index_shuffled else "lightgray",
        command=lambda l=letter: on_button_click(l)
    )
    button.grid(row=0, column=index, padx = 5, pady = 5)
    
word_entry = tk.Entry(root)
word_entry.pack(pady=10)


#button creations
enter_button =  tk.Button(text="SUBMIT", width=10, command=on_enter_click)
enter_button.pack(pady=20)

backspace_button = tk.Button(text="BACKSPACE", width = 10, command=on_backspace_click)
backspace_button.pack(pady=20)

shuffle_button = tk.Button(text="SHUFFLE", width=10, command=shuffle_click)
shuffle_button.pack(pady=10)

root.mainloop()
