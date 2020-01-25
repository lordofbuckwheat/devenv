package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"net/http"
	"sync"
	"time"
)

func checkMysql() bool {
	db, err := sql.Open("mysql", "root:root@tcp(mysql:3306)/master")
	if err != nil {
		return false
	}
	if err := db.Ping(); err != nil {
		return false
	}
	return true
}

func checkNginx() bool {
	resp, err := http.Get("https://master.tvbit.co")
	if err != nil {
		return false
	}
	if resp.StatusCode != 200 {
		return false
	}
	return true
}

func main() {
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		for !checkMysql() {
			fmt.Println("mysql is not available")
			time.Sleep(time.Second)
		}
		fmt.Println("mysql is ready")
		wg.Done()
	}()
	go func() {
		for !checkNginx() {
			fmt.Println("nginx is not available")
			time.Sleep(time.Second)
		}
		fmt.Println("nginx is ready")
		wg.Done()
	}()
	wg.Wait()
}
