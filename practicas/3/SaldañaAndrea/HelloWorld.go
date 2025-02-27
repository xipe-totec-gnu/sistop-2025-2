package main

import (
	"fmt"
	"os"
)

func main() {
	name := os.Args[1]
	fmt.Printf("Hello, %s!\n", name)
}
