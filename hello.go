package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

// TODO: Make sure there is a way to avoid this file getting copied over to docs or static
// When running `npx`
func main() {

	fs := http.FileServer(http.Dir("./local_answering"))

	http.Handle("/", fs)

	fmt.Println("asdfsdf")

	http.HandleFunc("/api/receive_answer", clue_answers)

	log.Print("Listening on :3000...")
	err := http.ListenAndServe(":3000", nil)
	if err != nil {
		log.Fatal(err)
	}
}

func clue_answers(rw http.ResponseWriter, req *http.Request) {
	decoder := json.NewDecoder(req.Body)
	var data map[string]interface{}
	err := decoder.Decode(&data)
	if err != nil {
		log.Println("Error decoding JSON:", err)
		return
	}
	log.Println("JSON Payload:", data)

	// format as sadfjasjidfds< i>
	// append to files
}
