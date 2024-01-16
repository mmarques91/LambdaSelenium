# LambdaSelenium

This repository was created to solve a problem that I was facing, the main problem is that I needed to create an automation to everytime an IP Address of an specific Load Balancer changes I had to create a new route on My Pritunl VPN Servers Configuration.

The first problem I was facing is due to Lambda quotas, that doesn't supports deployment package over 250 MB. The second problem was trying to configure the chromedriver to work on a serverless environment.

The best solution I found for this was using AWS SAM CLI (https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html). Using it, is possible to achieve a limit of 10 GB deployment package size limit and pre-configure the Chromedriver.

To deploy this solution:

1. Install AWS CLI and AWS CLI SAM;
2. Clone this repository;
3. Navigate to the repositpry;
4. Change the variables in main.py;
5. Change template.yml;
6. Build the app 'sam build';
7. Test the app locally 'sam local invoke';
8. Deploy the app to AWS 'sam deploy --guided'.