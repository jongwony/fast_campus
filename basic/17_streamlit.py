import pandas as pd
import streamlit as st

# display text
st.text('Fixed width text')
st.markdown('_Markdown_') # see #*
st.caption('Balloons. Hundreds of them...')
st.latex(r''' e^{i\pi} + 1 = 0 ''')
st.write('Most objects') # df, err, func, keras!
st.write(['st', 'is <', 3]) # see *
st.title('My title')
st.header('My header')
st.subheader('My sub')
st.code('for i in range(8): foo()')

# interactive widgets
st.button('Hit me')
# st.data_editor('Edit data', data)
st.checkbox('Check me out')
st.radio('Pick one:', ['nose','ear'])
st.selectbox('Select', [1,2,3])
st.multiselect('Multiselect', [1,2,3])
st.slider('Slide me', min_value=0, max_value=10)
st.select_slider('Slide to select', options=[1,'2'])
st.text_input('Enter some text')
st.number_input('Enter a number')
st.text_area('Area for textual entry')
st.date_input('Date input')
st.time_input('Time entry')
st.file_uploader('File uploader')
# st.download_button('On the dl', data)
st.camera_input("一二三,茄子!")
st.color_picker('Pick a color')

# Use widgets' returned values in variables
def foo(): st.write('foo')
def b(): st.write('b')
for i in range(int(st.number_input('Num:'))): foo()
if st.sidebar.selectbox('I:',['f']) == 'f': b()
my_slider_val = st.slider('Quinn Mallory', 1, 88)
st.write(my_slider_val)
st.slider('Pick a number', 0, 100, disabled=True)

# display media
data = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [10, 20, 30, 40]
})
st.dataframe(data)
st.table(data.iloc[0:10])
st.json({'foo':'bar','fu':'ba'})
st.metric(label="Temp", value="273 K", delta="1.2 K")

# display media
st.image('https://static.streamlit.io/examples/cat.jpg')

# mp3 audio data sample
data = b'hello'
st.audio(data)
# video data example
data = b'hello'
st.video(data)

col1, col2 = st.columns(2)
col1.write('Column 1')
col2.write('Column 2')

# Three columns with different widths
col1, col2, col3 = st.columns([3,1,1])
# col1 is wider

# Using 'with' notation:
with col1:
    st.write('This is column 1')

# Insert containers separated into tabs:
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")

# You can also use "with" notation:
with tab1:
  st.radio('Select one:', [1, 2])

# Show different content based on the user's email address.
def display_jane_content():
   st.write("Jane's content")

def display_adam_content():
    st.write("Adam's content")
    
if st.user.email == 'jane@email.com':
   display_jane_content()
elif st.user.email == 'adam@foocorp.io':
   display_adam_content()
else:
   st.write("Please contact us to get access!")

# # Stop execution immediately:
# st.stop()

# # Rerun script immediately:
# st.experimental_rerun()

# # Group multiple widgets:
# with st.form(key='my_form'):
#   username = st.text_input('Username')
#   password = st.text_input('Password')
#   st.form_submit_button('Login')