import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load data
url = 'https://raw.githubusercontent.com/VikramArunkumarSJSU/MotorSkillResponseTimeData/refs/heads/main/Controlled_EDK_Dataset2.csv'
df = pd.read_csv(url)
df.rename(columns={'RT': 'Button_Release_Time'}, inplace=True)
df['Total_Time'] = df['Button_Release_Time'] + df['Total_MT']

st.title("🤾‍♀️ Welcome to MotorSkillBot!")
st.markdown("Let's analyze some motor skills response time data! 💪🧠")

# Main menu
option = st.sidebar.selectbox("Pick an option:", [
    "Left Hand or Right Hand?",
    "About the Motor Skills Response study",
    "Which statistic would you like to see?",
    "Which plot would you like to see?"
])

if option == "Left Hand or Right Hand?":
    st.subheader("🖐️ Left vs Right")
    hand = st.selectbox('Are you', ['Left Handed', 'Right Handed', 'Both'])
    st.write("Are you A.Left handed, B.Right handed, C.Both?")
    hand_motor = input("Please type in your answer here: ")
    if hand_motor == 'A':
        st.write("Fun Fact: 10% - 15% of the population is left handed")

    elif hand_motor == 'B':
        st.write("Fun Fact: 85% - 90% of the population is right handed")
            

    elif hand_motor == 'C':
        st.write("Fun Fact: 1% of the population is ambidextrous, "
            "& can use both, left and right handed")
            
    else:
        st.write("Please select options A,B, or C")
    #st.info("🚧 This feature is under construction! But it's coming soon.")

elif option == "About the Motor Skills Response study":
    st.subheader("📚 About the Study")
    st.markdown("""
    This study investigates motor skill response times using button release metrics.
    Participants used both hands to interact with objects A, B, C, and D.
    We're analyzing their performance through various metrics. 🧪
    """)
    motor_impairement = st.selectbox("Would you have any motor skills"
                                        " impairment/difficulties?", ['Yes', 'No'])
    if motor_impairement.lower() == 'yes':
        st.write("Thank you for sharing.")
    else:
        st.write("Thank you for your input.")

    genetic_traits = st.selectbox("Do family members have similar "
                                 "motor skill traits? ", ['Yes', 'No'])
    if genetic_traits.lower() == 'yes':
        st.write("Genetics are strong!")
    else:
        st.write("Wow, you are unique in your family!")
        st.write("Next step, you will learn about the "
        "Motor Skills Response study...")
        
        st.write("A total of 15 participants were in this study")
        
        st.write("For each participant, 40 trials were completed using "
        "their left hand and 40 trial using their right hand.")
        
        st.write("A total of 80 trials were given to each participant.")
        
        all_trials = 15 * 80
        st.write(f"In total, the dataset indicates {all_trials} trials.")
    st.success("Thanks for being curious! 🤓")

elif option == "Which statistic would you like to see?":
    st.subheader("📊 Statistical Analysis")

    metric = st.selectbox("Choose a metric:", [
        'Button_Release_Time', 'MT_to_obj', 'MT_obj_to_tar', 'Total_MT'
    ])

    stat_type = st.selectbox("Choose a statistic type:", [
        'Max/Min', 'Average', 'Standard Deviation', 'T-test between LH and RH'
    ])

    left = df[df['Hand'] == 'Left'][metric]
    right = df[df['Hand'] == 'Right'][metric]

    if stat_type == 'Max/Min':
        st.write(f"**Left Hand**: Max = {left.max():.3f}, Min = {left.min():.3f}")
        st.write(f"**Right Hand**: Max = {right.max():.3f}, Min = {right.min():.3f}")
        st.info("Extremes can be interesting! 🧐")

    elif stat_type == 'Average':
        st.write(f"**Left Hand**: Mean = {left.mean():.3f}")
        st.write(f"**Right Hand**: Mean = {right.mean():.3f}")
        st.success("Got the averages for you! ✅")

    elif stat_type == 'Standard Deviation':
        st.write(f"**Left Hand**: Std = {left.std():.3f}")
        st.write(f"**Right Hand**: Std = {right.std():.3f}")
        st.warning("The spread tells us how consistent responses were.")

    elif stat_type == 'T-test between LH and RH':
        t_stat, p_val = ttest_ind(left, right)
        st.write(f"**T-test Result**: t = {t_stat:.3f}, p = {p_val:.5f}")
        if p_val < 0.05:
            st.success("🎯 Statistically significant difference!")
        else:
            st.info("😐 No statistically significant difference.")

elif option == "Which plot would you like to see?":
    st.subheader("📈 Visualization Options")
    plot_metric = st.selectbox("Choose a metric to plot:", [
        'Button_Release_Time', 'MT_to_obj', 'MT_obj_to_tar', 'Total_MT', 'Total_Time'
    ])

    plot_type = st.selectbox("Choose a plot type:", [
        'Histogram', 'Bar Plot', 'Regression Plot'
    ])
    

    if plot_type == 'Histogram':
        medium_type = st.selectbox("Choose a medium:", [
        'Right Hand', 'Left Hand', 'Object A', 'Object B', 'Object C', 'Object D'
    ])
        if medium_type == 'Right Hand':
            medium = df.loc[df['Hand'] == 'Right', [plot_metric]]
            color = 'red'
        elif medium_type == 'Left Hand':
            medium = df.loc[df['Hand'] == 'Left', [plot_metric]]
            color = 'green'
        elif medium_type == 'Object A':
            medium = df.loc[df['Object'] == 'A', [plot_metric]]
            color = 'blue'
        elif medium_type == 'Object B':
            medium = df.loc[df['Object'] == 'B', [plot_metric]]
            color = 'purple'
        elif medium_type == 'Object C':
            medium = df.loc[df['Object'] == 'C', [plot_metric]]
            color = 'orange'
        elif medium_type == 'Object D':
            medium = df.loc[df['Object'] == 'D', [plot_metric]]
            color = 'yellow'
        st.write(f"Histogram for {plot_metric} for Hand")
        fig, ax = plt.subplots()
        sns.histplot(data = df, x=plot_metric, hue='Hand', ax=ax)
        st.pyplot(fig)
        st.write(f"Histogram for {plot_metric} for Object")
        fig1, ax1 = plt.subplots()
        sns.histplot(data = df, x=plot_metric, hue='Object', ax=ax1)
        st.pyplot(fig1)
        st.write(f"Histogram for {plot_metric} for {medium_type}")
        fig2, ax2 = plt.subplots()
        sns.histplot(data = medium, x=plot_metric, color = color, ax=ax2)
        st.pyplot(fig2)
        st.info("📊 That’s one colorful distribution!")

    elif plot_type == 'Bar Plot':
        df_long = pd.melt(df, id_vars=['ppid', 'Hand', 'Object'],
                          value_vars=['Button_Release_Time', 'MT_to_obj',
                                      'MT_obj_to_tar', 'Total_MT', 'Total_Time'],
                          var_name='Metric', value_name='Value')
        subset = df_long[df_long['Metric'] == plot_metric]
        st.write("Comparing participants by hand and object")
        #fig = sns.barplot(data = subset, x = 'ppid', y = 'Value', hue = 'Hand')
        fig = sns.catplot(data=subset, x='ppid', y='Value', hue='Hand', col='Object', kind='bar')
        st.pyplot(fig)
        st.success("Nice! Bar plots are great for comparison.")

    elif plot_type == 'Regression Plot':
        #lh = df[df['Hand'] == 'Left'][plot_metric].reset_index(drop=True)
        #rh = df[df['Hand'] == 'Right'][plot_metric].reset_index(drop=True)
        medium_type = st.selectbox("Choose a medium:", [
        'Right Hand', 'Left Hand', 'Object A', 'Object B', 'Object C', 'Object D'
    ])
        if medium_type == 'Right Hand':
            medium = df.loc[df['Hand'] == 'Right', [plot_metric]]
            color = 'red'
        elif medium_type == 'Left Hand':
            medium = df.loc[df['Hand'] == 'Left', [plot_metric]]
            color = 'green'
        elif medium_type == 'Object A':
            medium = df.loc[df['Object'] == 'A', [plot_metric]]
            color = 'blue'
        elif medium_type == 'Object B':
            medium = df.loc[df['Object'] == 'B', [plot_metric]]
            color = 'purple'
        elif medium_type == 'Object C':
            medium = df.loc[df['Object'] == 'C', [plot_metric]]
            color = 'orange'
        elif medium_type == 'Object D':
            medium = df.loc[df['Object'] == 'D', [plot_metric]]
            color = 'yellow'
        medium_plot1 = st.selectbox("Choose another medium:", [
        'Right Hand', 'Left Hand', 'Object A', 'Object B', 'Object C', 'Object D'
        ])
        
        if medium_type == medium_plot1:
            st.write('Please choose another medium')

        if medium_plot1 == 'Right Hand':
            medium1 = df.loc[df['Hand'] == 'Right', [plot_metric]]
        elif medium_plot1 == 'Left Hand':
            medium1 = df.loc[df['Hand'] == 'Left', [plot_metric]]
        elif medium_plot1 == 'Object A':
            medium1 = df.loc[df['Object'] == 'A', [plot_metric]]
        elif medium_plot1 == 'Object B':
            medium1 = df.loc[df['Object'] == 'B', [plot_metric]]
        elif medium_plot1 == 'Object C':
            medium1 = df.loc[df['Object'] == 'C', [plot_metric]]
        elif medium_plot1 == 'Object D':
            medium1 = df.loc[df['Object'] == 'D', [plot_metric]]

        min_len = min(len(medium), len(medium1))
        fig, ax = plt.subplots()
        sns.regplot(x=medium[:min_len], y=medium1[:min_len], color = color, ax=ax)
        ax.set_xlabel(medium_type)
        ax.set_ylabel(medium_plot1)
        ax.set_title(f"Regression: {plot_metric}")
        st.pyplot(fig)
        st.info("🧠 Are we seeing any patterns here?")

st.markdown("---")
st.markdown("Do you want to explore more?")
if st.button("Restart Analysis"):
    st.rerun()
