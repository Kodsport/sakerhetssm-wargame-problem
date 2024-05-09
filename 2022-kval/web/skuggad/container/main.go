package main

import (
	"database/sql"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"

	_ "embed"

	"github.com/google/uuid"
	_ "github.com/mattn/go-sqlite3"
)

//go:embed index.html
var index []byte

//go:embed main.go
var sourceCode []byte

func main() {
	err := realMain()
	if err != nil {
		fmt.Fprint(os.Stderr, err)
		os.Exit(1)
	}
}

func realMain() error {
	dbFile, err := os.CreateTemp(os.TempDir(), "notes-*.db")
	if err != nil {
		return err
	}

	db, err := sql.Open("sqlite3", dbFile.Name())
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	_, err = db.Exec("CREATE TABLE IF NOT EXISTS notes (id TEXT PRIMARY KEY, user_id TEXT NOT NULL, note TEXT NOT NULL);")
	if err != nil {
		return err
	}

	err = createAdminNotes(db)
	if err != nil {
		return err
	}

	go func() {
		ticker := time.Tick(time.Minute * 5)
		for range ticker {
			_, err := db.Exec("DELETE FROM notes WHERE user_id != 'admin'")
			if err != nil {
				fmt.Println(err.Error())
			}
		}
	}()

	s := server{
		db:             db,
		apiKeyToUserID: make(map[string]string),
	}

	mux := http.NewServeMux()
	s.handleMux(mux)

	return http.ListenAndServe("0.0.0.0:8080", mux)
}

type server struct {
	db             *sql.DB
	apiKeyToUserID map[string]string
}

func (s *server) handleMux(mux *http.ServeMux) {
	mux.Handle("/api/note", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodPost:
			s.createNote(rw, r)
		case http.MethodGet:
			s.listNotes(rw, r)
		default:
			rw.WriteHeader(http.StatusMethodNotAllowed)
		}
	}))

	mux.Handle("/api/login", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			rw.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		s.login(rw, r)
	}))

	mux.Handle("/source", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		rw.Write(sourceCode)
	}))

	mux.Handle("/", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		rw.Write(index)
	}))
}

func (s *server) login(rw http.ResponseWriter, r *http.Request) {
	token := make([]byte, 64)
	_, err := rand.Read(token)
	if err != nil {
		rw.WriteHeader(http.StatusInternalServerError)
		return
	}
	token64 := make([]byte, base64.StdEncoding.EncodedLen(len(token)))
	base64.StdEncoding.Encode(token64, token)

	userID := uuid.NewString()
	s.apiKeyToUserID[string(token64)] = userID

	res := struct {
		Token string `json:"token"`
	}{
		Token: string(token64),
	}
	json.NewEncoder(rw).Encode(res)
}

type noteRow struct {
	ID     string `json:"id"`
	UserID string `json:"user_id"`
	Note   string `json:"note"`
}

var pattern = regexp.MustCompile(`[a-zA-z\ \_\}]`)

func (s *server) listNotes(rw http.ResponseWriter, r *http.Request) {
	search := r.URL.Query().Get("search")
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))

	conditions := []string{"'very cool chall' = 'very cool chall'"}
	params := []interface{}{}

	if search != "" {
		if !pattern.Match([]byte(search)) {
			rw.WriteHeader(http.StatusBadRequest)
			return
		}
	}
	conditions = append(conditions, "note LIKE ? ESCAPE '\\'")
	params = append(params, "%"+strings.ReplaceAll(search, "_", "\\_")+"%")

	rows := []*noteRow{}
	if userID, ok := s.apiKeyToUserID[r.Header.Get("Authorization")]; !ok {
		rw.WriteHeader(http.StatusForbidden)
		return
	} else {
		conditions := append(conditions, "user_id = ? LIMIT 30 OFFSET ?")
		params := append(params, userID, page)

		result, err := s.db.Query("SELECT id, user_id, note FROM notes WHERE "+strings.Join(conditions, " AND "), params...)
		if err != nil {
			rw.WriteHeader(http.StatusInternalServerError)
			return
		}

		for result.Next() {
			row := &noteRow{}
			err = result.Scan(&row.ID, &row.UserID, &row.Note)
			if err != nil {
				rw.WriteHeader(http.StatusInternalServerError)
				return
			}
			rows = append(rows, row)
		}
	}

	result := s.db.QueryRow("SELECT count(*) FROM notes WHERE "+strings.Join(conditions, " AND "), params...)
	if err := result.Err(); err != nil {
		rw.WriteHeader(http.StatusInternalServerError)
		return
	}

	var count int64
	err := result.Scan(&count)
	if err != nil {
		rw.WriteHeader(http.StatusInternalServerError)
		return
	}

	bytes, _ := json.Marshal(struct {
		Notes []*noteRow `json:"notes"`
		Count int64      `json:"count"`
		Page  int        `json:"page"`
	}{
		Notes: rows,
		Count: count,
		Page:  page,
	})
	rw.Write(bytes)
}

type createNotesReq struct {
	Note string `json:"note"`
}

func (s *server) createNote(rw http.ResponseWriter, r *http.Request) {
	var req createNotesReq
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		rw.WriteHeader(http.StatusBadRequest)
		return
	}

	if !pattern.Match([]byte(req.Note)) {
		rw.WriteHeader(http.StatusBadRequest)
		return
	}

	auth := r.Header.Get("Authorization")
	userID := s.apiKeyToUserID[auth]

	_, err = s.db.Exec("INSERT INTO notes (id, user_id, note) VALUES (?, ?, ?)", uuid.NewString(), userID, req.Note)
	if err != nil {
		rw.WriteHeader(http.StatusInternalServerError)
		return
	}

	rw.WriteHeader(http.StatusCreated)
}
