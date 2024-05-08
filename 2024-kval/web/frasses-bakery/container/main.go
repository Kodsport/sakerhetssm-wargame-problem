package main

import (
	"fmt"
	"database/sql"
	"html/template"
	"os"
	"log"
	"net/http"

	_ "github.com/mattn/go-sqlite3"
)

type Cake struct {
	ID int
	Name string
	Desc string
}

// Template caching
var templates = template.Must(template.ParseGlob("templates/*.html"))
var Cakes = map[string]interface{}{
	"Cakes": []string{"ducky", "vinyl", "cheeseburger", "typewriter", "teapot", "feather"},
}

func main() {
	// Database connection
	database, err := sql.Open("sqlite3", "./bakery.db")
	if err != nil {
		log.Fatal(err)
	}
	defer database.Close()


	fs := http.FileServer(http.Dir("./static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Routes
	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/login", loginHandler(database))
	http.HandleFunc("/about", aboutHandler(database)) // Intentionally vulnerable

	// Start server
	log.Println("Starting server on :"+os.Getenv("PORT"))
	log.Fatal(http.ListenAndServe(":"+os.Getenv("PORT"), nil))
}

func renderTemplate(w http.ResponseWriter, tmpl string, data interface{}) {
	err := templates.ExecuteTemplate(w, tmpl+".html", data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	renderTemplate(w, "index", Cakes)
}

func loginHandler(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
			case "GET":
			// Display the login form
			renderTemplate(w, "login", nil)
		case "POST":
			// Process the login form
			if err := r.ParseForm(); err != nil {
				renderTemplate(w, "login", map[string]string{"ErrorMessage": "Failed to parse form"})
				return
			}

			username := r.FormValue("username")
			password := r.FormValue("password")

			var dbPassword string
			err := db.QueryRow("SELECT password FROM users WHERE username = ?", username).Scan(&dbPassword)
			if err != nil {
				if err == sql.ErrNoRows {
					renderTemplate(w, "login", map[string]string{"ErrorMessage": "Invalid username or password"})
					return
				}
				log.Println("Database query error:", err)
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
				return
			}

			if password == dbPassword {
				// Redirect or display success message
				renderTemplate(w, "login", map[string]string{"SuccessMessage": "FLAG: "+os.Getenv("FLAG")})
			} else {
				renderTemplate(w, "login", map[string]string{"ErrorMessage": "Invalid username or password"})
			}
		default:
			http.Error(w, "Only GET and POST methods are allowed", http.StatusMethodNotAllowed)
		}
	}
}

func aboutHandler(db *sql.DB) http.HandlerFunc {
	type PageData struct {
		CakesStatic map[string]interface{} // Assuming this holds paths or names of all cakes
		CakeDetails Cake
	}

	return func(w http.ResponseWriter, r *http.Request) {
		// Extracting the 'id' parameter from the query string
		id := r.URL.Query().Get("id")
		if id == "" {
			http.Error(w, "ID parameter is missing", http.StatusBadRequest)
			return
		}

		// Intentionally vulnerable SQL statement
		query := fmt.Sprintf("SELECT id, name, desc FROM cakes WHERE id = %s", id)
		var cake Cake
		
		// Executing the query
		err := db.QueryRow(query).Scan(&cake.ID, &cake.Name, &cake.Desc)
		if err != nil {
			if err == sql.ErrNoRows {
				http.NotFound(w, r)
				return
			}
			log.Printf("QueryRow error: %v\n", err)
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}

		pageData := PageData{
			CakesStatic: Cakes,
			CakeDetails: cake,
		}

		renderTemplate(w, "about", pageData)
	}
}