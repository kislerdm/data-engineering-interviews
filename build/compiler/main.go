package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"os"
	"path"
	"path/filepath"

	"gopkg.in/yaml.v2"
)

func main() {

	dir, _ := filepath.Abs(filepath.Dir(os.Args[0]))

	dirSourceQuestions := os.Getenv("DIR_SOURCE_QUESTIONS")
	if dirSourceQuestions == "" {
		dirSourceQuestions = path.Join(dir, "../../questions/submission")
	}

	dirDestinationQuestions := os.Getenv("DIR_DESTINATION_QUESTIONS")
	if dirDestinationQuestions == "" {
		dirDestinationQuestions = path.Join(dir, "../../questions")
	}

	dirSourceImg := os.Getenv("DIR_SOURCE_IMG")
	if dirSourceImg == "" {
		dirSourceImg = path.Join(dir, "../../questions/img")
	}

	dirDestinationImg := os.Getenv("DIR_DESTINATION_IMG")
	if dirDestinationImg == "" {
		dirDestinationImg = path.Join(dir, "../website/static/img")
	}

	dirCategories, err := ioutil.ReadDir(dirSourceQuestions)
	if err != nil {
		log.Fatalln("Cannot list %s: %v", dirSourceQuestions, err)
		os.Exit(1)
	}

	var dirCategory string
	var listFiles []os.FileInfo
	var pathFile string

	var yamlBytes []byte

	var questionContent QuestionContent

	var pageTemplate *template.Template

	for _, category := range dirCategories[:1] {
		dirCategory = fmt.Sprintf("%s/%s", dirSourceQuestions, category.Name())

		listFiles, err = ioutil.ReadDir(dirCategory)
		if err != nil {
			log.Fatalln("Cannot list %s: %v", dirCategory, err)
			os.Exit(1)
		}

		var questions []QuestionContent

		pageTemplate, err = definePageTemplate()

		for _, file := range listFiles {
			pathFile = fmt.Sprintf("%s/%s", dirCategory, file.Name())

			yamlBytes, err = ioutil.ReadFile(pathFile)
			if err != nil {
				log.Fatalln("Cannot read file %s: %v", pathFile, err)
				os.Exit(1)
			}

			err = yaml.Unmarshal(yamlBytes, &questionContent)
			if err != nil {
				log.Fatalln("Cannot parse yaml from the file %s\ncontent:\n%s\nerror: %v", pathFile, string(yamlBytes), err)
				os.Exit(1)
			}

			questions = append(questions, questionContent)
		}

		err = pageTemplate.Execute(os.Stdout, Questions{category.Name(), questions})
		if err != nil {
			panic(err)
		}

	}

}
