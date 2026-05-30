package main

type pipeline struct {
	stages []stage
	ctx    *pContext
}

type pContext struct {
	fileName string
	content  string
}

func (p *pipeline) run() {
	for i := 0; i < len(p.stages); i++ {
		p.stages[i]()
	}
}

type stage func()

func newPipeline() *pipeline {
	return &pipeline{
		stages: make([]stage, 0),
		ctx:    &pContext{},
	}
}

func (p *pipeline) then(s stage) *pipeline {
	p.stages = append(p.stages, s)
	return p
}
