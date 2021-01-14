% prepara el repositorio para su despliegue.
release: sh -c 'cd decide && python manage.py migrate'
% especifica el comando para lanzar Decide
web: npx serve web-build
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -'
