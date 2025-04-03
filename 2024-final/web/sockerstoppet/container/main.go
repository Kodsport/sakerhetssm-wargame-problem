package main

import (
	"database/sql"
	"errors"
	"fmt"
	"net/http"
	"os"

	"github.com/Kansuler/bankid"
	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
	"movitz.dev/sockerstoppet/api"
)

func main() {
	err := realMain()
	if err != nil {
		fmt.Println(err.Error())
		os.Exit(1)
		return
	}
}

func realMain() error {

	db, err := sql.Open("sqlite3", "file:locked.sqlite?cache=shared")

	db.Exec(`
	CREATE TABLE sessions (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		session_secret TEXT NOT NULL,
		chefsgradde_approved BOOLEAN NOT NULL DEFAULT FALSE
	);
	`)

	if err != nil {
		return err
	}

	bid, err := bankid.New(bankid.Options{
		Passphrase:           "qwerty123",
		SSLCertificate:       bankid.TestSSLCertificate,
		CertificateAuthority: bankid.TestCACertificate,
		URL:                  bankid.TestURL,
		Timeout:              5,
	})
	if err != nil {
		return err
	}

	router := gin.Default()

	service := api.New(db, bid)

	router.POST("/bankid/logout", service.Logout)
	router.POST("/bankid/order", service.BankIDAuth)
	router.POST("/bankid/collect", service.BankIDCollect)
	router.POST("/bankid/sign_chefsgrädde_eula", service.GräddeEula)
	router.POST("/bankid/collect_chefsgrädde_eula", service.CollectGräddeEula)

	router.GET("/@me", func(c *gin.Context) {
		id, err := c.Cookie("sockerstoppkaka")
		if err != nil {
			c.AbortWithError(http.StatusBadRequest, err)
			return
		}

		user, err := service.GetSession(id)
		if err != nil {
			c.AbortWithError(http.StatusForbidden, err)
			return
		}

		c.JSON(http.StatusOK, user)
	})

	router.GET("/flag", func(c *gin.Context) {

		id, err := c.Cookie("sockerstoppkaka")
		if err != nil {
			c.AbortWithError(http.StatusBadRequest, err)
			return
		}

		user, err := service.GetSession(id)
		if err != nil {
			c.AbortWithError(http.StatusForbidden, err)
			return
		}

		if !user.ChefsgradeApproved {
			c.AbortWithError(http.StatusForbidden, errors.New("you have to sign the chefsgrädde pledge! you filthy bureaucrat!"))
			return
		}

		c.JSON(http.StatusOK, gin.H{
			"flag": os.Getenv("FLAG"),
		})
	})

	router.Static("/static", "static")
	router.StaticFile("/", "static/index.html")

	// Run the server
	return router.Run(":8000")

}

type server struct {
	bid *bankid.BankID
}
