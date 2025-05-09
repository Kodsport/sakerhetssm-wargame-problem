package main

import (
	"encoding/json"
	"errors"
	"net/http"
	"os"
	"regexp"

	"github.com/google/uuid"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type User struct {
	gorm.Model
	Name      string `gorm:"unique"`
	Password  string
	Money     int
	SessionID string
}

type BoughtItem struct {
	gorm.Model
	User      User
	UserID    uint
	ProductID int
}

type Product struct {
	gorm.Model
	Title       string
	Description string
	Price       int
}

// NO FUNKY BEHAVIOUR
func (u *User) BeforeUpdate(tx *gorm.DB) (err error) {

	if u.Money > 100 {
		return errors.New("too rich")
	}

	if u.Money < -4294967296 {
		return errors.New("too poor")
	}

	return nil
}

func main() {
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	db = db.Debug()
	// Migrate the schema
	db.AutoMigrate(&User{}, &BoughtItem{}, &Product{})

	db.Save(&Product{
		Title:       "Cool Sticker",
		Description: "nae",
		Price:       1,
	})

	db.Save(&Product{
		Title:       "Awesome Sticker",
		Description: "not so secret",
		Price:       95,
	})

	db.Save(&Product{
		Title:       "Flag Sticker",
		Description: os.Getenv("FLAG"),
		Price:       125,
	})

	mux := http.NewServeMux()

	mux.Handle("GET /", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		w.Write([]byte(`
		
		<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sticker Shop</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Sticker Shop</h1>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#shop">Shop</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <section id="home" class="hero">
        <h2>Unique & Trendy Stickers</h2>
        <p>Find the perfect sticker for your laptop, phone, or notebook.</p>
        <a href="#shop" class="btn">Shop Now</a>
    </section>
    

    <section id="auth">
        <h2>Login / Register</h2>
        <form id="registerForm">
            <h3>Register</h3>
            <input type="text" id="regName" placeholder="Username" required>
            <input type="password" id="regPassword" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
        <form id="loginForm">
            <h3>Login</h3>
            <input type="text" id="loginName" placeholder="Username" required>
            <input type="password" id="loginPassword" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </section>
    <section id="shop" class="products">
        <h2>Featured Stickers</h2>
        <div class="sticker-grid">
            <div class="sticker-item">
                <img src="sticker1.jpg" alt="Sticker 1">
                <p>Cool Sticker 1</p>
				<p>Price: 1</p>
                <button onclick="buy(1)">Add to Cart</button>
            </div>
            <div class="sticker-item">
                <img src="sticker2.jpg" alt="Sticker 2">
                <p>Awesome Sticker 2</p>
				<p>Price: 95</p>
                <button onclick="buy(2)">Add to Cart</button>
            </div>
            <div class="sticker-item">
                <img src="sticker3.jpg" alt="Sticker 3">
                <p>Flag Sticker 3</p>
				<p>Price: 125</p>
                <button onclick="buy(3)">Add to Cart</button>
            </div>
        </div>
    </section>



	<script>
	document.getElementById("registerForm").addEventListener("submit", async function(event) {
		event.preventDefault();
		const response = await fetch("/register", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				Name: document.getElementById("regName").value,
				Password: document.getElementById("regPassword").value
			})
		});
		const result = await response.text();
		alert(result);
	});

	document.getElementById("loginForm").addEventListener("submit", async function(event) {
		event.preventDefault();
		const response = await fetch("/login", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				Name: document.getElementById("loginName").value,
				Password: document.getElementById("loginPassword").value
			})
		});
		if (response.redirected) {
			window.location.href = response.url;
		} else {
			const result = await response.text();
			alert(result);
		}
	});

	async function buy(id) {
		const response = await fetch("/buy", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				ProductID: id,
			})
		});
		if (response.redirected) {
			window.location.href = response.url;
		} else {
			const result = await response.text();
			alert(result);
		}
	}
</script>

    
    <footer>
        <p>&copy; 2025 Sticker Shop. All rights reserved.</p>
    </footer>

	<style>
	body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f8f9fa;
    color: #333;
    text-align: center;
}

header {
    background-color: #ff6b6b;
    padding: 20px;
    color: white;
}

nav ul {
    list-style: none;
    padding: 0;
}

nav ul li {
    display: inline;
    margin: 0 15px;
}

nav ul li a {
    color: white;
    text-decoration: none;
    font-weight: bold;
}

.hero {
    padding: 50px 20px;
    background-color: #ffe066;
}

.btn {
    display: inline-block;
    background-color: #ff6b6b;
    color: white;
    padding: 10px 20px;
    margin-top: 10px;
    text-decoration: none;
    border-radius: 5px;
}

.products {
    padding: 40px 20px;
}

.sticker-grid {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}

.sticker-item {
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    width: 200px;
}

.sticker-item img {
    max-width: 100%;
    border-radius: 5px;
}

button {
    background-color: #ff6b6b;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #ff4757;
}

footer {
    background-color: #333;
    color: white;
    padding: 15px;
    margin-top: 20px;
}

	
	</style>
</body>
</html>
		
		`))

	}))

	mux.Handle("POST /register", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		var u User
		err = json.NewDecoder(r.Body).Decode(&u)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(err.Error()))
			return
		}
		u.Money = 100

		err = db.Create(&u).Error
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte(err.Error()))

			return
		}

		w.Write([]byte("Registered!"))
	}))

	mux.Handle("POST /login", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		var u User
		err = json.NewDecoder(r.Body).Decode(&u)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(err.Error()))
			return
		}

		if !regexp.MustCompile(`^[\d_\-a-zA-Z]+$`).Match([]byte(u.Name + u.Password)) {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("Invalid username"))
			return
		}
		err = db.First(&u, "name = '"+u.Name+"' and password = '"+u.Password+"'").Error

		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte(err.Error()))
			return
		}

		u.SessionID = uuid.Must(uuid.NewRandom()).String()
		http.SetCookie(w, &http.Cookie{
			Name:  "gogoworm",
			Value: u.SessionID,
		})

		err = db.Save(&u).Error
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte(err.Error()))
			return
		}

		http.Redirect(w, r, "/", http.StatusFound)

	}))

	mux.Handle("POST /buy", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		c, err := r.Cookie("gogoworm")

		if err != nil {
			w.Write([]byte(err.Error()))
			return
		}

		var u User
		err = db.Find(&u, "session_id = ?", c.Value).Error
		if err != nil {
			w.Write([]byte(err.Error()))
			return
		}

		var xx BoughtItem

		xx.UserID = u.ID
		json.NewDecoder(r.Body).Decode(&xx)

		var p Product
		err = db.Find(&p, "id = ?", xx.ProductID).Error
		if err != nil {
			w.Write([]byte(err.Error()))
			return
		}

		if p.Price > u.Money {
			w.Write([]byte(`too poor§`))
			return
		}

		err = db.Save(&xx).Error
		if err != nil {
			w.Write([]byte(err.Error()))
			return
		}

		w.Write([]byte(`du köpte: ` + p.Title + ` ` + p.Description))

	}))

	http.ListenAndServe(":8080", mux)
}
