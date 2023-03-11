import yaml
import streamlit as st
import st_pages as stp
import streamlit_authenticator as stauth

stp.show_pages(
    [
        stp.Page("app.py", "Main Page", "🏠"),
        stp.Page("pages/page_1.py", "Upload & Visualize", "📄"),
        stp.Page("pages/page_2.py", "Select & Analyze", "🏆"),
        stp.Page("pages/page_3.py", "Register", "🔒"),
        stp.Page("pages/page_4.py", "About", "💡")
    ]
)
st.sidebar.image("assets/Voliboli.jpg", use_column_width=True)

with open('auth.yaml') as file:
    config = yaml.load(file, Loader=yaml.loader.SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
authenticator._check_cookie() # NOTE: bug in the imported library (need to call it manually)

st.title("Register 🔒")
st.write("Welcome to our registration page!")

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.success("You have already successfuly registered 🙌")
elif st.session_state["authentication_status"] is False:
    name, authentication_status, username = authenticator.login('Login', 'sidebar')
    st.write("By creating an account, you will gain access to all the features of our platform, and more.")
    st.write("To get started, simply fill out the form with your information. \
          Please ensure that all the information provided is accurate and up-to-date. \
          Once you have completed the form, select the **`Register`** button to create your account.")
    st.sidebar.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    name, authentication_status, username = authenticator.login('Login', 'sidebar')
    st.write("By creating an account, you will gain access to all the features of our platform, and more.")
    st.write("To get started, simply fill out the form with your information. \
          Please ensure that all the information provided is accurate and up-to-date. \
          Once you have completed the form, select the **`Register`** button to create your account.")
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully 🙌')

            # Add used to .yaml authentication file
            with open('auth.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

            # TODO: Redirect to main page - not yet implemented by streamlit dev team
            st.header("Congratulations! 🎉")
            st.write("You have successfully registered with Voliboli organization. \
                    We are thrilled to have you as a part of our community. \
                    You can now login to your account and start exploring our exciting features for FREE. \
                    Thank you for choosing Voliboli, and we look forward to providing you with a delightful experience!")
    except Exception as e:
        st.error(e)
    st.write("By registering with us, you agree to our terms and conditions and privacy policy. \
          We take your privacy seriously and will never share your personal information with third parties without your consent. \
          Thank you for choosing our platform, and we look forward to providing you with a seamless and enjoyable experience!")