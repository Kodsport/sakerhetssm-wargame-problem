package main

import (
	"encoding/base64"
	"io/ioutil"
	"net/http"

	"github.com/dyatlov/go-opengraph/opengraph"
)

func (s *Server) fetchCTF(url string) (*ctf, error) {
	resp, err := http.DefaultClient.Get(url)
	if err != nil {
		return nil, err
	}

	og := opengraph.NewOpenGraph()
	err = og.ProcessHTML(resp.Body)
	if err != nil {
		return nil, err
	}

	ctf := &ctf{
		URL:         url,
		Title:       og.Title,
		Description: og.Description,
	}

	if len(og.Images) != 0 {
		resp, err := http.DefaultClient.Get(og.Images[0].URL)
		if err != nil {
			return nil, err
		}
		x, err := ioutil.ReadAll(resp.Body)
		if err == nil {
			ctf.Thumbnail = base64.StdEncoding.EncodeToString(x)
		}
	}

	return ctf, nil
}
