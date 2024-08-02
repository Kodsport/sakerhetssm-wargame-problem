package main

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	_ "embed"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"github.com/apple/pkl-go/pkl"
	"net/http"
	"os"
	"regexp"
	"time"
)

//go:embed html/index.html
var index []byte

//go:embed html/login.html
var loginIndex []byte

//go:embed html/register.html
var registerIndex []byte

var template = `
amends "file://%s/base.pkl"
username = "%s"
password = "%s".sha256
email = "%s"
/* inviteCode = email.sha256 */
`

type User struct {
	Username string `pkl:"username"`
	Password string `pkl:"password"`

	Email string `pkl:"email"`
}

type server struct {
	users          map[string]User
	tasks          map[string][]string
	apiKeyToUserID map[string]string
}

type registerRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
	Email    string `json:"email"`
}

type loginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type createTaskRequest struct {
	Title string `json:"title"`
}

type authenticationResponse struct {
	Token string `json:"token"`
}

type meResponse struct {
	Username string `json:"username"`
	Email    string `json:"email"`
}

func ParseUser(user string, pass string, email string) (*User, error) {
	path, err := os.Getwd()
	if err != nil {
		return nil, err
	}

	// I heard that PKL is the new best configuration language, so I decided to try it out
	evaluator, err := pkl.NewEvaluator(context.Background(), pkl.PreconfiguredOptions)
	if err != nil {
		return nil, err
	}

	defer evaluator.Close()

	var payload = fmt.Sprintf(template, path, user, pass, email)

	var data User
	err = evaluator.EvaluateModule(
		context.Background(),
		pkl.TextSource(payload),
		&data,
	)

	if err != nil {
		return nil, err
	}

	return &data, nil
}

func GetToken() (string, error) {
	token := make([]byte, 64)
	_, err := rand.Read(token)
	if err != nil {
		return "", err
	}

	token64 := make([]byte, base64.StdEncoding.EncodedLen(len(token)))
	base64.StdEncoding.Encode(token64, token)

	return string(token64), nil
}

func (s *server) GetUser(auth string) *User {
	if auth == "" {
		return nil
	}

	if len(auth) < 8 || auth[:7] != "Bearer " {
		return nil
	}

	userID, ok := s.apiKeyToUserID[auth[7:]]
	if !ok {
		return nil
	}

	data, ok := s.users[userID]
	if !ok {
		return nil
	}

	return &data
}

func main() {
	err := start()
	if err != nil {
		fmt.Fprint(os.Stderr, err)
		os.Exit(1)
	}
}

func start() error {
	flag := os.Getenv("FLAG")
	if flag == "" {
		return fmt.Errorf("FLAG environment variable not set")
	}

	s := server{
		users:          make(map[string]User),
		tasks:          make(map[string][]string),
		apiKeyToUserID: make(map[string]string),
	}

	go func() {
		ticker := time.Tick(time.Minute * 10)
		for range ticker {
			s.users = make(map[string]User)
			s.tasks = make(map[string][]string)
			s.apiKeyToUserID = make(map[string]string)
		}
	}()

	mux := http.NewServeMux()
	s.handleMux(mux)

	return http.ListenAndServe("0.0.0.0:5000", mux)
}

func (s *server) handleMux(mux *http.ServeMux) {
	mux.Handle("/api/register", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			rw.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		s.register(rw, r)
	}))

	mux.Handle("/api/login", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			rw.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		s.login(rw, r)
	}))

	mux.Handle("/api/me", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			rw.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		s.me(rw, r)
	}))

	mux.Handle("/api/tasks", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodPost:
			s.createTask(rw, r)
		case http.MethodGet:
			s.getTasks(rw, r)
		default:
			rw.WriteHeader(http.StatusMethodNotAllowed)
		}
	}))

	mux.Handle("/", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		rw.Write(index)
	}))

	mux.Handle("/login", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		rw.Write(loginIndex)
	}))

	mux.Handle("/register", http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		rw.Write(registerIndex)
	}))
}

func (s *server) register(rw http.ResponseWriter, r *http.Request) {
	var req registerRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		rw.WriteHeader(http.StatusBadRequest)
		return
	}

	if _, ok := s.users[req.Username]; ok {
		rw.WriteHeader(http.StatusConflict)
		rw.Write([]byte("User already exists"))
		return
	}

	userRegex := regexp.MustCompile(`^\w+$`)
	emailRegex := regexp.MustCompile(`^[0-z.]+@[0-z.]+$`)

	if len(req.Username) < 4 || len(req.Username) > 20 || !userRegex.MatchString(req.Username) {
		rw.WriteHeader(http.StatusBadRequest)
		rw.Write([]byte("Invalid username"))
		return
	}

	if len(req.Password) < 8 {
		rw.WriteHeader(http.StatusBadRequest)
		rw.Write([]byte("Invalid password"))
		return
	}

	if !emailRegex.MatchString(req.Email) {
		rw.WriteHeader(http.StatusBadRequest)
		rw.Write([]byte("Invalid email"))
		return
	}

	user, err := ParseUser(req.Username, req.Password, req.Email)
	if err != nil {
		fmt.Println(err)
		rw.WriteHeader(http.StatusBadRequest)
		rw.Write([]byte("Failed to parse user data"))
		return
	}

	// I should probably verify the email address, but I'm lazy

	token, err := GetToken()
	if err != nil {
		rw.WriteHeader(http.StatusInternalServerError)
		return
	}

	s.users[req.Username] = *user
	s.apiKeyToUserID[token] = user.Username

	rw.WriteHeader(http.StatusCreated)
	json.NewEncoder(rw).Encode(authenticationResponse{
		Token: token,
	})
}

func (s *server) login(rw http.ResponseWriter, r *http.Request) {
	var req loginRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		rw.WriteHeader(http.StatusBadRequest)
		return
	}

	user, ok := s.users[req.Username]
	if !ok {
		rw.WriteHeader(http.StatusNotFound)
		return
	}

	hash := fmt.Sprintf("%x", sha256.Sum256([]byte(req.Password)))
	if user.Password != hash {
		rw.WriteHeader(http.StatusUnauthorized)
		return
	}

	token, err := GetToken()
	if err != nil {
		rw.WriteHeader(http.StatusInternalServerError)
		return
	}

	s.apiKeyToUserID[token] = user.Username
	json.NewEncoder(rw).Encode(authenticationResponse{
		Token: token,
	})
}

func (s *server) me(rw http.ResponseWriter, r *http.Request) {
	auth := r.Header.Get("Authorization")
	user := s.GetUser(auth)
	if user == nil {
		rw.WriteHeader(http.StatusUnauthorized)
		return
	}

	data := meResponse{
		Username: user.Username,
		Email:    user.Email,
	}

	rw.Header().Set("Content-Type", "application/json")
	json.NewEncoder(rw).Encode(data)
}

func (s *server) createTask(rw http.ResponseWriter, r *http.Request) {
	auth := r.Header.Get("Authorization")
	user := s.GetUser(auth)
	if user == nil {
		rw.WriteHeader(http.StatusUnauthorized)
		return
	}

	var req createTaskRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		rw.WriteHeader(http.StatusBadRequest)
		return
	}

	s.tasks[user.Username] = append(s.tasks[user.Username], req.Title)
	rw.WriteHeader(http.StatusCreated)
}

func (s *server) getTasks(rw http.ResponseWriter, r *http.Request) {
	auth := r.Header.Get("Authorization")
	user := s.GetUser(auth)
	if user == nil {
		rw.WriteHeader(http.StatusUnauthorized)
		return
	}

	rw.Header().Set("Content-Type", "application/json")
	json.NewEncoder(rw).Encode(s.tasks[user.Username])
}
