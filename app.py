import streamlit as st
import json

# Load the faculty data from JSON file
def load_faculty_data():
    with open('harvard_faculty.json', 'r') as f:
        return json.load(f)

def save_faculty_data(data):
    with open('harvard_faculty.json', 'w') as f:
        json.dump(data, f, indent=4)

def display_faculty_profiles(faculty_list):
    for prof in faculty_list:
        st.subheader(prof['name'])
        st.write(f"Department: {prof['department']}")
        st.write(f"Email: {prof['email']}")
        st.write(f"Profile URL: [Link]({prof['profile_url']})")

def main():
    st.title('Harvard Kennedy School Faculty Ratings')

    # Load faculty data
    faculty_list = load_faculty_data()

    # Sidebar for rating faculty
    st.sidebar.header('Rate Faculty')
    selected_professor = st.sidebar.selectbox('Select Professor', [prof['name'] for prof in faculty_list])
    
    if selected_professor:
        prof = next((prof for prof in faculty_list if prof['name'] == selected_professor), None)
        if prof:
            rating = st.sidebar.slider('Rating (1-5)', 1, 5, 3)
            if st.sidebar.button('Submit Rating'):
                prof['ratings'].append(rating)
                save_faculty_data(faculty_list)
                st.sidebar.success(f'Rating for {selected_professor} submitted successfully!')

    # Display faculty profiles
    st.header('Faculty Profiles')
    display_faculty_profiles(faculty_list)

    # Show average ratings
    st.header('Average Ratings')
    for prof in faculty_list:
        if prof['ratings']:
            average_rating = sum(prof['ratings']) / len(prof['ratings'])
            st.write(f"{prof['name']} - Average Rating: {average_rating:.1f}")
        else:
            st.write(f"{prof['name']} - No ratings yet")

if __name__ == "__main__":
    main()
