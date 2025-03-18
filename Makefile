run:
	docker run -it -d --env-file .env --restart=unless-stopped --name lessons_mailing:bot lessons_mailing:latest
stop:
	docker stop easy_refer
attach:
	docker attach easy_refer
dell:
	docker rm easy_refer