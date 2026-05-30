package main

import "fmt"

func main() {
	fName := "the-verdict.txt"

	p := newPipeline()
	p.then(readFile(fName))
	p.then(printStats())

	err := p.run()
	if err != nil {
		fmt.Println("error during pipeine execution")
	}
	fmt.Println("pipeline run success!")
}
