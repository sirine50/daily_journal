import tkinter as tk
from transformers import pipeline
import json
import os

if os.path.exists("daily_journal.json"):
    with open("daily_journal.json", "r") as file:
        daily_journal = json.load(file)
else:        
    daily_journal = []

window = tk.Tk()
window.title("Daily Mood Journal")
window.geometry("500x400")
window.configure(bg="#f5f5f5")
default_font = ("Arial", 12)
button_style = {"font": default_font, "bg": "#4CAF50", "fg": "white", "relief": "flat", "width": 15, "height": 2}
sentiment_analysis = pipeline("sentiment-analysis") 

WelcomePage = tk.Frame(window)
EntryPage = tk.Frame(window)
ReviewPage = tk.Frame(window)

for frame in (WelcomePage, EntryPage, ReviewPage):
    frame.pack(fill="both", expand=True)

def show_frame(frame1):
    for frame in (WelcomePage, EntryPage, ReviewPage):
        frame.pack_forget()
    
    frame1.pack()


def write_entry():
    text_box.delete("1.0", "end")
    show_frame(EntryPage)

def submit_entry():
    text = text_box.get("1.0", tk.END).strip()
    sentiment = sentiment_analysis(text)[0]
    if text:
        daily_journal.append({
            "text": text,
            "sentiment": sentiment["label"],
            "score": sentiment["score"]
        })
        daily_journal.reverse()
        with open("daily_journal.json", "w") as file:
            json.dump(daily_journal, file, indent=4)
        text_box.delete("1.0", "end") 


def load_review_page():
    for widget in ReviewPage.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(ReviewPage)
    scrollbary = tk.Scrollbar(ReviewPage, orient="vertical", command=canvas.yview)
    scrollbarx = tk.Scrollbar(ReviewPage, orient="horizontal", command=canvas.xview)
    scrollbale_frame = tk.Frame(canvas)

    scrollbale_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=scrollbale_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbary.pack(side="right", fill="y")
    scrollbarx.pack(side="bottom", fill="x")

    entry_frame = tk.Frame(scrollbale_frame, bg="white", bd=2, relief="groove", padx=10, pady=10)
    entry_frame.pack(fill="x", padx=10, pady=10)

    for i, entry in enumerate(daily_journal):
        tk.Label(entry_frame, text=f"Entry: {entry['text'].capitalize()}", font=("Arial", 14), bg="white", anchor="w", wraplength=400, justify="left").pack(fill="x")
        tk.Label(entry_frame, text=f"Sentiment: {entry['sentiment'].capitalize()} ({round(entry['score']*100,1)}%)", font=("Arial", 12), fg="gray", bg="white", anchor="w").pack(fill="x")
        tk.Button(entry_frame, text="Delete", command=lambda idx=i: delete_entry(idx), font=("Arial", 11), bg="#e74c3c", fg="white", relief="flat").pack(pady=5)

    return_button2 = tk.Button(scrollbale_frame, text=" Return ", command=lambda: show_frame(WelcomePage), font=default_font, bg="#4CAF50", fg="white")
    return_button2.pack(pady=10)


def delete_entry(index):
      daily_journal.remove(daily_journal[index])
      with open("daily_journal.json", "w") as file:
        json.dump(daily_journal, file, indent=4)   
      load_review_page()   



# WelcomePage widgets
tk.Label(WelcomePage, text="✨ Daily Mood Journal ✨", font=("Arial", 22, "bold"), bg="#f5f5f5").pack(pady=20)
tk.Label(WelcomePage, text="Track your thoughts and moods easily.", font=("Arial", 14), bg="#f5f5f5", fg="gray").pack(pady=5)
tk.Label(WelcomePage, text="Click the button below to write a new entry").pack(pady=10)
tk.Button(WelcomePage, text="Write New Entry", command=write_entry, font=default_font, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(WelcomePage, text="  Review Entrys  ", command=lambda: [load_review_page() ,show_frame(ReviewPage)], font=default_font, bg="#4CAF50", fg="white").pack(pady=10)

# EntryPage widgets
tk.Label(EntryPage, text="Write your journal entry below:", font=default_font).pack(pady=10)
text_box = text_box = tk.Text(EntryPage, width=50, height=10, font=default_font, bd=2, relief="groove", wrap="word")
text_box.pack(pady=10)
submit_button = tk.Button(EntryPage, text=" Submit ", command=submit_entry, font=default_font, bg="#4CAF50", fg="white")
submit_button.pack(side=tk.LEFT, padx=80)
return_button = tk.Button(EntryPage, text=" Return ", command=lambda: show_frame(WelcomePage), font=default_font, bg="#4CAF50", fg="white")
return_button.pack(side=tk.LEFT, padx=80)



show_frame(WelcomePage)

window.mainloop()
