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

st.image("https://raw.githubusercontent.com/maxxx129/motor-skillbot/main/MotorSkillBot.jpg", caption="Welcome to MotorSkillBot 🤖")
st.title("MotorSkillBot")
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
    st.markdown("Are you A. Left handed, B. Right handed, C. Both?")
    hand_motor = st.text_input("Please type in your answer here (A/B/C):").strip().upper()

    if hand_motor == 'A':
        st.write("\n Fun Fact: 10% - 15% of the population is left handed")
        st.image("https://raw.githubusercontent.com/maxxx129/motor-skillbot/main/Left.jpeg")
    elif hand_motor == 'B':
        st.write("\n Fun Fact: 85% - 90% of the population is right handed")
        st.image("https://raw.githubusercontent.com/maxxx129/motor-skillbot/main/Right.jpeg")
    elif hand_motor == 'C':
        st.write("\n Fun Fact: 1% of the population is ambidextrous, & can use both left and right handed")
        st.image("https://raw.githubusercontent.com/maxxx129/motor-skillbot/main/Both_handed.jpeg")
    elif hand_motor:
        st.write("Please select options A, B, or C")

elif option == "About the Motor Skills Response study":
    st.subheader("📚 About the Study")
    st.markdown("""
    This study investigates motor skill response times using button release metrics.
    Participants used both hands to interact with objects A, B, C, and D.
    We're analyzing their performance through various metrics. 🧪
    """)

    motor_impairement = st.selectbox("Do you have any motor skills impairment or difficulties?", ['Yes', 'No'])
    if motor_impairement == 'Yes':
        st.write("Thank you for sharing.")
    else:
        st.write("Thank you for your input.")

    genetic_traits = st.selectbox("Do family members have similar motor skill traits?", ['Yes', 'No'])
    if genetic_traits == 'Yes':
        st.write("Genetics are strong!")
    else:
        st.write("Wow, you are unique in your family!")

    st.markdown("---")
    st.write("Next step, you will learn about the Motor Skills Response study...")
    st.write("A total of 15 participants were in this study")
    st.write("Each participant completed 40 trials using their left hand and 40 trials using their right hand.")
    st.write("That means 80 trials per participant.")
    total_trials = 15 * 80
    st.write(f"In total, the dataset includes **{total_trials} trials**.")
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
    elif stat_type == 'Average':
        st.write(f"**Left Hand**: Mean = {left.mean():.3f}")
        st.write(f"**Right Hand**: Mean = {right.mean():.3f}")
    elif stat_type == 'Standard Deviation':
        st.write(f"**Left Hand**: Std = {left.std():.3f}")
        st.write(f"**Right Hand**: Std = {right.std():.3f}")
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
        fig, ax = plt.subplots()
        sns.histplot(data=df, x=plot_metric, hue='Hand', ax=ax)
        st.pyplot(fig)
        fig2, ax2 = plt.subplots()
        sns.histplot(data=df, x=plot_metric, hue='Object', ax=ax2)
        st.pyplot(fig2)

    elif plot_type == 'Bar Plot':
        df_long = pd.melt(df, id_vars=['ppid', 'Hand', 'Object'],
                          value_vars=['Button_Release_Time', 'MT_to_obj',
                                      'MT_obj_to_tar', 'Total_MT', 'Total_Time'],
                          var_name='Metric', value_name='Value')
        subset = df_long[df_long['Metric'] == plot_metric]
        fig = sns.catplot(data=subset, x='ppid', y='Value', hue='Hand', col='Object', kind='bar')
        st.pyplot(fig)

    elif plot_type == 'Regression Plot':
        medium1 = df[df['Hand'] == 'Left'][plot_metric].reset_index(drop=True)
        medium2 = df[df['Hand'] == 'Right'][plot_metric].reset_index(drop=True)
        min_len = min(len(medium1), len(medium2))
        fig, ax = plt.subplots()
        sns.regplot(x=medium1[:min_len], y=medium2[:min_len], ax=ax)
        ax.set_xlabel("Left Hand")
        ax.set_ylabel("Right Hand")
        ax.set_title(f"Regression: {plot_metric}")
        st.pyplot(fig)

st.markdown("---")
st.markdown("Do you want to explore more?")
if st.button("Restart Analysis"):
    st.rerun()
