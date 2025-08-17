from datetime import datetime  
from transformers import pipeline
import os
import torch


def main():


    while True:
        print("Chose one of these option:")
        print("Click 1 to write a new entry")
        print("Click 2 to review your entry")
        print("Click 3 to exit")

        try:
            choice = int(input("Your choice: "))
        except ValueError:
            print("You should enter an integer either 1, 2 or 3")
            continue

        if choice == 1:
            text = input("What's on your mind today? ")
            word_count = len(text.split(" ")) 
            date = datetime.now()
            day = date.strftime("%A")
            name = date.strftime("%Y-%m-%d_%H-%M-%S")
            print(f"Nice! You wrote {word_count} words today on this beautiful {day}.")

            summarizer  = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
            sentiment_analyzer = pipeline("sentiment-analysis")

            summary = summarizer(text, max_length=50, min_length=25, do_sample=False)[0]["summary_text"]
            sentiment = sentiment_analyzer(text)[0]
            print("\nAI Summary:")
            print(summary)
            print(f"Sentiment: {sentiment['label']} ({round(sentiment['score']*100, 2)}%)")
            priny

            if not os.path.exists("journal_entries"):
               os.makedirs("journal_entries")      

            with open(f"journal_entries/{name}.txt", 'w') as file:
                file.write(text) 
            print(f"Your journal was saved as {name}.txt\n")  

        elif choice == 2:
            files = os.listdir("journal_entries")
            if files:
                print("Chose the file that you want to review")
                for i ,file in enumerate(files):
                    print(f"{i + 1} {file}")

                try:
                    file_num = int(input("Enter number of the file: ")) - 1
                    if file_num in [i for i in range(len(files))]:
                        chosen_file = files[file_num]
                        with open(f"journal_entries/{chosen_file}", "r") as file:
                            print(file.read())
                    else:
                         print(f"the number should be between 1 and {len(files)}")       
                except ValueError:
                    print("It should one of the number showed in the screen")
                    continue
            else:
                print("You need to add entrys before reviewing it")
                continue                

        elif choice == 3:
            break

if __name__ == "__main__":
    main()