pipeline {
   agent { docker { image 'mcr.microsoft.com/playwright/python:v1.45.0-jammy' } }
   stages {
      stage('scrapper') {
         steps {
            sh 'pip install -r requirements.txt'
            sh 'ls'
            sh 'python -m main.py'
         }
      }
   }
}