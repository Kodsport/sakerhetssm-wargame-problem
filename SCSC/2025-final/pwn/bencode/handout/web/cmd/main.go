package main

import (
	_ "embed"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
)

//go:embed website/index.html
var indexHTML string

func serve(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "%s", indexHTML)
}

func parse(w http.ResponseWriter, r *http.Request) {
	file, _, err := r.FormFile("torrentFile")

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	defer file.Close()

	w.Header().Add("Content-Disposition", "inline")

	cmd := exec.Command("qemu-aarch64", "./parse")
	cmd.Env = os.Environ()
	cmd.Env = append(cmd.Env, "QEMU_LD_PREFIX=/usr/aarch64-linux-gnu/")
	cmd.Stdin = file
	out, err := cmd.CombinedOutput()

	fmt.Fprintf(w, "%s", out)

}

func main() {
	http.HandleFunc("GET /", serve)
	http.HandleFunc("POST /", parse)
	fmt.Println("Listening on :8000")
	log.Fatal(http.ListenAndServe(":8000", nil))
}
