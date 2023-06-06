import streamlit as st
import pandas as pd
import io

# Title and Description
st.title("SCS Conversor")
st.write("Upload a CSV file and select an option to modify it:")

# Upload CSV file
uploaded = st.file_uploader("Select a file ", type="csv")

# Check if a file was uploaded
if uploaded is not None:
    # Reading user CSV file
    file_name =  uploaded.name
    file_data = io.BytesIO(uploaded.read())

    # Read CSV file and name the column
    df1 = pd.read_csv(file_data, names=['Column'], nrows = 3)
    
    # Capture the contents of the first column
    first_column = df1['Column']

    # Reset Buffer
    file_data.seek(0)
    
    # Read the CSV file
    df = pd.read_csv(file_data, skiprows=5, sep=';')

    # Variables
    old_values_RP = ['L','L\'\'','P','Q','R','R\'','R\'\'','T','V','Y']
    old_values_RP_S = ['L','L\'\'','P','Q','R','R\'','R\'\'','T','V','Y','S']
    old_values_P = ['F\'\'\'','O']

    # Options to modify the file
    options = ["Yes", "No"]
    selected_option = st.selectbox('O pneu é bordo Avolgente?', options)

    # Modify the file based on the selected option
    if selected_option == "Yes":
        df.loc[df['Name'].isin(old_values_RP_S), 'Type'] = 'RP'
    elif selected_option == "No":
       df.loc[df['Name'].isin(old_values_RP), 'Type'] = 'RP'
    
    df.loc[df['Name'].isin(old_values_P), 'Type'] = 'P'

    # New file name
    new_file_name = file_name[:-4] + "_f" + file_name[-4:]

    # Create new file
    with io.StringIO() as f:
    # Write comments to new file
        for comment in first_column:
            f.write(comment)
            f.write('\n')
        f.write('\n\n')   

        # Write the dataframe to the new file
        df.to_csv(f, index=False, sep=';')

        # Get the file content as a string
        f.seek(0)
        csv_content = f.read()

    # Option to download the modified CSV file 
    st.markdown("### Download the modified CSV file")
    st.download_button("Click here to download", data=csv_content, file_name=new_file_name)
else:
    st.warning('Please, upload a file!')

