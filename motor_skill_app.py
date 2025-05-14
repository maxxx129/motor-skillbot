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

    medium_type = st.selectbox("Choose a medium:", [
        'Right Hand', 'Left Hand', 'Object A', 'Object B', 'Object C', 'Object D'])

    if medium_type == 'Right Hand':
        medium = df[df['Hand'] == 'Right'][plot_metric]
        color = 'red'
    elif medium_type == 'Left Hand':
        medium = df[df['Hand'] == 'Left'][plot_metric]
        color = 'green'
    elif medium_type == 'Object A':
        medium = df[df['Object'] == 'A'][plot_metric]
        color = 'blue'
    elif medium_type == 'Object B':
        medium = df[df['Object'] == 'B'][plot_metric]
        color = 'purple'
    elif medium_type == 'Object C':
        medium = df[df['Object'] == 'C'][plot_metric]
        color = 'orange'
    elif medium_type == 'Object D':
        medium = df[df['Object'] == 'D'][plot_metric]
        color = 'yellow'

    if plot_type == 'Histogram':
        fig, ax = plt.subplots()
        sns.histplot(medium, color=color, ax=ax)
        ax.set_title(f"Histogram for {plot_metric} ({medium_type})")
        st.pyplot(fig)

    elif plot_type == 'Bar Plot':
        df_long = pd.melt(df, id_vars=['ppid', 'Hand', 'Object'],
                          value_vars=['Button_Release_Time', 'MT_to_obj',
                                      'MT_obj_to_tar', 'Total_MT', 'Total_Time'],
                          var_name='Metric', value_name='Value')
        subset = df_long[(df_long['Metric'] == plot_metric) & (df_long['Object'] == medium_type[-1] if 'Object' in medium_type else df_long['Hand'] == medium_type.split()[0])]
        fig = sns.catplot(data=subset, x='ppid', y='Value', hue='Hand', col='Object', kind='bar')
        st.pyplot(fig)

    elif plot_type == 'Regression Plot':
        secondary_type = st.selectbox("Compare with:", [
            'Right Hand', 'Left Hand', 'Object A', 'Object B', 'Object C', 'Object D'])

        def get_data(label):
            if label == 'Right Hand':
                return df[df['Hand'] == 'Right'][plot_metric].reset_index(drop=True)
            elif label == 'Left Hand':
                return df[df['Hand'] == 'Left'][plot_metric].reset_index(drop=True)
            elif label.startswith('Object'):
                obj = label[-1]
                return df[df['Object'] == obj][plot_metric].reset_index(drop=True)

        y_data = get_data(medium_type)
        x_data = get_data(secondary_type)
        min_len = min(len(x_data), len(y_data))
        fig, ax = plt.subplots()
        sns.regplot(x=x_data[:min_len], y=y_data[:min_len], color=color, ax=ax)
        ax.set_xlabel(secondary_type)
        ax.set_ylabel(medium_type)
        ax.set_title(f"Regression Plot: {plot_metric}")
        st.pyplot(fig)

st.markdown("---")
st.markdown("Do you want to explore more?")
if st.button("Restart Analysis"):
    st.rerun()
