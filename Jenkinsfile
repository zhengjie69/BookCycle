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
				            dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'OWASP Dependency-Check'
			      }
		}
	}
}

