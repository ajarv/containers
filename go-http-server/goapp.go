package main

import (
	"flag"
	"log"
	"net/http"
	"os"
	"sort"
	"strings"
)

// We define a type "fit" and the methods "Len", "Swap" and "Less" on
// it so that we can sort a slice of files.

type fit []os.FileInfo

func (fi fit) Len() int {
	return len(fi)
}

func (fi fit) Swap(i, j int) {
	fi[i], fi[j] = fi[j], fi[i]
}

func (fi fit) Less(i, j int) bool {
	return strings.ToLower(fi[i].Name()) < strings.ToLower(fi[j].Name())
}

type sortedFile struct {
	// We use "of" for Close, Read, Stat, and Seek methods.
	of http.File
	// The list of files.
	fi fit
	// Index for Readdir.
	n int
	// The total number of files in this directory.
	total int
	// Has this structure been initialized yet?
	init bool
}

func (f sortedFile) Close() error {
	return f.of.Close()
}

func (f sortedFile) Read(p []byte) (n int, err error) {
	return f.of.Read(p)
}

func (f sortedFile) Seek(offset int64, whence int) (int64, error) {
	return f.of.Seek(offset, whence)
}

func (f sortedFile) Stat() (os.FileInfo, error) {
	return f.of.Stat()
}

// Substitute Readdir with a sorted version.

func (f sortedFile) Readdir(n int) (fi []os.FileInfo, err error) {
	if !f.init {
		var err error
		f.fi, err = f.of.Readdir(-1)
		if err != nil {
			return fi, err
		}
		f.init = true
		f.total = len(f.fi)
		sort.Sort(f.fi)
	}
	max := f.n + n
	if n == -1 || max > f.total {
		max = f.total
	}
	fi = f.fi[f.n:max]
	f.n += n
	return fi, nil
}

// Our replacement for http.Dir. The only method we need is actually
// Open, below.

type sortedDir struct {
	d http.Dir
}

// Substitute for Open.

func (f sortedDir) Open(name string) (http.File, error) {
	var s sortedFile
	var err error
	s.of, err = f.d.Open(name)
	if err != nil {
		return nil, err
	}
	return http.File(s), nil
}

func main() {
	// The directory to serve.
	directory := flag.String("staticDir", "/www/", "Static file directory")
	flag.Parse()
	// var dir = "/usr/local/www/data"
	var d = sortedDir{d: http.Dir(*directory)}
	fileserver := http.FileServer(d)
	http.HandleFunc("/", fileserver.ServeHTTP)
	log.Printf("Serving %s on HTTP port: 8080\n", *directory)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
