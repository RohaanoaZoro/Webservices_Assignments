package main

import (
	"log"
)

func Authentication(username string, password string) (string, bool) {

	UserDetails, err := GetUserDetails(username)
	if err != nil {
		return err.Error(), false
	}

	// if EncryptedPassword(password) != UserDetails.Password {
	// 	log.Println("Epass Not Same")
	// 	return "", false
	// }

	if password != UserDetails.Password {
		log.Println("Epass Not Same")
		return "password mismatch", false
	}

	return UserDetails.Client_ID, true
}
