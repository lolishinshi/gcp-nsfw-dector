FUNCTION_NAME=nsfw-model
REGION=us-east1

deploy:
	gcloud functions deploy $(FUNCTION_NAME) \
		--gen2 \
		--runtime python311 \
		--memory 300MB \
		--timeout 10s \
		--region $(REGION) \
		--source=. \
		--entry-point detect \
		--trigger-http \

delete:
	gcloud functions delete $(FUNCTION_NAME) --region $(REGION)
