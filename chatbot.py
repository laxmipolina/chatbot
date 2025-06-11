import nltk
import re
import datetime
from queries import pairs
from nltk.chat.util import Chat, reflections

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()
    return text

def is_math_query(text):
    #regex math expression like 3+2 10/2
    return bool(re.match(r'^\s*\d+(\s*[\+\-\*/]\s*\d+)+\s*$', text))

def solve_math(text):
    try:
        #only allow safe characters
        safe_text= re.sub(r'[^0-9\+\-\*\/\.\(\) ]','', text)
        result = eval(safe_text)
        return f"The answer is {result}"
    except Exception:
        return "Sorry!! I could not slove the problem."

def get_time():
    now = datetime.datetime.now()
    return now.strftime("current date and time: %Y-%m-%d  %H:%M:%S")

def log_conversation(log, user, bot):
    with open("chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {user}\n")
        f.write(f"Bot: {bot}\n")

def main():
    print("ChatBot:Hello! What's Your Name?")
    user_name = input("you: ").strip()
    if not user_name:
        user_name="User"
    print(f"ChatBot: Hi,{user_name}! type 'bye','quit'or 'exit' to end the conversation.")

    chat = Chat(pairs, reflections)
    question_count = 0

    while True:
        user_input = input(f"{user_name}:")
        processed = preprocess(user_input)

        #math handling
        if is_math_query(processed):
            bot_response = solve_math(processed)
        #date and time handling
        elif any(word in processed for word in ['time','date','day','month','year']):
            bot_response = get_time()
        #thanks and compliments
        elif re.search(r'thank(s|you)|great|awesome|good bot|nice|well done', processed):
            bot_response="You're Welcome!☻"
        else:
            bot_response = chat.respond(processed)
            if bot_response is None:
                bot_response = "Sorry, I didn't quite get that.could you rephrase?"
        print(f"ChatBot: {bot_response}")
        log_conversation("chat_log.txt", user_input, bot_response)

        if processed in ["bye","quit","exit","goodbye"]:
           print(f"ChatBot: you asked {question_count} questions.Have a nice day, {user_name}!")
           break
        question_count += 1
if __name__ == "__main__":
    main()


























               

















            
