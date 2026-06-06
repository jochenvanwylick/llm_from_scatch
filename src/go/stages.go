package main

import (
	"fmt"
	"os"
)

func readFile(filename string) step {
	return func(doc *document) error {
		b, err := os.ReadFile(filename)
		if err != nil {
			return fmt.Errorf("read file %q: %w", filename, err)
		}

		doc.fileName = filename
		doc.content = string(b)

		return nil
	}
}

func printStats() step {
	return func(doc *document) error {
		fmt.Printf("file: %s\n", doc.fileName)
		fmt.Printf("length: %d\n", len(doc.content))
		return nil
	}
}
