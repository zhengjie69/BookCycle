pipeline {
    agent any
	
    stages {
        stage('Build') { 
            steps {
                echo 'Test'
            }
        }
	stage('OWASP DependencyCheck') {
			      steps {
				            dependencyCheck additionalArguments: '--format HTML --format XML --enableExperimental', odcInstallation: '3203DependencyCheckTest730'
			      }
		}
	}
	post {
        success {
            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
        }
    }
}
