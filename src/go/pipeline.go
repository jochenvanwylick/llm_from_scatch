package main

type pipeline struct {
	steps []step
	doc   *document
}

type document struct {
	fileName string
	content  string
	tokens   []string
}

type step func(*document) error

func newPipeline() *pipeline {
	return &pipeline{
		steps: make([]step, 0),
		doc:   &document{},
	}
}

func (p *pipeline) then(s step) *pipeline {
	p.steps = append(p.steps, s)
	return p
}

func (p *pipeline) run() error {
	for _, s := range p.steps {
		if err := s(p.doc); err != nil {
			return err
		}
	}

	return nil
}
