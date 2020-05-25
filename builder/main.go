package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"os"
	"path"
	"path/filepath"
	"time"

	"gopkg.in/yaml.v2"
)

// fileCreate function to open a new file
func fileCreate(path string) (*os.File, error) {

	dir := filepath.Dir(path)

	// check if output file exists
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		err := os.MkdirAll(dir, 0777)
		if err != nil {
			log.Fatalf("Cannot create dir %s\nerror: %v", dir, err)
		}
	}

	return os.Create(path)
}

// writePage function to execute and write template as md file on disk
func writePage(template *template.Template, path string, obj interface{}) error {
	fOut, err := fileCreate(path)
	if err != nil {
		return err
	}

	err = template.Execute(fOut, obj)
	if err != nil {
		return err
	}
	return nil
}

func main() {
	dir, _ := filepath.Abs(filepath.Dir(os.Args[0]))

	// read env vars
	// dir with questions yaml files
	dirSourceQuestions := os.Getenv("DIR_SOURCE_QUESTIONS")
	if dirSourceQuestions == "" {
		dirSourceQuestions = path.Join(dir, "questions")
	}
	// dir to store website content
	dirSiteContent := os.Getenv("DIR_SITE_CONTENT")
	if dirSiteContent == "" {
		dirSiteContent = path.Join(dir, "website/content")
	}
	// dir containing images used as illustrations
	dirSourceImg := os.Getenv("DIR_SOURCE_IMG")
	if dirSourceImg == "" {
		dirSourceImg = path.Join(dir, "img")
	}
	// dir to storage images for website
	dirDestinationImg := os.Getenv("DIR_DESTINATION_IMG")
	if dirDestinationImg == "" {
		dirDestinationImg = path.Join(dir, "website/static/img")
	}
	// path to code of conduct
	pathCoc := os.Getenv("PATH_COC")
	if pathCoc == "" {
		pathCoc = path.Join(dir, "code-of-conduct.md")
	}

	pageLPTemplate, err := defineLandingPage()
	if err != nil {
		log.Fatalf("Cannot instantiate landing page template: %v", err)
	}

	pageQuestionsTemplate, err := defineQuestionsPageTemplate()
	if err != nil {
		log.Fatalf("Cannot instantiate output questions page template: %v", err)
	}

	pageLPQuestionsTemplate, err := defineLPQuestionsPageTemplate()
	if err != nil {
		log.Fatalf("Cannot instantiate output LP questions page template: %v", err)
	}

	// scan questions directory
	dirCategories, err := ioutil.ReadDir(dirSourceQuestions)
	if err != nil {
		log.Fatalf("Cannot list %s: %v", dirSourceQuestions, err)
	}

	var questionCategories QuestionsCategories
	var siteStats SiteStats
	siteStats.Date = time.Now().UTC().Format("2006-01-02")

	for _, category := range dirCategories {
		catName := category.Name()
		dirCategory := fmt.Sprintf("%s/%s", dirSourceQuestions, catName)

		listFiles, err := ioutil.ReadDir(dirCategory)
		if err != nil {
			log.Fatalf("Cannot read dir %s: %v", dirCategory, err)
		}

		if len(listFiles) == 0 {
			continue
		}

		questionCategories.Categories = append(questionCategories.Categories, catName)

		var questions []QuestionContent

		for _, file := range listFiles {
			pathFile := fmt.Sprintf("%s/%s", dirCategory, file.Name())

			yamlBytes, err := ioutil.ReadFile(pathFile)
			if err != nil {
				log.Fatalf("Cannot read file %s: %v", pathFile, err)
			}

			var questionContent QuestionContent

			err = yaml.Unmarshal(yamlBytes, &questionContent)
			if err != nil {
				log.Fatalf("Cannot parse yaml from the file %s\ncontent:\n%s\nerror: %v", pathFile, string(yamlBytes), err)
			}

			// copy required image
			if len(questionContent.Figures) > 0 {
				for _, img := range questionContent.Figures {
					source := fmt.Sprintf("%s/%s", dirSourceImg, img)
					destination := fmt.Sprintf("%s/%s", dirDestinationImg, img)

					err := os.Link(source, destination)
					if err != nil {
						log.Printf("Cannot move from %s to %s: %s", source, destination, err)
					}
				}
			}

			questions = append(questions, questionContent)
		}

		err = writePage(pageQuestionsTemplate, fmt.Sprintf("%s/questions/%s/_index.md", dirSiteContent, catName), Questions{catName, questions})
		if err != nil {
			log.Fatalf("Error saving md to %s\nerror: %v", fmt.Sprintf("%s/questions/%s/_index.md", dirSiteContent, catName), err)
		}

		siteStats.CntQuestions += len(questions)
	}

	// save questions landing page
	err = writePage(pageLPQuestionsTemplate, fmt.Sprintf("%s/questions/_index.md", dirSiteContent), questionCategories)
	if err != nil {
		log.Fatalf("Error saving md to %s\nerror: %v", fmt.Sprintf("%s/questions/_index.md", dirSiteContent), err)
	}

	// save main landing page
	err = writePage(pageLPTemplate, fmt.Sprintf("%s/_index.md", dirSiteContent), siteStats)
	if err != nil {
		log.Fatalf("Error saving md to %s\nerror: %v", fmt.Sprintf("%s/_index.md", dirSiteContent), err)
	}

	// prepare and save code of conduct page
	CocBytes, err := ioutil.ReadFile(pathCoc)
	if err != nil {
		log.Fatalf("Cannot read file %s: %v", pathCoc, err)
	}

	CocText := fmt.Sprintf(`---
title: Code of Conduct
weight: 3
---

%s`, string(CocBytes))

	CocFile, err := fileCreate(fmt.Sprintf("%s/code-of-conduct/_index.md", dirSiteContent))
	if err != nil {
		log.Fatalf("Cannot write to file %s: %v", fmt.Sprintf("%s/code-of-conduct/_index.md", dirSiteContent), err)
	}

	_, err = CocFile.WriteString(CocText)
	if err != nil {
		log.Fatalf("Cannot write to file %s: %v", fmt.Sprintf("%s/code-of-conduct/_index.md", dirSiteContent), err)
	}

}
