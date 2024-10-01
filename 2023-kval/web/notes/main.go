package main

import (
	"embed"
	"fmt"
	"html/template"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/google/uuid"
)

//go:embed static/*
var f embed.FS

type Note struct {
	ID        int
	Contents  string
	CreatedAt string
}

type userdata struct {
	Notes []int
}

var db map[string]*userdata

var notes []*Note

var cookieName = "notessession"

type Server struct {
	indexTmpl *template.Template
	noteTmpl  *template.Template
}

func main() {
	mux := http.NewServeMux()
	s := newServer()
	s.fixRoutes(mux)

	notes = append(notes, &Note{
		Contents:  "Välkommen till anteckningsappen för alla dina anteckningsapplikativa behov.",
		ID:        len(notes),
		CreatedAt: time.Now().Format(time.ANSIC),
	})

	notes = append(notes, &Note{
		Contents:  "Funderar på om jag borde byta till UUIDs, det ska tydligen vara bättre för sådana där moderna mikrotjänster.",
		ID:        len(notes),
		CreatedAt: time.Now().Format(time.ANSIC),
	})

	// removed in wargame
	// notes = append(notes, &Note{
	// 	Contents:  "SECT{Is You Taking Notes On a Criminal Fucking Conspiracy?}",
	// 	ID:        len(notes),
	// 	CreatedAt: time.Now().Format(time.ANSIC),
	// })
	//
	// notes = append(notes, &Note{
	// 	Contents:  "Oj, fel CTF...",
	// 	ID:        len(notes),
	// 	CreatedAt: time.Now().Format(time.ANSIC),
	// })

	notes = append(notes, &Note{
		Contents:  os.Getenv("FLAG"),
		ID:        len(notes),
		CreatedAt: time.Now().Format(time.ANSIC),
	})

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
		panic(err.Error())
	}

	noteTmpl, err := template.ParseFS(f, "static/note.html")
	if err != nil {
		panic(err.Error())
	}

	return &Server{
		indexTmpl: templ,
		noteTmpl:  noteTmpl,
	}
}

func (s *Server) fixRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/", s.index)
	mux.HandleFunc("/new-note", s.newNote)
	mux.HandleFunc("/note", s.getNote)
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
		Notes: []int{0},
	}
	return db[value]
}

func (s *Server) index(w http.ResponseWriter, r *http.Request) {
	user := s.getUser(w, r)

	s.indexTmpl.Execute(w, map[string]any{
		"Notes": notes,
		"User":  user,
	})
}

func (s *Server) getNote(w http.ResponseWriter, r *http.Request) {
	idx, err := strconv.Atoi(r.URL.Query().Get("id"))
	if err != nil {
		w.Write([]byte(err.Error()))
		return
	}
	if idx < 0 || len(notes) <= idx {
		w.Write([]byte("nah, 404"))
		return
	}

	s.noteTmpl.Execute(w, map[string]any{
		"Note": notes[idx],
	})
}

func (s *Server) newNote(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	user := s.getUser(w, r)
	user.Notes = append(user.Notes, len(notes))

	notes = append(notes, &Note{
		Contents:  r.FormValue("contents"),
		ID:        len(notes),
		CreatedAt: time.Now().Format(time.ANSIC),
	})

	http.Redirect(w, r, "/", http.StatusMovedPermanently)
}
