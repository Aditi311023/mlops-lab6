pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = 'Aditi311023/mlops-lab6'
        CURRENT_ACCURACY = ''
        BEST_ACCURACY = ''
        SHOULD_BUILD = 'false'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                echo 'Training model...'
                sh '''
                    . venv/bin/activate
                    python train.py
                '''
            }
        }

        stage('Read Accuracy') {
    steps {
        script {
            echo 'Reading accuracy from metrics.json...'
            def metrics = readJSON file: 'app/artifacts/metrics.json'
            echo "Raw metrics: ${metrics}"
            env.CURRENT_ACCURACY = metrics['accuracy'] ? metrics['accuracy'].toString() : null
            echo "Current Accuracy: ${env.CURRENT_ACCURACY}"
        }
    }
}


        stage('Compare Accuracy') {
    steps {
        script {
            if (!env.CURRENT_ACCURACY) {
                error "Current accuracy is null or missing in metrics.json"
            }
            withCredentials([string(credentialsId: 'best-accuracy', variable: 'STORED_ACCURACY')]) {
                env.BEST_ACCURACY = STORED_ACCURACY ?: '0.0'
                echo "Stored Best Accuracy: ${env.BEST_ACCURACY}"

                def current = env.CURRENT_ACCURACY.toFloat()
                def best = env.BEST_ACCURACY.toFloat()

                if (current > best) {
                    echo "New model is better (${current} > ${best})"
                    env.SHOULD_BUILD = 'true'
                } else {
                    echo "New model is NOT better (${current} <= ${best})"
                    env.SHOULD_BUILD = 'false'
                }
            }
        }
    }
}


        stage('Build Docker Image') {
            when {
                expression { env.SHOULD_BUILD == 'true' }
            }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                        def img = docker.build("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}")
                        env.DOCKER_IMAGE = "${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}"
                    }
                }
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.SHOULD_BUILD == 'true' }
            }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                        def img = docker.image("${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER}")
                        img.push()
                        img.push('latest')
                    }
                    echo "Pushed ${env.DOCKERHUB_REPO}:${env.BUILD_NUMBER} and :latest"
                }
            }
        }
    }

    post {
        always {
            echo 'Archiving artifacts...'
            archiveArtifacts artifacts: 'app/artifacts/**', allowEmptyArchive: false
        }
    }
}
