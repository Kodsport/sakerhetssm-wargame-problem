package main

import (
	"errors"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"os"
	"os/exec"
	"path"
	"strings"
)

func index(w http.ResponseWriter, r *http.Request) {
	f, err := os.Open("index.html")
	if err != nil {
		w.Write([]byte(fmt.Sprintf("Broken chall, contact admins! %v", err)))
		return
	}
	defer f.Close()
	io.Copy(w, f)
}

func formatDocument(r *http.Request) string {
	firstname := r.FormValue("firstname")
	lastname := r.FormValue("lastname")
	email := r.FormValue("email")
	cv := r.FormValue("cv")
	dir, _ := os.Executable()
	dir = path.Dir(dir)
	return fmt.Sprintf(`
//#show heading: x => x.with(body: box[#image("%%s", width: 1em, height: auto) x.body])
#show heading: x => [#box(height: 1em,image("%s")) #x.body]
#stack(
	dir: ltr,
	spacing: 1fr,
	align(bottom, text(24pt)[%s\ %s]),
	rect(image("%s", width: 4cm, height: auto)),
)
Email: #link("mailto:%s")

%s

#align(center, image("%s", width: 5cm, height: auto))
	`,
		path.Join(dir, "mining.jpg"),
		firstname,
		lastname,
		path.Join(dir, "face.png"),
		email,
		strings.ReplaceAll(cv, "#", "="),
		path.Join(dir, "default.png"),
	)
}

func compile(doc string) ([]byte, error) {
	name := fmt.Sprintf("/tmp/doc-%d", rand.Int())
	docname := name + ".typ"
	fdoc, err := os.Create(docname)
	if err != nil {
		return nil, fmt.Errorf("broken chall, contact admins: %v", err)
	}
	fdoc.WriteString(doc)
	fdoc.Close()

	pdfname := name + ".pdf"
	cmd := exec.Command("typst", "--root=/", "compile", docname, pdfname)
	var sb strings.Builder
	cmd.Stderr = &sb
	if err := cmd.Run(); err != nil {
		return nil, errors.New(err.Error() + "\n" + sb.String())
	}

	data, err := os.ReadFile(pdfname)
	if err != nil {
		return nil, fmt.Errorf("broken chall, contact admins: %v", err)
	}
	os.Remove(docname)
	os.Remove(pdfname)
	return data, nil
}

func document(w http.ResponseWriter, r *http.Request) {
	doc := formatDocument(r)
	pdf, err := compile(doc)
	if err != nil {
		w.WriteHeader(500)
		w.Write([]byte(fmt.Sprintf("Error while making document:\n%s", err.Error())))
		return
	}
	w.Header().Set("Content-Type", "application/pdf")
	w.Write(pdf)
}

func gif(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "image/gif")
	b, _ := os.ReadFile("gif.gif")
	w.Write(b)
}

func main() {
	http.HandleFunc("/", index)
	http.HandleFunc("/document", document)
	http.HandleFunc("/gif", gif)
	panic(http.ListenAndServeTLS(":8443", "cert.pem", "key.pem", nil))
}
