pipeline {
    agent any

    environment {
        // code for manual case
        //CODE = git(branch: 'master', credentialsId: '2018devopsday', url: 'git@github.com:flywindy/gitops.git')
        //VERSION = sh (script: './bin/version.sh', returnStdout: true).trim()
        APP_NAME = 'devopsdays'
        REGISTRY = 'docker.trendops.co'
    }
    
    stages{
        stage('Build'){
            steps {
                sh 'docker build --pull -t ${REGISTRY}/${APP_NAME} .'
                sh 'docker push ${REGISTRY}/${APP_NAME}'
                sh 'docker rmi  ${REGISTRY}/${APP_NAME} || true'
            }
        }   
    
        stage('Unit Test'){
            steps {
                echo 'TBD'
            }
        }
        
        stage('Deploy'){
            steps {
                echo "Deploying..."
                sshagent (credentials: ['2018devopsday']) {
                   sh 'ssh -o StrictHostKeyChecking=no devopsdays@54.212.220.243 deploy'
                }
            }
        }
    }
    post {
        always {
            echo 'One way or another, I have finished'
        }
        changed {
            echo 'Things were different before...'
        }
        success {
            emailext(attachLog: true,
                     body: '''${SCRIPT, template="groovy-html.template"}''',
                     replyTo: 'noreply@2018devopsdays.trendmicro.com',
                     recipientProviders: [[$class: 'DevelopersRecipientProvider'],[$class: 'RequesterRecipientProvider']],
                     subject: "'${currentBuild.fullDisplayName} ${currentBuild.currentResult}'",
                     to: 'eric_chen@trend.com.tw')
            deleteDir() /* clean up our workspace */
        }
        unstable {
            echo 'I am unstable :/'
        }
        failure {
            echo 'I failed :('
            emailext(attachLog: true,
                     body: '''${SCRIPT, template="groovy-html.template"}''',
                     replyTo: 'noreply@2018devopsdays.trendmicro.com',
                     recipientProviders: [[$class: 'DevelopersRecipientProvider'],[$class: 'RequesterRecipientProvider']],
                     subject: "'${currentBuild.fullDisplayName} ${currentBuild.currentResult}'",
                     to: 'eric_chen@trend.com.tw')
            deleteDir() /* clean up our workspace */
        }
    }
}   
