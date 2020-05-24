package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
	"path/filepath"

	"gopkg.in/yaml.v2"
)

func errorLog(msg string) {
	log.Fatalln(msg)
	os.Exit(1)
}

func fileCreate(path string) *os.File {

	dir := filepath.Dir(path)

	// check if output file exists
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		err := os.MkdirAll(dir, 0777)
		if err != nil {
			errorLog(fmt.Sprintf("Cannot create dir %s\nerror: %v", dir, err))
		}
	}

	// open file
	f, err := os.Create(path)
	if err != nil {
		errorLog(fmt.Sprintf("Cannot open file %s\nerror: %v", f.Name(), err))
	}

	return f
}

func main() {

	dir, _ := filepath.Abs(filepath.Dir(os.Args[0]))

	dirSourceQuestions := os.Getenv("DIR_SOURCE_QUESTIONS")
	if dirSourceQuestions == "" {
		dirSourceQuestions = path.Join(dir, "../../questions/submission")
	}

	dirDestinationQuestions := os.Getenv("DIR_DESTINATION_QUESTIONS")
	if dirDestinationQuestions == "" {
		dirDestinationQuestions = path.Join(dir, "../website/content/questions")
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
		errorLog(fmt.Sprintf("Cannot list %s: %v", dirSourceQuestions, err))
	}

	pageQuestionsTemplate, err := defineQuestionsPageTemplate()
	if err != nil {
		errorLog(fmt.Sprintf("Cannot instantiate output questions page template: %v", err))
	}

	pageLPQuestionsTemplate, err := defineLPQuestionsPageTemplate()
	if err != nil {
		errorLog(fmt.Sprintf("Cannot instantiate output LP questions page template: %v", err))
	}

	var dirCategory string
	var catName string
	var listFiles []os.FileInfo
	var pathFile string

	var yamlBytes []byte

	var questionContent QuestionContent
	var questions []QuestionContent
	var questionCategories QuestionsCategories

	var fOut *os.File

	for _, category := range dirCategories {
		catName = category.Name()

		dirCategory = fmt.Sprintf("%s/%s", dirSourceQuestions, catName)

		listFiles, err = ioutil.ReadDir(dirCategory)
		if err != nil {
			errorLog(fmt.Sprintf("Cannot read dir %s: %v", dirCategory, err))
		}

		if len(listFiles) == 0 {
			continue
		}

		questionCategories.Categories = append(questionCategories.Categories, catName)

		for _, file := range listFiles {
			pathFile = fmt.Sprintf("%s/%s", dirCategory, file.Name())

			yamlBytes, err = ioutil.ReadFile(pathFile)
			if err != nil {
				errorLog(fmt.Sprintf("Cannot read file %s: %v", pathFile, err))
			}

			err = yaml.Unmarshal(yamlBytes, &questionContent)
			if err != nil {
				errorLog(fmt.Sprintf("Cannot parse yaml from the file %s\ncontent:\n%s\nerror: %v", pathFile, string(yamlBytes), err))
			}

			questions = append(questions, questionContent)
		}

		// open file
		fOut = fileCreate(fmt.Sprintf("%s/%s/_index.md", dirDestinationQuestions, catName))

		// write page md to the file
		err = pageQuestionsTemplate.Execute(fOut, Questions{catName, questions})
		if err != nil {
			errorLog(fmt.Sprintf("Cannot save page md to %s\nerror: %v", fOut.Name(), err))
		}

	}

	// open file
	fOut = fileCreate(fmt.Sprintf("%s/_index.md", dirDestinationQuestions))

	// write LP page md to the file
	err = pageLPQuestionsTemplate.Execute(fOut, questionCategories)
	if err != nil {
		errorLog(fmt.Sprintf("Cannot save page md to %s\nerror: %v", fOut.Name(), err))
	}

}
