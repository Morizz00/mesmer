package main

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"os/exec"
	"strconv"
	"strings"

	"github.com/dgrijalva/jwt-go"
	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin:     func(r *http.Request) bool { return true },
}

type Client struct {
	conn   *websocket.Conn
	mode   string
	userID int
}

var clients = make(map[*Client]bool)

const secretKey = "your-secret-key-here"

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	tokenStr := r.Header.Get("Authorization")
	if tokenStr == "" || !strings.HasPrefix(tokenStr, "Bearer ") {
		http.Error(w, "Missing or invalid token", http.StatusUnauthorized)
		return
	}

	tokenStr = strings.TrimPrefix(tokenStr, "Bearer ")
	token, err := jwt.Parse(tokenStr, func(token *jwt.Token) (interface{}, error) {
		return []byte(secretKey), nil
	})
	if err != nil || !token.Valid {
		http.Error(w, "Invalid token", http.StatusUnauthorized)
		return
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || claims["user_id"] == nil {
		http.Error(w, "Invalid token claims", http.StatusUnauthorized)
		return
	}
	userIDFloat, ok := claims["user_id"].(float64)
	if !ok || userIDFloat <= 0 {
		http.Error(w, "Invalid user ID in token", http.StatusUnauthorized)
		return
	}

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error:", err)
		return
	}
	defer conn.Close()

	userID := int(userIDFloat)
	client := &Client{conn: conn, mode: "friend", userID: userID}
	clients[client] = true

	for {
		_, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("Read error:", err)
			delete(clients, client)
			return
		}

		if string(msg) == "switch:friend" {
			client.mode = "friend"
			conn.WriteMessage(websocket.TextMessage, []byte("Switched to Friend mode"))
		} else if string(msg) == "switch:therapist" {
			client.mode = "therapist"
			conn.WriteMessage(websocket.TextMessage, []byte("Switched to Therapist mode"))
		} else {
			response := processWithPython(msg, client.mode, userID)
			conn.WriteMessage(websocket.BinaryMessage, response)
		}
	}
}

func processWithPython(audio []byte, mode string, userID int) []byte {
	cmd := exec.Command("python3", "../python/main.py", mode, strconv.Itoa(userID)) // Changed to strconv.Itoa
	cmd.Stdin = bytes.NewReader(audio)
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		log.Println("Python error:", err)
		return []byte("Error processing audio")
	}
	return out.Bytes()
}

func handleLogin(w http.ResponseWriter, r *http.Request) {
	var creds struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}
	if err := json.NewDecoder(r.Body).Decode(&creds); err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}
	if creds.Username == "jace" && creds.Password == "test123" {
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{"user_id": 1})
		tokenStr, _ := token.SignedString([]byte(secretKey))
		json.NewEncoder(w).Encode(map[string]string{"token": tokenStr})
	} else {
		http.Error(w, "Invalid credentials", http.StatusUnauthorized)
	}
}

func main() {
	http.HandleFunc("/ws", handleWebSocket)
	http.HandleFunc("/login", handleLogin)
	log.Println("Server starting on :8080...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal("ListenAndServe error:", err)
	}
}
