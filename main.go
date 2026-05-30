package main

func main() {
	fName := "the-verdict.txt"

	p := newPipeline()
	p.then(read(fName))
	p.run()
}
