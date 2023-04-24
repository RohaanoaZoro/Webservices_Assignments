package main

import (
	"log"
	"net/http"
	"time"
)

type RefreshTokenClaims struct {
	ClientId      string `json:"clientid"`
	ClientSecret  string `json:"clientsecret"`
	SessionId     string `json:"sessionid"`
	ApplicationId string `json:"appId"`
	StandardClaims
}

func GenerateToken(clientId string, sessionId string, SignatureKey string) (string, bool) {
	expirationTime := time.Now().Add(time.Minute * 15)

	claims := Claims{
		ClientId:  clientId,
		SessionId: sessionId,
		StandardClaims: StandardClaims{
			IssuedAt:  time.Now().Unix(),
			ExpiresAt: expirationTime.Unix(),
		},
	}

	tokenString, err := GenerateJWT(SignatureKey, claims)
	if err != nil {
		log.Println("token err", err)
		return err.Error(), false
	}

	return tokenString, true
}

func GenerateRefreshToken(clientId string, clientSecret string, sessionId string, applicationId string, signatureKey string) (http.Cookie, bool) {
	expirationTime := time.Now().Add(time.Hour * 24)

	claims := RefreshTokenClaims{
		ClientId:      clientId,
		SessionId:     sessionId,
		ApplicationId: applicationId,
		StandardClaims: StandardClaims{
			ExpiresAt: expirationTime.Unix(),
		},
	}

	tokenString, err := GenerateJWT(signatureKey, claims)
	if err != nil {
		log.Println("token err", err)
		return http.Cookie{}, false
	}

	return http.Cookie{
		Name:     "refresh_token",
		Value:    tokenString,
		Expires:  time.Now().Add(time.Hour * 24),
		HttpOnly: true,
		SameSite: http.SameSiteLaxMode,
	}, true

}
