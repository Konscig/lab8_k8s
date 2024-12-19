package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"sync"
)

// WordCount represents the word and its count
type WordCount struct {
	Word  string `json:"word"`
	Count int    `json:"count"`
}

func countWords(chunk string, resultChan chan map[string]int, wg *sync.WaitGroup) {
	defer wg.Done()
	wordCounts := make(map[string]int)
	words := strings.Fields(chunk)
	for _, word := range words {
		wordCounts[word]++
	}
	resultChan <- wordCounts
}

func mergeWordCounts(resultChan chan map[string]int, wg *sync.WaitGroup) map[string]int {
	finalCounts := make(map[string]int)
	wg.Wait()
	close(resultChan)

	for partialCounts := range resultChan {
		for word, count := range partialCounts {
			finalCounts[word] += count
		}
	}

	return finalCounts
}

func wordCountHandler(w http.ResponseWriter, r *http.Request) {
	text := r.URL.Query().Get("text")
	if text == "" {
		http.Error(w, "Missing 'text' parameter", http.StatusBadRequest)
		return
	}

	resultChan := make(chan map[string]int)
	var wg sync.WaitGroup

	// Split text into chunks to simulate parallel processing
	chunks := strings.FieldsFunc(text, func(r rune) bool { return r == '.' || r == '!' || r == '?' })
	for _, chunk := range chunks {
		wg.Add(1)
		go countWords(chunk, resultChan, &wg)
	}

	// Merge results from all goroutines
	finalCounts := mergeWordCounts(resultChan, &wg)

	// Convert results to JSON
	response := []WordCount{}
	for word, count := range finalCounts {
		response = append(response, WordCount{Word: word, Count: count})
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, "Failed to encode response", http.StatusInternalServerError)
		return
	}
}

func main() {
	http.HandleFunc("/word-count", wordCountHandler)
	fmt.Println("Starting server on port 80...")
	if err := http.ListenAndServe(":80", nil); err != nil {
		fmt.Println("Failed to start server:", err)
	}
}
