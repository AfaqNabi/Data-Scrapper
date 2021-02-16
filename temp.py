import keyring

def main():
	service = "login"
	info = "info"
	keyring.set_password(service, "username", "password") # type real username and pass
	keyring.set_password(service, info, "username") # type real username

	
	### getter functions to get username and pass in DataGetter.py file ###

	# username = keyring.get_password(service, info)
	# password = keyring.get_password(service, username)


if __name__ == '__main__':
    main()
