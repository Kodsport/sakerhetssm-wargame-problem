package main

import (
	"embed"
	"fmt"
	"html/template"
	"net/http"
	"os"
	"strings"

	"github.com/google/uuid"
)

type ctf struct {
	URL         string
	Thumbnail   string
	Title       string
	Description string
}

//go:embed static/* main.go
var f embed.FS

type userdata struct {
	suggestions []*ctf
}

var db map[string]*userdata

var globalDB []*ctf

var cookieName = "ctfplansession"

type Server struct {
	flagStr   []byte
	indexTmpl *template.Template
}

func main() {
	mux := http.NewServeMux()
	s := newServer()
	s.fixRoutes(mux)

	{
		ctf, err := s.fetchCTF("https://securityfest.com")
		if err != nil {
			fmt.Println(err.Error())
		} else {
			globalDB = append(globalDB, ctf)
		}

		ctf, err = s.fetchCTF("https://2023.ctf.dicega.ng/")
		if err != nil {
			fmt.Println(err.Error())
		} else {
			globalDB = append(globalDB, ctf)
		}

		ctf, err = s.fetchCTF("https://ctf.idek.team/")
		if err != nil {
			fmt.Println(err.Error())
		} else {
			globalDB = append(globalDB, ctf)
		}

	}
	db = map[string]*userdata{}

	http.ListenAndServe("0.0.0.0:8080", mux)
}

func newServer() *Server {
	x, _ := f.ReadDir("static/")
	for i, de := range x {
		fmt.Println(i, de)
	}

	templ, err := template.ParseFS(f, "static/index.html")
	if err != nil {
		fmt.Println(err.Error())
	}

	return &Server{
		flagStr:   []byte(os.Getenv("FLAG")),
		indexTmpl: templ,
	}
}

func (s *Server) fixRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/", s.index)
	mux.HandleFunc("/flag", s.flag)
	mux.HandleFunc("/suggest", s.addSuggestion)
	mux.HandleFunc("/source", s.source)
}

func (s *Server) getUser(w http.ResponseWriter, r *http.Request) *userdata {
	cookie, err := r.Cookie(cookieName)
	if err == nil {
		if _, ok := db[cookie.Value]; ok {
			return db[cookie.Value]
		}
	}

	value := uuid.NewString()
	http.SetCookie(w, &http.Cookie{
		Name:  cookieName,
		Value: value,
	})

	db[value] = &userdata{
		suggestions: []*ctf{},
	}
	return db[value]
}

func (s *Server) index(w http.ResponseWriter, r *http.Request) {
	user := s.getUser(w, r)

	s.indexTmpl.Execute(w, map[string]any{
		"Suggestions": user.suggestions,
		"Global":      globalDB,
	})
}

func (s *Server) source(w http.ResponseWriter, r *http.Request) {
	ff, _ := f.ReadFile("main.go")
	w.Write(ff)
}

func (s *Server) addSuggestion(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	r.ParseForm()
	url := r.Form.Get("url")

	ctf, err := s.fetchCTF(url)
	if err != nil {
		w.Write([]byte(err.Error()))
		return
	}

	user := s.getUser(w, r)
	user.suggestions = append(user.suggestions, ctf)

	http.Redirect(w, r, "/", http.StatusMovedPermanently)
}

func (s *Server) flag(w http.ResponseWriter, r *http.Request) {
	if strings.HasPrefix(r.RemoteAddr, "127.0.0.1:") {
		w.Write(s.flagStr)
	} else {
		w.Write([]byte("SSM{________?_}"))
	}
}
