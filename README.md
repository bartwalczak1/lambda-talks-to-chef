----
## Lambda talks to Chef and slack
#### Remove node from Chef on node termination event.

This project let you create lambda function which will trigger on any action
specified in Cloudwatch event.

These steps need to be done manually. Once you're happy with your Cloudwatch rule,
and blueprint lambda function zip this directory and upload to Lambda.

Most values are hard coded but can be easily replaced directly in the code or via
environment variables.

To replace key used by Lambda to trigger action on Chef, simply encrypt it with kms
and give Lambda permission to decrypt the key.
