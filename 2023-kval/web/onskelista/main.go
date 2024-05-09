package main

import (
	"embed"
	"fmt"
	"net/http"
	"net/url"
	"os/exec"
	"strings"
	"text/template"
	"time"

	"github.com/google/uuid"
)

//go:embed static/*
var f embed.FS

type Wish struct {
	ID        string
	Content   string
	CreatedAt string
}

type User struct {
	ID       string
	Username string
	Password string
	Wishlist []Wish
}

var db map[string]*User

var cookieName = "errorklubba"

type Server struct {
	indexTmpl *template.Template
	loginTmpl *template.Template
}

func main() {
	mux := http.NewServeMux()
	s := newServer()
	s.fixRoutes(mux)

	db = map[string]*User{
		"admin": {
			ID:       uuid.NewString(),
			Username: "admin",
			Password: "019287430875109438",
			Wishlist: []Wish{{
				ID:      uuid.NewString(),
				Content: "SSM{0n5k31ist4_c0n741n5_k0b41tn37z}",
			}},
		},
	}
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

	loginTmpl, err := template.ParseFS(f, "static/login.html")
	if err != nil {
		panic(err.Error())
	}

	return &Server{
		indexTmpl: templ,
		loginTmpl: loginTmpl,
	}
}

func (s *Server) fixRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if s.getUser(w, r) == nil {
			http.Redirect(w, r, "/login", http.StatusSeeOther)
		} else {
			http.Redirect(w, r, "/wishlist", http.StatusSeeOther)
		}
	})
	mux.HandleFunc("/wishlist", s.wishlist)
	mux.HandleFunc("/new-wish", s.newWish)
	mux.HandleFunc("/login", s.login)
	mux.HandleFunc("/visit", s.visit)
}

func (s *Server) getUser(w http.ResponseWriter, r *http.Request) *User {
	cookie, err := r.Cookie(cookieName)
	if err != nil {
		return nil
	}

	a := strings.SplitN(cookie.Value, ":", 2)
	if u, ok := db[a[1]]; ok && u.ID == a[0] {
		return u
	}

	return nil
}

func (s *Server) wishlist(w http.ResponseWriter, r *http.Request) {
	user := s.getUser(w, r)
	if user == nil {
		http.Redirect(w, r, "/login", http.StatusSeeOther)
		return
	}

	s.indexTmpl.Execute(w, map[string]any{
		"User": user,
		"Msg":  r.URL.Query().Get("msg"),
		"Msg2": r.URL.Query().Get("msg2"),
	})
}

func (s *Server) login(w http.ResponseWriter, r *http.Request) {

	if r.Method != http.MethodPost {
		if s.getUser(w, r) != nil {
			http.Redirect(w, r, "/wishlist?msg=Already authed", http.StatusSeeOther)
			return
		}

		s.loginTmpl.Execute(w, map[string]any{
			"Msg": r.URL.Query().Get("msg"),
		})
		return
	}

	user := r.FormValue("username")
	pass := r.FormValue("password")

	u, ok := db[user]
	if ok && u.Password != pass {
		http.Redirect(w, r, "/login?msg=Bad Auth", http.StatusSeeOther)
		return
	}
	if !ok {
		u = &User{
			ID:       uuid.NewString(),
			Username: user,
			Password: pass,
			Wishlist: []Wish{},
		}
		db[user] = u
	}

	http.SetCookie(w, &http.Cookie{
		Name:     cookieName,
		Value:    u.ID + ":" + u.Username,
		HttpOnly: true,
	})
	http.Redirect(w, r, "/wishlist", http.StatusSeeOther)
}

func (s *Server) newWish(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	user := s.getUser(w, r)
	if user == nil {
		http.Redirect(w, r, "/login", http.StatusSeeOther)
		return
	}

	if user.Username == "admin" {
		w.WriteHeader(http.StatusOK)
		return
	}

	user.Wishlist = append(user.Wishlist, Wish{
		ID:        uuid.NewString(),
		Content:   r.FormValue("wish"),
		CreatedAt: time.Now().Format(time.ANSIC),
	})

	http.Redirect(w, r, "/wishlist?msg2=Wish created!", http.StatusSeeOther)
}

func (s *Server) visit(w http.ResponseWriter, r *http.Request) {

	if s.getUser(w, r) == nil {
		http.Redirect(w, r, "/wishlist?msg=plox authenticate", http.StatusSeeOther)
		return
	}

	u, err := url.Parse(r.FormValue("url"))

	if err != nil || u.Scheme != "http" {
		http.Redirect(w, r, "/wishlist?msg=bad url", http.StatusSeeOther)
		return
	}

	err = exec.Command("node", "visit.js", u.String()).Run()
	if err != nil {
		http.Redirect(w, r, "/wishlist?msg=något gick snett", http.StatusSeeOther)
		return
	}

	http.Redirect(w, r, "/wishlist?msg=admin kommer att besöka länken", http.StatusSeeOther)

}
