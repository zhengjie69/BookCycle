pipeline {
    agent any
	
    tools {nodejs "nodejs"}
	
    stages {
        stage('Build') { 
            steps {
                echo 'Run NPM Install'
		sh 'npm install'
            }
        }
	stage('OWASP DependencyCheck') {
			      steps {
				            dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: '3203DependencyCheckTest730'
			      }
		}
	}
	post {
        success {
            dependencyCheckPublisher pattern: 'dependency-check-report.xml'
        }
    }
}
