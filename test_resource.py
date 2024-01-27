from IPython.display import display, HTML, Image, clear_output
import time
import random
random.seed(1)
from ipywidgets import widgets
from jupyter_ui_poll import ui_events
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def data_consent_info():

    '''This function asks the participant for their consent on participating in the study '''
    
    info = """DATA CONSENT INFORMATION:
    
    Please read:
    we wish to record your response data
    to an anonymised public data repository.
    Your data will be used for educational teaching purposes
    practising data analysis and visualisation.
    Please type yes in the box below if you consent to the upload."""
    
    print(info)
    
    result = input("> ")
    
    if result.lower() == "yes":
    
        print("Thanks for your participation.")
        print("Please contact philip.lewis@ucl.ac.uk")
        print("If you have any questions or concerns")
        print("regarding the stored results.")

        time.sleep(3)
    
    else:

        raise(Exception("User did not consent to continue test."))


def send_to_google_form(data_dict, form_url):
    
    '''The function that sends test results to a google form'''
    
    form_id = form_url[34:90]
    view_form_url = f'https://docs.google.com/forms/d/e/{form_id}/viewform'
    post_form_url = f'https://docs.google.com/forms/d/e/{form_id}/formResponse'

    page = requests.get(view_form_url)
    content = BeautifulSoup(page.content, "html.parser").find('script', type='text/javascript')
    content = content.text[27:-1]
    result = json.loads(content)[1][1]
    form_dict = {}
    
    loaded_all = True
    for item in result:
        if item[1] not in data_dict:
            print(f"Form item {item[1]} not found. Data not uploaded.")
            loaded_all = False
            return False
        form_dict[f'entry.{item[4][0][0]}'] = data_dict[item[1]]
    
    post_result = requests.post(post_form_url, data=form_dict)
    return post_result.ok

#all photos used in the test are defined here
pic1 = Image("1_12v9_min.jpg", width = 500)
pic2 = Image("2_9v12_min.jpg", width = 500)

pic3 = Image("2_18v21_min.jpg", width = 500)
pic4 = Image("1_21v18_min.jpg", width = 500)

pic5 = Image("1_20v15_min.jpg", width = 500)
pic6 = Image("2_15v20_min.jpg", width = 500)

pic7 = Image("2_16v18_min.jpg", width = 500)
pic8 = Image("1_18v16_min.jpg", width = 500)

pic9 = Image("1_20v18_min.jpg", width = 500)
pic10 = Image("2_18v20_min.jpg", width = 500)

pic11 = Image("1_10v9_min.jpg", width = 500)
pic12 = Image("2_9v10_min.jpg", width = 500)

pic13 = Image("1_14v12_min.jpg", width = 500)
pic14 = Image("2_12v14_min.jpg", width = 500)

pic15 = Image("1_16v12_min.jpg", width = 500)
pic16 = Image("2_12v16_min.jpg", width = 500)

test_photos = ["1_12v9_min.jpg", "2_9v12_min.jpg", "2_18v21_min.jpg", "1_21v18_min.jpg", "1_20v15_min.jpg", "2_15v20_min.jpg", "2_16v18_min.jpg", "1_18v16_min.jpg", "1_20v18_min.jpg", "2_18v20_min.jpg", "1_10v9_min.jpg", "2_9v10_min.jpg", "1_14v12_min.jpg", "2_12v14_min.jpg", "1_16v12_min.jpg", "2_12v16_min.jpg"]

random.shuffle(test_photos) 

#this dictionary basically tells us which ratio category a particular photo belongs to
# a = 4:3, b = 7:6, c = 9:8, d=10:9
ratios = {
    'a': ["1_12v9_min.jpg", "2_9v12_min.jpg", "1_20v15_min.jpg", "2_15v20_min.jpg", "1_16v12_min.jpg", "2_12v16_min.jpg"],
    'b': ["2_18v21_min.jpg", "1_21v18_min.jpg", "1_14v12_min.jpg", "2_12v14_min.jpg"],
    'c': ["2_16v18_min.jpg", "1_18v16_min.jpg"],
    'd': ["1_20v18_min.jpg", "2_18v20_min.jpg", "1_10v9_min.jpg", "2_9v10_min.jpg"]  
}

def find_group(photo):
    '''This is to use later on to see which ratio category a particular photo belongs to.'''
    for group, photos in ratios.items():
        if photo in photos:
            return group


#to store all user responses to each photo that is shown
results_dict = {

'filename': [],

'response': [],

'ratio': [],
    
'correct': [],

'elapsed time': [],

'image time': []

}

def display_gradually(text, delay=0.05):
    
    '''This function prints out strings letter by letter. This makes it easier for participants 
    to understand the instructions'''
    
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
    return

def introduction(): 

    '''Here the user is introduced to what the test is about, and what they need to do'''
    
    intro_out = """This is the Approximate Number Sense (ANS) test. It tests how well you can approximate numerical 
    quantities, without the use of language!"""
    display_gradually(intro_out)
    time.sleep(1)

    intro_out_2 = """To test your ANS, we will show you a series of photos with two groups of dots on them - one will contain
    blue dots and the other one orange dots."""
    display_gradually(intro_out_2)
    time.sleep(1)

    intro_out_3 = "They will basically look like this:"
    display_gradually(intro_out_3)

    display(pic1)
    time.sleep(3)

    intro_out_4 = """Each photo will be shown to you only briefly, and you will have 3 seconds to give us your answer by 
    clicking either on a button that says blue (if you think there are more blue dots) or on a button that says 
    orange (if you think there are more orange dots). The test will last less than 8 minutes."""
    display_gradually(intro_out_4) 
    time.sleep(1)

    intro_out_5 = """Before we start, we will create a unique anonymous ID for you and just ask you a few questions so 
    that we know a little more about you!"""
    display_gradually(intro_out_5)
    time.sleep(3)


    display_gradually("""Type "ready" when you're ready to move on.""")
    state = input("> ")
    if state.lower() != "ready":
        display_gradually("""Please type "ready" when you're ready!""")
        state = input("> ")
    
    return

correct_answer_list = []

def get_ans_list():

    '''This function creates a list of correct answers for the list of test photos'''
    
    len_test = len(test_photos)
    
    for i in range (len_test):
        individual_correct_ans = test_photos[i][0]
        correct_answer_list.append(individual_correct_ans)

    return test_photos, correct_answer_list

#this creates a blue response button

custom_style_blue = """
<style>
.jupyter-widgets.widget-button_blue {
    background-color: blue;
    color: white;
}
 </style>
"""
    
display(HTML(custom_style_blue))
    
#here the button is created
button_blue = widgets.Button(description='Blue')
    
button_blue.add_class('widget-button_blue')
    
#here the button is stylised 
button_blue.style.button_color = 'blue'
button_blue.style.color = 'white'
    
#display(button_blue)



#this creates an orange response button

custom_style_orange = """
<style>
.jupyter-widgets.widget-button_orange {
    background-color: orange;
    color: white;
}
</style>
"""
    
display(HTML(custom_style_orange))
    
#here the button is created
button_orange = widgets.Button(description='Orange')
    
button_orange.add_class('widget-button_orange')
    
#here the button is stylised 
button_orange.style.button_color = 'orange'
button_orange.style.color = 'white'

#display(button_orange)


event_info = {
    'type': '',
    'description': '',
    'time': -1
}

def wait_for_event(timeout=-1, interval=0.001, max_rate=20, allow_interupt=True):   

    '''This function ensures that participant button presses are registered and that 
    they have limited time to respond'''
    
    start_wait = time.time()

    event_info['type'] = ""
    event_info['description'] = ""
    event_info['time'] = -1

    n_proc = int(max_rate*interval)+1
    
    with ui_events() as ui_poll:
        keep_looping = True
        while keep_looping==True:
            # process UI events
            ui_poll(n_proc)

            # end loop if we have waited more than the timeout period
            if (timeout != -1) and (time.time() > start_wait + timeout):
                keep_looping = False
                
            # end loop if event has occured
            if allow_interupt==True and event_info['description']!="":
                keep_looping = False
                
            # add pause before looping
            # to check events again
            time.sleep(interval)
    
    # return event description after wait ends
    # will be set to empty string '' if no event occured
    return event_info


def register_btn_event(btn):

    '''This function lets buttons register events when clicked'''
    
    event_info['type'] = "button click"
    event_info['description'] = btn.description
    event_info['time'] = time.time()
    return event_info


#to store user responses
user_responses = []

class ManualProgressBar:
    def __init__(self, total):
        '''It takes two parameters: self (which refers to the instance being created) and total (the total number 
        of units in the progress bar). In it, self.total stores the total number of units, and self.progress 
        stores the current progress (initialized to 0).'''
        self.total = total
        self.progress = 0

    def update(self, value):
        '''The function takes one value that represents the amount by which the progress should be updated.
        It increments self.progress by the specified value, and then ensures that self.progress does not 
        exceed self.total'''
        self.progress += value
        self.progress = min(self.progress, self.total)

    def display(self):
        '''It calculates the progress percentage, the length of the filled part of the progress bar, and 
        creates a visual representation of the progress bar.'''
        progress_percentage = (self.progress / self.total) * 100
        bar_length = 20
        filled_length = int(bar_length * self.progress / self.total)

        bar = f"[{'=' * filled_length}{' ' * (bar_length - filled_length)}] {progress_percentage:.1f}%"

        print("Progress:", bar)

progress_bar = ManualProgressBar(144) #the quiz has 144 questions


def initiate_arrays_of_image_display_time():
    """
    Initiates variables time_A, time_B, time_C. The test shows 16 different photos for either 0.5s, 0.75s, or 1s. 
    Throughout the test, every photo will be shown 3 times at all of those three image display times.
    This function generates 3 sequences of image display times for all 16 photos.
    """

    image_display_times = [0.5, 0.75, 1.0]
    time_A, time_B, time_C = [], [], []
    results = []
    for _ in range(16):
        display_times = image_display_times.copy()
        random.shuffle(display_times)
        time_A.append(display_times[0])
        time_B.append(display_times[1])
        time_C.append(display_times[2])

    return time_A, time_B, time_C

a, b, c = initiate_arrays_of_image_display_time()
#print("Time A:", a, len(a))
#print("Time B:", b, len(b))
#print("Time C:", c, len(c))

time_A, time_B, time_C = initiate_arrays_of_image_display_time()

def choose_winner(time_list):
    '''This function displays all possible photos in the test and asks the user to give their answers.
    This function will run 9 times in total later on. It also saves user responses to the results dictionary.'''

    get_ans_list()

    button_blue.on_click(register_btn_event)
    button_orange.on_click(register_btn_event)
    
    for i in range (len(test_photos)):
        progress_bar.display()
        pic = Image(test_photos[i], width = 500)
        display(pic)
        time.sleep(time_list[i])
        clear_output(wait = False)
        progress_bar.display()
        panel = widgets.HBox([button_blue, button_orange])

        display(panel)
        start_time = time.time()

        #to give the user 3 seconds to respond
        result = wait_for_event(timeout=3)
        end_time = time.time()
        elapsed_time = end_time - start_time

        #feedback for the user
        if result['description'] == 'Blue':
            print("Blue button was pressed")
        elif result['description'] == 'Orange':
            print("Orange button was pressed")
        elif result['description'] == '':
            print("No button was pressed! Answer more quickly")

        #storing user responses
        if result['description']=='Blue':
            user_responses.append(1)
            results_dict['response'].append("1")
            
        elif result['description']=='Orange':
            user_responses.append(2)
            results_dict['response'].append("2")
            
        elif result['description'] == '':
            user_responses.append(0)
            results_dict['response'].append("0")

        #storing all data
        results_dict['filename'].append(test_photos[i])

        ratio = find_group(test_photos[i])
        
        results_dict['ratio'].append(ratio)

        correct_ans = test_photos[i][0]
        results_dict['correct'].append(correct_ans)

        results_dict['elapsed time'].append(elapsed_time)

        results_dict['image time'].append(time_list[i])
        
        #to give people enough time to see the feedback message for the button press
        progress_bar.update(1)
        time.sleep(1)
        clear_output(wait = False)
        

    #print(correct_answer_list)
    #print(user_responses)

    return user_responses, results_dict

#to get a list of all user ids to make sure that no 2 people end up having the anonymous code
def list_of_user_ids():
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTP_c6_vpPzF9lyd_QcQjZILIUeGFH8mjLCbRTXeWfdM9_5SlmUaiO6kCvU4A0wQ1rHuza-PlakqEev/pub?output=csv")
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTP_c6_vpPzF9lyd_QcQjZILIUeGFH8mjLCbRTXeWfdM9_5SlmUaiO6kCvU4A0wQ1rHuza-PlakqEev/pub?output=csv")
    df = df.dropna()
    df = df.set_index("name")
    df = df.drop('TEST') #to remove test trials made to see if the test is working
    df = df.drop('ABAB') #to remove test trials made to see if the test is working
    
    unique_participants = df_all_results.index.unique()
    return unique_participants

def whole_ANS_test():
    '''This function runs everything needed for the complete ANS test'''
    
    data_consent_info()
    clear_output(wait = False)
    introduction()
    clear_output(wait = False)

    list_of_user_ids()
    capitalized_participants = [word.upper() for word in unique_participants]

    #to collect personal data
    id_instructions = """
    
    We would like to create you an anonymous 4-letter unique user identifier!
    To do so, could you please enter:
    
    - two letters based on the initials (first and last name) of a childhood friend
    
    - two letters based on the initials (first and last name) of a favourite actor / actress
    
    e.g. if your friend was called Charlie Brown and film star was Tom Cruise
    then your unique identifier would be CBTC
    
    """
    
    display_gradually(id_instructions)
    
    user_id = input("> ").upper()

    while user_id in capitalized_participants:
            
        user_id = input("Unfortunately this user ID is already taken:( Please enter a different one:").upper()
    
        
    while len(user_id) != 4:
        user_id = input("Invalid input! Please enter exactly 4 characters. Try again:").upper()
    
    display_gradually("Nice, thank you!:)!")

    display_gradually("We would also like to ask - how old are you? Please enter a number!")
    
    user_age = input("> ")

    #to make sure the user wrote down a number
    while not user_age.isdigit():
        display_gradually("Invalid input:( Please enter a number!")
        user_age = input("How old are you? ")

    #to make it easier to categorise genders
    gender_categories = ["m", "f", "nb", "o", "pns"]
    display_gradually("""What's your gender? Press f for female, m for male, nb for non-binary, 
    o for other and pns if you would rather not say!""")
    user_gender = input("> ")

    user_gender = user_gender.lower()
    
    if user_gender not in gender_categories:
        display_gradually("Please format your response differently!")
        user_gender = input("> ")

    user_gender = user_gender.lower()
    
    display_gradually("Great, now we know you a bit better! Now we can start the test!")

    time.sleep(3)

    clear_output(wait = False)


    display_gradually("Get ready!")
    clear_output(wait = False)
    time.sleep(1)

    display_gradually("Get set!")
    clear_output(wait = False)
    time.sleep(1)

    display_gradually("Go!")
    clear_output(wait = False)
    time.sleep(1)

    #the start of the actual ANS test
    total_start_time = time.time()

    for i in range (3):
        choose_winner(time_A)
        choose_winner(time_B)
        choose_winner(time_C)

    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time
    
    #turning data into a dataframe and then to json
    mydataframe_ANS = pd.DataFrame(results_dict)
    myjson = mydataframe_ANS.to_json()

    #showing the final score
    score = 0
    for i in range (len(user_responses)):
        if int(user_responses[i])== int(correct_answer_list[i]):
            score = score +1
    print("You scored", score, "out of 144!")

    answer_string = ''.join(correct_answer_list)
    response_string = ''.join(map(str, user_responses))
    
    data_dict = {

    'name': user_id,
    
    'age': user_age,
    
    'gender': user_gender,

    'score': score,

    'correct answer list': answer_string,

    'user responses': response_string,

    'time': total_elapsed_time,

    'json': myjson
        
    }

    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSewUYQ8u7q1iBiWtQS6lNBnKba5CjpLGqfjHoUkn1menM7TbQ/viewform?usp=sf_link'
    send_to_google_form(data_dict, form_url)
    
    return