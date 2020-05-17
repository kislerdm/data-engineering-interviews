#! /bin/bash

# data engineering interview questions
# Dmitry Kisler © 2020-present
# www.data-engineering-interview.org

CONTACT=admin@dkisler.com

DIR_BASE="$( cd "$(dirname "${0}")" >/dev/null 2>&1 ; pwd -P )"
DIR_QUESTIONS=${DIR_BASE}/questions

msg () {
    echo "$(date +"%Y-%m-%d %H:%M:%S") ${1}"
}

get_categories() {
	echo $(ls ${DIR_QUESTIONS})
}

print_categories() {
	ind=0
	for cat in ${@}; do
		echo ${ind}: ${cat}
		((ind++))
	done
}

generate_template() {

	cat <<EOF > $1
-
 question: "YOUR QUESTION1 HERE"
 answer: "YOUR ANSWER1 HERE"
 references:
 - link1
 - link2
-
 question: "YOUR QUESTION2 HERE"
 answer: "YOUR ANSWER2 HERE"
 references:
 - link1
 - link2
EOF

}

question_categories=$(get_categories)

echo "Thanks a lot for contributing to data-engineering-interview.org!"
echo

# select category
echo "Please select the question category:"

print_categories ${question_categories[@]}

echo
read -n 1 -p "Choice: " inpt

read -r -a arr <<< ${question_categories[@]}
echo

# validate selection 
if [[ (${inpt} -gt ${#arr[@]}) || (${inpt} -lt 0) ]]; then
	echo "Selected category doesn't exist."
	echo "Please contact ${CONTACT} if you have issues/want to add new category."
	exit 1
fi

category=${arr[${inpt}]}

# checkout new branch
branch=${category}/$(date +'%Y%m%dT%H%M%s')

if [[ "$(git branch -v | grep "${branch}")" == "" ]]; then
	git checkout -b ${branch}
else
	git checkout ${branch}
fi

if [[ "$?" -gt 0 ]]; then
	echo "Git checkout error"
	git checkout master
	git branch -d ${branch}
	exit $?
fi

# add questions template
ofile=${DIR_QUESTIONS}/${category}/${category}-$(date +'%Y%m%dT%H%M%S%s').yaml

generate_template ${ofile}

# link to temp file
echo "Please edit the file to add questions:"
echo ${ofile}
echo
echo "Don't forget to commit your questions and to open a pull request afterwards!"
