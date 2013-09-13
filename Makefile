deps:
	@pip install -r test-requirements.txt

test: deps
	@python api_test.py
