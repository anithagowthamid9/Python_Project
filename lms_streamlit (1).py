import streamlit as st

# Initial data
def get_library():
    return {
        "python_basics": {"Author": "author1", "Availability": "available", "Issued_to": "none"},
        "python_functions": {"Author": "author2", "Availability": "available", "Issued_to": "none"},
        "python_loops": {"Author": "author3", "Availability": "available", "Issued_to": "none"}
    }

def main():
    st.title("📚 Library Management System (LMS)")
    st.write("A simple Library Management System with Streamlit UI.")

    # Session state for library and login
    if 'library2' not in st.session_state:
        st.session_state.library2 = get_library()
    if 'login_success' not in st.session_state:
        st.session_state.login_success = False
    if 'username' not in st.session_state:
        st.session_state.username = ''

    credentials = {"admin": "admin123", "librarian": "lib123"}

    # Login UI
    if not st.session_state.login_success:
        st.subheader("Login")
        login_form = st.form("login_form")
        with login_form:
            username = st.text_input("Username", value=st.session_state.get('username', ''), key="login_username").lower()
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if username in credentials and credentials[username] == password:
                    st.session_state.login_success = True
                    st.session_state.username = username
                    st.success("Successfully logged in!")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
        st.stop()

    # Main menu
    menu = [
        "View Books",
        "Add a Book",
        "Issue a Book",
        "Return a Book",
        "View Issued Books",
        "Logout"
    ]
    choice = st.sidebar.selectbox("Select an option", menu)

    library2 = st.session_state.library2

    if choice == "View Books":
        st.subheader("Library Books")
        for title, info in library2.items():
            if info["Availability"] == "available":
                st.write(f"**{title.title()}** | Author: {info['Author'].title()} | Status: Available")
            else:
                st.write(f"**{title.title()}** | Author: {info['Author'].title()} | Status: Issued to {info['Issued_to'].title()}")

    elif choice == "Add a Book":
        st.subheader("Add a Book")
        with st.form("add_book_form"):
            title = st.text_input("Book Name").lower().strip()
            author = st.text_input("Author").lower().strip()
            submitted = st.form_submit_button("Add Book")
            if submitted:
                if title in library2 and library2[title]["Author"] == author:
                    st.warning("The book already exists.")
                else:
                    library2[title] = {"Author": author, "Availability": "available", "Issued_to": "none"}
                    st.success("Book added successfully!")

    elif choice == "Issue a Book":
        st.subheader("Issue a Book")
        available_books = [k for k, v in library2.items() if v["Availability"] == "available"]
        if available_books:
            book_to_issue = st.selectbox("Select a book to issue", available_books)
            issuer_name = st.text_input("Name of person issuing the book").lower().strip()
            if st.button("Issue Book"):
                if book_to_issue and issuer_name:
                    library2[book_to_issue]["Availability"] = "unavailable"
                    library2[book_to_issue]["Issued_to"] = issuer_name
                    st.success(f"{book_to_issue.title()} issued to {issuer_name.title()}.")
        else:
            st.info("No books available to issue.")

    elif choice == "Return a Book":
        st.subheader("Return a Book")
        issued_books = [k for k, v in library2.items() if v["Availability"] == "unavailable"]
        if issued_books:
            book_to_return = st.selectbox("Select a book to return", issued_books)
            if st.button("Return Book"):
                prev_issuer = library2[book_to_return]["Issued_to"]
                library2[book_to_return]["Availability"] = "available"
                library2[book_to_return]["Issued_to"] = "none"
                st.success(f"{book_to_return.title()} returned successfully by {prev_issuer.title()}.")
        else:
            st.info("No books are currently issued.")

    elif choice == "View Issued Books":
        st.subheader("Issued Books")
        found = False
        for title, info in library2.items():
            if info["Availability"] == "unavailable" and info["Issued_to"] != "none":
                st.write(f"**{title.title()}** | Issued to: {info['Issued_to'].title()}")
                found = True
        if not found:
            st.info("No books are currently issued.")

    elif choice == "Logout":
        for key in ["login_success", "username", "login_username", "login_password"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
