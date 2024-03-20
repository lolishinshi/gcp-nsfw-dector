FUNCTION_NAME=nsfw-model
REGION=us-east1
USEROUTPUT=false

deploy:
	gcloud functions deploy $(FUNCTION_NAME) \
		--gen2 \
		--runtime python311 \
		--memory 350MB \
		--timeout 10s \
		--region $(REGION) \
		--source=. \
		--entry-point detect \
		--trigger-http \
		--user-output-enabled=$(USEROUTPUT)

delete:
	gcloud functions delete $(FUNCTION_NAME) --region $(REGION)
