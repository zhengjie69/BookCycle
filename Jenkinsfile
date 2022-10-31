pipeline {
    agent any
    
    stages {
        stage('Build') { 
            steps {
                echo 'Test'
		sh 'npm install'
            }
        }
	stage('OWASP DependencyCheck') {
			      steps {
				            dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: '3203DependencyCheckTest730'
			      }
		}
	}
}
