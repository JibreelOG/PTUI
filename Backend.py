# Here we create the dashboard from the user, and we store and pull info from a text file so we dont lose it

# pip install streamlit
# pip install matplotlib
# pip install streamlit-option-menu
# pip install openai streamlit

import streamlit as st
from matplotlib import pyplot as plt # For plotting graphs
from datetime import datetime, timedelta
import time
from streamlit_option_menu import option_menu
import openai

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Pull all information from trainer submitted form, image the string is info from google form
Name = 'Mohammad'
Monday = 'Rest'
MondayWorkout = ''
starting_weight = 85

##with open('OpenAPI.txt', "a") as file:
    ##OPENAI_API_KEY = file.readable()

OPENAI_API_KEY = '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'

st.markdown("<h1 style='text-align: center; color: white;'>Progress Logged By PT Reagan</h1>", unsafe_allow_html=True)
st.markdown('---')

# Initialize navigation menu
selected = option_menu(
    menu_title=None,
    options=['Weight Graph', 'Book a Session', 'Workouts'],
    icons=['graph-up', 'calendar2-plus', 'list-check'],
    default_index=0,
    orientation='horizontal',
)

st.markdown('---')

if selected == 'Weight Graph':
    st.markdown("<h1 style='text-align: center; color: white;'>Mohammads Weight Tracker</h1>", unsafe_allow_html=True)

    # Assign info in text files to x and y values
    with open('weighins.txt', "r") as file:
        weight_content = file.readlines()
    recoreded_weight = [wei.strip() for wei in weight_content]  # Remove newline characters from each line and converts to a list (Converts text file into readable list for python)
    y_value = recoreded_weight

    with open('dateofweighins.txt', "r") as file:
        date_content = file.readlines()
    recoreded_date = [dat.strip() for dat in date_content]  # Remove newline characters from each line and converts to a list (Converts text file into readable list for python)
    x_value = recoreded_date

    # Plot initial graph from info in text files
    fig=plt.figure()
    # Set an astetich style for the graph
    plt.style.use('https://raw.githubusercontent.com/dhaitz/matplotlib-stylesheets/master/pitayasmoothie-dark.mplstyle')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=90, fontsize=6)
    plt.yticks(fontsize=6)

    # Now create a plot on that figure

    plt.plot(x_value,y_value)
    # Use st.write to display the graph

    # Make the x and y ticks readable when in large amounts
    # First determine the positions for y ticks by deterimning how many we have
    All_Different_Weights = list(set(recoreded_weight))
    Ytick_len = len(All_Different_Weights)
    ##st.write(Ytick_len)
    All_Different_Dates = list(set(recoreded_date))
    Xtick_len = len(All_Different_Dates)

    Last_Date_Recorded = recoreded_date[-1]
    Starting_Date = recoreded_date[0]
    Starting_Date_DateTime = datetime.strptime(Starting_Date, "%Y-%m-%d").date()
    Last_Recorded_Weight = recoreded_weight[-1]
    Last_Recorded_Weight_Float = float(Last_Recorded_Weight)
    Last_Date_Recorded_DateTime = datetime.strptime(Last_Date_Recorded, "%Y-%m-%d").date()

    # All y tick labels that arent fully divisible by 0.5 need their font size to be 0


    ax = plt.gca()
    ytick_labels = ax.get_yticklabels()
    ytick_positions = ax.get_yticks()

    xtick_labels = ax.get_xticklabels()
    xtick_positions = ax.get_xticks()

    # Define the font size for values with decimals between 0.1 and 0.4
    decimal_font_size = 4
    decimal_label_colour = '#84bdf0'
    milestone_font_size = 4
    milestone_label_colour = '#34e7f7'
    invisible_colour = '#212946'

    # Set the font size for tick labels with decimals between 0.1 and 0.4
    for label in ytick_labels:
        # Extract the numeric value from the label
        value = float(label.get_text())
        if value % 1 != 0:
            label.set_fontsize(decimal_font_size)
            label.set_color(decimal_label_colour)
        elif value % 1 ==0:
            label.set_color(milestone_label_colour)

    if Ytick_len > 60:
        for label in ytick_labels:
            value = float(label.get_text())
            if value % 1 != 0:
                label.set_fontsize(decimal_font_size)
                label.set_color(invisible_colour)

    # Set the font size for tick labels with date
    for xlabel in xtick_labels:
        xlabelstr = str(xlabel)
        # Find the index of the first single quote
        start_index = xlabelstr.find("'")
        # Find the index of the last single quote
        end_index = xlabelstr.rfind("'")
        # Extract the date substring
        xlabel_date = xlabelstr[start_index + 1:end_index]

        xlabel_DateTime = datetime.strptime(xlabel_date, '%Y-%m-%d').date()
        date = Starting_Date_DateTime - xlabel_DateTime
        num_days = date.days
        xlabel.set_color(decimal_label_colour)
        if num_days % 10 != 0:
            xlabel.set_fontsize(milestone_font_size)
            xlabel.set_color(milestone_label_colour)
    if Xtick_len > 90:
        for xlabel in xtick_labels:
            xlabelstr = str(xlabel)
            # Find the index of the first single quote
            start_index = xlabelstr.find("'")
            # Find the index of the last single quote
            end_index = xlabelstr.rfind("'")
            # Extract the date substring
            xlabel_date = xlabelstr[start_index + 1:end_index]
            xlabel_DateTime = datetime.strptime(xlabel_date, '%Y-%m-%d').date()
            date = Starting_Date_DateTime - xlabel_DateTime
            num_days = date.days
            if num_days % 10 != 0:
                xlabel.set_color(invisible_colour)

    st.write(fig)

    st.markdown('---')

    # Progress report
    st.markdown("<h1 style='text-align: center; color: white;'>Your current weight is</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: green;'>{Last_Recorded_Weight_Float}kg</h1>", unsafe_allow_html=True)
    Weight_Lost = 83 - float(Last_Recorded_Weight)
    if Weight_Lost > 0:
        st.markdown("<h1 style='text-align: center; color: white;'>So far you have lost</h1>",unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: green;'>{round(Weight_Lost,2)}kg</h1>", unsafe_allow_html=True)
    elif Weight_Lost < 0:
        st.markdown("<h1 style='text-align: center; color: white;'>So far you have gained</h1>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: red;'>{abs(round(Weight_Lost, 2))}kg</h1>",unsafe_allow_html=True)

    st.markdown('---')

    # Aquire new weight by date info and append it to the list
    New_Weight = st.text_input("Enter a new weight")
    if New_Weight:
        New_Weight_Float = float(New_Weight)
        New_Weight = round(New_Weight_Float, 1)
    if New_Weight:
        if float(New_Weight) > 85:
            New_Weight = '85'
    New_Date = st.date_input("Enter date of weigh in") # Already in datetime
    if New_Date:
        if New_Date < Last_Date_Recorded_DateTime:
            New_Date = None
            st.write('Sorry you cant log past weights without undoing previous entries')
            st.write('Click the [Undo Weight Entry] Button below')
    Log_Weight = st.button('Log Weight on graph')
    Undo_Button = st.button('Undo weight entry')

    # If undo button pressed delete the last entry from each list
    if Undo_Button:
        with open('weighins.txt', 'r') as file: # Read the file then rewrite it without the last entry
            lines = file.readlines()

        with open('weighins.txt', 'w') as file:
            file.writelines(lines[:-1])

        with open('dateofweighins.txt', 'r') as file:
            lines = file.readlines()

        with open('dateofweighins.txt', 'w') as file:
            file.writelines(lines[:-1])

        st.rerun()

    # When the user wants to log their weight
    if New_Weight and New_Date and Log_Weight:
        Input_Day_Difference = New_Date - Last_Date_Recorded_DateTime # The difference between the dates
        Days = 1
        Days_DateTime = timedelta(days=Days)

        New_Weight_Float = float(New_Weight)
        Last_Recorded_Weight_Float = float(Last_Recorded_Weight)
        Input_Weight_Difference = Last_Recorded_Weight_Float - New_Weight_Float
        Weight_Difference_Rounded = round(Input_Weight_Difference, 1)
        ##st.write(Weight_Difference_Rounded, 'Is the weight difference')
        Decimal = float(0.1)

        ##st.write(Input_Day_Difference, ' Is the day difference')

        # If neither the weight nor the date were logged linearly (Most common)
        if (Weight_Difference_Rounded > Decimal) and Input_Day_Difference > Days_DateTime:
            ##st.write('Neither weight nor date was logged linearly')
            # figure out which input has the biggest discrepency
            Weight_Discrepency = Weight_Difference_Rounded * 10
            Weight_Discrepency = int(Weight_Discrepency)
            Date_Discrepency = Input_Day_Difference.days

            ##st.write(Date_Discrepency, 'Is the date discrepency')
            ##st.write(Weight_Discrepency, 'Is the weight discrepency')

            if Weight_Discrepency > Date_Discrepency: # If the discrepency in weight is higher we need to append extra to date text file
                ##st.write('The bigger discrepency is in weight')
                Discrepency_Difference = Weight_Discrepency - Date_Discrepency

                # Add filler for weights
                Repetitions = Weight_Difference_Rounded * 10
                Repetitions_Int = int(Repetitions)
                # Log the missed weights
                for r in range(0, Repetitions_Int, 1):
                    Last_Recorded_Weight_Float -= 0.1
                    Addition = round(Last_Recorded_Weight_Float, 1)
                    with open('weighins.txt', 'a') as f:
                        f.write(f'{Addition}\n')
                    ##st.write('Filler weight logged')

                # Add filler for dates
                # Here detect the dates between that were missed in the input
                end_date = Last_Date_Recorded_DateTime + Input_Day_Difference
                st.write(end_date)
                dates_between = [Last_Date_Recorded_DateTime + timedelta(days=i) for i in range((Input_Day_Difference).days)]
                dates_between_final = dates_between[1:]  # Now we've isolated the non-plotted dates in a list
                # Convert datetime objects to strings
                dates_between_final_string = [date_obj.strftime('%Y-%m-%d') for date_obj in dates_between_final]
                # Write the non plotted dates in the dates file
                with open('dateofweighins.txt', 'a') as file:
                    for date in dates_between_final_string:
                        file.write(f'{date}\n')

                with open('dateofweighins.txt', "r") as file:
                    date_content = file.readlines()
                recoreded_date_2 = [dat.strip() for dat in date_content]
                Last_Date_Recorded_2 = recoreded_date_2[-1]

                Discrepency_Difference += 1

                for i in range(0,Discrepency_Difference,1): # Append extra to date file to ensure graph is formatted correctly
                    with open('dateofweighins.txt', 'a') as file:
                        file.write(f'{Last_Date_Recorded_2}\n')
                    ##st.write('Discrepency filled')

            elif Weight_Discrepency < Date_Discrepency: # If the discrepency in date is higher we need to append extra to weight text file
                ##st.write('The bigger discrepency is in date')
                Discrepency_Difference = Date_Discrepency - Weight_Discrepency
                # Add filler for weights
                Repetitions = Weight_Difference_Rounded * 10
                Repetitions_Int = int(Repetitions)
                # Log the missed weights
                for r in range(0, Repetitions_Int, 1):
                    Last_Recorded_Weight_Float -= 0.1
                    Addition = round(Last_Recorded_Weight_Float, 1)
                    with open('weighins.txt', 'a') as f:
                        f.write(f'{Addition}\n')
                    ##st.write('Filler weight logged')

                # Add filler for dates
                # Here detect the dates between that were missed in the input
                end_date = Last_Date_Recorded_DateTime + Input_Day_Difference
                st.write(end_date)
                dates_between = [Last_Date_Recorded_DateTime + timedelta(days=i) for i in
                                 range((Input_Day_Difference).days)]
                dates_between_final = dates_between[1:]  # Now we've isolated the non-plotted dates in a list
                # Convert datetime objects to strings
                dates_between_final_string = [date_obj.strftime('%Y-%m-%d') for date_obj in dates_between_final]
                # Write the non plotted dates in the dates file
                with open('dateofweighins.txt', 'a') as file:
                    for date in dates_between_final_string:
                        file.write(f'{date}\n')

                for i in range(1, Discrepency_Difference,1):  # Append extra to date file to ensure graph is formatted correctly
                    with open('weighins.txt', 'a') as file:
                        file.write(f'{Last_Recorded_Weight_Float}\n')

        # If Date wasn't logged linearly but weight was
        elif Input_Day_Difference > Days_DateTime: # In case date input doesn't align with graph, fill in empty date slots
            # Here detect the dates between that were missed in the input
            end_date = Last_Date_Recorded_DateTime + Input_Day_Difference
            ##st.write(end_date)
            dates_between = [Last_Date_Recorded_DateTime + timedelta(days=i) for i in range((Input_Day_Difference).days)]
            dates_between_final = dates_between[1:] # Now we've isolated the non-plotted dates in a list
            # Convert datetime objects to strings
            dates_between_final_string = [date_obj.strftime('%Y-%m-%d') for date_obj in dates_between_final]
            # Write the non plotted dates in the dates file
            with open('dateofweighins.txt', 'a') as file:
                for date in dates_between_final_string:
                    file.write(f'{date}\n')

            len = len(dates_between_final_string)
            for i in range (0,len,1):
                with open('weighins.txt', 'a') as file:
                    file.write(f'{New_Weight}\n')

            ##st.write(dates_between_final,)
            # Write them in the dates text file
            # And Put a null point for the weights
            ##st.write('Do some correcting')


            with open('weighins.txt', 'a') as f:
                f.write(f'{New_Weight}\n')
            with open('dateofweighins.txt', 'a') as f:
                f.write(f'{New_Date}\n')
            st.write('Weight logged on system')


        # If weight wasnt logged linearly but date was (Writes weight correctly)
        elif Weight_Difference_Rounded > Decimal:
            Repetitions = Weight_Difference_Rounded * 10
            Repetitions_Int = int(Repetitions)
            # Log the missed weights
            for r in range (0,Repetitions_Int,1):
                Last_Recorded_Weight_Float -= 0.1
                Addition = round(Last_Recorded_Weight_Float, 1)
                with open('weighins.txt', 'a') as f:
                    f.write(f'{Addition}\n')
                st.write('Filler weight logged')
                # Add filler dates so graph renders correctly
                with open('dateofweighins.txt', 'a') as f:
                    f.write(f'{Last_Date_Recorded}\n')


        # If both the date and the weight were logged linearly (Writes the data correctly)
        with open('weighins.txt', 'a') as f:
            f.write(f'{New_Weight}\n')
        with open('dateofweighins.txt', 'a') as f:
            f.write(f'{New_Date}\n')
        st.write('Weight logged on system')

        time.sleep(1)
        st.rerun()

if selected == 'Workouts': # Right now is demo but pull info from google form for workout

    st.markdown("""
            <style>
            .st-emotion-cache-1ir3vnm eeusbqq3
            {
                visibility: hidden;
            }
            </style>
            """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: white;'>Today Is Chest day</h1>", unsafe_allow_html=True)
    st.markdown('---')
    st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>Bench Press</h1>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 12px;'>3 Sets 10 Reps</h1>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>Dumbbell Press</h1>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 12px;'>3 Sets 10 Reps</h1>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>Chest Press Machine</h1>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 12px;'>3 Sets 10 Reps</h1>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 24px;'>Pushups</h1>",unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 12px;'>3 Sets 10 Reps</h1>",unsafe_allow_html=True)

    st.markdown('---')

    st.markdown("<h1 style='text-align: center; color: white;'>Ask our trained AI any fitness question</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 12px;'>It has your weight goal and circumstances in mind when calculating a response</h1>",
        unsafe_allow_html=True)

    openai.api_key = 'sk-my-service-key-VAld8xdbIjToAgWc2n6ET3BlbkFJ2ngBmj1F9P6fytFFiisY'
    pre_existing_info = 'Imagine your a personal trainer coaching me i am 83kg and my goal is to build muscle and lose fat, when answering me make sure to include my weight and goal in your response, also aim to keep the response short but dense with usefull info, also display what you wrote in english in arabic aswell below, remember to mention my weight and goal!'

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How many reps should I do for bench press?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        ##with st.chat_message("user"):
            ##st.markdown(prompt)

        # Add the pre-existing information as context for the GPT model
        st.session_state.messages.append({"role": "assistant", "content": pre_existing_info})

        # Handle the AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if selected == 'Book a Session':

    default_index = 2

    Session_Date = st.date_input('What day would you like to book?')
    Session_Time = st.time_input('What time would you like to book?')
    Book_Button = st.button('Confirm Session Booking')
    st.text('(Keep in mind the gyms hours)')
    if Session_Date and Session_Time and Book_Button:
        st.write('Training session booked!')
        st.write('Trainer Reagan has been alerted')
    # Send this info to their whatsapp or google calendar


# isuue 1
     # X and Y sticks overlap when theirs to many,
     # Either decrease font size of sticks as the number of them increases
     # or find a way to make only a certain amount visible

     # Then finished send demo and start working on somehting else

# Issue 2
    # When weight is submitted below the starting weight it just records it as
    # the starting weight
    # Soution is to detect when weight is below the starting and add filler



