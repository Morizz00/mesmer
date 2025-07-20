package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

type promptRequest struct {
	Message string `json:"message"`
}
type promptResponse struct {
	Reply string `json:"reply"`
}

func handler(w http.ResponseWriter, r *http.Request) {

	if r.Method != "POST" {
		http.Error(w, "post not allowed", http.StatusMethodNotAllowed)
		return
	}

	body, _ := io.ReadAll(r.Body)
	var req promptRequest
	json.Unmarshal(body, &req)

	reply := fmt.Sprintf("Go aligned at %s", req.Message)

	response := promptResponse{Reply: reply}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	port := os.Getenv("GO_PORT")
	if port == "" {
		port = "8080"
	}
	fmt.Println("GO llm microservice running at http://localhost:" + port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
