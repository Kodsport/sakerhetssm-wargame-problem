package main

import (
	"bytes"
	"embed"
	"fmt"
	"html/template"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/julienschmidt/httprouter"
	cache "github.com/victorspringer/http-cache"
	"github.com/victorspringer/http-cache/adapter/memory"
)

//go:embed static/*
var f embed.FS

func main() {
	err := realMain()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func realMain() error {

	adapter, err := memory.NewAdapter(
		memory.AdapterWithAlgorithm(memory.LRU),
		memory.AdapterWithCapacity(1337),
	)
	if err != nil {
		return err
	}

	// mmm, fazer
	// mmmmm big speed, big cash
	cacheClient, err := cache.NewClient(
		cache.ClientWithAdapter(adapter),
		cache.ClientWithTTL(1*time.Minute),
		cache.ClientWithRefreshKey("opn"),
	)
	if err != nil {
		return err
	}

	mux := httprouter.New()

	mux.GET("/flag", func(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
		w.Header().Add("Access-Control-Allow-Origin", "http://admin.local")
		if strings.HasPrefix(r.RemoteAddr, "127.0") || strings.HasPrefix(r.RemoteAddr, "[::1]") {
			w.Write([]byte(os.Getenv("flag")))
			return
		}

		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("SSM{nej}"))
	})

	templ := template.Must(template.ParseFS(f, "static/cv/*"))
	mux.GET("/api/doc", func(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
		err := templ.Execute(w, r.URL.Query())
		if err != nil {
			w.Write([]byte(err.Error()))
		}
	})

	mux.POST("/api/gen-cv", func(w http.ResponseWriter, r *http.Request, p httprouter.Params) {

		b := &bytes.Buffer{}
		wr := multipart.NewWriter(b)
		wr.WriteField("remoteURL", "http://localhost:80/api/doc?"+r.URL.RawQuery)
		wr.Close()

		req, _ := http.NewRequest(http.MethodPost, "http://localhost:3000/convert/url", b)
		req.Header.Add("Content-Type", wr.FormDataContentType())

		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			fmt.Println(err)
			w.Write([]byte(err.Error()))
			return
		}

		io.Copy(w, resp.Body)
	})

	mux.NotFound = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// look at me normals
		if bs, err := f.ReadFile("static" + r.URL.Path); err == nil {
			w.Write(bs)
		} else {
			http.Redirect(w, r, fmt.Sprintf("https://%s/index.html", r.Host), http.StatusFound)
		}
	})

	muxx := cacheClient.Middleware(mux)
	go func() {
		http.ListenAndServe("0.0.0.0:80", muxx)
	}()
	server := &http.Server{Addr: "0.0.0.0:443", Handler: muxx}
	return server.ListenAndServeTLS("cert.pem", "privkey.pem")
}

// vill du inte att någon ska sno din flagga? planera då i förväg
// vill du sno någon annans flagga? planera i förväg
