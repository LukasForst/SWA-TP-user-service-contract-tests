pull:
	docker pull lukaswire/swa-user-service

clean:
	docker-compose rm -f

up:
	docker-compose up -d

test: clean pull up
	# I'd use wait for it, but it does not work on mac https://github.com/vishnubob/wait-for-it/issues/55
	sleep 30; \
	R=$$(python contract_tests.py); \
	docker-compose stop; \
	exit $$R


