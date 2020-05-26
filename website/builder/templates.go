package main

import (
	"html/template"
)

// levelMap function to convert int level to its string representation
func levelMap(level int) string {
	switch lvl := level; lvl {
	case 2:
		return `⭐️`
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

// defineQuestionsPageTemplate function to compile a page of questions
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

	return template.New("questionsCategory").Delims("<<", ">>").Funcs(
		template.FuncMap{
			"levelMap": levelMap,
		}).Parse(TemplatePage)
}

// QuestionsCategories list of questions categories
type QuestionsCategories struct {
	Categories []string
}

// defineLPQuestionsPageTemplate function to compile a "LP" for questions pages
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
	return template.New("questions").Delims("<<", ">>").Parse(TemplatePage)
}

// SiteStats website stats
type SiteStats struct {
	CntQuestions int
	Date         string
}

// defineLandingPage function to compile landing page
func defineLandingPage() (*template.Template, error) {
	TemplatePage := `# Data Engineering Interviews

Data engineering related Q&A for *data community* by *data community*.

The database contains **<< .CntQuestions >>** questions as of *<<.Date>>*. Find the full list [here](questions).

## Contribution

It is fully community driven project - **your contribution matters**:

- If you know a question you would like to share — please create a PR
- If you know how to answer a question — please create a PR with the answer
- If you think you can improve an answer — please create a PR with improvement suggestion
- If you see a mistake — please create a PR and propose a fix

For updates, join our <a href="https://join.slack.com/t/dataengineeri-dg22406/shared_invite/zt-eeydzktu-uJ2mc4a45OrtzDMqekiqDQ" target="_blank">slack workspace</a> and follow me on LinkedIn (<a href="https://www.linkedin.com/in/dkisler/" target="_blank">dkisler</a>).

*Respect your peers and follow our [code of conduct](code-of-conduct)*

<a href="https://github.com/kislerdm/data-engineering-interviews/contributors" target="_blank">List of contributors</a>
`
	return template.New("LP").Delims("<<", ">>").Parse(TemplatePage)
}
