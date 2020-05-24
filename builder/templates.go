package main

import (
	"html/template"
)

// levelMap function to convert int level to its string representation
func levelMap(level int) string {
	switch lvl := level; lvl {
	case 2:
		return `‍⭐️`
	case 3:
		return `🚀`
	default:
		return `👶`
	}
}

// Questions content of a question page
type Questions struct {
	Category string
	Content  []QuestionContent
}

// QuestionContent question content
type QuestionContent struct {
	Question   string   `yaml:"question"`
	Answer     string   `yaml:"answer"`
	Level      int      `yaml:"level"`
	References []string `yaml:"references"`
	ID         string   `yaml:"id"`
	Date       string   `yaml:"date"`
	Figures    []string `yaml:"figure,omitempty"`
}

// defineQuestionsPageTemplate func to compile a page of questions
func defineQuestionsPageTemplate() (*template.Template, error) {
	TemplatePage := `---
title: <<.Category>>
weight: 2
---
{{<panel title="Warning" style="warning" >}}
The answers here are given by the community. Be careful and double check the answers before using them. If you see an error, please create a PR with a fix
{{</panel >}}

{{<panel title="Legend" style="success" >}}
👶 easy ‍⭐️ medium 🚀 expert
{{</panel>}}
<<range .Content>>
### <<.Question>> << levelMap .Level >>

<<.Answer>>

***References***:
<<range .References>>
- <<.>>
<<end>>

***ID***: *<<.ID>>*

***Last Updated***: *<<.Date>>*

<<end>>
`

	return template.New("page").Delims("<<", ">>").Funcs(
		template.FuncMap{
			"levelMap": levelMap,
		}).Parse(TemplatePage)
}

// QuestionsCategories list of questions categories
type QuestionsCategories struct {
	Categories []string
}

// defineLPQuestionsPageTemplate func to compile a "LP" for questions pages
func defineLPQuestionsPageTemplate() (*template.Template, error) {
	TemplatePage := `---
title: Questions
weight: 2
---
{{<panel title="Warning" style="warning" >}}
The answers here are given by the community. Be careful and double check the answers before using them. If you see an error, please create a PR with a fix
{{</panel >}}
<<range .Categories>>
- [<<.>>](<<.>>)
<<end>>
`
	return template.New("page").Delims("<<", ">>").Parse(TemplatePage)
}
