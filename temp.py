import keyring
import getpass 
  

def main():
	email = input("Email: ")
	try: 
		pwd = getpass.getpass("password: ") # protected input
	except Exception as error: 
		print('ERROR', error) 
	service = "login"
	info = "info"
	keyring.set_password(service, email, pwd) # type real username and pass
	keyring.set_password(service, info, email) # type real username


	### getter functions to get username and pass in DataGetter.py file ###

	# username = keyring.get_password(service, info)
	# password = keyring.get_password(service, username)


if __name__ == '__main__':
    main()
