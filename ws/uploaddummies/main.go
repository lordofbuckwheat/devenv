package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"mime/multipart"
	"net/http"
	"os"
)

func upload(t string, arch string) {
	var payload = &bytes.Buffer{}
	writer := multipart.NewWriter(payload)
	if err := writer.WriteField("master_key", "ko5V38Mmh5mXP62pHvnLMYioUBJkGDiX5J1ju9YYuohIMnhZROqiCECXpYzmna4S"); err != nil {
		panic(err)
	}
	if err := writer.WriteField("controller", "distribute"); err != nil {
		panic(err)
	}
	if err := writer.WriteField("action", "upload"); err != nil {
		panic(err)
	}
	if err := writer.WriteField("type", t); err != nil {
		panic(err)
	}
	if err := writer.WriteField("version", "3.0.89.0"); err != nil {
		panic(err)
	}
	if err := writer.WriteField("description", fmt.Sprintf("3.0.89.0_%s", arch)); err != nil {
		panic(err)
	}
	if err := writer.WriteField("account_id", "0"); err != nil {
		panic(err)
	}
	var fileName = fmt.Sprintf("setup_TVBitServices__3.0.89.0_%s.exe", arch)
	file, err := os.Open(fileName)
	if err != nil {
		panic(err)
	}
	defer func() { _ = file.Close() }()
	part, err := writer.CreateFormFile("file", fileName)
	if err != nil {
		panic(err)
	}
	if _, err := io.Copy(part, file); err != nil {
		panic(err)
	}
	if err := writer.Close(); err != nil {
		panic(err)
	}
	resp, err := http.Post("https://master.tvbit.local", writer.FormDataContentType(), payload)
	if err != nil {
		panic(err)
	}
	defer func() { _ = resp.Body.Close() }()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	var j interface{}
	if err := json.Unmarshal(body, &j); err != nil {
		panic(err)
	}
}

func main() {
	upload("0", "x86")
	upload("1", "x64")
}
