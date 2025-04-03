package main

import (
	"archive/zip"
	"bytes"
	"embed"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"text/template"

	"github.com/google/uuid"
)

// finns massa "defer close" som saknas säkert, orkar inte atm

var flag string

func init() {
	c1, err := os.ReadFile("hihi.txt")
	if err != nil {
		fmt.Println("no flag file")
		os.Exit(1)
	}
	flag = string(c1)
}

//go:embed static
var f embed.FS

func werr(w http.ResponseWriter, err error) {
	w.WriteHeader(http.StatusBadRequest)
	w.Write([]byte(err.Error()))
}

type Conf struct {
	Name      string `json:"name"`
	HatImage  string `json:"hat_image"`
	HeadImage string `json:"head_image"`
	BodyImage string `json:"body_image"`
}

func main() {

	mux := http.NewServeMux()

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			w.WriteHeader(http.StatusNotFound)
			w.Write([]byte("404"))
			return
		}
		f, _ := f.Open("static/start.html")
		io.Copy(w, f)
	})

	mux.HandleFunc("/static/", func(w http.ResponseWriter, r *http.Request) {
		fb, err := f.ReadFile("static" + r.URL.Path)
		if err != nil {
			w.WriteHeader(http.StatusNotFound)
			w.Write([]byte(err.Error()))
			return
		}
		w.Write(fb)
	})

	mux.HandleFunc("/images/", func(w http.ResponseWriter, r *http.Request) {
		parts := strings.Split(r.URL.Path, "/")
		id := parts[2]
		filename := parts[3]

		_, err := uuid.Parse(id)
		if err != nil {
			werr(w, err)
			return
		}

		fb, err := os.ReadFile("games/" + id + "/" + filename)
		if err != nil {
			w.WriteHeader(http.StatusNotFound)
			w.Write([]byte(err.Error()))
			return
		}
		w.Write(fb)
	})

	mux.HandleFunc("/start", func(w http.ResponseWriter, r *http.Request) {

		s := uuid.NewString()
		os.Mkdir("games/"+s, 0o755)

		bs, _ := json.Marshal(Conf{
			Name:      "Fighter",
			HatImage:  "static/victoriantophat.jpg",
			HeadImage: "static/carl.jpeg",
			BodyImage: "static/hasmat.jpg",
		})
		err := os.WriteFile("games/"+s+"/config.json", bs, 0o755)
		if err != nil {
			log.Println(err.Error())
		}

		http.Redirect(w, r, "/game?id="+s, http.StatusFound)
	})

	bs, _ := fs.ReadFile(f, "static/game.html")
	gameTemplate := template.Must(template.New("x").Parse(string(bs)))
	mux.HandleFunc("/game", func(w http.ResponseWriter, r *http.Request) {
		id, err := uuid.Parse(r.URL.Query().Get("id"))
		if err != nil {
			werr(w, err)
			return
		}

		conf, err := loadConf(id.String())
		if err != nil {
			return
		}
		gameTemplate.Execute(w, map[string]string{
			"Name":     conf.Name,
			"HAT_IMG":  conf.HatImage,
			"HEAD_IMG": conf.HeadImage,
			"BODY_IMG": conf.BodyImage,
		})
	})

	mux.HandleFunc("/resume", func(w http.ResponseWriter, r *http.Request) {
		f, _, err := r.FormFile("save")
		if err != nil {
			werr(w, err)
			return
		}
		defer f.Close()

		id := uuid.NewString()

		tf, err := os.CreateTemp("temp", "hehe-*.zip")
		if err != nil {
			werr(w, err)
			return
		}
		defer tf.Close()
		defer os.Remove(tf.Name())
		io.Copy(tf, f)

		c := exec.Command("unzip", tf.Name(), "-d", "games/"+id)

		err = c.Run()
		if err != nil {
			werr(w, err)
			return
		}

		http.Redirect(w, r, "/game?id="+id, http.StatusFound)
	})

	mux.HandleFunc("/export", func(w http.ResponseWriter, r *http.Request) {

		id, err := uuid.Parse(r.URL.Query().Get("id"))
		if err != nil {
			werr(w, err)
			return
		}

		path := "games/" + id.String()
		_, err = os.Stat(path)
		if err != nil {
			werr(w, err)
			return
		}

		b := bytes.NewBuffer([]byte{})
		writer := zip.NewWriter(b)

		xx := os.DirFS(path)
		matches, err := fs.Glob(xx, "*")
		if err != nil {
			werr(w, err)
			return
		}
		for _, match := range matches {
			wr, err := writer.Create(match)
			if err != nil {
				werr(w, err)
				return
			}
			f, _ := xx.Open(match)
			io.Copy(wr, f)
		}
		err = writer.Close()
		if err != nil {
			werr(w, err)
			return
		}

		w.WriteHeader(http.StatusOK)
		w.Write(b.Bytes())
	})

	mux.HandleFunc("/customImage", func(w http.ResponseWriter, r *http.Request) {
		id, err := uuid.Parse(r.URL.Query().Get("id"))
		if err != nil {
			werr(w, err)
			return
		}

		f, fh, err := r.FormFile("image")
		if err != nil {
			werr(w, err)
			return
		}

		newFile, err := os.OpenFile("games/"+id.String()+"/"+fh.Filename, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0o0755)
		if err != nil {
			werr(w, err)
			return
		}
		io.Copy(newFile, f)

		conf, err := loadConf(id.String())
		if err != nil {
			werr(w, err)
			return
		}

		url := "/images/" + id.String() + "/" + fh.Filename

		switch r.URL.Query().Get("img") {
		case "head":
			conf.HeadImage = url
		case "body":
			conf.BodyImage = url
		case "hat":
			conf.HatImage = url
		default:
			werr(w, errors.New("nah bruh"))
			return
		}

		err = storeConf(id.String(), conf)
		if err != nil {
			werr(w, err)
			return
		}

		w.WriteHeader(http.StatusOK)

	})

	mux.HandleFunc("/validate", validate_flag)

	mux.HandleFunc("/setkv", func(w http.ResponseWriter, r *http.Request) {

		id, err := uuid.Parse(r.URL.Query().Get("id"))
		if err != nil {
			werr(w, err)
			return
		}

		path := "games/" + id.String() + "/config.json"
		confb, err := os.ReadFile(path)
		if err != nil {
			werr(w, err)
			return
		}

		var x map[string]string
		err = json.Unmarshal(confb, &x)
		if err != nil {
			werr(w, err)
			return
		}

		x[r.URL.Query().Get("key")] = r.URL.Query().Get("value")
		bs, _ := json.Marshal(x)
		os.WriteFile(path, bs, 0o0755)

	})

	err := http.ListenAndServeTLS("0.0.0.0:8443", "self.crt", "self.key", mux)
	if err != nil {
		fmt.Println(err.Error())
	}

}

func storeConf(id string, conf *Conf) error {

	bs, err := json.Marshal(&conf)
	if err != nil {
		return err
	}
	path := "games/" + id + "/config.json"
	err = os.WriteFile(path, bs, 0o0755)
	if err != nil {
		return err
	}

	return nil

}

func loadConf(id string) (*Conf, error) {

	path := "games/" + id + "/config.json"
	confb, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var conf *Conf
	err = json.Unmarshal(confb, &conf)
	if err != nil {
		return nil, err

	}

	return conf, nil

}

func validate_flag(w http.ResponseWriter, r *http.Request) {

	if flag == r.URL.Query().Get("flag") {
		w.Write([]byte("nice"))
		return
	}

	w.WriteHeader(http.StatusBadRequest)
	w.Write([]byte("nah"))
}
