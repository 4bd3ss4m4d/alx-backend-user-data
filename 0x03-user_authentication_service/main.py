#!/usr/bin/env python3

'''
This is the main file for the flask app
'''

from requests import get, put, post, delete


def register_user(email: str, password: str) -> None:
    '''
    Register user test
    Args:
        email: str: Email of user
        password: str: Password of user
    Returns:
        None
    '''
    req = post("http://0.0.0.0:5000/users",
                   data={'email': email, "password": password})
    res = req.json()
    assert res == {"email": email, "message": "user created"}
    assert req.status_code == 200

    req = post("http://0.0.0.0:5000/users",
                   data={'email': email, "password": password})
    res = req.json()
    assert res == {"message": "email already registered"}
    assert req.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """ Wrong password test
    """
    req = post("http://0.0.0.0:5000/sessions",
                   data={'email': email, "password": password})
    assert req.status_code == 401
    assert req.cookies.get("session_id") is None


def log_in(email: str, password: str) -> str:
    '''
    Login test
    Args:
        email: str: Email of user
        password: str: Password of user
    Returns:
        str: Session ID
    '''
    req = post("http://0.0.0.0:5000/sessions",
                   data={'email': email, "password": password})
    response = req.json()
    session_id = req.cookies.get("session_id")
    assert req.status_code == 200
    assert response == {"email": email, "message": "logged in"}
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    '''
    Unlogged user profile test
    Returns:
        None
    '''
    req = get("http://0.0.0.0:5000/profile")
    assert req.status_code == 403


def profile_logged(session_id: str) -> None:
    '''
    Logged user profile test
    Args:
        session_id: str: Session ID
    Returns:
        None
    '''
    re = get("http://0.0.0.0:5000/profile",
                  cookies={"session_id": session_id})
    res = re.json()
    assert re.status_code == 200
    assert res == {"email": EMAIL}


def log_out(session_id: str) -> None:
    '''
    Logout test
    Args:
        session_id: str: Session ID
    Returns:
        None
    '''
    req = delete("http://0.0.0.0:5000/sessions",
                     cookies={"session_id": session_id},
                     allow_redirects=True)
    res = req.json()
    hist = req.history
    assert req.status_code == 200
    assert len(hist) == 1
    assert hist[0].status_code == 302
    assert res == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    '''
    Reset password token test
    Args:
        email: str: Email of user
    Returns:
        str: Reset token
    '''
    req = post("http://0.0.0.0:5000/reset_password",
                   data={"email": email})
    resp = req.json()
    resToken = resp.get("reset_token")
    assert req.status_code == 200
    assert type(resToken) is str
    return resToken


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''
    Update password test
    Args:
        email: str: Email of user
        reset_token: str: Reset token
        new_password: str: New password
    Returns:
        None
    '''
    req = put("http://0.0.0.0:5000/reset_password",
                  data={"email": email, "new_password":
                        new_password, "reset_token":
                        reset_token})
    res = req.json()
    assert req.status_code == 200
    assert res == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
