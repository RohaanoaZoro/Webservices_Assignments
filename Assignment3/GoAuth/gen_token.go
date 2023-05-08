package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"strings"
	"time"
)

type StandardClaims struct {
	Audience  string `json:"aud,omitempty"`
	ExpiresAt int64  `json:"exp,omitempty"`
	Id        string `json:"jti,omitempty"`
	IssuedAt  int64  `json:"iat,omitempty"`
	Issuer    string `json:"iss,omitempty"`
	NotBefore int64  `json:"nbf,omitempty"`
	Subject   string `json:"sub,omitempty"`
}

type Claims struct {
	ClientId  string `json:"clientid"`
	SessionId string `json:"seesionid"`
	StandardClaims
}

func GenerateJWT(secretKey string, claims interface{}) (string, error) {

	// Encode the claims as a base64 string
	claimsBytes, err := json.Marshal(claims)
	if err != nil {
		return "", err
	}
	claimsBase64 := base64.RawURLEncoding.EncodeToString(claimsBytes)

	// Create the header object
	header := map[string]string{
		"alg": "HS256",
		"typ": "JWT",
	}

	// Encode the header as a base64 string
	headerBytes, err := json.Marshal(header)
	if err != nil {
		return "", err
	}
	headerBase64 := base64.RawURLEncoding.EncodeToString(headerBytes)

	// Concatenate the header and claims strings with a dot separator
	unsignedToken := fmt.Sprintf("%s.%s", headerBase64, claimsBase64)

	// Sign the token with the secret key using HMAC-SHA256
	signature := hmacSHA256(unsignedToken, []byte(secretKey))

	// Concatenate the unsigned token and signature with a dot separator
	signedToken := fmt.Sprintf("%s.%s", unsignedToken, signature)

	return signedToken, nil
}

func VerifyJWT(token string, secretKey string) (map[string]interface{}, error) {

	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return nil, errors.New("Invalid token format")
	}
	header := make(map[string]string)
	decodedBytesHeader, err := base64.StdEncoding.DecodeString(parts[0])
	if err != nil {
		return nil, err
	}
	if err := json.Unmarshal(decodedBytesHeader, &header); err != nil {
		return nil, err
	}
	log.Println("header", header)

	claims := make(map[string]interface{})
	encodedString := parts[1]
	decodedBytes, err := base64.StdEncoding.DecodeString(encodedString)
	decodedString := string(decodedBytes) + "}"
	log.Println("decodedString", decodedString)
	if err := json.Unmarshal([]byte(decodedString), &claims); err != nil {
		return nil, err
	}

	signature := parts[2]
	message := parts[0] + "." + parts[1]
	expectedSignature := hmacSHA256(message, []byte(secretKey))
	if signature != expectedSignature {
		return nil, errors.New("Invalid signature")
	}
	if exp, ok := claims["exp"].(float64); ok && exp < float64(time.Now().Unix()) {
		return nil, errors.New("Token expired")
	}
	return claims, nil
}

func hmacSHA256(data string, key []byte) string {
	h := hmac.New(sha256.New, key)
	h.Write([]byte(data))
	return base64.RawURLEncoding.EncodeToString(h.Sum(nil))
}
